# Change Record — 2026-09-19 — Student decisions D-43 … D-48 adopted and implemented: interval semantics, lagged-selection owner, IRI reference disposition, F10.7 composition (reading B), recomputation tolerance, December scan repair and class 5; P-5 correction; six-entry configuration diff prepared

**Change ID:** `CR-2026-09-19-SCI-DECISIONS`
**Authority:** the project decision owner's instruction of 2026-09-19 ("This message
supplies my student decisions and authorizes their narrowly scoped implementation,
documentation, and verification", items 1–10), continuing `CR-2026-09-19-SCI-REVIEW`.
**Boundary respected:** no configuration transcription, producer artifact,
`write_release`, `permitted_producers` entry, dataset registration, model training,
commit or push. D-39 … D-42 and unrelated working-tree changes preserved. No supervisor
approval fabricated; every mandatory approval is listed as OPEN where it is.
**Repository state:** HEAD `18843aa`; no commit.

Status vocabulary used per item: **[ADOPTED]** student decision recorded in
`evidence/DECISIONS.md`; **[IMPLEMENTED]** code/contract/test change complete and
verified; **[APPROVAL OPEN]** mandatory external approval outstanding; **[UNRESOLVED]**
evidence or mathematical issue still open.

---

## 1 — P-1: interval semantics → **D-43** [ADOPTED] [IMPLEMENTED] [APPROVAL OPEN: supervisor countersignature, TE §18.2 Q-16]

