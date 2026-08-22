# External Dependency Map — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.8 (`delivery-planning`), intent `260813-tec-hourly-forecast`.

Everything below is something this initiative **cannot decide, build or unblock
on its own**. Each row names what it is, who owns it, roughly how long it takes,
the Bolt or gate it blocks, and what happens if it slips. A **Bolt** is one build
pass over a piece of the work, ending in something that runs; the twelve of them
are defined in `bolt-plan.md`.

Per the Q7 answer, all four classes are tracked in full rather than sampled. This
document is the input to **Gate 0**, the pre-Construction decision pack the Q8
answer requires.

## Sources

- `bolt-plan.md` and `risk-and-sequencing-rationale.md` — the Bolt numbering and risk ranking referenced throughout.
- `../units-generation/unit-of-work.md` — the blocker register BLK-01…BLK-07, the residual obligations RES-01…RES-03, and each blocker's stated approval authority.
- `../units-generation/unit-of-work-dependency.md` — the integration-point table, which is where the released-artifact contracts between units come from.
- `../units-generation/unit-of-work-story-map.md` — the acceptance rows each gated item reaches.
- `../application-design/components.md` — the module boundaries the licence and reuse rules attach to.
- `../requirements-analysis/requirements.md` — § Open supervisor gates (all seventeen), § Known defects, § Constraints, FR-P1-01-6 and FR-P1-01-7 for the provider and outage detail.
- `../practices-discovery/team-practices.md` — § Deployment (two platforms, releases as this project's deliverable), § Testing Posture (the in-Kaggle gate rule).
- **Absent by scope design:** `stories` (`../user-stories/stories.md`), `mockups` (`../refined-mockups/`) — stages 2.4, 1.6 and 2.5 are `SKIP`. Neither would have contributed an external dependency; this pipeline has no user-facing surface and no story-derived stakeholder.

---

## A. Decisions this project cannot make for itself

These are the Gate 0 items. **No frozen value may be invented, inferred or
substituted** — `project.md` § Forbidden bars any agent from filling a
`TBD — freeze gate` value by convenience, and BLK-02 states the same rule for its
own manifest in its own words.

They split into two kinds, and the split matters because it determines *when* the
decision can actually be taken.

### A1 — Decidable at Gate 0, with no design work behind them

| Item | What is needed | Owner | Lead time | Blocks | If it slips |
|---|---|---|---|---|---|
| **BLK-02** — the `plumbing_7day` fixture station | **RESOLVED 2026-08-22 — BSHM 32/35 (D-20)**, on the only complete observed coverage of D-11's window. Measured evidence in § A1b | Project owner, under Q-31 | Decided | **Bolt 12** owns the manifest; **Bolt 3 onward** needed the identity for the per-Bolt measurement rule | **No longer a Gate 0 blocker.** Still pending: the manifest does not exist, the fixture has never been run, and no measured value exists or is claimed |
| **F10.7 selection decisions** (three, recorded as D-21/D-22/D-23; transcribed into `features.yaml` at Bolt 1) | **RESOLVED 2026-08-22** — (a) daily value = **daily median** (D-21, with its availability rule); (b) duplicate UT = **mean** + count log + QC flag, provider-correction semantics taking precedence when documented (D-22); (c) high-spread = **flag and retain** (D-23). Measured evidence in § A1a | Project owner, before G-05 | Decided | **Bolt 5** — `external-products` builds the F10.7 series | **No longer a Gate 0 blocker.** A run whose `features.yaml` leaves any of the three unset still **fails the zero-`TBD` preflight**; the values are now available to transcribe rather than absent |

### A1b — the `plumbing_7day` station, with the measured evidence behind it

**The window is already frozen and is not in question:** D-11 fixes
2022-11-01 to 2022-11-07 inclusive. What is unselected is the **single station**
that executes the fixture, TE §15.1 mandating one.

**Measured completeness in that window**, quoted from D-11, which sources it from
`evidence/audit_evidence_2022-11/madrigal_coverage_raw_records.csv`:

| Candidate cell | Days present | Hourly bins | Records | Note recorded in D-11 |
|---|---|---|---|---|
| **ARUC 40/44** | 7/7 | 163/168 (97.02%) | 1,195 | Short **exactly one bin on five of the seven days** (3–7 November). D-11 calls the uniformity suggestive of a **systematic single-bin gap rather than random loss**, and requires it to be **explained before the manifest is frozen** |
| **BSHM 32/35** | 7/7 | 168/168 (100.00%) | 1,810 | Complete. No recorded caveat |
| **NICO 35/33** | 7/7 | 155/168 (92.26%) | 964 | Thinnest of the three; weakest day 2022-11-04 at 20/24 bins. Fewest records |

All three satisfy D-2's ≥95%-of-calendar-days rule applied by analogy (7/7 day
presence in every cell). **No fixture completeness threshold exists to clear** —
§15.1 states these figures are measured and frozen into the manifest, not tested
against a bar.

**The board selects nothing.** ARUC, BSHM and NICO are presented as they measure;
the choice is the owner's under Q-31 and **no station may be selected by
convenience**. The trade-offs, stated without a preference being smuggled in: the
completeness ranking is BSHM > ARUC > NICO; ARUC carries an unexplained
obligation that must be discharged first if chosen; NICO is thinnest and would
exercise the missing-data path hardest, which is either an advantage or a
distraction depending on what the owner wants a plumbing smoke test to prove.

### A1c — fixture reconciliation against the decision records

Checked 2026-08-22 against `evidence/DECISIONS.md` per the owner's instruction.

| Fixture | Frozen as | Window | Cells | Status |
|---|---|---|---|---|
| `plumbing_7day` | **D-11** (2026-08-16) | 2022-11-01 to 2022-11-07 | Window characterised on all three; **execution scope is one station, unselected** | Window frozen; station open (**BLK-02**) |
| `scientific_1month` | **D-14** (2026-08-21) | **March 2022**, 2022-03-01 to 2022-03-31 | All three cells | Frozen |