Recorded as a **new clarification** (not something D-42 or TE §6.2 had unambiguously
specified — Vision §7.3's "time represented by the value" names no boundary). Source
labels and both interval boundaries are preserved in every derived row
(`source_interval_start_utc`, `source_interval_end_utc`); the reference instant (interval
END) is a separate field and never overwrites the provider label. Kp/ap
`available_at = end + 3 h`, Hp60/ap60 `= end + 1 h` — assumptions for retrospective
evaluation, establishing no historical publication or revision-completion time.

## 2 — P-2: one lagged-selection owner → **D-44** [ADOPTED] [IMPLEMENTED]

**Interfaces inspected:** `build_features` reads `driver_values[origin]` from the hourly
`source_series` and applied no lag; `_assert_driver_alignment` (R-76a) required a value to
sit inside its own raw interval, which a lagged series cannot satisfy; the matrix rows
were caller-built. **Smallest coherent repair:**

| Where | What |
|---|---|
| `src/external/spaceweather.py` | `select_lagged_series(observations, epochs, safe_lag_hours)` — the ONE place the lag is applied; per origin: selected value, source interval (both boundaries), `available_at_utc = end + lag`, origin. A selected interval with a missing value keeps its identity (`value` None); no older interval is reached back to. `assert_lagged_selection` — the alignment contract for lagged series (traceability, `available_at` = end + lag ≤ origin, latest eligible chosen, no present value dropped). `availability_rows_from_selection` — matrix rows with `observation_timestamp` = source END. |
| `src/features/build.py` | `_assert_driver_alignment` in two explicit forms: raw own-interval check unchanged; lagged series (`attrs["selection"]`) checked by `assert_lagged_selection`, rows must carry the selection fields, and a selection lag ≠ the matrix's `safe_lag_hours` is refused (no double lag / shortfall). Nothing is shifted and nothing is relabelled. |
| Design text | `external-products` R-58 and `features-and-splits` R-76a amended with dated blocks. |

**Verified (synthetic, source values unchanged):** Kp `[00,03)` unavailable at 05:00,
eligible at 06:00; `[03,06)` eligible from 09:00; Hp60 `[04,05)` unavailable at 05:00,
eligible at 06:00; open / not-yet-available interval refused; stale selection refused;
double lag and shortfall refused; untraceable value refused; dropped present value
refused; the same rows re-checked under a different lag refused; missing selected value
composes with `apply_carry_forward` (fill recorded, excluded beyond the bound);
end-to-end through `build_features` the value at day-2 09:00 is the raw `[03,06)` value
(no second shift), a mismatched selection lag and an unrecognised rule are refused, a
lagged series presented as raw is refused by the own-interval check, a raw series still
passes. Tests: `tests/test_external_drivers.py` (+8), `tests/test_feature_availability.py`
(+1 build-level).

## 3 — P-3: standard IRI as a disclosed retrospective reference → **D-45** [ADOPTED] [APPROVAL OPEN: TE §18.3 "the IRI role"; Vision §6.11 driver-input freeze] — dependent patch PREPARED, not applied

**Inspection performed on the actual package (not comments or presumed defaults).**
`iricore` is **not installed** in the governed environment and is **not pinned** in
`requirements.txt` (TE §8.1 lists it as required — an environment gap, listed below). The
current release is **1.9.0** (PyPI, 2026-09-19); its repository source at `master` was
downloaded to the scratchpad and read:

| Question | Resolved from | Answer |
|---|---|---|
| Wrapper / entry point | `src/iricore/tec.py:vtec`, `iri.py:iri` | `vtec(dt, lat, lon, hbot=90, htop=2000, hstep=0.5, version=DEFAULT_IRI_VERSION, jf=None, **kwargs)`; refuses `htop > 2000` (the project's ceiling is the wrapper's maximum); integrates `iri()` electron density in ≤1000-point stages. `iri()` converts inputs to Fortran types and calls `iricore_` (IRI_SUB) with `aap, af107, nlines` from `_APF107_DATA`. |
| IRI version | `config.py: DEFAULT_IRI_VERSION = 20` | **Default is IRI-2020**; the project must pass `version=16` explicitly (IRI-2016 Fortran shipped under `iri2016/`). |
| Index data path | `read_iri_data.py:read_apf107`, `data/index/` | `apf107.dat` (format `(13I3, 3F5.1)`: 8 × 3-hourly ap, daily Ap, F10.7 daily, F10.7_81, F10.7_365) and `ig_rz.dat`; shipped in the package; `indices_uptodate(dt)` only checks coverage; `iricore.update()` replaces them (must never run after the freeze — pin by SHA-256). Shipped `apf107.dat` ends 2024-06-17; `ig_rz.dat` updated 6/2024, so 2022 IG12/Rz12 are final centered means, not predictions. |
| Observed vs adjusted F10.7 | `irisub.for` lines 1092–1096; shipped `apf107.dat` vs `fluxtable.txt` | IRI: *"F10.7 should be adjusted (to top of atmosphere) value not observed"*; the file's daily value on 2022-06-15 (144.5), 03-31 (239.0), 08-28 (257.0), 08-29 (133.1) equals the **`fluxadjflux` of the 20 UT reading** on each day — **adjusted, single 20 UT reading, flare-contaminated readings included** (vs the project's observed median). MSIS-side quantities are converted back to observed inside IRI (`f_adj = radj²`). |
| Daily / 81-day / 365-day defaults | `APF_ONLY` header; recomputed from the file | daily = target day; F10.7_81 = **centered** 81-day mean (file 131.8 = centered 131.8; trailing would be 132.6); F10.7_365 = **centered** 365-day mean (123.6 = centered). |
| Override coupling | `irisub.for` 1103–1120; `iri.py` oarr40/oarr45 | `oarr40` alone also sets F107_81 and F107_365 to the daily value; `oarr45` alone also sets the daily to the 81-day value — overrides change three quantities at once. **No override is used (D-45).** |
| Target-day ap | `irisub.for:1349 call apf(isdate,hourut,indap)`; `jf(26)` default true | foF2 storm model consumes the 3-hourly ap history up to the **target** UT hour of the **target** day; `jf(35)` foE storm off by default; no ap override exists. |
| Other centered/predicted inputs | `read_ig_rz` header | IG12/Rz12: 12-month running means using six months before and after the month; predictions only within six months of the file's update date (not 2022). |
| Exact invocation for this project | D-45 item 1 | `iricore.vtec(dt=target_time, lat, lon, hbot=90, htop=2000, hstep=<frozen>, version=16, jf=None)` — `default_edens` jf preset, no `oarr` kwargs, shipped index files pinned by hash. |