**There is no January fixture, and none was ever frozen.** 2022-01 was explicitly
**considered and rejected** in D-14's own "Alternatives rejected" list: it had the
best coverage (NICO 98.9%) and was the closest seasonal analogue to December, but
`audit_evidence_2022-01/` is the folder carrying the year-blind predicate's
custody irregularity — **743 December-2022 records** filed under a January label,
with open findings `VAL-1` and `VAL-3` against exactly those bytes. D-14 records
the reasoning as trading "a statistical nicety for an audit problem". Any later
reference to a January fixture is a misreading of that rejected alternative.

**December 2022 is excluded from both development fixtures**, and the exclusion is
asserted on **record observation dates**, never on the directory a file was filed
under — which is precisely the failure the January folder demonstrates. Enforced
by `tests/test_acquisition_window.py` (FR-WS-3). Neither fixture window overlaps
December by date: November 1–7 and March 1–31.
**Sequencing, corrected 2026-08-22 against `DP-TEC-02`.** The earlier text placed
these both at Gate 0 and behind Bolt 1, which read as a contradiction. The two
timings are separate steps and neither is deferred:

1. **The scientific decisions are taken at Gate 0** and recorded formally as a
   D-number. They need no code and no configuration file.
2. **The approved values are transcribed into `features.yaml` when Bolt 1 creates
   it**, citing that D-number.

### A1a — the F10.7 decisions, with the measured evidence behind them

Derived on 2026-08-22 directly from the held provider file
`evidence/audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt` (Canada's Solar Radio
Monitoring Program, observed flux column). Every figure below was computed from
that file and printed before being written here. **No option is recommended into
existence, and no value is frozen by this artifact.**

**Measured facts about calendar 2022 in that file:**

- **365 distinct days present — zero missing dates.** The whole calendar year is
  covered.
- **1,101 readings** across those 365 days: 360 days carry 3 readings, 4 days
  carry 4, and 1 day carries 5.
- **Observation times drift seasonally.** By UT hour: 17 UT ×245, 18 UT ×121,
  20 UT ×366, 22 UT ×121, 23 UT ×248. The pattern is three daily slots — an early
  slot that moves between 17 and 18 UT, a **20 UT slot present on every day of the
  year**, and a late slot that moves between 22 and 23 UT.
- **Five duplicate-UT days**: 2022-03-26, 2022-09-20, 2022-10-17 (23 UT repeated),
  2022-10-23 (20 UT repeated), 2022-12-08 (18 and 22 UT repeated).
- **Four high-spread days** where within-day spread exceeds 20% of the day's
  median: 2022-01-18 (32.5%), 2022-03-31 (60.6%), 2022-08-28 (78.1%),
  2022-08-29 (179.2%).

**A correction that changes the shape of decision (c).** `requirements.md`
FR-P1-01-7 states that *"three of those four contaminated readings"* fall at
20 UT. Derived from the file, **two** do:

| Day | 17/18 UT | 20 UT | 22/23 UT | Outlier sits at |
|---|---|---|---|---|
| 2022-01-18 | **148.8** | 114.5 | 111.6 | **18 UT** |
| 2022-03-31 | 148.7 | **239.5** | 149.8 | **20 UT** |
| 2022-08-28 | 151.6 | **251.9** | 133.5 | **20 UT** |
| 2022-08-29 | **357.1** | 130.6 | 123.0 | **17 UT** |

The outlier falls at the early slot on two days and at 20 UT on two days. **No
single hour is clean**, which materially weakens any fixed-hour pick and is the
opposite of what the carried "three of four at 20 UT" implied. This is a
`requirements.md` defect; it is **recorded here and not corrected there**, since
that is an approved stage 2.3 artifact and its amendment is a separate owner
decision routed through Vision §15.2.

**Decision (a) — which reading defines the daily value.** Options: the 20 UT
reading (the only slot present on all 365 days); the daily **median** of the
readings; the daily mean; or a named local-noon-equivalent slot. Evidence bearing
on it: 20 UT has complete coverage, but carries the outlier on two of the four
high-spread days. The median returns the clean value on **all four** of those days
(114.5, 149.8, 151.6, 130.6).

**Decision (b) — duplicate UT records.** Options: first record wins; last record
wins; mean of the duplicates; or reject the day and treat it as missing. Affects
exactly the five days listed above.

**Decision (c) — high-spread observations.** Options: accept as measured; take the
median; flag and exclude the day; or flag, retain, and carry the flag into the
availability matrix. Affects exactly the four days listed above.

**Outage status, stated at its measurement granularity.** An earlier revision of
this map carried *"a documented month-long outage from 2022-03-18"* as a live
provider hazard. The suspected outage was audited against the available 2022
source data: **no missing calendar day was observed — at least one observation is
present on 365 of 365 calendar days.** This finding does **not** assert
uninterrupted within-day coverage or uninterrupted provider availability, and is
**not** described as "zero outage". It is no longer carried as an open hazard at
day granularity. Separately unresolved and asserted neither way: whether values
spanning the incident were measured, recovered or reconstructed — the file
carries no qualifier, flag or provenance column (EC1-R-4).

**A bound on the high-spread evidence.** The four-day distribution above shows
outliers at 18, 20, 20 and 17 UT. Because outliers occur across multiple UT
slots, **fixed-hour selection without quality controls can retain contaminated
observations.** This artifact does **not** claim that no single slot is clean or
that no fixed-hour convention is safe; neither has been independently
demonstrated.

### A2 — Presented at Gate 0, decided at the functional-design gate

**Owner ruling, 2026-08-22** (`DP-CHAIR-02`), replacing the interpretation this
section previously carried:

> Functional design **may begin** while BLK-05 and BLK-06 remain open, **but only
> to analyze those blockers and generate the evidence required for their
> resolution**. Neither is marked resolved and no approval is assumed until the
> owner explicitly decides. **No dependent implementation, code generation,
> governed execution or downstream activity may begin** until the corresponding
> blocker decision is approved and recorded.

So functional design produces the analysis; the owner takes the decision; the
implementation stays barred until the decision is recorded. Both blockers are
presented below with options, evidence, risks and a recommendation — and neither
is closed by this artifact.

**BLK-06 — the canonical protected set. Options, with the derivation already
performed.** Both source lists were enumerated from the Technical Environment on
2026-08-22 and counted:

- **TE §2.2** lists **12** items: model source; TensorFlow/Keras environment;
  architecture serialization; feature manifest; target contract; split/mask
  manifests; grids; selected hyperparameters; optimizer/loss policy; seeds;
  metrics; statistical configuration.
- **TE §7.0B** lists **16**: TensorFlow/Keras model source and serialized
  architecture; feature schema and safe lags; history window; target
  cadence/horizon; station encoding; loss; optimizer policy; selected
  hyperparameters; splits; embargo; baselines; comparison-set masks; seeds;
  metrics; bootstrap; reporting hierarchy.
- **FR-P1-06-1's fourteen-item list** is §2.2's twelve plus `bootstrap` and
  `reporting hierarchy`.

Cross-checking §7.0B against that list, item by item: `feature schema and safe
lags` maps to `feature manifest`; `target cadence/horizon` to `target contract`;
`loss` and `optimizer policy` to `optimizer/loss policy`; `splits`, `embargo` and
`comparison-set masks` to `split/mask manifests`. **Three items map to nothing.**
`history window` and `station encoding` are *plausibly* inside `feature manifest`
but no artifact says so, and **`baselines` has no plausible home in the list at
all** — which is the consequential one, because a Phase 2 run could change the
M-01/M-02/M-03 baseline definitions and still produce the empty hash diff that
*is* G-P3C's pass condition.

Options: **(1)** adopt a canonical set as the deduplicated union with the three
unmapped items added explicitly, and amend FR-P1-06-1 under Vision §15.2 to match
whatever cardinality that derivation yields; **(2)** adopt the union but record
`history window` and `station encoding` as subsumed by `feature manifest` with the
subsumption written down, adding only `baselines`; **(3)** keep FR-P1-06-1's
fourteen and record the three as a known, accepted gap. **Recommendation: option
1.** It is the only one where the manifest hashes what §7.0B actually declares
immutable, and the precedence rule already recorded upstream — authority-derived
content over an unsupported count — points the same way. **The cardinality is not
stated here and must be calculated from the enumeration, never assumed.**
Option 3 is not recommended: it leaves baseline drift undetectable at a full-board
gate.

**BLK-05 — the D-17 target-schema test module. Creation approved 2026-08-22; the
name awaits owner selection.** The owner approved creating a new dedicated module
and the corresponding §12 amendment, and directed that three candidate names be
presented against the repository's existing conventions before any is finalized.

**Existing convention, enumerated from the amended §12 tree (19 modules).** All
are flat under `tests/`, all `test_<subject>.py`, all snake_case, subject a noun
phrase naming the thing under test: `test_station_registry`,
`test_acquisition_window`, `test_determinism`, `test_rinex_schema`,
`test_dcb_sign`, `test_hourly_target`, `test_iri_denial`, `test_phase_boundary`,
`test_reuse_registry`, `test_feature_availability`, `test_split_embargo`,
`test_train_only_transforms`, `test_common_masks`, `test_models_smoke`,
`test_checkpoint_restore`, `test_bootstrap`, `test_locked_test_guard`,
`test_release_hashes`, `test_clean_run`. Two carry a phase qualifier in
responsibility but not in name, and `test_hourly_target.py` is **Phase 2 only** —
so the new module cannot reuse that name.

**Proposed location:** `tests/`, flat, alongside the other 19. The tree has no
subdirectories other than `fixtures/`.

**Exact responsibility.** Assert that a Phase 1 target row carries **exactly**
D-17's frozen field set — `interval_start_utc`, `station_id`, `cell_gdlat`,
`cell_glon`, `cell_lat_bounds`, `cell_lon_bounds`, `vtec_tecu`,
`valid_observation_count`, `within_hour_spread_tecu`, `largest_internal_gap_s`,
`provider_dtec_summary`, `aggregation_config_id`, `target_valid`, `phase_id`,
`source_id`, `target_definition_id` — such that **a row carrying an excluded
field fails and a row missing a required field fails**. Excluded and never
substituted: `valid_satellite_count`, any per-satellite or per-IPP quantity,
zenith angle or weight, elevation, DCB, STEC, mapping output, arc or slip
statistics. This is FR-P1-03-5's own criterion; the module is its missing home.

**Three candidate names:**

| # | Name | Fit against the convention |
|---|---|---|
| 1 | `test_prepared_target_schema.py` | Mirrors the owning module `src/data/prepared.py`, as `test_station_registry.py` mirrors `registry.py`. Names the subject (prepared target) and the check (schema) |
| 2 | `test_target_contract.py` | Uses the phrase the authority itself uses — "target contract" appears in TE §2.2's protected list and throughout D-17. Shortest; does not disambiguate from Phase 2 by name |
| 3 | `test_phase1_target_schema.py` | Explicit phase scoping, distinguishing it from the Phase 2-only `test_hourly_target.py`. No existing module carries a phase prefix, so it would introduce a new naming pattern |

**No name is finalized here, and none is a recommendation dressed as a default.**
Candidate 1 fits the established mirroring convention most closely; candidate 3
is the most self-documenting against the Phase 2 module but breaks convention.