**Comparison framing retained:** same target, `target_definition_id`, locations, units,
target times and comparison-wide scoring rows; the information asymmetry (model inputs at
the origin under D-25/D-42/D-43; reference inputs retrospective, centered, target-day) and
the benchmark's purpose (climatological reference, not an operational forecast) are stated
wherever the comparison is interpreted; outperforming it establishes no operational
superiority. **Dependent patch:** `governance/proposed/P-3_iri_report_confirmations.patch`
(R-59 limb-3 confirmations become a recorded disclosure + hash/version/no-override
fields) — applies only with the supervisor's approval; TE §6.2 row and Vision §6.11 text
amendments listed in D-45 item 4 likewise wait.

**[UNRESOLVED — environment]:** `iricore` pin absent from `requirements.txt` and package
not installed; the "installed version" could not be inspected, so the freeze must pin the
version (1.9.0 today) and the shipped index-file hashes when it is installed.

## 4 — A3 = option B → **D-46** [ADOPTED] [IMPLEMENTED] [APPROVAL OPEN: supervisor countersignature, TE §18.2 Q-16/Q-17]

Implemented in `spaceweather.resolve_f107_at_origin` (returns `F107Selection`); ordinary
reuse vs missing-update extension separated; clock from the expected availability instant;
inclusive `≤ carry_forward_bound_hours` (00:00–03:00 kept, 04:00–23:00 excluded until a
valid update); NaN medians are missing; unknown vocabulary refused; a frozen composition
without the configured bound refuses. `f107_81_trailing`: exact window at the eligible
anchor, never imputed, never an older window → unavailable for the whole affected day; with
both rows in the feature set the completeness rule drops all 24 origins (documented in
D-46 item 3). **Affected-origin count** (`daily_medians_from_readings` — D-21 median,
D-22 duplicate averaging, D-23 flag-and-retain — on the held file; December readings never
read): 365/365 days 2021-12-01 … 2022-11-30 carry a median; duplicate days
{03-26, 09-20, 10-17, 10-23} and high-spread days {01-18 32.5 %, 03-31 60.6 %, 08-28
78.1 %, 08-29 179.2 %} reproduce D-22/D-23 exactly; **8016 origins, 0 carried, 0 excluded**.
The sensitivity protocol stops at Step 0. No December outcome inspected. Design text:
R-57a amended (dated block). Tests: +4 in `tests/test_external_drivers.py`, +1 (medians).

## 5 — A4: 8.0e-12 sfu → **D-47** [ADOPTED — conditional approval VERIFIED] [IMPLEMENTED]

**Derivation checked against the actual calculation** (`trailing_mean`: parse to float64,
Python `sum` over 81 terms, `/ 81`; governed CPython 3.11 `sum` is plain sequential —
compensated summation on ≥ 3.12 only reduces error):

| Component | Bound on the mean's error |
|---|---|
| decimal → float64 per constituent | ≤ u·B (u = 2⁻⁵³, correctly rounded) |
| N−1 sequential additions | ≤ γ_{N−1}·Σ|xᵢ|/N ≤ (N−1)·u·B·(1 + O(N·u)) |
| division by N | ≤ u·B |
| **total** | **(N+1)·u·B + O(N²u²B)**; stated as **(N+1)·ε·B with ε = 2⁻⁵² = 2u**, a factor ≈ 2 of margin that absorbs the second-order term — the bound is rigorous, not merely first-order |

(N+1)·ε·B = 82 × 2.220446e-16 × 400 = **7.283 × 10⁻¹²** → rounded **up** to one significant
figure **8.0 × 10⁻¹²** (the only adjustment). **Reference representation:** constituents
are exact decimals — D-21 medians of 0.1-sfu readings, D-22 duplicate means → multiples of
0.05 sfu; the reference is `Fraction` arithmetic end to end. **Daily aggregation:** the
median of ≤ 5 slot values is a grid value (odd count) or a half-grid mean (even count) —
exact. **Storage round trip:** `json` writes `repr`, read back exactly; a 6-decimal writer
breaks the certificate in > 300 of 320 synthetic windows and must be refused at freeze.
**Independent checks:** max |float − exact| = 1.9 × 10⁻¹³ (synthetic 0.05-grid windows in
60–400 sfu); 80-day and shifted-anchor perturbations differ by > 10⁻³ sfu.
**Applicability condition:** **B = 400 sfu**, explicit, not a physical maximum
(`assert_recomputation_domain`: a constituent above B fails the certification with a
clear `IntegrityError`, is left unchanged, never clipped or deleted; the tolerance is never
raised silently). Held daily medians (Dec 2022 excluded) reach 311.7. **Numerical agreement
only**, not sensor accuracy. **Result: the derivation supports 8.0e-12 → recorded as D-47.**
Code: `recomputation_tolerance_bound`, `assert_recomputation_domain`, optional
`input_bound` on `assert_anchor_recomputed`; test
`test_d47_tolerance_derivation_against_an_exact_reference_and_the_certified_domain`.

## 6 — G-3/P-4: December scanning → **D-48** [ADOPTED] [IMPLEMENTED]

**Comparison of the prepared class-5 wording with the owner's conditions:** the prepared
text included `GFZ-AUDIT.md`, `retrieval_record.json`, `sha256_manifest*.json` and
`environment_supplemental.json`; the owner's scope covers *raw external-driver captures and
source-version audit summaries*. The adopted class is **narrower**: three patterns
(`Kp_*.wdc`, `hp60ap60doi_*.txt`, `gfz-comparison-report.json`), content validated by
schema (raw lines parse with no extra column; the report's fixed key set with `y` admitted
only inside `{y, m, d, h}` epoch keys and `coverage` only under `validation`), provenance
required (sibling `retrieval_record.json`: SHA-256 for raw files, `run_id` for the report),
mixed/unknown content fail-closed, excluded files inventoried with reason and exposure.
Authority: R-26's class list was amended by the owner before (D-30) — the same authority
applies; no target value is involved.

**Scanner coverage (reported separately from compliance)** — `december_custody_inventory`
on the real tree, 369 files outside the restricted root, 0.9 s:

| Detection method | Files | Formats |
|---|---|---|
| json-structural (parsed: literals anywhere, `{y,m}` records at any depth, month-number keys) | 29 | `.json` |
| wdc-line / hpo-line (date layout of the provider format) | 2 / 2 | `.wdc`, Hpo `.txt` |
| text-literal (`2022-12` / `202212`) | 51 | `.txt` (fluxtable), `.html`, `.csv`, `.jsonl` |
| csv-epoch (`ut1_unix` in December 2022) | subset of the CSVs | Madrigal record CSVs |
| isprint-endpoint (first/last record epoch only — **endpoint inspection, not a full parse**, disclosed) | 282 | `raw_isprint_cache/*.txt` |
| **outside automated inspection** | 5 | `.md` (EC1-AUDIT, GFZ-AUDIT, DECISIONS, experiment_registry, CORRECTION_2026-08-16) — governance prose, handled by human review, never labelled clean |

**Compliance result:** 0 flagged; **9 excluded and inventoried**: class 3
`ec1-audit-report.json` (month-number keys), class 4 `.dst_summary.json` (month-number key
"12" — corrected from the 2026-09-19 review's "not detected"), class 1
`dst_provisional_202211.html` (one `202212` navigation link), class 2 `fluxtable.txt` (95
December-2022 reading lines), class 5 `Kp_now2022.wdc`, `Kp_def2022.wdc` (31 December day
lines each), `hp60ap60doi_2022_v2.txt`, `_v3.txt` (744 December hourly lines each),
`gfz-comparison-report.json` (229 December epoch records). A legacy-encoded provider page
(`onDstindex.html`, non-UTF-8) is decoded as Latin-1 for detection (non-JSON only; JSON
must be UTF-8 and fails otherwise) — previously that file would have made the widened scan
fail as unreadable. Existing exclusions verified against their content conditions (class-1
page carries `Dst` and no target word; every `fluxtable.txt` line parses; classes 3/4 carry
no target key token).

**Exposure versus use (what was actually read):** the four GFZ files were parsed in full
(calendar 2022, December included) on 2026-09-18 for identification, hashing, format
validation and version comparison; the comparison report records the December differing
epochs; `fluxtable.txt` was read for measurement times (all months), the pre-2022 window
test (dates < 2022 only), the A4 bound (December 2022 excluded) and the A3 count (December
readings skipped). **No method, feature, threshold, lag, missingness policy or model
decision was informed by any December value**: D-43/D-44 are semantics decisions on the
rule text; D-46 was selected by the owner and its count excludes December; D-47's bound
excludes December; D-48 is a custody rule. **No concrete method-selection use exists to
flag for disposition.** Holdout independence is not asserted "unaffected"; the record
above is the evidence.

## 7 — P-5: stale authorization wording [IMPLEMENTED]

`governance/CHANGE_RECORD_2026-08-22_EV-12_f107_publication.md` records **"APPROVED AND
APPLIED 2026-08-22"** by the project decision owner, scope = the EV-12 row shape (TE EV-12
row, §7.0A stage 4, `components.md`/`availability.py`). Corrected with dated references,
history preserved: `src/external/iri.py` (module docstring, R-59 limb-4 docstring and error
text — the pre-grant wording quoted as history); `evidence/DECISIONS.md` D-25 review-table
row and the D-31 §18.3 row annotated in place (owner-authorised, this instruction). The
grant is not broadened: it certifies no lag, producer or G-04 outcome.