**BLK-06 — closed 2026-08-22.** The canonical protected set is frozen as **D-24**:
the 17-item deduplicated union, cardinality calculated from the enumeration, with
`history window`, `station encoding` and `baselines` added explicitly and
`baselines` enumerated to M-01, M-02, M-03, B-01 (IRI-2016 with its 2000 km
ceiling) and C-01 (CODE GIM). FR-P1-06-1 amended 14 → 17 under
`CR-2026-08-22-PROTECTED-SET`. **The implementation limb stays open** and gated by
G-09.

| Item | What is needed | Owner | Lead time | Blocks | If it slips |
|---|---|---|---|---|---|
| **BLK-05** — the D-17 target-schema test module | A **module name** for the test FR-P1-03-5's criterion implies, which exists in none of the 19 modules the §12 tree enumerates. Naming it is a §12 tree amendment | Functional design names it; **Supervisor** approves the tree amendment | Amendment lead time — the same class of change as the 2026-08-16 and 2026-08-22 amendments, both of which took a change record | **Bolt 6**. Reaches `features-and-splits`, which consumes the target rows the test would validate | Bolt 6 closes on everything except the schema test; the target contract goes unverified by any named module |
| **BLK-06** — the canonical protected set | An **item-by-item derivation** of the protected set from Technical Environment §2.2 and §7.0B under an **explicit deduplication rule**, with its **cardinality calculated from that enumeration** — never assumed, never hard-coded, and **not forced to equal fourteen** merely to preserve FR-P1-06-1 | Functional design derives; the **authorized project decision owner** approves the enumeration. Any change to FR-P1-06-1's item set, or to §2.2/§7.0B, runs through **Vision §15.2** change control | Derivation plus approval, plus a conditional §15.2 amendment if the derived set differs from FR-P1-06-1 in content or cardinality | **Bolt 2**'s transition-manifest scope. Reaches **G-P2** and **G-P3C**, whose pass condition is an empty protected-hash diff | While open, `diff_protected_hashes` could return the empty mapping that *is* G-P3C's pass condition **while a Phase 2 run has changed a baseline definition, a history window or a station encoding** — protected-protocol drift passing undetected at a full-board gate. Three §7.0B immutables (**history window**, **station encoding**, **baselines**) map to none of FR-P1-06-1's items today |

### A3 — Contract-type blockers, explicitly *not* Gate 0 items

Recorded here so their exclusion is deliberate rather than an omission. Per the
2026-08-22 ruling — which corrected an earlier wording that made them
unsatisfiable — these are **exit conditions on functional design, not entry
conditions**. The affected units **may enter** that stage; that is where the
contract is authored. **No affected Bolt or gate is marked complete until its
applicable exit conditions are satisfied**, and no implementation proceeds while
they stand.

| Item | Contract needed | Approval | Blocks completion of |
|---|---|---|---|
| **BLK-03** | The confirmatory-prediction contract — input and output types, alignment, ownership of the frozen seed set, allowed partitions, failure conditions. The frozen set reaches `three_seed_mean` as a **parameter from `ConfigSnapshot.seeds`**, never inlined in `src/models`, never weakened to a pairwise-distinctness check | Functional design | Bolts 8, 9, 10, 11, 12 |
| **BLK-04** | The per-fold train-only transform contract — including a `LeakageError` when `train`'s index is not a subset of the named fold's training partition | Functional design; the leakage **evidence** is accepted by the Supervisor at G-04 and G-05 | Bolts 7, 8, 9, 10, 11, 12 |
| **BLK-07** | The routing contract putting **every** `acquisition` read or write under `evidence/locked_test_restricted/` through `governance-guards.open_restricted`, so the `locked_test_accessed = true` row is written **before** the first December record is read | Functional design | Bolt 3 — and **no acquisition run may touch calendar 2022-12** while it stands |

---

## B. Supervisor-held gates

Seventeen gates govern this project. The seven this plan actually runs into are
below, each with the status and due condition the Vision gate table records. None
is this initiative's to grant, and **no Bolt order changes when they are signed**.