## 8 — Verification

Focused runs during implementation (governed pin, conda `tec-thesis-311`): every touched
module green after each step. **Full suite:** see § 8.1 (appended when the run completes).
No test weakened; no skip added; the D-25 tests updated for the `F107Selection` return type
assert the same facts plus the new fields.

### 8.1 Full-suite result

Governed pin (conda `tec-thesis-311`, CPython 3.11.16, every `requirements.txt` pin), `python -m pytest tests -q`: **1273 passed / 4 skipped / 0 failed / 0 errors**, exit 0 (previous full run: 1256 passed / 4 skipped; +17 tests this pass). The four skips are the pre-existing environment preconditions. `compileall` on `src`, `scripts`, `tests`: clean. `git -c core.whitespace=cr-at-eol diff --check`: clean; `configs/`: zero diff; HEAD `18843aa`; no commit.

## 9 — Proposed six-entry `availability_lags` configuration diff (NOT applied)

Consistent with D-25 (rule), D-42 (floors as assumptions), D-43 (interval END), D-46
(composition), D-47 (tolerance and domain). `release_status_required` values must equal
the grade token the producer stamps (D-39 nowcast; D-40 Hpo.0002 V2.0) and are written
here as proposals for that reason.

```yaml
# configs/features.yaml — PROPOSED, not applied (CR-2026-09-19-SCI-DECISIONS §9)
carry_forward_bound_hours: 3                 # TE §6.2 / TC-09 (D-116)
carry_forward_composition: "clock_hours"     # D-46 (reading B); supervisor countersignature OPEN

availability_lags:
  kp_safe:
    safe_lag_hours: 3                        # D-10.3 / D-116; D-42 floor accepted as an assumption
    lag_reference_instant: "interval_end_utc"   # D-43: completion + 3 h (supervisor countersignature OPEN)
    selection_rule: "latest_completed_interval_plus_lag"   # D-44 (spaceweather.select_lagged_series)
    release_status_required: "nowcast"       # D-39: archived settled nowcast (Kp_now2022.wdc)
    publication_latency_statement: >-
      GFZ Kp_now2022.wdc (DOI 10.5880/Kp.0001) carries no per-value publication timestamp; the
      3-hour floor after interval completion is a project assumption for a retrospective study
      (D-42, D-43), not a demonstrated publication or revision-completion bound; results using
      this archive do not establish exact operational replay or absence of revision-related
      look-ahead.
  ap_safe:
    safe_lag_hours: 3
    lag_reference_instant: "interval_end_utc"
    selection_rule: "latest_completed_interval_plus_lag"
    release_status_required: "nowcast"
    publication_latency_statement: >-
      (identical to kp_safe; same provider file and floor.)
  hp60_safe:
    safe_lag_hours: 1
    lag_reference_instant: "interval_end_utc"   # D-43: completion + 1 h
    selection_rule: "latest_completed_interval_plus_lag"
    release_status_required: "hpo_v2.0_contemporaneous"   # D-40: Hpo.0002 V2.0; V3.0 is a comparator only
    publication_latency_statement: >-
      GFZ Hp60ap60doi_2022.txt V2.0 (DOI 10.5880/Hpo.0002) carries no publication timestamp and no
      definitive grade; the 1-hour floor after interval completion is a project assumption for a
      retrospective study (D-42, D-43); V3.0 (DOI 10.5880/Hpo.0003) is a later algorithm-recomputed
      comparator, never an input.
  ap60_safe:
    safe_lag_hours: 1
    lag_reference_instant: "interval_end_utc"
    selection_rule: "latest_completed_interval_plus_lag"
    release_status_required: "hpo_v2.0_contemporaneous"
    publication_latency_statement: >-
      (identical to hp60_safe; same provider file and floor.)
  f107_safe:
    availability_rule: "previous_day_median_midnight_utc"   # D-25 (Route 1); no scalar lag
    release_status_required: "observed"      # NRCan fluxobsflux; project-derived daily median (D-21/D-22/D-23)
    publication_latency_statement: >-
      fluxtable.txt carries no publication timestamp; availability_ts(median(D-1)) = 00:00 UTC on D is
      an explicit project assumption (D-25), 1-2 h after the day's last reading (23 UT Mar-Oct, 22 UT
      Nov-Feb); publication latency unverified (EC1-R-4 open).
  f107_81_trailing:
    availability_rule: "previous_day_median_midnight_utc"   # A2: window end day derived from the rule
    release_status_required: "observed"
    window:
      kind: "trailing"                       # never centered (TE §6.2)
      days: 81
      source: "f107_daily_median"            # the D-21 series the producer releases
      recomputation_tolerance: 8.0e-12       # D-47, sfu, absolute
      recomputation_input_bound_sfu: 400     # D-47 applicability condition (not a physical maximum)
    publication_latency_statement: >-
      (as f107_safe; the window's constituents are the same daily medians.)
```

Reader compatibility: `read_availability_lags` accepts the rule/scalar/window shapes above
and ignores the additive keys (`lag_reference_instant`, `selection_rule`,
`recomputation_input_bound_sfu`) until a reviewed reader change consumes them — the
transcription record must add that reader change so the fields are asserted, not merely
carried. Transcription waits on the D-42/D-43/D-46 countersignatures (item 10).

## 10 — Closure table

| Item | Student decision | Implementation | External approval | Evidence / maths |
|---|---|---|---|---|
| P-1 interval semantics | **D-43 adopted** | complete (fields, tests) | **OPEN** — supervisor countersignature (Q-16) | verified on file headers |
| P-2 selection owner | **D-44 adopted** | complete and verified | none required (mechanism); rides D-43 | — |
| P-3 IRI reference | **D-45 selected** | patch prepared, not applied | **OPEN** — TE §18.3 IRI role / Vision §6.11 | semantics resolved from source + data; **UNRESOLVED:** `iricore` pin/install |
| A3 option B | **D-46 adopted** | complete; 0 affected origins | **OPEN** — supervisor countersignature (Q-16/Q-17) | count verified, December unread |
| A4 tolerance | **D-47 adopted** (conditional approval verified) | complete (bound, domain check, test) | none required | derivation supports 8.0e-12 |
| G-3/P-4 scanning | **D-48 adopted** (narrower than prepared) | complete; 0 flagged, 9 inventoried | none required (D-30 precedent) | coverage reported separately |
| P-5 wording | — | complete (dated, history kept) | none | grant verified in the 08-22 record |
| Six-entry config | prepared (§9) | **not applied** | waits on D-42/D-43/D-46 countersignatures | — |
| G-04 | — | — | **OPEN** | requirements not yet satisfied: countersignatures; producer artifacts; transcription |

**Remaining concrete blockers:** (1) supervisor countersignatures of D-42, D-43, D-46
(one act, TE §18.2 Q-16/Q-17); (2) supervisor approval of the IRI role (D-45) before the
P-3 patch and the Vision §6.11 / TE §6.2 wording apply; (3) `iricore` pinned and installed
in the governed environment (TE §8.1) with the index files hashed; (4) producer artifacts
(`gfz_kp_ap_3h_2022_v1`, `gfz_hp60_ap60_1h_2022_v1`, `srmp_f107_observed_daily_2022_v1`)
built with `select_lagged_series` / `daily_medians_from_readings` under the release
machinery — authorised in a later pass, after (1); (5) the six-entry transcription and its
reader change, after (1). Code-summaries of `external-products`, `features-and-splits`,
`governance-guards` are stale under receipts for this pass (gf-3), carried.