| Gate | What it accepts | Status | Due | Owner | Bolt or scope it affects |
|---|---|---|---|---|---|
| **G-09** | Agent preflight — all P0 freezes complete, automated zero-`TBD` check, `aws_ai_dlc_preflight_report` | Open | **Before any affected component is coded** | Supervisor / project owner | **Surfaced at Gate 0; signed later.** It cannot be signed at Gate 0 — its own §18.3 preconditions require the four configs to exist and their zero-`TBD` assertion to pass, and Bolt 1 creates those files. §18.3 is **component-scoped** (*"an affected component"*, *"its P0 decision"*), so scaffold work precedes it and implementation of an affected component does not. The permitted-before / barred-until boundary is enumerated in `bolt-plan.md` § "G-09 and G-01 — surfaced at Gate 0, signed later" |
| **G-01** | Scientific framing — question, IRI-role statement, comparison hierarchy, claims, horizon scope | Pending sign-off | Before implementation freeze | Supervisor | All Bolts. Its decision-log evidence already exists at `ideation/approval-handoff/decision-log.md` |
| **G-04** | Feature safety — availability matrix and dictionary, IRI-free contract proven | Open | **Before model tuning** | Supervisor (for ambiguous inputs) | **Bolt 7**, and gates Bolt 8's tuning. Accepts the FR-P1-04 group including the closed input space and the target-derived lag contract |
| **G-P1A** | Prepared-data acceptance and source viability, including the §6.1B coverage minimum (frozen as D-12) | Blocked — on the Madrigal replacement audit | Before the phase transition | Supervisor | **Bolt 4**. The threshold is frozen; the gate is blocked on the audit, which is a separate question |
| **G-05** | Experiment freeze — folds, masks, grids, seeds, estimand, bootstrap, regimes, storm rule, December regime audit | Open | **Before December access** | Supervisor | **Bolts 7, 8, 9.** Evaluation code must be authored, reviewed and frozen as part of the G-05 set before December is opened |
| **G-P2** | Phase transition — protocol hashes frozen, reuse and licence register complete | Blocked | Before Phase 2 raw processing | Supervisor | **Bolt 2** (both limbs: BLK-06's enumeration and the §10.1 register) |
| **G-07** | Reproducibility — CPU clean run, `environment_and_cpu_preflight_report`, clean-run log, matched artifacts | Blocked | Before thesis submission | Supervisor / reviewer | **Bolt 12** |

**G-06** (the locked evaluation) is listed for completeness: blocked on G-05, due
after it, executed by the student and authorised by the supervisor. It sits
outside the twelve Bolts — it is the one-shot, hash-before-metrics December run,
a distinct event from the **required, performance-blind** pre-G-05 December
coverage and regime audit that Bolt 4 performs.

---

## C. External data and product providers

Six providers. Every one is outside this project's control, and none has a
substitution path that does not change the science.

| Provider | What it supplies | Consumed by | Known hazard | If it slips |
|---|---|---|---|---|
| **Madrigal** (MAPGPS `gps` binned VTEC) | The Phase 1 prepared VTEC product, under D-144 | Bolt 3 | The CEDAR rules-of-the-road and acknowledgment must be attached. `madrigalWeb` client version must be **pinned and recorded — never `"unknown"`**; the FULL manifest has no such key today | Bolt 3 cannot start. No alternative source is approved; the ICTP source already failed on coverage (ARUC 27/365, BSHM 35/365, NICO 0/365) and is recorded rejected |
| **GFZ** | Kp/ap3 (≥ 3 h availability lag) and Hp60/ap60 (≥ 1 h) | Bolt 5 | Release status must be recorded, not only the lag | Bolt 5 stalls; Bolt 7's availability matrix has nothing to assert against |
| **Kyoto WDC** | Hourly Dst | Bolt 5 | **Release grades must never be mixed within one series** — real-time, provisional and final are different products. The non-commercial-use notice must be recorded **verbatim**, not by reference. Dst is diagnostic/hindcast-only and never a confirmatory ML feature | Bolt 5 stalls. Provisional Dst may characterise fixture selection only — never a modelling input, a frozen tolerance, or a G-05 regime count |
| **Canada, Solar Radio Monitoring Program** | Observed (not 1-AU-adjusted) F10.7 | Bolt 5 | A **documented month-long outage from 2022-03-18**. No imputation, substitution or reconstruction until the measured gap is recorded and governed. The trailing 81-day mean must end at the safe-lagged day — a centered mean is a defect, not a fallback | Bolt 5 stalls on the driver series. The three selection freezes in A1 are separate and additional |
| **CODE** | Final GIM comparator | Bolt 5, consumed at evaluation time by Bolt 9 | Evaluation-time only — never a model input. **No independence claim may precede the network-overlap audit**, and `gim_network_overlap_flag` must be disclosed once it runs | Bolt 9's comparison set is incomplete |
| **IRI-2016** | The benchmark | Bolt 5, consumed at evaluation time by Bolt 9 | **Generation is blocked if its validation report fails.** No `iri_*` field, IRI-derived residual or IRI-computed value may reach training or inference; IRI joins only onto the already-frozen comparison-wide mask | Bolt 5 stalls, and the primary comparison has no benchmark |

**Cross-cutting provider hazard.** Provider version drift is already observed in
this dataset (`g.002` versus `g.003`). Every retrieved file must record its **full
provider filename including the version suffix**, retrieval date and SHA-256, and
any mismatch against a previously recorded suffix must be **surfaced rather than
silently accepted**. For the three months with no `raw_isprint_cache/`, the
original suffixes were never recorded — which is why a disagreement between
original and re-acquired bytes would be uninterpretable there.

---

## D. Platform

| Item | Detail | Blocks | If it slips |
|---|---|---|---|
| **Kaggle** | The primary compute host and the Phase 1 acquisition/audit host. **Exactly two platforms are authorised** — Kaggle and local; Google Colab and Google Drive are explicitly removed as governed platforms | **Bolts 1, 3, 4, 12** directly. Bolt 1 needs install logs from **both** platforms for TA-03; Bolts 3, 4 and 12 must run the critical test set **inside the Kaggle session** | **No substitution path exists.** No third platform is authorised, and a governed run whose recorded `platform` is neither Kaggle nor local **fails**. A quota or availability problem stops the affected Bolts outright |
| **The 10.0 GB planning envelope** | A hard planning limit. The heaviest single job — 10,000 bootstrap replicates over 24-hour vector blocks carrying all three stations — runs inside it | **Bolt 10**; measured at Bolt 1 and re-measured at Bolt 12 | Recorded storage use above 10.0 GB fails REQ-ENG-11 rather than being reported as a warning |
| **CPU as a complete path** | GPU may only be an optional accelerator, never a dependency of any result | **Bolt 12**'s clean run; every Bolt's evidence | A result that depends on GPU cannot be accepted at G-07 |

**Why the in-session rule exists**, since it looks like duplication: a Kaggle
session carries no git working tree, so a commit hook cannot fire there and a
local suite run proves nothing about the environment the governed run actually
executes in. **The rule is conditional on the session, not on a Bolt number** —
any Bolt performing a governed Kaggle run owes in-session evidence, a new or
materially changed session owes fresh evidence, and pure-library work owes
nothing. Stated in full in `bolt-plan.md` § "What every Bolt owes".

**Infrastructure Design (3.4) is `SKIP` and stays `SKIP`.** The obligations that
stage would normally carry — platform responsibilities, configuration and secrets
handling, transfer hashes and provenance, storage and memory limits, CPU
execution and the clean run, and session-specific Kaggle evidence — are each
mapped to an owning Bolt, its required evidence and its accepting gate in
`bolt-plan.md` § "Infrastructure Design is `SKIP` — where its obligations went".
No obligation is dropped by the skip; only its usual carrier is.

---

## E. Licensing and third-party reuse

| Item | Detail | Owner | Blocks | If it slips |
|---|---|---|---|---|
| **The AGPLv3 Global-TEC-forecasting repository** | The one approved direct-copy source today. Whether its repository-distribution obligations permit that copying is **a governance dependency this project does not resolve on its own** | Outside this project | **G-P2** | **A defined fallback already exists**, which is why this degrades rather than blocks: reimplement the published method from the paper with a citation. That is the **standing default** while the question is open, not a decision deferred to discretion |
| **The §10.1 reuse register** | Every reused or materially adapted third-party source records all fifteen fields — `reuse_id`, repository URL, immutable commit or tag, upstream file and line or function, retrieval date, licence and SPDX ID, copied-versus-adapted status, destination file, scientific purpose, modifications, tests, original citation, notice location, reviewer, approval date — **before the code is used** | This project | **Bolt 2**; gate G-P2 | Bolt 2 cannot close, and G-P2 cannot pass |

**Standing rule.** No source whose licence is absent, ambiguous or incompatible
may be copied or materially adapted. Reimplement from the paper with a citation
instead.

---

## F. Obligations carried in from earlier stages

Not blockers, but items this plan hands to Construction with an owner and a due
gate rather than dropping.

| ID | Obligation | Owner | Due | Status |
|---|---|---|---|---|
| **RES-01** | No dedicated acceptance criterion verifies that a **permitted** December read — including the required pre-G-05 coverage and regime audit — writes its access-log row **before** the first December record is read. **This scenario is NOT TESTED** | The read is performed by `inventory-and-registry` (Bolt 4); the criterion is authored by **NFR requirements**, routed through Vision §15.2 | Before **G-05** | Ownership remediated; dedicated test coverage open |
| **RES-02** | `team-practices.md` § Testing Posture is stale on two figures: it defines Phase 1's acceptance set as WS-09 through WS-20, omitting FR-WS-4's WS-01 exception; and it states 17 §12-tree test modules where the amended tree and REQ-ENG-4 both now read 19 | The practices-affirmation gate owner | Next authorized practices-affirmation gate | Deferred. `org.md` reserves that file for that gate, so this plan does not edit it. **The Q11 answer adds a third item to flag there**: the narrower reading of TC-06's "test suite" |
| **RES-03** | FR-P1-06-1 still requires `protected_hashes.keys()` to equal a "fourteen-item enumeration" while the canonical set has not been derived | **Functional design** derives; the project decision owner approves; §15.2 amends FR-P1-06-1 if the derived set differs | Derivation before `phase_contract.py` is designed; reconciliation before **G-P2** and G-P3C | Pending canonical derivation; amendment conditionally required. See **BLK-06** |
| **TA-24** | The Technical Environment document checked against the current Vision version and marked superseded if the Vision changed | Author and supervisor document control | — | **No implementing unit.** Recorded as unassigned rather than attached to a Bolt that does not own it |
| **WS-13 evidence** | The story map gives WS-13's evidence as a matched-window parity assertion; §16's WS-13 row names `test_common_masks.py`, owned by a different unit. Two defensible readings exist and neither was adopted | **Functional design**, which owns verification planning; any change to §16's evidence column runs through Vision §15.2 | Before Bolt 7 closes | Open, pre-existing |
| **The `02` ordinal collision** | Phase 1's `02_standardize_prepared_target.py` and Phase 2's `02_build_vtec_target.py` share the ordinal in the §12 tree | A §12 defect, not this project's to amend | — | Open. The adopted reading: the ordinal denotes pipeline position and `--phase` selects exactly one. **Code generation must not invent a `02a`/`02b` convention** |

---

## Summary — what Gate 0 must put in front of the owner

Enumerated rather than counted, so nothing is lost to a wrong total:

### Closed by owner decision, 2026-08-22

| Item | Decision | Record |
|---|---|---|
| **BLK-02** — plumbing fixture station | **BSHM 32/35**, on the only complete measured coverage of D-11's window (168/168 bins, 7/7 days). ARUC and NICO reserved for separate missing-data and robustness tests | **D-20** |
| **F10.7 daily value** | **Daily median**, with an enforced observation-availability rule and no same-day look-ahead | **D-21** |
| **F10.7 duplicate UT** | **Mean of duplicates** + count logging + QC flag; provider-correction semantics take precedence if ever established | **D-22** |
| **F10.7 high-spread days** | **Flag and retain**; median is the representative value; the QC flag is not a model feature without separate approval and a causality check | **D-23** |
| **BLK-06** — canonical protected set | **17-item deduplicated union**, cardinality calculated; `history window`, `station encoding`, `baselines` added; FR-P1-06-1 amended 14 → 17 | **D-24**, `CR-2026-08-22-PROTECTED-SET` |
| **"Full-year job"** | **Defined in TE §9.2**: three classes, only class C (full-year scientific processing and evaluation) requires prior fixture evidence. Class A acquisition and integrity verification do not — with every December restriction intact | `CR-2026-08-22-SCOPE-DEFS` |
| **Stub stage scripts** | **Scaffolding**, provided they carry no scientific implementation, governed execution, full-year processing, acquisition, feature-generation or model-training logic, and no December access. One-unit-per-Bolt preserved | Owner ruling; recorded in `bolt-plan.md` § G-09 |
| **BLK-05** — new module | **Name chosen: `tests/test_prepared_target_schema.py`**, with the §12 tree entry and amendment-provenance row added. **Naming is not building** — the module does not exist and has never been run; creation stays gated by G-09 and stage 3.5. Acceptance behaviour fixed by the owner: exactly D-17's 16 fields **passes**, an excluded or additional field **fails**, a missing required field **fails**. (Superseded literal, preserved: "**The name is not chosen** — three candidates await owner selection") | **`CR-2026-08-22-TARGET-SCHEMA-TEST`**; see § A2 |

### Still open

**Surfaced at Gate 0, signed later:**

1. **G-09** — agent preflight. Cannot be signed at Gate 0; signed before any affected component is coded.
2. **G-01** — scientific framing, pending sign-off.

**Awaiting the owner's explicit selection or final wording — NOTHING REMAINS
UNDER THIS HEADING.** All four items (3, 4, 5, 6) were decided and applied on
2026-08-22 and are retained below under their original numbers, marked `CLOSED`,
so the numbering the rest of this document cites stays stable. The heading is kept
for the same reason.

**Consequence for Gate 0, recorded at its discharge:** with these four closed and
BLK-02 plus the three F10.7 freezes resolved by D-20 through D-23, **Gate 0 holds
no live owner decision.** What is left is not decidable there by design — G-09
cannot be signed at Gate 0 because its §18.3 preflight reads four config files
that Bolt 1 creates, G-01 is pending sign-off before the implementation freeze,
and BLK-06's per-item config binding belongs to the functional-design gate under
the `DP-CHAIR-02` ruling.

3. **CLOSED 2026-08-22 — BLK-05's module name is chosen: `tests/test_prepared_target_schema.py`.** Approved by the project decision owner under **`CR-2026-08-22-TARGET-SCHEMA-TEST`**, added to the TE §12 `tests/` tree with its responsibility comment and to the §12 amendment-provenance table. **Naming a module is not building it — two of four limbs remain open:** the test **does not exist** (creation gated by G-09 and stage 3.5) and has **never been run** (no result of any kind is claimed). The approved acceptance behaviour is fixed so implementation cannot narrow it: a row with exactly D-17's approved 16 fields **passes**; a row with an excluded or additional field **fails**; a row missing any required field **fails**. The item as originally stated, retained: *"Creation is approved; the name is not. Three candidates, the proposed location and the module's exact responsibility are in § A2."*
4. **CLOSED 2026-08-22 — FR-P1-01-7's amendment is applied.** Applied under **`CR-2026-08-22-F107-CORRECTIONS`** after the owner-directed presentation of the current text, the exact replacement, both corrections, the downstream effects and the leakage confirmation. The row now reads that the suspected 2022-03-18 outage was audited and **no missing calendar day was observed — at least one observation present on 365 of 365 days** — while explicitly **not** asserting uninterrupted within-day coverage or provider availability; and it names the four high-spread days with their true outlier hours (18, 20, 20, 17 UT), replacing the wrong claim that three of four fell at 20 UT. The item as originally stated, retained: *"Approved in principle under Vision §15.2; the owner directed that the current text, the exact replacement, the two corrections, the downstream effects and a leakage confirmation be presented before finalization. **Not applied.**"*

<!--
  Items 3 and 4 annotated in place 2026-08-22, AFTER this stage's approval gate,
  on the project decision owner's explicit approval at the Gate 0 discharge —
  following the annotate-in-place precedent the owner set at
  GOV-2026-08-22-INC-01 Rec 7, where the board itself split on whether a
  completed stage's artifact may be annotated after its gate.

  Both were stale STATUS CLAIMS carrying no numeral: item 3 said the name "is
  not chosen" when CR-2026-08-22-TARGET-SCHEMA-TEST had chosen it, and item 4
  said "Not applied" when CR-2026-08-22-F107-CORRECTIONS had applied it. Neither
  was findable by CR-2026-08-22-INC-CORRECTIONS Rec 5's sweep, which searched
  superseded count literals. They are the eighth and ninth defects of that class
  recorded in CR-2026-08-22-SWEEP-COMPLETENESS.

  Superseded text preserved verbatim inside each item. No gate, owner, lead
  time, provider, December protection, access-log statement, acceptance row or
  scientific value is changed.
-->
<!-- markdownlint-disable-line -->
5. **CLOSED 2026-08-22 — the four leakage prohibitions have §19 TA rows.** Approved by the project decision owner and applied the same day under **`CR-2026-08-22-LEAKAGE-TA`**: TE §19 gains **TA-33, TA-34, TA-35 and TA-36**, one negative-path row per requirement (FR-P1-04-12, -13, -16, -17), each naming the prohibited behaviour, the deliberately invalid input and the expected protective behaviour. **What that closes and what it does not:** each requirement now has an acceptance **criterion**; none has an implemented test (no module exists), none has been executed, none has passed, and all four rows read `Pending`. Module placement is an open assignment at stage 3.1. The recommendation as originally recorded, retained: *"Recommendation: approve — a prerequisite with no acceptance row is enforced only by attention."*
6. **CLOSED 2026-08-22 — `unit-of-work.md`'s blocker register is synced.** Annotated in place under **`CR-2026-08-22-INC-CORRECTIONS`** (`GOV-2026-08-22-INC-01` Rec 7), the owner having settled the annotate-in-place question that the board itself split on: **BLK-02**'s station limb discharged by **D-20**, `fixture_manifest.yaml` limb open; **BLK-05**'s naming and documentation limbs discharged, implementation and execution limbs open; **BLK-06**'s enumeration limb discharged by **D-24**, per-item config binding and implementation open. **No blocker is closed outright and the count of open blockers remains six.** The conflict as originally stated, retained: *"D-20 discharges BLK-02's station limb and D-24 discharges BLK-06's enumeration limb, but the stage 2.7 register still shows both open. Leaving it stale is the unpropagated-correction defect `GOV-2026-08-22-UG-02` Rec 3 already flagged once."*

**Open obligations, not decisions:**

7. **F10.7 publication latency — handled by a conservative convention (D-25), not blocked on NRCan.** The held file carries no publication timestamp, so actual latency is **unverified**. A daily median becomes available no earlier than `00:00 UTC` on the following day, which prevents same-day look-ahead by construction and is 1–2 hours more conservative than measured observation completion. **An explicit project assumption; it proves nothing about historical publication availability and supports no operational real-time claim.**
8. **F10.7 March–April 2022 provenance — recorded unresolved (D-26).** Measured, reconstructed, interpolated or provider-corrected: **asserted in no direction**, because the file carries no qualifier, flag or provenance column. Data retained. Two clarification routes identified that change no frozen source and re-download nothing: internal consistency of the provider's own `fluxadjflux` / `fluxursi` derivations across the window (analysis of held bytes), and the optional NRCan enquiry. An `ABL-NOSW`-style F10.7 sensitivity is **identified, not approved or scheduled**, and would run on frozen January–November folds only, predeclared in `experiment.yaml`, without touching locked December.

**The §15.2 amendment was approved and applied 2026-08-22 — item 9 below.**

9. **CLOSED 2026-08-22 — TE §7.0A stage 4 and EV-12 amended so a declared conservative convention satisfies the F10.7 publication-timestamp obligation.** Approved by the project decision owner and applied the same day under **`CR-2026-08-22-EV-12`**; the preceding request is retained as `CQ-2026-08-22-EV-12`. **Bolt 5 now has a sanctioned instruction for the F10.7 row** — record D-25's convention, the documented absence of a provider publication timestamp, and an explicit unverified-latency statement — **and is not forced to proceed with an incomplete row.** The conflict as originally stated, retained for the record: The exact conflicting text: TE §7.0A stage 4 requires *"the space-weather availability matrix with observation and publication timestamps"*, and **EV-12** names *"Provider release documentation"* as the evidence for external-feature publication latency, due at **Feature freeze (G-04)**. `components.md`'s `availability.py` mirrors the same obligation. **Not in conflict:** F10.7's own §6.2 dictionary rows record provenance as *"Approved source"* and demand no publication timestamp — unlike `kp_safe` / `ap_safe`, whose row explicitly requires *"observation + publication timestamps"*. **Registered as `CQ-2026-08-22-EV-12`** (`governance/CHANGE_REQUEST_2026-08-22_EV-12_f107_publication.md`), awaiting owner decision — **not approved, not applied**. **Minimum amendment sought:** that the F10.7 row of the availability matrix may record D-25's convention plus the documented absence of a provider timestamp in place of a verified one, and that EV-12 be satisfied for F10.7 by that record. **Granted 2026-08-22. EV-12's F10.7 limb is no longer unmet at G-04.**

## Assumptions & Open Questions

- **[assumption]** Lead times are described qualitatively ("one decision", "an
  amendment lead time") rather than in days. No artifact records a calendar
  estimate for any of these, and inventing one would put an unsupported number
  into a governed document.
- **Resolved 2026-08-22, no longer an assumption.** The A1/A2 split is now an
  explicit owner ruling (`DP-CHAIR-02`), recorded in § A2 and in `bolt-plan.md`
  § Gate 0: functional design may analyze BLK-05 and BLK-06 and produce their
  resolution evidence, the owner decides, and dependent implementation stays
  barred until the decision is recorded.
- **Open.** Whether the ten-item list above is the owner's intended scope for
  "all unresolved owner decisions and other true entry-blocking conditions". It
  was assembled from the blocker register, the two gates that bound
  implementation, and four questions this remediation surfaced. If the owner has
  an item in mind that is recorded nowhere in the artifact set, this stage cannot
  have found it.
- **Not measured here.** Every provider figure in § A1a was derived from the held
  `fluxtable.txt` on 2026-08-22 and is a property of **that retrieved file**, not
  an independent verification of the provider's archive. Re-acquisition could
  yield different bytes, which is exactly why FR-P1-01-2 requires the version
  suffix to be recorded and any mismatch surfaced.
- **No locked-test access occurred in producing this artifact.** The F10.7 file
  sits at `evidence/audit_ec1_2026-08-15/nrcan_f107/`, outside
  `evidence/locked_test_restricted/`. It is a time-indexed solar driver series,
  not December target values or model performance; one December-dated row
  (2022-12-08) appears in the duplicate-UT list as a property of the driver file.
  Reading it is not a December access under Vision §8.3, and no access-log row
  was owed or written.
- **None** of the above adopts a reading on a supervisor-owned value, and none
  decides a scientific constant.

## Corrections applied on resume, 2026-08-22

Two items under § Still open → "Awaiting the owner's explicit selection or final
wording" were **stale**: both had been decided and applied on 2026-08-22, and this
document still listed them as pending an owner decision. A dependency map that
reports a closed decision as open is worse than one that omits it, because the
reader budgets time for a decision that has already been made.

| Item | Was | Now |
|---|---|---|
| **5** — whether the four leakage prohibitions get §19 TA rows | Awaiting owner; carried a "Recommendation: approve" | **CLOSED** — approved and applied under `CR-2026-08-22-LEAKAGE-TA`; TA-33…TA-36 exist. Recorded with the four distinctions intact: criterion **yes**; implemented test **no**; executed **no**; passed **no**; all four rows `Pending`; module placement open at stage 3.1 |
| **6** — whether `unit-of-work.md`'s blocker register is synced | Awaiting owner; carried a "Recommendation: sync it" | **CLOSED** — annotated in place under `CR-2026-08-22-INC-CORRECTIONS` (`GOV-2026-08-22-INC-01` Rec 7). **No blocker closed outright; the open-blocker count remains six** — BLK-02, BLK-05 and BLK-06 each had one limb discharged |

**Numbering is deliberately unchanged.** Both items keep their original numbers
and stay in place, marked `CLOSED`, because other sections of this document and of
`bolt-plan.md` cite them by number. The heading above them now says items 3 and 4
only. This follows the pattern item 9 already set in this file.

Each closed item retains its original conflict statement and recommendation
verbatim, so what was proposed stays separately auditable from what was decided.

**Neither correction carries a numeral**, which is why `CR-2026-08-22-INC-CORRECTIONS`
Rec 5 — a sweep for count literals — could not have found them. Raised at the
approval gate.

**Not changed in this file:** every gate, owner, lead time, external provider,
December protection and access-log statement. No scientific constant, no
supervisor-owned value, no acceptance row.
