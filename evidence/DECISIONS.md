# Phase 1 Source Decisions — Madrigal MAPGPS Coverage Audit

**Decision date:** 2026-08-13
**Decided by:** Kimia Rezaei (student), Amirkabir University of Technology
**Supervisor status:** unavailable at time of decision; these were taken as sole-signed
student decisions. **Updated 2026-08-15: D-3/D-144 has since been countersigned by the
supervisor** (see the signature table below). Every other item below remains sole-signed
and uncountersigned.
**Governance context:** Project Vision Document v4.2 §6.1A, §6.1B, §6.2, §§1.2, §§1.7
(Recommendation 10); Technical Environment and Research Implementation v3.2 §5.1, §7.0
(stage P1-02), EV-23, D-144, gate G-P1A.

> **Standing of this document.** The governance documents require several of the items
> below to be *"resolved, recorded, and approved"*, with approval understood as student
> **and** supervisor sign-off. D-3/D-144 has now reached that standard. Every other item
> is resolved and recorded but **not** approved in that sense. Each item is written so a
> supervisor can countersign or overturn it individually on return, without
> reconstructing the reasoning.

---

## D-1 — Coordinate-to-cell convention (freeze)

**Decision.** A station maps to the 1°×1° Madrigal bin identified by its lower-left floor
corner: `cell = (floor(lat), floor(lon))`, tested half-open as
`[floor, floor+1)` on both axes.

| Station | Coordinates | Assigned cell |
|---|---|---|
| ARUC | 40.286 N, 44.086 E | 40 / 44 |
| BSHM | 32.778987 N, 35.022987 E | 32 / 35 |
| NICO | 35.140989 N, 33.396450 E | 35 / 33 |

**Rationale.** Madrigal labels each 1°×1° bin with an integer `gdlat`/`glon`, so this rule
resolves to exactly one real grid point per station — a selection, not an interpolation.
Verified against executed 2022 output (2022-11-30: ARUC 208 rows at 40/44, BSHM 269 at
32/35, NICO 227 at 35/33).

**Alternative rejected.** Nearest-bin-centre assignment. It returns the identical cell for
all three stations here, so it offers no practical difference; floor is simpler to state
and to reproduce.

**Known limitation.** Station coordinates are taken from IGS network pages, **not** from
the official IGS site-log PDFs, which rank higher in the §6.2 evidence hierarchy. All
three stations sit well away from cell edges (nearest approach ≈ 0.14°), so a small
coordinate correction would not change any assignment. Site-log validation remains
outstanding.

**Annotation, 2026-09-19 — site-log validation performed; registry transcribed (owner-authorized; original text above preserved).**
On the owner's instruction ("transcribe existing authoritative values … with provenance"), the
three official IGS site logs were retrieved from `https://files.igs.org/pub/station/log/`
(ARUC `aruc00arm_20260317.log` SHA-256 `858aa54b36b43011f48f0329cce7a3f974dfbd5adb752e2fc02d6746a5f5ef25`;
BSHM `bshm00isr_20260422.log` `d0dae80429fac5cc065b6bfdec87d2f948754d3d243b9e8dfb74c1005d37770f`;
NICO `nico00cyp_20251027.log` `2740b73a695c5a4a3faab3a989407893b4786735587c4c41ee036f9c2f3d719a`;
copies in `evidence/station_registry_sources_2026-09-19/`). The "known limitation" above is
closed by this check: the site logs give ARUC 40.285722 N / 44.085583 E, BSHM 32.778986 /
35.022986, NICO 35.140989 / 33.396450 — the approved values above differ by at most 0.0004°
(ARUC, a rounding of the network-page value); every cell assignment is unchanged. The
approved D-1 values are what `configs/data.yaml: stations` now carries (transcribed
2026-09-19); the site-log values are recorded beside them in the per-field provenance,
never averaged. Also transcribed from the same logs: DOMES 12312M002 / 20705M001 /
14302M001, ellipsoidal heights 1222.0 / 225.1 / 190.1 m, and the receiver, antenna and
firmware intervals covering 2022 (no hardware change falls inside 2022 at any station);
sampling interval 30 s from the IGS daily file names `…_01D_30S_MO` (BKG data centre,
2022-001). `igrf_version` is transcribed as **IGRF-13** — the generation compiled into the
pinned `iricore` 1.8.0 IRI-2016 library, the only IGRF consumer in the Phase 1 executable
path (D-49 item 3). **Still absent from every governing record:** the available observable
codes (Vision §6.2; a 2022 RINEX header, Phase 2 material) — `assert_registry_resolved`
keeps refusing on that one field; `load_registry` (the B-01 path) is satisfied.

---

## D-2 — Coverage minimum for G-P1A

**Decision.** Pass requires, per station cell:
- ≥ 95% of calendar days present in each month, and
- 100% of December days present (31/31).

**Rationale.** December is the locked-test month; a hole there invalidates the test
directly. 95% elsewhere tolerates isolated outages without tolerating a systematic gap.

**Disclosure — this threshold was set after partial data was seen.** Five of twelve months
(April, July, October, November, December) had already been audited at 100% day coverage
when this threshold was chosen. It was **not** set blind. It is stated here so a reviewer
can discount it accordingly. The seven remaining months (Jan, Feb, Mar, May, Jun, Aug,
Sep) were unaudited at decision time, and this threshold is fixed before they are run.

---

## D-3 — D-144: Phase 1 source replacement

**Decision.** Adopt MIT Haystack CEDAR Madrigal, instrument 8000 (World-wide GNSS Receiver
Network), kindat 3500 ("TEC binned 1 degree by 1 degree by 5 min") as the Phase 1 VTEC
source, replacing the ICTP prepared-VTEC source rejected at D-143.

**Evidence.** Five audited months, three cells, zero file-level errors:

| Month | Days | ARUC | BSHM | NICO |
|---|---|---|---|---|
| April | 30/30 | ✓ | ✓ | ✓ |
| July | 31/31 | ✓ | ✓ | ✓ |
| October | 31/31 | ✓ | ✓ | ✓ |
| November | 30/30 | ✓ | ✓ | ✓ |
| December | 31/31 | ✓ | ✓ | ✓ |

153/153 station-days. ICTP for comparison (D-143): ARUC 27/365, BSHM 35/365, NICO 0/365
with HTTP 404.

**Excluded products.** kindat 3505 (line-of-sight TEC) is excluded per §6.1A; kindat 3506
is a site list, not data.

**Condition.** This decision is taken on five months of evidence. The full-year audit is in
progress; if any remaining month falls below D-2, this decision is reopened.

---

## D-4 — Parameter set for Phase 1 acquisition

**Decision.** Acquire `ut1_unix, gdlat, glon, tec, dtec, kp, dst, f10.7, ap3`.

**Rationale.** The four geomagnetic/solar drivers reside in the same HDF5 files and cost no
additional request time — retrieval cost is dominated by the server reading the file, which
happens regardless. A TEC forecasting model without geomagnetic drivers is substantially
handicapped, and adding them after the fact would require re-running the entire year.

---

## D-5 — Gap policy

**Decision.** Gaps are stored as explicit NaN. **No interpolation, smoothing, or filling at
acquisition time.** Any imputation is a modelling decision, applied downstream and recorded
separately.

**Rationale.** Interpolating at acquisition destroys the distinction between measured and
invented values permanently, and makes it impossible to report how much of a result rests
on real data. Observed density varies materially by cell — NICO recorded 699 of 744
possible hourly bins in November against ARUC's 738 — and that variation must stay visible.

---

## D-6 — Citation and acknowledgement

**Decision.** Cite the standard MAPGPS reference plus the date range used, together with the
CEDAR Madrigal acknowledgement, rather than per-day permanent experiment citations.

**Rationale.** Standard practice for daily-file products; per-day citation of 365 files adds
no attribution value. Citation strings are collected manually from the Madrigal web
interface — the audit notebook deliberately does not fetch them, because the API surface
varies by Madrigal site version and a wrong or empty citation is worse than an obvious gap.

**Outstanding.** The citation text has not yet been collected.

---

---

## Status update — 2026-08-13 — full-year audit closed

The full calendar-2022 coverage audit completed. All twelve months were run, each in its own
session, each with its own manifest and SHA-256 set; every per-month hash manifest verifies.
Results were merged by `scripts/merge_coverage_year.py` into
`evidence/audit_evidence_2022-FULL/`.

| Station | Days | Coverage | December | Records | Hourly bins |
|---|---|---|---|---|---|
| ARUC | 365/365 | 100.000% | 31/31 | 71905 | 8742 / 8760 (99.8%) |
| BSHM | 365/365 | 100.000% | 31/31 | 94511 | 8749 / 8760 (99.9%) |
| NICO | 365/365 | 100.000% | 31/31 | 56528 | 8447 / 8760 (96.4%) |

Merge totals: 223586 unique rows; 8148 cross-month duplicate rows dropped (consecutive
monthly runs legitimately re-fetch the straddling boundary file); 642 rows dated 2021-12-31
excluded from coverage statistics and retained in the merged raw records. Zero file-level
errors across all twelve runs.

**Effect on D-2.** Every month meets ≥ 95% of days in every cell, and December is 31/31.
The threshold passes in all twelve months with margin.

**Effect on D-3.** The reopening condition — *"if any remaining month falls below D-2, this
decision is reopened"* — is **not triggered**. No month fell short. D-3 stands on full-year
evidence rather than the five months it was originally taken on.

**Carried forward, not a failure.** NICO remains the least dense cell at sub-daily
resolution: 8447 of 8760 hourly bins against ARUC's 8742. D-2 is defined on days, so this
does not affect the verdict. It is a modelling consideration, and D-5 (gaps stored as NaN,
never interpolated) is what keeps it visible.

**Note for reviewers.** ~~The January folder's monthly breakdown shows one day in month 12.
That is 2022-12-31, fetched because its experiment ends on 2023-01-01 and therefore matched
the January filter. It is in-year, correct, and deduplicated during the merge.~~

**SUPERSEDED 2026-08-16 — the struck note above was wrong on both its mechanism and its
verdict. Retained struck rather than deleted, so the correction is auditable.**

The stated mechanism was incomplete and the verdict "correct" was wrong. The actual root
cause is that the acquisition query's experiment-selection predicate tested **month without
year**: `if exp.startmonth not in RUN_MONTHS and exp.endmonth not in RUN_MONTHS: continue`
(`notebooks/madrigal_phase1_coverage_audit.ipynb`, Cell 10). The enclosing whole-year
`getExperiments` window legitimately returns experiments overlapping 2022 at both ends, so a
31-December experiment from **either year** matched. Two symmetric misfilings resulted, and
calling the first "correct" is why the second was never found:

- **`audit_evidence_2022-01/`** received 743 records dated **2022-12-31 — the locked test
  month** — matching on `endmonth == 1`;
- **`audit_evidence_2022-12/`** received 642 records dated **2021-12-31**, matching on
  `startmonth == 12`. This counterpart was previously unrecorded anywhere in this file.

**The figure the struck note defended has since been corrected to zero.** The January
folder's `december_days_present` was 1 and `december_coverage_pct` 3.226; both are now 0
after regeneration on 2026-08-16, and its `unique_days` is 31 rather than 32. December's
statistics were unchanged by its own correction, because the merge script's calendar-year
guard had already excluded the 2021 rows from every aggregate.

Full record, including the fix, the owning test, the locked-month custody classification and
what remains open: `evidence/CORRECTION_2026-08-16_acquisition_window.md`. Locked-month
access log: `evidence/experiment_registry.md`. Pre-correction artifacts are preserved under
`superseded_2026-08-16/` in both folders.

Raised by the TEC governance board (findings IMPL-01, IMPL-02, DATA-01, DATA-02, ML-07,
TEC-09, VAL-01); the defect was missed by this stage's own evidence pass and by all three of
its support reviews.

---

## D-7 — Modelling resolution: hourly, not 5-minute

**Decision date:** 2026-08-13. **Decided by:** Kimia Rezaei, sole-signed.

**Decision.** The model is built on an **hourly** grid. The native 5-minute Madrigal binning
is aggregated to hourly before modelling.

**Evidence.** Measured over the merged calendar-2022 records, against 105120 possible
5-minute slots per cell (365 × 288):

| Station | 5-min slots present | Hourly bins present | Longest gap |
|---|---|---|---|
| ARUC | 71905 (68.4%) | 8742 / 8760 (99.8%) | 1.7 h |
| BSHM | 94511 (89.9%) | 8749 / 8760 (99.9%) | 2.5 h |
| NICO | 56528 (53.8%) | 8447 / 8760 (96.4%) | 2.6 h |

**Rationale.** Day-level coverage is 100% in every cell (D-2, discharged), but that measure
conceals sub-daily sparsity: NICO is missing nearly half its 5-minute slots. Training on the
native grid would require imputing ~46% of the weakest station, and a model whose worst cell
is half-imputed cannot be defended. At hourly resolution the same data is 96.4–99.9%
complete. Gap structure supports this: no outage anywhere in the year exceeds 2.6 hours and
there is no multi-day hole, so hourly aggregation bridges real gaps rather than papering
over a systemic outage.

**Consequence.** Any scientific question requiring 5-minute resolution is out of reach for
NICO on this dataset and must not be claimed.

**Interaction with D-5.** Unchanged. Gaps remaining after hourly aggregation stay NaN and
are never interpolated at acquisition time.

---

## D-8 — Claim scope

**Decision date:** 2026-08-13. **Decided by:** Kimia Rezaei, sole-signed.

**Decision.** Claims are strictly limited to: **hourly VTEC forecasting at the three frozen
cells (ARUC 40/44, BSHM 32/35, NICO 35/33) for calendar year 2022, tested on December 2022.**
No claim of generalisation beyond these cells, this year, or this test month.

**Rationale — the limits this scope acknowledges.**

- **Single year.** 2022 only; no interannual variation. 2022 falls on the rising phase of
  solar cycle 25, so the model is fitted to one solar regime.
- **Test month n = 1.** One December, one storm climatology. A strong December 2022 result
  is a result about December 2022, not about Decembers generally.
- **Correlated folds.** F1–F4 all sit inside the same year and therefore share a solar
  trend; they are less independent than the fold count implies.
- **Spatially clustered cells.** All three lie within 32–40 °N, 33–44 °E. No spatial
  generalisation claim is available.

**Rationale — why the scope is nonetheless sound.** Within these bounds the data is complete
(365/365 days, all cells, zero file-level errors) and the evidence chain is verified end to
end. A narrow claim fully supported by the data is worth more than a broad one that is not.

**Identified path to a stronger result, not taken.** Adding calendar years 2021 and 2023
through the identical pipeline (~17 h each; change `AUDIT_YEAR` and re-run) would supply
interannual variation, three test Decembers, and folds not sharing a trend. This is recorded
as the highest-value future extension. Adding further stations would broaden geography while
leaving every claim resting on a single year, and is therefore lower value.

---

## D-9 — Acquisition route: promote audited rows, drivers from canonical sources

**Decision date:** 2026-08-13. **Decided by:** Kimia Rezaei, sole-signed.

**Decision.** Option B. The VTEC data acquired for Phase 1 is the audited calendar-2022
record set already on disk (`evidence/audit_evidence_2022-FULL/`), **promoted from audit
evidence to acquisition input**. The four D-4 driver parameters (Kp, Dst, F10.7, ap3) are
obtained from their canonical sources — GFZ Potsdam for Kp/ap, NOAA/OMNI for Dst and F10.7 —
rather than by re-fetching them from Madrigal.

**Rationale.** The audited rows are the same measurements a fresh acquisition run would
return: `ut1_unix, gdlat, glon, tec, dtec` at 5-minute resolution, 365/365 days, all three
cells, 223586 unique rows, verified against twelve independent per-month SHA-256 manifests.
Re-downloading identical values for ~17 h buys provenance tidiness, not data — and the
existing per-month hash chain is arguably stronger evidence than a single fresh run, because
it was verified twelve times independently. Madrigal itself imports Kp/ap from GFZ and
Dst/F10.7 from NOAA, so the canonical sources are upstream of Madrigal's own copies, not a
substitute for them.

**Option rejected.** Option A — re-run the full year with all nine parameters in one pass
(~17 h). Rejected on cost-for-value. It remains available if a reviewer requires every byte
of the dataset to trace to a single acquisition run with a single manifest.

**Explicit acknowledgement — this crosses a governance line.** The audit notebook states in
its own header that running it does **not** constitute Phase 1 acquisition. This decision
deliberately promotes its output to acquisition input. That promotion is the substance of
this decision and must not be presented as though the data were acquired by a separate
acquisition run. Any write-up must state that Phase 1 VTEC data originated in the
target-independent coverage audit and was promoted after D-144.

**Consequences to carry into implementation.**
- The dataset draws on **two sources**, not one. Provenance, licensing and citation must
  cover both Madrigal (D-6) and the GFZ/NOAA index sources.
- Driver series are time-indexed only — one value per epoch, identical across all three
  cells. Joining them must not imply per-cell measurement.
- Kp is 3-hourly and F10.7 daily; both are coarser than the hourly modelling grid (D-7).
  The forward-fill or step-interpolation rule for each must be stated before use, and
  recorded as a decision.
- D-5 is unchanged and applies to the joined product: gaps stay NaN.

**Not executed.** No acquisition has been performed under this decision. It records the
chosen route only.

---

## D-10 — Correction and addendum to D-9: driver sources, alignment, and leakage control

**Decision date:** 2026-08-13. **Decided by:** Kimia Rezaei, sole-signed.
**Status:** supersedes the driver-source clause of D-9. D-9 otherwise stands unchanged.

### D-10.1 Driver sources (corrects D-9)

D-9 named "GFZ Potsdam for Kp/ap, NOAA/OMNI for Dst and F10.7". That clause was
under-specified and is corrected as follows.

| Driver | Source | Correction made |
|---|---|---|
| Kp, ap3 | GFZ Potsdam | unchanged — GFZ originates these indices |
| Dst (hourly) | **Kyoto WDC** (World Data Center for Geomagnetism, Kyoto) | was "NOAA/OMNI" |
| F10.7 | **Canada's Solar Radio Monitoring Program — OBSERVED flux, NOT 1-AU-adjusted** | was unqualified "F10.7" |

**Rationale.** OMNI redistributes Kyoto's Dst rather than originating it; citing OMNI would
credit a mirror instead of the producer. "F10.7" unqualified is ambiguous between the
observed flux (as measured at Earth) and the flux scaled to 1 AU — the two differ by up to
several percent seasonally, and silently mixing them corrupts any solar-activity signal the
model learns. The observed series is specified. This is consistent with the Madrigal
parameter dictionary, which labels its own field *"F10.7 solar flux observed (Ottawa)"*.

**To verify before use, not assumed here.** Kyoto Dst is published in real-time,
provisional, and final grades, and the grade available for calendar 2022 must be checked and
recorded rather than presumed final. Mixing grades within one series is not acceptable.

### D-10.2 Alignment onto the hourly grid (extends D-5 and D-7)

- **Kp and ap3** are 3-hourly. Each value is repeated **only within its own defined 3-hour
  interval**. It is never spread beyond that interval.
- **Dst** is hourly and is aligned to **its own hourly averaging interval**, not shifted to a
  neighbouring hour for convenience.
- **F10.7 observed** is treated as a **daily** value.
- **No interpolation of any driver.** This restates D-5 for the driver series specifically:
  gaps stay NaN; no linear fill, no smoothing, no carry-forward beyond a value's own defined
  interval.

### D-10.3 Forecast-leakage control (new requirement, precedes modelling)

Before any modelling, each predictor is assigned an **availability timestamp** — the instant
its value could actually have been known — and every predictor is lagged accordingly. Rules:

- Use only **completed** Kp and ap3 intervals available at the forecast origin. A 3-hour
  interval that has not closed by the origin is not available.
- Use only **completed** Dst hourly intervals available at the forecast origin.
- For F10.7, use the **previous day's** observed value by default. A same-day value may be
  used only where documented release timing demonstrably supports it, and that documentation
  must be recorded with the decision.

**Rationale.** Without this, a model trained on 2022 can consume index values published after
the forecast origin and score well by reading the future. That failure is invisible in
validation metrics and fatal on discovery. Conservative lagging costs a little skill and
buys a defensible result.

**Consequence.** Availability timestamps are part of the dataset contract, not a modelling
convenience — they are defined and recorded before the model is built, not fitted afterwards.

---

## Status of items NOT decided here

- **Site-log validation** of the three station coordinate sets (D-1 limitation above).
- ~~**Full-year coverage audit** — 7 of 12 months outstanding.~~ **Closed 2026-08-13** —
  all 12 months audited at 100% day coverage. See status update above.
- **Citation text** — not yet collected (D-6).
- ~~**Acquisition route** — OPEN.~~ **Closed 2026-08-13 — Option B selected, see D-9.**
  Route decided; **not executed**. Nothing has been acquired.
- ~~**Driver resampling rule** — undecided.~~ **Closed 2026-08-13 — see D-10.2.**
- **Kyoto Dst data grade for 2022** — real-time / provisional / final not yet checked
  (D-10.1). Must be verified and recorded before the drivers are used.
- **F10.7 release timing** — the previous-day default (D-10.3) stands unless documented
  release timing is obtained and recorded.
- **Phase 1 acquisition itself** — not started, and out of scope for the audit notebook.
  Acquisition is a separate implementation against the now-frozen target definition.
- **Model build** — not started. D-7 and D-8 fix its resolution and claim scope; no code
  exists.

## D-11 — Walking-skeleton fixture window

**Decision date:** 2026-08-16. **Decided by:** Kimia Rezaei, sole-signed.
**Authority:** Q-31 (fixture station, dates, acceptance tolerances) is assigned to the
Student in `Technical_Environment_and_Research_Implementation` §18.2. This decision is
student-owned and needs no supervisor countersignature.

**Decision.**

- **Fixture month:** November 2022.
- **Fixture window:** 2022-11-01 through 2022-11-07 inclusive (seven days).
- **Stations:** all three governed cells — ARUC 40/44, BSHM 32/35, NICO 35/33.
- **Seasonal character:** late autumn, pre-solstice.
- **Geomagnetic character:** disturbed, on provisional Dst.

**Rationale.** November is the closest eligible late-year month to the locked test month,
and 2022-11-01..07 is deliberately stress-bearing rather than quiet: it is November's most
disturbed seven-day window, carrying the month's minimum provisional Dst of -92 nT and
three of the year's storm days (3, 7, 8 November, minimum hourly Dst <= -50 nT). A fixture
that exercises a disturbed interval tests the pipeline where it is most likely to break.

**Eligibility basis.** April, July and December 2022 were excluded before selection.
April and July have no `raw_isprint_cache/` retrieval evidence; December is the locked
test month. The remaining nine months were characterised on provisional Kyoto Dst.

**Measured VTEC completeness in the selected window** (from
`evidence/audit_evidence_2022-11/madrigal_coverage_raw_records.csv`):

| Cell | Days present | Hourly bins | Records |
|---|---|---|---|
| ARUC 40/44 | 7/7 | 163/168 (97.02%) | 1195 |
| BSHM 32/35 | 7/7 | 168/168 (100.00%) | 1810 |
| NICO 35/33 | 7/7 | 155/168 (92.26%) | 964 |

ARUC is short exactly one bin on five of the seven days (3-7 November), a uniformity that
suggests a systematic single-bin gap rather than random loss and should be explained
before the manifest is frozen. NICO's weakest day is 2022-11-04 at 20/24 bins.

**Status of these figures.** No fixture completeness threshold exists to test them
against. `Technical Environment` §15.2 requires the fixture manifest to record row-count
ranges and support/missingness limits, and §15.1 states that exact counts, tolerances and
runtimes are "measured from the fixtures and frozen; they are not invented here". The
numbers above are therefore the measured baseline to be frozen into
`tests/fixtures/<fixture_id>/fixture_manifest.yaml`, not a bar that was cleared. Day
presence (7/7 in every cell) satisfies D-2's >= 95%-of-calendar-days rule applied by
analogy; D-2 itself governs monthly G-P1A coverage, not fixture windows.

**Mandatory limitation — must accompany any use of this fixture.** This window does not
reproduce December's winter-solstice regime or its activity distribution and must not be
treated as representative of the locked month. December 2022 is solstitial; November is
pre-solstice late autumn, and no eligible month is solstitial. Diurnal VTEC amplitude and
the day/night ratio differ materially between the two regimes at all three cells, so
row-count ranges, support and missingness limits, and floating-point tolerances derived
from this fixture are not transferable to December. December also carries the year's
highest weak-disturbance count (15 of 31 days at minimum hourly Dst <= -30 nT) against
November's 10 of 30. 2022 is the rising phase of solar cycle 25, so months are not
interchangeable across the year.

**Dst restriction.** Every Dst value informing this decision is **provisional grade**,
read from `evidence/audit_ec1_2026-08-15/kyoto_dst/dst_provisional_2022MM.html`.
Provisional values may characterise fixture selection only. They must not become
modelling inputs, frozen tolerances, or G-05 regime counts. D-10.1's single-grade rule
applies, and its open item — the Kyoto Dst release grade for calendar 2022 — remains
unchecked. Definitive-grade verification is required before any Dst value is used beyond
this selection.

**Storm-day definition used.** A storm day is a calendar day whose minimum hourly
provisional Dst reaches or falls below the stated threshold, attributed to the day of the
minimum. Both -50 nT (moderate) and -30 nT (weak) were reported; no project-level storm
definition exists, and this one is adopted for characterisation only.

**Not decided here.** The seven-day plumbing fixture's station is not fixed by this entry
(TC-03f permits a single station); the one-month all-station scientific fixture window is
not fixed by this entry. Both remain open under Q-31.

### D-11 clarification — scope of the `Stations:` line (2026-08-22)

**Approved 2026-08-22 by the project owner** under the recorded student/supervisor
authority equivalence, on governance finding `REM-03` (`GOV-2026-08-22-REM-01` Rec 3,
option C). Q-31 assigns fixture station, dates and tolerances to the Student, so this
clarification is student-owned and needs no separate countersignature.

**This clarification resolves a tension inside D-11's own text. It is not a statement
that the entry was already unambiguous.** D-11 contains two statements about stations:

- under **Decision**, "**Stations:** all three governed cells — ARUC 40/44, BSHM 32/35,
  NICO 35/33";
- under **Not decided here**, "the seven-day plumbing fixture's **station is not fixed by
  this entry** (TC-03f permits a single station)".

Read together with the surrounding text, the `Stations:` line describes **the scope over
which the seven-day window was evaluated and frozen** — the same three cells the
"Measured VTEC completeness in the selected window" table reports, which is the evidence
the window's eligibility rests on. It does **not** set the plumbing fixture's execution
scope, which the "Not decided here" paragraph expressly leaves open. Where the two are in
tension the more specific statement governs, and "Not decided here" is the sentence that
speaks about the plumbing fixture.

**What is therefore settled and what is not:**

| Dimension | Status |
|---|---|
| Fixture **window** — 2022-11-01…07, November 2022 | **Frozen by D-11.** Unchanged by this clarification |
| Three-cell completeness figures | **Eligibility evidence** for that window. Unchanged, and not a claim about execution scope |
| Plumbing fixture **station count** | **One**, per `Technical Environment` §15.1 ("One station") and TC-03f. This clarification retains §15.1's execution scope rather than displacing it |
| Plumbing fixture **station identity** | **OPEN.** Not selected, not frozen. Reserved to the project owner under Q-31 |

**No authority document is amended by this clarification** — §15.1's "One station" stands
as written, and no window, measured figure, tolerance or scientific value changes.
**BLK-02 remains open** until the single station is explicitly selected and approved and
the manifest evidence exists. D-11's standing pre-freeze obligation is unaffected: ARUC's
one-bin shortfall on five of seven days must be explained before the manifest is frozen,
and that obligation applies to any option in which ARUC is the selected station.

---

## D-12 — Vision §6.1B numerical coverage minimum (freeze)

**Decision.** G-P1A acceptance requires, per station cell, per month:

- at least **90% usable hourly coverage** (distinct in-month station-hours present, straddle days excluded), **and**
- D-2's day rule: ≥95% of calendar days present per month, 100% of December days (31/31).

Both conditions must pass. Neither substitutes for the other.

**Rationale.** The figure is not new. Vision §6.12 already states "At least 90% usable
hourly coverage per station" — as an *aspiration* with a supervisor-exception path. This
decision promotes it to a hard gate and closes that exception path at G-P1A, so the
project is held to a number its own approved Vision already names. No external threshold
was invented: a literature survey on 2026-08-21 found no published TEC-completeness
acceptance threshold to cite, and storm-sample sizes in the field span 11 to 170 events
with no stated minimum anywhere.

**Why both limbs.** D-7 records that the day measure conceals sub-daily sparsity — NICO
holds 53.8% of its native 5-minute slots against 96.4% of its hourly bins — so a day-only
rule can pass a month that is materially thin at the modelling cadence. The hourly gate
closes that; the day rule still catches whole-day outages.

**Measured position at freeze time** (in-month distinct station-hours, straddle days
excluded, computed 2026-08-21 from the acquired evidence):

| Month | ARUC | BSHM | NICO |
|---|---|---|---|
| 2022-01 | 99.9% | 100.0% | 98.9% |
| 2022-02 | 100.0% | 100.0% | 98.5% |
| 2022-03 | 99.5% | 99.9% | 97.8% |
| 2022-05 | 99.6% | 100.0% | 97.6% |
| 2022-06 | 99.9% | 99.3% | 94.0% |
| 2022-08 | 100.0% | 99.9% | 95.0% |
| 2022-09 | 100.0% | 99.9% | 93.2% |
| 2022-10 | 99.9% | 99.9% | 95.3% |
| 2022-11 | 99.2% | 100.0% | 94.2% |

Every station-month clears 90%. 2022-04 and 2022-07 have no `raw_isprint_cache/`.
December was deliberately **not** read for this table — see the limitation below.

**Alternatives rejected.** (a) **95% hourly**: fails NICO in September (93.2%), November
(94.2%) and June (94.0%), discarding data already held — including the month D-11's
plumbing fixture lives in. (b) **Per-station two-tier** (95% ARUC/BSHM, 90% NICO): more
precise but reads as fitting the criterion to the data, for no measured gain.
(c) **Leaving §6.1B unfrozen on D-2 alone**: leaves a `TBD` inside the G-05/G-09 set, so
§18.3's zero-TBD preflight cannot go green.

**Limitation.** December 2022's own hourly coverage is not stated here. Producing it would
have added a third — and unlogged — December read on top of the two already recorded, which
`GOV-2026-08-20-RA-01` finding `VAL-2` is open against. The required pre-G-05 December
coverage audit produces that figure, performance-blind, with an access-log row written
**before** the read.

**Approved** 2026-08-21 by the project owner under the recorded student/supervisor
authority equivalence. Change record: `governance/CHANGE_RECORD_2026-08-21_freezes.md`.
Fixed before any model performance was viewed — no model, prediction or metric exists.

---

## D-13 — H4 / SRQ-5 demotion threshold (freeze)

**Decision.** H4 ("forecast-safe space-weather features improve disturbed-condition
performance more than quiet-condition performance") and secondary research question 5
remain **confirmatory** only if December 2022 contains **at least three independent storm
events**. With fewer, both are predeclared **validation-fold-only** and reported as such,
and the demotion is recorded **before** the G-05 freeze.

Definitions are Vision §9.3's, unchanged: a storm event is a contiguous interval of
\(Kp\ge5\); two events are independent if separated by at least 24 hours of \(Kp<4\);
the reporting window for each event is −12 h to +24 h.

**Rationale.** Vision §5.2 conditioned the demotion on "the supervisor-approved minimum"
disturbed-hour count, and no such value existed. Rather than invent one, this decision
reuses the threshold Vision §9.3 **already** freezes for the general storm-performance
claim. Three consequences, all wanted: no new number enters the freeze set; nothing new
has to be defended at examination; and H4's fate and the storm-claim rule turn on one
measured quantity instead of two thresholds that could disagree.

**Alternatives rejected.** A 72-hour disturbed floor (~10% of December) and a 48-hour
floor (~6.5%) were both considered and rejected: each requires defending an unsourced
figure, and the 2026-08-21 literature survey found no basis for either. A two-part floor
(≥48 disturbed hours **and** ≥1 storm event) covers one extra failure shape but was
rejected on the same ground for its hour limb.

**Source of the count.** GFZ Kp/ap3 and Hp60/ap60 at a single recorded release grade.
**D-11 bars provisional Dst from becoming a G-05 regime count**, so the December material
in `.dst_summary.json` must not supply this figure. For the record, and as orientation
only, that material is provisional *Dst*, not Kp: December 2022 shows a minimum of −68 nT
(27 Dec), two days at or below −50 nT (7 and 27 Dec) and fifteen at or below −30 nT, and
NOAA SWPC separately recorded a G1 storm on 29–30 December 2022. None of that is a
Kp ≥ 5 event count, and none of it may be used as one.

**Approved** 2026-08-21 by the project owner under the recorded authority equivalence.
Change record: `governance/CHANGE_RECORD_2026-08-21_freezes.md`.

---

## D-14 — One-month all-station scientific fixture window (freeze, Q-31)

**Decision.** The one-month all-station scientific walking-skeleton fixture is
**March 2022, 2022-03-01 to 2022-03-31 inclusive, all three cells** (ARUC 40/44,
BSHM 32/35, NICO 35/33).

**Rationale.** Two criteria decided it. **Regime separation:** D-11's frozen seven-day
plumbing window is 2022-11-01 to 2022-11-07, so placing the scientific fixture in a
different season means the two fixtures probe different diurnal and seasonal structure,
which is what a scientific fixture is for. March is an equinox month; November is late
autumn. **Measured coverage:** March is the best-covered eligible month outside January
and February — ARUC 99.5%, BSHM 99.9%, NICO 97.8% in-month hourly — with a 32-day run
staged and `raw_isprint_cache/` present. Provisional Dst shows real activity (minimum
−85 nT, four days at or below −50 nT), so the disturbed code path is exercised rather
than idle.

**Alternatives rejected.**

- **2022-11**, the plumbing month: convenient and closest to December's regime, but it
  concentrates all fixture evidence in one month, so a November-specific processing quirk
  would be invisible to both fixtures — the weakness D-11's own limitation already warns
  about. NICO 94.2%, the second-thinnest eligible month.
- **2022-01**, best coverage (NICO 98.9%) and the closest seasonal analogue to December:
  rejected because `audit_evidence_2022-01/` is the folder carrying the year-blind
  predicate's custody irregularity — 743 December-2022 records, the copy still present
  under `superseded_2026-08-16/` — and `GOV-2026-08-20-RA-01` findings `VAL-1` and
  `VAL-3` are open against exactly those bytes. Siting the scientific fixture there
  trades a statistical nicety for an audit problem.
- **2022-10**: a middle path, but its regime is close enough to November that the
  separation gain is modest, and NICO is 1.5 points thinner than March.

**Mandatory limitation.** March 2022 is an equinox month and does not reproduce
December's winter-solstice regime or its activity distribution. It is **not**
representative of the locked test month, and no fixture result may be read as evidence
about December behaviour.

**Measured, not invented.** Per TE §15.1 and §15.2 the fixture's exact counts, tolerances,
row-count ranges, support and missingness limits, timestamp tolerances, required outputs
and expected CPU runtime range are **measured from the fixture run and frozen into**
`tests/fixtures/scientific_1month/fixture_manifest.yaml`. The coverage figures above are
selection evidence only.

**Ownership.** Q-31 assigns fixture station, dates and acceptance tolerances to the
Student, so no countersignature is required; recorded here under the same authority
equivalence for consistency with D-12 and D-13.

**Approved** 2026-08-21. Change record: `governance/CHANGE_RECORD_2026-08-21_freezes.md`.

---

## D-15 — Locked-month custody relocation (freeze)

**Decision.** Every artifact containing December 2022 target values is relocated under the
restricted custody root `evidence/locked_test_restricted/`, effective **2026-08-21**.

| Old path | New path | Files |
|---|---|---|
| `evidence/audit_evidence_2022-12/` | `evidence/locked_test_restricted/audit_evidence_2022-12/` | 10 (incl. its own `superseded_2026-08-16/`) |
| `evidence/audit_evidence_2022-FULL/` | `evidence/locked_test_restricted/audit_evidence_2022-FULL/` | 6 |
| `evidence/audit_evidence_2022-01/superseded_2026-08-16/` | `evidence/locked_test_restricted/superseded_2026-08-16_from_2022-01/` | 5 |

Twenty-one files moved with `git mv`, so rename history is preserved. **All 21 verified
byte-identical after the move** against a pre-move SHA-256 inventory: 21 identical, 0
changed, 0 missing, and no old path left behind. No file was deleted and no existing file
was overwritten — the three target paths were confirmed absent before the move.

**Custody rationale.** Technical Environment §12 states two obligations in one sentence:
locked-test artifacts *"use restricted paths until G-05 is complete"* **and** must carry
`locked_test_accessed = true` in the registry. Only the registry half had been
decomposed into a requirement. Before this relocation, December 2022 `tec`/`dtec` values
were readable from four unrestricted locations totalling roughly 58 MB — 21,258 December
rows each in `audit_evidence_2022-12/`, `audit_evidence_2022-FULL/` and
`audit_evidence_2022-12/superseded_2026-08-16/`, plus 743 in
`audit_evidence_2022-01/superseded_2026-08-16/` — while the restricted path held a single
isprint extract. Origin: `GOV-2026-08-20-RA-01` finding `VAL-1`, a Validation Auditor
veto.

**What the restricted path is, stated accurately.** A **governance boundary, not an access
control.** The directory carries no special filesystem permission, no encryption and no
ACL in this repository: any process that can read `evidence/` can read
`evidence/locked_test_restricted/`. What it provides is (a) one declared location, so an
unintended December read is a detectable path violation rather than an untraceable one,
(b) a machine-checkable invariant — `tests/test_acquisition_window.py::test_locked_month_values_exist_only_under_the_restricted_path`
— and (c) an unambiguous trigger for the Vision §8.3 access-log obligation. It must never
be described as preventing access, and this decision does not claim that it does.

**Affected manifests.** None required editing. Every `sha256_manifest.json` addresses its
artifacts by bare filename, relative to its own directory, so all fifteen manifests
continue to verify after the move: **60 of 60 declared artifacts verified**, 0 failed.
`audit_evidence_2022-FULL/request_manifest.json` names its twelve `source_runs` by
directory name (`audit_evidence_2022-01` … `-12`) rather than by path, so those
references remain correct; the root each name now resolves under is recorded in this
decision rather than by rewriting the manifest, which would have altered a hashed
provenance record.

**Access-log implications.** Access-log row **6** was written **before** the move, as
FR-P1-02-3 now requires — the first December access in this project logged in advance.
Row **5** was added at the same time and is marked **retrospective**: it records the
2026-08-21 governance review's December row counts, which were themselves an unlogged
December access. Rows 3 and 4 remain retrospective for the 2026-08-13 merge and the
2026-08-16 correction. Six rows total; three retrospective, one logged in advance, two
original.

**Relationship to D-9.** D-9 promotes `audit_evidence_2022-FULL/` as the Phase 1
acquisition input. That promotion is unchanged in substance — the artifact is the same
bytes at a new path — but two consequences are recorded rather than left implicit:

1. **Reading the D-9 input is now a logged December access.** FULL contains 21,258
   December rows, so any consumer that opens it must write an access-log row first. This
   is a real constraint on downstream work and is the intended effect of the custody
   rule, not a side effect of the move.
2. **FULL's provenance remains unresolved, independently of this move.** Its
   `PROVENANCE_NOTICE.md` records that it must be re-merged from the corrected months or
   have its provenance explicitly re-pointed, and its `merged_at_utc` of
   `2026-08-13T06:27:03` predates the 2026-08-16 regeneration of the January and December
   folders. D-15 does not cure that, and FULL must not be relied on at a freeze gate while
   the notice stands.

`scripts/merge_coverage_year.py` now resolves month folders under **both** roots and
writes its output inside the restricted root, and refuses to run if a month resolves in
both roots rather than guessing which copy is authoritative.

**Approved** 2026-08-21 by the project owner under the recorded student/supervisor
authority equivalence. No supervisor signature artifact exists and none is claimed.

---

## D-16 — Phase 1 hourly aggregation statistic (freeze)

**Decision.** The Phase 1 hourly target aggregation statistic is the **median** of the
valid provider VTEC samples falling inside the UTC hour \([h, h+1)\) for the station's
frozen grid cell.

**Zenith-weighted aggregation is a separately declared sensitivity analysis only.** It may
be run only if (a) the data required to weight by zenith angle genuinely exists for the
Phase 1 product, and (b) it is formally authorised as a named, registered run **before**
training. Neither condition is met today: see the availability finding below.

**No automatic substitution.** Where satellite-level or zenith-angle information is
unavailable, **nothing is substituted for it** — not a proxy, not a default weight, not an
assumed elevation. The affected quantity is reported as unavailable and the dependent
analysis is not run.

**Rationale.** Vision §6.6 marked *"the exact cell-selection and hourly statistic"* as
`TBD — supervisor freeze gate`, and TE §18.2 lists the aggregation statistic as a
Student + Supervisor forbidden choice. Median is not a new preference: TE §6.1 already
defines `vtec_tecu` as a **median**, and Vision §6.6 makes median the default with
zenith-weighted a declared sensitivity requiring approval before training. This decision
records that default as frozen rather than leaving an implementer to infer it, and
supersedes the earlier requirement text that described the aggregation as already frozen
when no decision had frozen it (`GOV-2026-08-20-RA-01` findings `DATA-05` and
`TEC-04`).

**Availability finding, measured 2026-08-21.** The Phase 1 product cannot support
zenith weighting as things stand. `request_manifest.json` records
`parameters_requested = ["ut1_unix", "gdlat", "glon", "tec", "dtec"]` for every month, and
the retrieved isprint extracts carry exactly those five columns. There is no elevation, no
zenith angle, no satellite identifier and no per-IPP record in the Phase 1 data — so a
zenith-weighted aggregate is not computable from it, and could only become available
through a separately governed re-acquisition or in Phase 2. The sensitivity is therefore
declared and **deferred**, not silently dropped.

**Consequence for TE §6.1's definition.** TE §6.1 defines `vtec_tecu` as the median of
valid VTEC *"at observed IPPs"*. On the Phase 1 gridded product there are no IPPs: the
median is taken over the provider's binned cell samples within the hour. The statistic is
the same; the population differs, and that difference is part of the target-domain shift
already recorded under `target_definition_id`. See § Known defects in
`requirements.md` and D-17.

**Approved** 2026-08-21 by the project owner under the recorded authority equivalence.

---

## D-17 — Phase 1 target-row contract (freeze)

**Decision.** The Phase 1 hourly target row carries exactly the fields below. The contract
is defined from the **product that actually exists**, audited 2026-08-21, and no field is
invented.

**What the Phase 1 product genuinely provides.** `instrument_code 8000`,
`kindat_code 3500` (Madrigal MAPGPS `gps` binned VTEC), with
`parameters_requested = ["ut1_unix", "gdlat", "glon", "tec", "dtec"]` — five columns,
confirmed identical across all twelve monthly request manifests and matching the retrieved
isprint extracts. Native cadence inside a cell is 5-minutely, so an hour holds **at most
12** samples per cell; measured range on a sampled day was 2 to 12. `dtec`, the provider's
reported uncertainty, is populated on every record sampled.

**Phase 1 target row.**

| Field | Source | Status |
|---|---|---|
| `interval_start_utc` | derived from `ut1_unix`, hour start \([h,h+1)\) | available |
| `station_id` | location key assigned by D-1's cell rule | available |
| `cell_gdlat`, `cell_glon` | provider `gdlat`, `glon` (integer 1°×1° bin labels) | available |
| `cell_lat_bounds`, `cell_lon_bounds` | D-1: half-open \([floor, floor+1)\) on both axes | available |
| `vtec_tecu` | **median** of in-hour cell samples (D-16) | available |
| `valid_observation_count` | count of provider samples contributing to the hour | **derivable** |
| `within_hour_spread_tecu` | spread of those samples; statistic `TBD — freeze gate` | **derivable**, threshold open |
| `largest_internal_gap_s` | largest gap between contributing samples | **derivable** |
| `provider_dtec_summary` | summary of provider-reported `dtec` over contributing samples; statistic `TBD — freeze gate` | **available** (genuine provider uncertainty) |
| `aggregation_config_id` | frozen hourly-target configuration snapshot | available |
| `target_valid` | boolean; invalid primary targets are **never** imputed | available |
| `phase_id`, `source_id`, `target_definition_id` | stamped per TE §13 | available |

Release-level companions (`dataset_version`, `source_manifest_id`, `processor_config_id`,
`target_qc_version`) are unchanged and do not replace row-level fields.

**Explicitly NOT in the Phase 1 row, and not substituted.** `valid_satellite_count`;
any per-satellite or per-IPP quantity; zenith angle or zenith weight; elevation; DCB;
STEC; mapping function output; arc or cycle-slip statistics. None is derivable from a
five-column gridded product, and TE §7.0 requires `test_phase_boundary.py` to **fail** if
Phase 1 produces a satellite field. These remain Phase 2 quantities unless a separately
recorded governance decision moves the boundary.

`processor_qc_flags`: TE §6.1's codebook lists package, DCB, arc, elevation, slip,
mapping and aggregation flags. Only **aggregation** flags are meaningful in Phase 1; the
others are Phase 2 and are recorded as not-applicable rather than emitted empty.

**Freeze-gate items, named as holes rather than defaulted.**

1. `within_hour_spread_tecu` — statistic and threshold, `TBD — freeze gate` (TE §6.1
   requires it to be *reported, not merely stored*).
2. `largest_internal_gap_s` maximum — TE §6.1's provisional 1200 s is plausible against a
   5-minute cadence but is not frozen.
3. `provider_dtec_summary` — statistic and any acceptance threshold.
4. `valid_observation_count` minimum — **and TE §6.1's provisional value of 20 is
   unsatisfiable on this product.** An hour holds at most 12 native samples per cell, so a
   minimum of 20 valid observations per hour would reject **every** row. The provisional
   figure was written for the Phase 2 IPP population, where dozens of observations per hour
   are normal. A Phase 1 minimum must be set on the 0–12 scale and is left as an explicit
   freeze-gate hole; no default is assigned here.
5. `valid_satellite_count` minimum — **not applicable in Phase 1** rather than open. The
   quantity does not exist on this product; TE §6.1's provisional 4 applies to Phase 2.

**Observation-quality strata** are aligned to what the product contains: bins over
`valid_observation_count`, `within_hour_spread_tecu` and `provider_dtec_summary`. No
stratum is defined on satellite count, elevation or zenith angle.

**Related, and recorded rather than smoothed over.** D-4 decided to acquire
`ut1_unix, gdlat, glon, tec, dtec, kp, dst, f10.7, ap3`. The executed requests took the
first **five** only: no `kp`, `dst`, `f10.7` or `ap3` column is present in any retrieved
extract or derived artifact. D-4's stated rationale — that the four drivers were free to
retrieve alongside the target — was therefore never realised, and the drivers must come
from their governed external sources per D-10.1 (GFZ, Kyoto WDC, Canadian Solar Radio
Monitoring Program). One favourable side effect: no driver column of unrecorded release
grade sits inside the Phase 1 target files, which was the concrete risk
`GOV-2026-08-20-RA-01` finding `ML-01` raised against D-4.

**Approved** 2026-08-21 by the project owner under the recorded authority equivalence.
The unresolved Vision/TE schema conflict this contract sits inside is recorded, still
open, at § Known defects row 10 of `requirements.md`; D-17 defines what Phase 1 will
build **without** adopting a reading of that conflict, by enumerating only fields whose
availability was measured.

---

## D-18 — Merged-year re-merge and merge determinism (freeze)

**Decision.** `evidence/locked_test_restricted/audit_evidence_2022-FULL/` is **regenerated**
from the corrected per-month folders, discharging the re-merge obligation its
`PROVENANCE_NOTICE.md` carried. The prior artifact is preserved, not overwritten, at
`evidence/locked_test_restricted/superseded_2026-08-21_audit_evidence_2022-FULL/`.

**Why.** The previous merge stamped `merged_at_utc = 2026-08-13T06:27:03Z`, predating the
2026-08-16 acquisition-window correction of the January and December folders, so its
`source_runs` digests referenced **superseded** per-month hashes. The notice's own terms
were "re-merge from the corrected months, or record an explicit decision re-pointing FULL's
provenance"; re-merging was chosen because it produces a verifiable artifact rather than a
statement about one.

**Executed** 2026-08-21 at `merged_at_utc = 2026-08-21T09:25:59Z` with a real interpreter
(Python 3.11.9). All twelve per-month hash manifests verified first — the script prints
`All per-month hash manifests verify.` and exits on any mismatch, which is the first time
that check has passed on a Windows checkout since the `.gitattributes` repair.
Access-log row **7** was written **before** the read.

**What changed: provenance only.** The record set is identical to the 2026-08-13 merge —
223,586 unique rows, 6,763 cross-month duplicates dropped, 642 out-of-year rows excluded
from statistics, and byte-identical when sorted. `madrigal_coverage_summary.csv`
(`b40304b5…`) and `madrigal_coverage_monthly.csv` (`6b53d385…`) are unchanged. Coverage
remains ARUC/BSHM/NICO at 365/365 days, 100%, December 31/31.

**A determinism defect was found and fixed.** The first regeneration hashed differently
from the 2026-08-13 artifact **despite holding the identical record set**, because output
order followed month-directory traversal and dedup insertion order. To anyone verifying
hashes that is indistinguishable from a content change. `merge_coverage_year.py` now sorts
rows on the dedup key `(station, ut1_unix, gdlat, glon)` before writing; two consecutive
runs were confirmed byte-identical (`d1527eca…`). TE §13.7 requires exact equality for
deterministic CPU transformations, and a merge is one — so this was a live reproducibility
defect, not a cosmetic one.

**Not cured by this re-merge**, and still travelling with every FULL-derived figure: the
twelve monthly runs rest on retrievals whose provider byte streams were never retained;
2022-04, 2022-07 and 2022-12 have no `raw_isprint_cache/`; `madrigalWeb_version` is
`"unknown"` in all twelve manifests; and none captured TE §13.1's per-run environment
fields.

**Approved** 2026-08-21 by the project owner under the recorded student/supervisor authority
equivalence.

---

## D-19 — Phase 1 support thresholds (freeze)

**Decision.** The four support values D-17 left as freeze-gate holes are frozen from
**measured** distributions, per TE §15.1's rule that such values are measured and frozen,
never invented.

| Field | Frozen value | Retention |
|---|---|---|
| `valid_observation_count` minimum | **3** contributing samples per cell-hour | keeps 95.24% of cell-hours |
| `within_hour_spread_tecu` | statistic = **range (max − min)** of contributing samples; **10.0 TECU** threshold, above which the row is flagged and excluded from the primary target | p99 = 9.616 TECU |
| `largest_internal_gap_s` maximum | **1800 s** (30 min) | keeps 93.39% |
| `provider_dtec_summary` | statistic = **median** of provider-reported `dtec`; **1.5 TECU** quality-flag threshold | p99 = 1.314 TECU |

**Measurement basis.** 23,709 deduplicated cell-hours over **January–November 2022 only**,
all three cells, read 2026-08-21 from the eleven non-December acquisition folders.
**December was excluded by construction** — it is the locked test month, and deriving a
governed constant from it would let the locked month influence the freeze set. This
measurement is therefore not a locked-test access.

Measured distributions:

- `valid_observation_count`: min 1, p05 3, p10 4, median 9, **max 12**. The histogram is
  {1: 393, 2: 736, 3: 874, 4: 1119, 5: 1601, 6: 1977, 7: 2075, 8: 2085, 9: 2173, 10: 2090,
  11: 1838, 12: 6748}.
- `within_hour_spread_tecu`: min 0, median 2.357, p95 6.873, p99 9.616, max 51.206.
- `largest_internal_gap_s`: **median 300 s**, confirming the 5-minute native cadence;
  p95 2100, p99 3600.
- median `dtec`: min 0.355, median 0.920, p95 1.305, p99 1.314, max 5.553.

**Rationale for each choice.** The observation minimum of 3 matches the ≥95% retention
posture D-2 already sets for day coverage, and three points is the smallest set on which a
range and a gap statistic mean anything. The spread and `dtec` thresholds are set at the
99th percentile so they flag genuine outliers rather than reshaping the dataset. The gap
maximum of 1800 s tolerates five consecutive missing 5-minute slots; TE §6.1's provisional
1200 s would keep 85.81%, and 2400 s (96.76%) was judged too permissive to detect a real
outage.

**TE §6.1's provisional minima are superseded for Phase 1, with the reason measured.** Its
provisional `valid_observation_count >= 20` retains **zero** cell-hours: the deduplicated
maximum is 12, because the product's native cadence is 5-minutely and an hour holds twelve
slots. That figure was written for the Phase 2 IPP population, where dozens of observations
per hour are normal. Its `valid_satellite_count >= 4` remains **not applicable** in Phase 1
— the quantity does not exist on this product (D-17).

**A measurement error found and corrected in the process, recorded so the number is
trustworthy.** The first pass over the eleven months reported counts up to 24 and suggested
a minimum of 20 was merely restrictive rather than impossible. That pass double-counted the
documented straddle day, which appears in two adjacent months' folders, so every affected
cell-hour was counted twice — the tell was that every value above 12 was exactly even. The
figures above are from a pass deduplicated on `(station, ut1_unix, gdlat, glon)`, the same
key `merge_coverage_year.py` uses, giving 201,686 records and a hard maximum of 12.

**Approved** 2026-08-21 by the project owner under the recorded student/supervisor authority
equivalence. TE §18.2 classes hourly support thresholds as a Student + Supervisor forbidden
choice (Q-12); the supervisor role is exercised under the recorded delegation, and no
signature is claimed. EV-06 requires the freeze before feature construction, which is
satisfied — no feature has been built.

---

## D-20 — Plumbing fixture station (freeze, Q-31)

**Decision date:** 2026-08-22. **Decided by:** the project decision owner under the
recorded student/supervisor authority equivalence. **Authority:** Q-31 assigns fixture
station, dates and acceptance tolerances to the Student (TE §18.2).

**Decision.** The `plumbing_7day` walking-skeleton fixture executes on **BSHM 32/35**, the
single station TE §15.1 mandates. D-11's window (2022-11-01 to 2022-11-07 inclusive) is
unchanged; this decision supplies only the station identity D-11 left open.

**Measured basis** — from D-11, sourced from
`evidence/audit_evidence_2022-11/madrigal_coverage_raw_records.csv`:

| Cell | Days present | Hourly bins | Records |
|---|---|---|---|
| **BSHM 32/35 — selected** | 7/7 | **168/168 (100.00%)** | 1,810 |
| ARUC 40/44 | 7/7 | 163/168 (97.02%) | 1,195 |
| NICO 35/33 | 7/7 | 155/168 (92.26%) | 964 |

**Rationale.** BSHM is the only candidate with complete observed coverage of the window.
The plumbing fixture is a smoke test of pipeline wiring (TC-03f), so avoidable missingness
in it would confound a plumbing failure with a data gap. ARUC and NICO remain available —
and are the better choices — for **separate** missing-data and robustness tests, where
their gaps are the point rather than a confound.

**What this closes and what it does not.** It closes **BLK-02**'s station limb, so
`tests/fixtures/plumbing_7day/fixture_manifest.yaml` can now state its identity. It does
**not** supply any manifest content: per TE §15.1 and §15.2 every count, tolerance,
row-count range, support and missingness limit, timestamp tolerance and CPU runtime range
is **measured from the fixture run and frozen**, and none exists yet because no fixture has
been run. **ARUC's unexplained one-bin shortfall on five of seven days** — D-11's pre-freeze
obligation — is **not** discharged and does not need to be, because ARUC is not selected;
it revives only if ARUC is later chosen for this fixture.

**Limitation carried from D-11, unchanged.** The window does not reproduce December's
winter-solstice regime or activity distribution and is not representative of the locked
month. The seven-day fixture is never scientific evidence.

---

## D-21 — F10.7 daily value and its availability rule (freeze)

**Decision date:** 2026-08-22. **Decided by:** the project decision owner under the
recorded authority equivalence. **Authority:** EC1-R-2 (decide and freeze the F10.7
daily-value selection rule), due G-04 before G-05; TE §18.2 Q-16/Q-17 (any feature, its
safe lag, or its missing rule) is a Student + Supervisor item exercised under the recorded
delegation.

**Decision.** The canonical daily F10.7 value is the **median of that UT day's observed
flux readings** (`fluxobsflux`, observed and **not** 1-AU-adjusted, per D-10.3).

**Measured basis**, derived 2026-08-22 from the held provider file
`evidence/audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt` (SHA-256 recorded in
`evidence/audit_ec1_2026-08-15/EC1-AUDIT.md`):

- **At calendar-day granularity, at least one observation is present on 365 of 365 days of
  2022** — 1,101 readings across those days, 360 days with 3 readings, 4 with 4, 1 with 5.
  This does **not** assert uninterrupted within-day coverage or uninterrupted provider
  availability, and is not a claim of "zero outage".
- Three daily observing slots, whose UT drifts seasonally: **(17, 20, 23) UT on 245 days**
  and **(18, 20, 22) UT on 120 days**. 20 UT is the only slot present on every day.
- On the four high-spread days the observed outlier occurs at **18 UT** (2022-01-18),
  **20 UT** (2022-03-31), **20 UT** (2022-08-28) and **17 UT** (2022-08-29). **Because
  outliers occur across multiple UT slots, fixed-hour selection without quality controls
  can retain contaminated observations.** The median returns the uncontaminated value on
  all four of these days.

  *Bounded deliberately.* This decision does **not** claim that no single slot is clean, or
  that no fixed-hour convention is safe. Neither stronger statement has been independently
  demonstrated; what is demonstrated is the four-day distribution above.

**Availability rule — binding, and the reason the median is usable at all.** A daily
median is not available until every reading it is computed from has been observed.

- **Observation-completion time of day *D*'s median** is the timestamp of *D*'s **last**
  reading: **23 UT on 245 days and 22 UT on 120 days** of 2022, derived from the same file.
  Worst case is 23 UT on day *D*.
- **The value used at a forecast origin is the most recent daily median whose
  observation-completion time is strictly earlier than that origin.** Under D-10.3's
  previous-day contract this is `median(D-1)` for any origin on day *D*: complete by 23 UT
  on *D-1* at the latest, which precedes the earliest possible origin (00 UT on *D*) by at
  least one hour.
- **No same-day look-ahead.** `median(D)` is never used at any origin on day *D*.
- **Carry-forward on unavailability.** Where the next daily median is not yet available at
  an origin, the **most recent previously available approved value** is used, and the
  carry-forward is recorded. This composes with, and does not override, the ≤ 3 h
  carry-forward bound on external drivers.
- The **trailing 81-day mean** is computed over daily medians ending at the safe-lagged
  day, never centered.

**One limb evidenced, one limb open — stated rather than assumed.** The rule above is
enforced on **observation availability**, which is fully derivable from the held file. The
provider's **publication** latency is **not** derivable from it: `fluxtable.txt` carries
observation date and time but no publication timestamp, and `EC1-AUDIT.md` records that the
file "carries no qualifier, flag or provenance column". So this decision fixes the
observation-availability rule and leaves publication latency as an **open obligation**
(EC1-R-4: ask NRCan directly). Until it is established, the ≥ 1 hour observation margin
above is the whole of the guarantee, and it is not claimed to cover publication delay.

**Not a model feature.** This decision fixes a predictor value and its availability. It
creates no quality-control feature — see D-23.

---

## D-22 — F10.7 duplicate-UT record handling (freeze)

**Decision date:** 2026-08-22. **Decided by:** the project decision owner under the
recorded authority equivalence. **Authority:** EC1-R-2's duplicate-stamp tie-break limb.

**Decision.** Where two or more readings share one UT timestamp, the **mean of the
duplicated measurements** is taken as that timestamp's value, with the **duplicate count
logged** and a **quality-control flag** set on the affected day.

**Provider-correction precedence, and why it is currently unexercisable.** If authoritative
provider documentation or the source data establishes that one duplicate is an official
correction or replacement, **the provider's correction semantics take precedence over the
mean.** On the evidence held today that clause cannot be exercised: `fluxtable.txt` has
exactly seven columns — `fluxdate`, `fluxtime`, `fluxjulian`, `fluxcarrington`,
`fluxobsflux`, `fluxadjflux`, `fluxursi` — and **no correction, revision, version or
provenance column**, which `EC1-AUDIT.md` records independently. Nothing in the file
distinguishes a correction from a repeat measurement. The precedence clause therefore
stands as a standing rule that activates if NRCan documentation is later obtained
(EC1-R-4); it is **not** applied by inference now.

**No day is silently discarded.** All five affected days remain in the primary dataset:

| Date | UT slots as recorded | Duplicated slot |
|---|---|---|
| 2022-03-26 | 17, 20, 23, 23 | 23 UT |
| 2022-09-20 | 17, 20, 23, 23 | 23 UT |
| 2022-10-17 | 17, 20, 23, 23 | 23 UT |
| 2022-10-23 | 17, 20, 20, 23 | 20 UT |
| 2022-12-08 | 18, 18, 20, 22, 22 | 18 UT and 22 UT |

**On 2022-12-08.** It is a December date in a **driver** series, not a target value or a
performance quantity. `EC1-AUDIT.md` already records that its year-wide predictor scan
touched no seal: no VTEC target, model, prediction or December performance quantity was
accessed. Handling it under this rule is predictor bookkeeping and is **not** a locked-test
access under Vision §8.3.

---

## D-23 — F10.7 high-spread day handling (freeze)

**Decision date:** 2026-08-22. **Decided by:** the project decision owner under the
recorded authority equivalence. **Authority:** EC1-R-3.

**Decision.** High-spread days are **flagged and retained**. The D-21 daily median is the
representative daily value; the day stays in the primary dataset.

**Affected dates, spreads and slot of the outlier**, derived 2026-08-22 from the held file.
"High spread" is within-day range (max − min) exceeding 20% of the day's median:

| Date | min | max | median | Spread | % of median | Outlier at |
|---|---|---|---|---|---|---|
| 2022-01-18 | 111.6 | 148.8 | 114.5 | 37.2 | 32.5% | 18 UT |
| 2022-03-31 | 148.7 | 239.5 | 149.8 | 90.8 | 60.6% | 20 UT |
| 2022-08-28 | 133.5 | 251.9 | 151.6 | 118.4 | 78.1% | 20 UT |
| 2022-08-29 | 123.0 | 357.1 | 130.6 | 234.1 | 179.2% | 17 UT |

**No exclusion.** None of the four is dropped from the primary dataset. Exclusion would
require a separately approved scientific decision under its own D-number, and none exists.

**The quality-control flag is not a model feature.** It is recorded in the driver manifest
as a diagnostic. Admitting it as a model input requires **explicit approval and a causality
check** establishing that the flag is derivable from information available at the forecast
origin — the same availability discipline every predictor is held to. Until then it is
excluded from the feature dictionary, and FR-P1-04-12's closed-input-space assertion is
what keeps it out.

---

## D-24 — Canonical protected set for the phase-transition manifest (freeze)

**Decision date:** 2026-08-22. **Decided by:** the project decision owner under the
recorded authority equivalence. **Authority:** BLK-06; TE §2.2, §7.0B; Vision §15.2 for the
consequent FR-P1-06-1 amendment.

**Decision.** The canonical protected set hashed by `phase_transition_manifest` is the
**deduplicated union of TE §2.2 and TE §7.0B**, with the three previously unmapped §7.0B
immutables — **history window**, **station encoding** and **baselines** — carried as
explicit items rather than left as assumed subsumptions.

**Both source lists enumerated from the authority, 2026-08-22.** TE §2.2 lists **12**
items; TE §7.0B lists **16**. FR-P1-06-1's existing list is §2.2's twelve plus `bootstrap`
and `reporting hierarchy` — **14**.

**Deduplication rule, stated explicitly as BLK-06 requires.** A §7.0B item maps onto a §2.2
item only where the §2.2 item's name covers it without inference:
`feature schema and safe lags` → `feature manifest`; `target cadence/horizon` →
`target contract`; `loss` and `optimizer policy` → `optimizer/loss policy`; `splits`,
`embargo` and `comparison-set masks` → `split/mask manifests`; `TensorFlow/Keras model
source and serialized architecture` → `model source` + `architecture serialization`.
`history window`, `station encoding` and `baselines` map onto nothing and are added.

**The canonical set — 17 items. The cardinality is calculated from the enumeration below,
not assumed** (14 carried forward + 3 added = 17).

| # | Protected item | Governing artifact | Hashable representation |
|---|---|---|---|
| 1 | Model source | `src/models/` | Source-file content hash of every model module |
| 2 | Architecture serialization | TF/Keras serialized architecture | Serialized-architecture hash |
| 3 | TensorFlow/Keras environment | `requirements.txt` + per-run `pip freeze` | Environment hash (TE §13.1) |
| 4 | Feature manifest | `configs/features.yaml` | Config-section hash |
| 5 | **History window** *(added)* | `configs/experiment.yaml` | Field hash — frozen at 24 h and absent from every grid |
| 6 | **Station encoding** *(added)* | `configs/features.yaml` | Field hash — `station_onehot_*` plus verified `station_lat` |
| 7 | Target contract | D-17 contract as recorded in `configs/data.yaml` | Config-section hash |
| 8 | Split/mask manifests | Fold, embargo and comparison-mask manifests | Manifest hashes; covers splits, the 24-hour embargo, and comparison-set masks |
| 9 | Grids | `configs/experiment.yaml` | Config-section hash — ridge 6, RF 18, LSTM 16 |
| 10 | Selected hyperparameters | Run record | Selected-value hash |
| 11 | Optimizer/loss policy | `configs/experiment.yaml` | Config-section hash; covers §7.0B's separate `loss` and `optimizer policy` |
| 12 | Seeds | `configs/seeds.yaml` | Config hash |
| 13 | Metrics | `src/evaluation/metrics.py` + config | Source + config-section hash |
| 14 | Statistical configuration | `configs/experiment.yaml` | Config-section hash |
| 15 | Bootstrap | `src/evaluation/bootstrap.py` + `configs/seeds.yaml` | Source + parameter hash — 24-hour vector blocks, 10,000 replicates, seed 20221201 |
| 16 | Reporting hierarchy | `configs/experiment.yaml` | Config-section hash |
| 17 | **Baselines** *(added)* | See the enumeration below | Source + config hash of every listed method |

**Item 17 — what "baselines" protects, enumerated as required.** The frozen comparison
methods and their configuration artifacts:

- **M-01** persistence — `src/models/persistence.py` + its `experiment.yaml` entry.
- **M-02** 24-hour seasonal persistence — same module + entry.
- **M-03** station×month×hour climatology, fitted on training partitions only —
  `src/models/climatology.py` + entry.
- **B-01 — IRI-2016 benchmark**, included on the owner's explicit instruction:
  `src/external/iri.py` plus its frozen generation configuration — implementation,
  switches, topside option and the **2000 km altitude ceiling** (TE §18.2 Q-14).
- **C-01 — CODE final GIM comparator**: `src/external/gim.py` plus the frozen product
  identity and interpolation rule (TE §18.2 Q-15).

**Consequences, both recorded rather than assumed.**

1. **FR-P1-06-1 conflicts and must be amended under Vision §15.2.** It requires
   `protected_hashes.keys()` to equal a "fourteen-item enumeration"; the approved canonical
   set has **17**. The owner authorized the amendment in advance; it is applied against
   this decision and annotated in place.
2. **Binding to concrete files completes at functional design.** The "hashable
   representation" column names the intended form. None of the four config files or six
   `src/` packages exists yet, so the exact field paths are fixed when the scaffold is
   built. **No file path or field name in the table above is claimed to exist today.**

**What this closes.** BLK-06's enumeration and cardinality limbs. It does **not** close the
implementation: `TransitionManifest.protected_hashes` and `diff_protected_hashes` are still
unwritten, and creating them stays gated by G-09 and stage 3.5.

---

## D-25 — F10.7 conservative availability convention (freeze, explicit assumption)

**Decision date:** 2026-08-22. **Decided by:** the project decision owner under the
recorded authority equivalence. **Authority:** EC1-R-2/EC1-R-4; TE §6.2; supplements
**D-21**.

**Why this decision exists.** D-21 fixed the daily F10.7 value as the daily median and
enforced availability on **observation completion**, which is derivable from the held file.
It could not fix **publication** availability, because the held archive contains no
publication timestamp. Rather than block on a provider response, the owner approved a
conservative convention.

**Decision — the availability convention.**

> A daily F10.7 median for UT day *D* becomes available **no earlier than the start of the
> following UTC day**, `00:00 UTC on D+1`.

Applied as an availability timestamp on the series:

- `availability_ts( median(D) ) = 00:00 UTC on D+1`.
- At a forecast origin *t*, the value used is the **most recent daily median whose
  `availability_ts` is at or before *t***.
- **`median(D)` is therefore never available at any origin on day *D*.** Same-day
  look-ahead is prevented by construction, not by review.
- Under D-10.3's previous-day contract this yields `median(D-1)` for every origin on day
  *D*, since `availability_ts(median(D-1)) = 00:00 UTC on D`.
- Where no median is yet available, the most recent previously available approved value
  carries forward and the carry-forward is recorded.
- The trailing 81-day mean is computed over daily medians ending at the safe-lagged day,
  never centered.

**How conservative this is, stated in measured terms.** Observation completion of
`median(D)` is **22 UT on 120 days and 23 UT on 245 days** of 2022 (derived from the held
file). The convention delays availability past that by **1 to 2 hours** in every case. It
is strictly more conservative than the observation-completion rule it supplements, and
never less.

**This is an explicit project assumption, not a demonstrated fact.** It does **not** prove
that NRCan published any 2022 value by `00:00 UTC on D+1`, and it does **not** establish
historical real-time publication availability. **No operational real-time availability
claim is made or supported by it.** What it does is bound the project's use of the series
to a rule that cannot leak forward, on an assumption stated in the open.

**Conflicting frozen obligations, identified exactly as required.** Three places require a
publication timestamp rather than an assumed convention:

| Locus | Text | Bearing on F10.7 |
|---|---|---|
| **TE §7.0A stage 4** | *"Build the space-weather availability matrix with observation and publication timestamps."* | Covers the whole matrix, F10.7 included |
| **EV-12** (TE evidence register) | *"External-feature publication latency … Provider release documentation; 2022 availability matrix; Hp60 availability"*, due at **Feature freeze (G-04)** | Names **provider release documentation** as the evidence |
| **`components.md`**, `availability.py` | *"observation timestamp, publication timestamp, release status and safe lag per feature"* | Design-level mirror of the same obligation |

**Note what does *not* conflict.** F10.7's own §6.2 dictionary rows — `f107_safe` and
`f107_81_trailing` — record provenance as *"Approved source"* and do **not** themselves
demand a publication timestamp, unlike `kp_safe` / `ap_safe`, whose row explicitly reads
*"observation + publication timestamps"*. The conflict is therefore with the matrix-level
and evidence-register obligations, not with the feature contract.

**Amendment GRANTED and APPLIED 2026-08-22 — `CR-2026-08-22-EV-12`.** The F10.7 row of the
availability matrix now records **this declared convention plus the documented absence of a
provider publication timestamp and an explicit unverified-latency statement**, in place of
a verified publication timestamp, and **EV-12 is satisfied for F10.7** by that record
rather than by provider release documentation. Applied to TE **EV-12**, TE **§7.0A stage
4** and `components.md` → `availability.py` under Vision §15.2, on the project decision
owner's express approval. The change request that preceded it is retained as
`governance/CHANGE_REQUEST_2026-08-22_EV-12_f107_publication.md`.

**What the grant does not change.** The convention remains an **explicit project
assumption**: it still proves nothing about historical publication latency, and **no
operational real-time availability claim rests on it**. What changed is that recording the
assumption, the absence and the unverified status is now the sanctioned evidence — so
**Bolt 5 is not forced to fill a field it cannot obtain**, and EV-12's F10.7 limb is no
longer unmet at G-04.

---

## D-26 — F10.7 March–April 2022 provenance: recorded unresolved

**Decision date:** 2026-08-22. **Decided by:** the project decision owner under the
recorded authority equivalence. **Authority:** EC1-R-4; supplements **D-21**.

**Decision.** The provenance of the March–April 2022 F10.7 values spanning the suspected
outage is recorded as **UNRESOLVED**. The data is **retained**.

**What is asserted, and what is not.**

- **Asserted, measured:** at calendar-day granularity, at least one observation is present
  on **365 of 365 days** of 2022 in the held archive. This does not assert uninterrupted
  within-day coverage or uninterrupted provider availability.
- **NOT asserted, in either direction:** whether values spanning the incident were
  **measured**, **reconstructed**, **interpolated**, or **provider-corrected**. The held
  file carries seven columns — `fluxdate`, `fluxtime`, `fluxjulian`, `fluxcarrington`,
  `fluxobsflux`, `fluxadjflux`, `fluxursi` — and **no qualifier, flag, revision or
  provenance column**. `EC1-AUDIT.md` records the same limitation independently. The
  distinction is **not determinable from this file**, and no inference is drawn.

**Retention.** The values stay in the primary dataset. No governing rule requires their
exclusion: D-5's gap policy governs missing values (none are missing at day granularity),
and no requirement conditions retention on provenance being established.

**Reporting obligation.** This limitation is carried into the thesis reporting obligations
alongside the existing F10.7 caveats: any result whose interpretation leans on F10.7
behaviour across March–April 2022 states that the provenance of those values is unresolved.
It joins the claims-and-limitations checklist rather than being left in this register only.

**Clarification routes that change no frozen source and re-download nothing.** Two are
already authorized and are named so the obligation is actionable:

1. **Provider metadata already held.** The file's `fluxadjflux` and `fluxursi` columns are
   provider-derived from `fluxobsflux`. Their internal consistency across the window is
   inspectable **from bytes already in the repository** and would show whether the
   provider's own derivations were computed from the same observed values. This is
   analysis of held data, not re-acquisition.
2. **NRCan direct enquiry (EC1-R-4).** Already recorded as optional. **Project progress
   does not block on a response** (D-25).

**Neither route re-downloads data, changes the frozen source, or touches locked December.**

**A sensitivity analysis that could quantify the dependence — identified, not approved.**
`ABL-NOSW` already exists as a predeclared ablation in TE §7.2: *"Do forecast-safe
space-weather features add value beyond lagged VTEC and time?"*, dropping `kp_safe`,
`ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe` and `f107_81_trailing`. A narrower
F10.7-only variant would isolate dependence on the affected series specifically.

**Constraints on any such analysis, stated so it cannot drift:** it runs on the **frozen
January–November folds only**, uses identical folds, masks and tuning budget, is
**predeclared as a named run in `experiment.yaml` with a run ID before it executes**, and
**does not touch locked December** — the locked test is opened once, after G-05, and no
ablation may precede or substitute for that. **This decision identifies the analysis; it
does not approve or schedule it.** Approval is a separate owner decision.

---

## D-27 — The primary target is not transformed; the inverse obligation is ABL-DIFF's alone (reading)

**Decision date:** 2026-08-24. **Decided by:** the project decision owner under the
recorded authority equivalence, at the delivery-planning approval gate.
**Authority:** TE §7.2 (ablation register); TE §6.2 (feature dictionary);
NFR-LEAK-01. **Raised by:** blocker **BLK-08**, registered 2026-08-23 against
`evaluation-and-comparison` and `features-and-splits`.

**Decision.** The **primary configuration's train-only transform does not touch the
target.** It acts on target-**derived input features**; the target itself remains
**raw TECU**. `ABL-DIFF` is the sole configuration that transforms the target, and its
inverse obligation is unchanged.

**This is a reading of already-frozen text, not a new scientific value.** No constant,
threshold, window, seed or grid is set, changed or reinterpreted by this decision.

**The evidence it was read from.**

| # | Source | What it states |
|---|---|---|
| 1 | **TE §7.2 ablation table, `ABL-DIFF` row** | Its **Primary remains** column reads **"Raw TECU"**. The first-difference target is an ablation-only change: *"Target becomes \(y_{t+1}-y_t\); predictions inverse-transformed to absolute TECU before any metric is computed"* |
| 2 | **TE §6.2 dictionary** | This is the **feature** table. Its only train-only standardization on anything target-derived applies to **inputs** — `vtec_lag_1h/2h/3h/24h` and `vtec_seq_24`, *"Train-only standardization for ridge/LSTM; none for RF"*. Those are lagged values used as predictors, not the \(y\) being predicted |
| 3 | **Both governing documents** | Neither states anywhere that the target itself is scaled. The only normalization applied to it at P1-03 is **UTC** normalization — timestamps, not magnitudes |
| 4 | **NFR-LEAK-01** | Its *"no all-data scaling"* prohibition is a constraint on features |

**Consequences.**

- **The primary path needs no inverse transform.** Model output is already in raw TECU, so the paired loss differential, the vector time-block bootstrap interval and the practical-relevance threshold are computed on the quantity the model emits. **This must be stated explicitly** in the design (`component-methods.md`, ADR-11 § Consequences) so the `ABL-DIFF` obligation is visibly satisfied rather than silently assumed.
- **`ABL-DIFF` retains its obligation in full**, per TE §7.2: it inverse-transforms to absolute TECU **before** metrics *"so every ablation is scored on the same quantity in the same units as the primary"*, and **error propagation through the inverse transform is recorded**.
- **BLK-08's mechanism limb narrows and stays open.** `functional-design` (3.1) names how `ABL-DIFF`'s inverse is reached and where its error propagation is recorded, jointly for `features-and-splits` and `evaluation-and-comparison`. It no longer requires a general `src/evaluation` → `src/features` route for the primary path.
- **No import-boundary change is authorised by this decision.** The §12 rule and its allowlist are untouched.

**What is NOT asserted.** That the LSTM or ridge implementation may not internally
scale its own inputs — that is the §6.2 dictionary's train-only standardization, which
this decision leaves exactly as written. And that `ABL-DIFF` is approved or scheduled;
it remains a predeclared ablation requiring its own registration in `experiment.yaml`.

**Limitation.** This decision is a reading of frozen text taken before any code exists.
If `code-generation` or `build-and-test` finds a model path that scales the target
contrary to this reading, that is a **contradiction to surface**, not a licence to
adjust the target contract — TE §18.2's absolute rule bars changing a scientific value
in response to what a run produced.

---

## D-28 — The G-06 locked-test scored set is 2–31 December 2022 (30 days)

**Decision date:** 2026-08-28. **Decided by:** the project decision owner under the
recorded authority equivalence (D-1 addendum), at the `functional-design` (3.1)
governance gate, on governance report `GOV-2026-08-28-FD-01` Recommendation 6.
**Authority:** `requirements.md` FR-P1-04-5; `component-methods.md` ADR-11
(2026-08-23, the `lead_in_hours` removal); Vision §8.2, §8.7, §15.1; TE §7.1.
**Raised by:** the full-board review of stage 3.1 — Review Chair findings CHAIR-01 and
CHAIR-02 (graded BLOCKER) and Validation Auditor finding VAL-04 (graded MAJOR).

**Decision.** The locked-test scored set is **2–31 December 2022 inclusive, 30 days**.
The first 24 hours of the locked month are **excluded and counted**, exactly as they are
for every validation month, because no window may cross a partition boundary. A
1 December row reaching any metric entry point raises.

**This ratifies a ruling already taken and already built upon.** The reduction was
decided at stage 3.1 on 2026-08-26 as answer **FU-7 = A** in
`construction/features-and-splits/functional-design/functional-design-questions.md`,
superseding the earlier same-stage answer FU-5 = D ("1 December stays in the G-06 locked
test with no first-day loss"), which had been decided on 2026-08-24 against the interface
ADR-11 retired the day before. FU-7 = A now propagates as live design fact through eight
units. **What this decision adds is the record, not the number.**

**The authority conflict, disclosed rather than resolved by inference.**

The board found — and this decision records without softening — that the two highest
authorities do not say what FR-P1-04-5 says:

| Source | Text, byte-exact |
|---|---|
| `PreFlight/vision_document(3)(2)(2).md:751` | `| Locked test | — | — | December 2022 only |` |
| `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md:400` | `| Locked test | — | — | December 2022 only |` |

Both assign F1–F4 an explicit `24 hours` embargo and assign the Locked-test row **`—`**
in the Embargo column. The November/December boundary protection those tables name is
the **frozen manifest**, on the Final refit row, not a 24-hour exclusion. Vision §8.2
adds that December 2022 is "the only locked test period".

`requirements.md` FR-P1-04-5 — a level-4 artifact in the precedence chain — states
"each with a 24-hour embargo … the first 24 h are excluded and counted", and cites as
its source the very tables carrying `—`. Its own acceptance criterion says the split
manifest "enumerates **all five partitions**", which excludes December from the five.
**A level-4 paraphrase is therefore the sole textual basis for the 30-day reading, and
it over-reaches the levels 1 and 2 it cites.** The conflict was not escalated when
FU-7 = A was answered, and this decision does not pretend it was.

**Why the number is nonetheless accepted, on three independent grounds.**

1. **Physical.** 1 December is the day of December furthest from the 21 December
   solstice, so removing it leaves a scored set whose mean solar-declination distance
   from solstice is marginally *smaller*. No regime-skewing loss. No disturbed day named
   in D-13's December characterisation falls on 1 December.
2. **Statistical.** The vector time-block bootstrap loses one of 31 24-hour blocks — a
   3.2% reduction (72 of 2,232 station-hours). Fewer blocks widens the interval, so the
   error is toward under-claiming.
3. **Arithmetic, and load-bearing.** 2–31 December is 720 hours, divisible by both 24
   and 48, giving 30 blocks and 15 blocks. Under the superseded 31-day reading, 744
   hours is **not** divisible by 48, so the 48-hour block-length sensitivity TE §13.6
   *requires* would itself have raised. The 31-day reading was internally inconsistent
   with a mandatory sensitivity.

**What is NOT decided here.**

- **No embargo is introduced on the locked test.** The 24-hour exclusion is the
  boundary rule FR-P1-04-5 applies to every partition, not a new embargo row on a table
  that carries `—`.
- **The authority conflict is not resolved.** Whether FR-P1-04-5's paraphrase should be
  amended to match Vision §8.2, or Vision §8.2's table annotated to match FR-P1-04-5,
  is left open and is carried to G-05 as a stated item. This decision fixes the
  operative value and records the disagreement; it does not rewrite either authority.
- **No claim boundary is widened.** D-8's boundary is unchanged in substance; its
  *statement* now owes the precision this decision supplies — see the consequence below.

**Consequences.**

- **The scored set is 30 days everywhere, and must be disclosed as 30 days.** Governance
  report Recommendation 16 records that the reduction is encoded rigorously where it
  bites (the DEC mask range assertion, the excluded-and-counted rule) and disclosed on
  **no** claim surface, while `REQ-CLAIM-01` still reads "tested on December 2022 only".
  The primary results table, the breakdown artifacts and the claims-and-limitations
  checklist each carry the scored-window statement.
- **A revised split manifest is owed.** Vision §8.2 requires one for any date
  adjustment. None exists yet because no manifest exists yet; the obligation attaches at
  G-05 and is recorded here so it is not discovered later.
- **Every December denominator inherits this.** The bootstrap's 30 blocks (15 at 48 h),
  the regime-count audit's relationship to the scored set (governance report
  Recommendation 15, still open), the coverage denominator, and every reported December
  figure.

**Limitation, stated plainly.** This is an owner ratification under the recorded
student/supervisor authority equivalence. **No supervisor signature artifact exists and
none is claimed.** Vision §15.1 places "test dates" under "Supervisor: Approval
required", and the Review Chair seat of the board held that the equivalence's scope over
a G-05-frozen split value is unestablished; the Validation Auditor seat, whose exclusive
domain this is, held the equivalence sufficient and the record the only defect. Both
readings are on the record. An examining committee requiring an independent supervisor
signature for a locked-test date adjustment is outside this repository's control, and
this decision does not represent itself as satisfying such a requirement.

---

## D-29 — `dataset_version` is a 12-hex prefix of `content_hash`, verified unused on write (freeze)

**Decision date:** 2026-08-28. **Decided by:** the project decision owner under the
recorded authority equivalence (D-1 addendum), at the `functional-design` (3.1)
governance gate, on governance report `GOV-2026-08-28-FD-01` Recommendation 42
(board option 2, which was the board's own recommendation).
**Authority:** TE §13.3 line 532 (`dataset_version` = "Stable release ID"; "The
final-results dataset is write-protected or stored under a new version rather than
overwritten"); §19 TA-15; `team.md` § Deployment. **Raised by:** Benchmark & Deployment
seat finding `BENCH-08`, against `foundation` R-12's own disclosure that injectivity is
**NOT YET ESTABLISHED** "and it is what 'never reused' actually requires".

**Decision.** `dataset_version` is the **first 12 hexadecimal characters of the release's
`content_hash`**, and `write_release` **verifies on write that the prefix is not already
in use** among existing releases, raising `ReleaseError` if it is. Three parts, all
binding:

1. **Encoding — 12 hex characters** (48 bits) taken from the front of the SHA-256
   `content_hash` that R-11 already makes the release's identity. The label is derived,
   never allocated; no ledger is introduced.
2. **A recorded collision bound.** At 48 bits, the probability that any two of *n*
   releases share a prefix is approximately n² / 2⁴⁹. For **n = 1,000** releases that is
   about **1.8 × 10⁻⁹**; for **n = 10,000**, about **1.8 × 10⁻⁷**. This project's expected
   release population is far below either figure. **The bound is recorded so it can be
   checked, not so it can be relied on** — the verify-on-write check below is what
   actually establishes never-reuse, and the bound only says how rarely that check is
   expected to fire.
3. **Verify-on-write.** `write_release` reads back the existing release population and
   refuses a write whose 12-hex prefix already names a different `content_hash`. A prefix
   collision is therefore **surfaced, never silently accepted** — the integrity-violation
   tier of the two-tier error posture `team.md` § Code Style fixes.

**Why this option and not the other two.** The full 64-hex `content_hash` (board option 1)
inherits injectivity for free and needs no read-back, but is unusable as the human
citation label R-12 says is the label's entire purpose. Declaring the label explicitly
non-unique (option 3) is honest but requires a Vision §15.2 act to withdraw an obligation
§13.3 states, and pushes every citation to 64 hex anyway. Option 2 is the only one
delivering **both** a citable label and an **established** never-reuse property, and its
cost is exactly the `verify_release` amendment `foundation` R-12 had already listed as
open — so this decision closes two of R-12's three open items in one act.

**What this decision does NOT change.**

- **Release immutability is untouched, and never depended on this.** It rests on R-13's
  directory-level overwrite refusal and R-11's identity-equals-`content_hash`, neither of
  which uses `dataset_version`. What was open, and is now closed, is **citation
  uniqueness** — a traceability property, not a mutation property. `foundation` R-12's
  characterisation of the label as "a citation device with idempotence, not an identity
  guarantee" is **superseded**: it is now a citation device with idempotence **and**
  verified injectivity within the release population.
- **No release ledger is introduced.** The verify-on-write check reads the existing
  releases; it allocates nothing and stores no separate index. The distinction matters
  because a ledger was declined deliberately.

**Consequences.**

- **`write_release` becomes implementable**, and the 3.5 block recorded at
  `fixtures-and-reproducibility` and `foundation` R-12 lifts.
- **`foundation` R-12 owes an amendment**: injectivity moves from **NOT YET ESTABLISHED**
  to **established by verify-on-write**, and the `verify_release` open item closes.
- **TA-15 is still NOT covered, and this decision does not cover it.**
  `tests/test_release_hashes.py` exists and its name matches §12's mandated module, but
  derived 2026-08-28 it exercises **none** of §13.3's manifest fields and does not test
  R-13's overwrite refusal. The closure evidence owed is: that module extended to assert
  `write_release` refuses a second write to an occupied directory and leaves the original
  bytes unchanged; every §13.3 field present including `mask_ids`, `feature_set_ids`,
  `row_counts` and `exclusions_qc_summary`; and `dataset_version` corresponding to its
  release's `content_hash` under this encoding. **Until that lands, no artifact may read
  TA-15 as satisfied.**

**Limitation, stated plainly.** The collision bound is arithmetic, not measurement — no
release exists yet, so the release population is projected rather than observed. If the
population ever approaches the figures above, the prefix length is the parameter to
revisit, and revisiting it is a fresh D-number rather than an implementation choice
(TE §18.2).

---

## D-30 — `.dst_summary.json` relocates into the guarded evidence tree (freeze)

**Decision date:** 2026-08-28. **Decided by:** the project decision owner under the
recorded authority equivalence (D-1 addendum), at the `functional-design` (3.1)
governance gate, on governance report `GOV-2026-08-28-FD-01` Recommendation 44(b)
(board option 2). **Authority:** D-15 (the custody-relocation precedent and its
verify-byte-identical method); TE §13.4 and the locked-month access-log obligation;
`governance-guards` R-26 and R-27. **Raised by:** Validation Auditor finding `VAL-08`.

**Decision.** `.dst_summary.json` moves from the repository root to
**`evidence/audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json`**, inside R-27's `evidence/`
scan root, verified byte-identical across the move on the D-15 method (SHA-256 before and
after). On completion, `governance-guards` R-26's driver-exclusion **class 4 ceases to be
conditional** and becomes an unconditional enumerated class.

**Why it matters, stated concretely.** The file carries December 2022 content: twelve
month keys, with `"12"` holding `days_parsed: 31`, `hours: 744`, `min: -68`,
`storm50: [7, 27]`, a `storm30` list of 15 days, and `daily_min` with 31 entries. At the
repository root it sits **outside** the scan root of the guard designed to find exactly
this class of artifact, so the December guard could not see it. `governance-guards`
identified the relocation as the fix, **declined to perform it** without this decision,
and made class 4 conditional on the move so the design would not claim a closure it had
not earned.

**Why relocation and not widening the scan root.** Widening R-27 to the repository root
was considered and rejected by the owning unit: it pulls every unrelated file at the root
into the guard's reach and makes its exclusion list unbounded, which trades a known gap
for an open-ended one. Moving one file into the tree the guard already walks is the
narrower act.

**What this decision does NOT do.**

- **It is not a December read.** The move is a byte-level relocation with hash
  verification; **no field is parsed, no value inspected, no statistic computed** — the
  same scope and method as D-15's relocation and access-log rows 6, 7 and 11. An
  access-log row is written **before** the move, as FR-P1-02-3 requires.
- **It changes no value.** The file's contents are untouched; only its path changes.
- **It does not make `.dst_summary.json` an approved input to anything.** Dst remains
  diagnostic/hindcast-only and never a confirmatory ML feature (`project.md` § Mandated;
  TC-11), and the provisional-grade restriction recorded in D-11 is unaffected.

**Consequences.**

- `governance-guards` R-26 class 4 becomes unconditional; the OPEN item recorded at its
  `business-rules.md` closes.
- A change record is filed under Vision §15.2's six fields:
  `governance/CHANGE_RECORD_2026-08-28_dst_summary_relocation.md`.
- Any path reference to the old root location is swept; none may remain pointing at a file
  that has moved.

**Limitation.** This decision closes the *reachability* gap only. Whether
`.dst_summary.json` should exist as a derived artifact at all, and under whose provenance
record, is not decided here — it is a derived driver summary whose own §13.1 environment
capture was never taken, and it inherits the standing pre-git provenance limitation the
experiment registry records for every artifact of that era.

---

## D-31 — G-09 (Agent preflight) is signed, with its §18.3 preconditions recorded as unmet

**Decision date:** 2026-08-28. **Decided by:** the project decision owner, in the
`functional-design` (3.1) session, under the recorded student/supervisor authority
equivalence (D-1 addendum). **Authority:** TE §18.3 (Preflight gate); TE §1.2 gate table
row *"Agent preflight passed — Student and supervisor — Any affected component is coded —
Pending — G-09"*; TE:97 (*"Blocks coding until P0 freezes pass"*); TE:735 (authority to
create a module is not authority to write it). **Raised by:** the owner, unprompted, at the
`functional-design` remediation gate.

**Decision.** **G-09 is signed and approved.** The gate that blocked creation of any
module — every `src/` package, every `configs/` file, every `tests/` module this stage
designed — is **open**. Work previously deferred *solely* on the ground "G-09 is unsigned"
may now proceed.

**This decision is recorded with its preconditions disclosed rather than presumed
satisfied.** TE §18.3 states three preconditions and a decision criterion. As of
2026-08-28, derived by direct workspace inspection and printed here before assertion,
**none of the three is met**:

| §18.3 precondition | State on 2026-08-28 | Evidence |
|---|---|---|
| 1. All P0 decision-register entries for the affected component resolved and recorded | **Partially met.** D-1…D-31 exist and the register is maintained, but freeze-gate holes remain open by design — D-17's four support thresholds, D-25's requested §15.2 amendment *[granted and applied 2026-08-22, `CR-2026-08-22-EV-12`; annotated 2026-09-19, P-5]*, D-26's UNRESOLVED provenance, and the nine unfrozen scientific values this stage routed to G-04/G-05 rather than defaulting | `evidence/DECISIONS.md`; stage 3.1 gate items |
| 2. An automated preflight asserts no required field in `data.yaml`, `features.yaml`, `experiment.yaml` or `seeds.yaml` is `TBD`, that every declared source and hash exists, **and that all gate tests pass** | **NOT MET — the assertion cannot run.** `configs/` does not exist; none of the four config files exists; `src/` does not exist; `pyproject.toml` does not exist. There is no preflight to run and nothing for it to assert over | Workspace inspection 2026-08-28 |
| 3. The supervisor has signed the scientific hierarchy, IRI role, horizons, estimand, seeds and locked-test protocol | **Met only under the recorded authority equivalence.** No independent supervisor signature artifact exists for any of the six, and none is claimed. G-05 and G-06 remain `Blocked` | `evidence/DECISIONS.md` D-1 addendum; Vision §13.1 gate table |
| **Decision criterion:** zero unresolved P0 fields **and no failing critical test** | **NOT VERIFIABLE in this environment.** The ten named critical tests cannot be executed: no Python interpreter is installed (`python.exe` is a zero-byte Windows Store stub; no registry entry; no interpreter on disk). "No failing critical test" is therefore **unproven, not proven** — an absence of executions, not an absence of failures | Environment inspection 2026-08-28 |
| **Evidence artifact:** `aws_ai_dlc_preflight_report` | **DOES NOT EXIST.** No unit produces it; `foundation` owns FR-WS-7/TA-23, which discharge onto it, and the artifact is designed but unwritten | `GOV-2026-08-28-FD-01` Rec 9 |

**What this decision therefore is, stated exactly.** It is the **owner exercising authority
to open the gate**, not a record that the gate's evidentiary conditions were satisfied. The
owner may do this — G-09 is theirs to sign under the recorded equivalence, exactly as D-11
through D-30 were taken — and the project is entitled to proceed on it. What must never
happen is a later reader inferring from "G-09 signed" that a preflight ran, that the four
configs exist and are TBD-free, or that the ten critical tests were executed and passed.
**None of those things happened.** This entry exists so that inference is impossible.

**What G-09's signature unblocks.**

- Creation of `src/`, `configs/`, `pyproject.toml`, `tests/fixtures/` and the modules §12
  mandates — the authority TE:735 says is separate from the authority to write them.
- Correction of defects previously deferred *solely* because G-09 barred editing the file.
  Specifically: `tests/test_release_hashes.py`'s §13.3 field coverage and R-13 overwrite
  refusal (TA-15), and routing the two unlogged restricted reads at
  `tests/test_release_hashes.py:137` and `tests/test_acquisition_window.py:195` through
  `open_restricted`.

**What G-09's signature does NOT unblock, and this list is exhaustive of the gates that
still bind.**

- **G-05 and G-06 remain `Blocked`.** No locked-test access, no December prediction, no
  metric. `tests/test_locked_test_guard.py`'s obligations are untouched.
- **G-P1A, G-P2, G-P3A, G-P3C and G-07 are unaffected.** G-09 is the coding gate, not the
  scientific, licence, phase-transition or reproducibility gate.
- **TE §18.2's absolute rule stands**: no scientific value may be changed after seeing a
  result, and no agent may fill a freeze-gate value by convenience. **Every value this
  stage routed to G-04/G-05 stays routed.** G-09 authorises writing code; it authorises
  nothing about choosing a constant.
- **TE §18.3's stop-and-report obligation survives its own gate.** The sentence *"Claude
  Code or any equivalent agent must not implement an affected component while its P0
  decision is unresolved, and must stop and report rather than choose a default"* is a
  standing rule on implementation, not a one-time gate condition. An unresolved P0 still
  stops implementation of the component it governs.

**Limitation, stated plainly.** This is an owner signature under the recorded
student/supervisor authority equivalence. **No independent supervisor signature artifact
exists and none is claimed.** TE §1.2 assigns G-09 to "Student and supervisor" jointly. An
examining committee requiring an independent supervisor signature for the coding gate — in
a project where the automated preflight it names never ran — is outside this repository's
control, and this decision does not represent itself as satisfying such a requirement. The
row in the §18.3 table above is the disclosure that makes that judgeable.

---

## D-32 — All eight candidate Vision §15.2 acceptance rows are approved (freeze)

**Decision date:** 2026-08-28. **Decided by:** the project decision owner under the
recorded student/supervisor authority equivalence (D-1 addendum), at the
`functional-design` (3.1) governance gate, on governance report `GOV-2026-08-28-FD-01`
**Recommendation 22**, **board option 1** — which was the board's own recommendation.
**Authority:** Vision §15.2 (acceptance-row amendments); TE §16/§16.1 (WS-01…WS-20
pass/fail, *"visual inspection alone is insufficient"*); TE §19 (TA-01…TA-36); TE §18.3
(*"zero unresolved P0 fields and no failing critical test"*); `team.md` § Testing Posture
(the §16/§19 rows are "the real bar"). **Raised by:** Benchmark & Deployment seat finding
`BENCH-05`, graded `MAJOR` and recorded as a **gate condition rather than an artifact
defect**.

**Decision.** **All eight candidate rows are approved** and become part of the §16/§19
acceptance surface. None is deferred; the deferral option the board offered as its
fallback (option 3, four rows now and four at G-05) is **not taken**.

| # | ID | What the row accepts | Owning rule(s) | Gate |
|---|---|---|---|---|
| 1 | **FR-P1-04-15** | The IRI-2016 benchmark is validated **before** generation and generation is **blocked** if validation fails; `iri_implementation_validation_report` records the pinned build, all model switches and the topside option, the **2000 km altitude ceiling stated explicitly**, units and extraction | `external-products` R-59 | G-04, G-05 |
| 2 | **FR-P1-04-18** | The GIM comparator contract — bilinear-in-space / linear-in-time interpolation with the longitude-rotation correction, plus the independence obligations split out of FR-P1-04-9 | `external-products` R-60 | G-05 |
| 3 | **FR-P1-05-7** | The **confirmatory estimand**: paired loss differential, mean within-station difference of squared errors, **benchmark minus model**, equal-station weighting, positive favouring the model, at 95%; percentage reduction only as a labelled derived summary; **every table states the sign convention** | `evaluation-and-comparison` R-108 | G-05, G-06 |
| 4 | **FR-P1-05-20** | The **binding honesty rule**: any baseline beating the LSTM on the locked test appears in the primary results table **and** the abstract-level conclusion | `evaluation-and-comparison` R-110; `regimes-diagnostics-reporting` R-126 | G-06 |
| 5 | **`TST-CLAIMS-01`** | The claims-and-limitations checklist test — **named by Vision §11.2 with no acceptance row anywhere in the project** until now | `regimes-diagnostics-reporting` R-126 | G-06, G-07 |
| 6 | **FR-P1-05-19** | The plasmaspheric-offset disclosure accompanies **every** interpretation of the primary comparison (Vision §6.11: the discrepancy carries a physical, structured, time-varying component that is **not forecast error**) | `regimes-diagnostics-reporting` R-126 | G-06 |
| 7 | **FR-P1-05-16** | The required reporting breakdowns, with observation-quality strata computed from **D-17's measured-available fields only** | `regimes-diagnostics-reporting` R-127 | G-05 |
| 8 | **FR-P1-05-18** | The December regime-count audit as **required G-05 evidence**, and the H4 / SRQ-5 demotion legitimate **only if recorded before the freeze** | `regimes-diagnostics-reporting`; `inventory-and-registry` | **G-05** |

**Why option 1 rather than the alternatives.** Option 2 (approve 3.1 and make the
dispositions a G-05 precondition) would have left the unrowed set as exactly what
Construction builds against during the interval — the `GOV-F-06` hazard `team.md` records
as precedent, where a narrow executing-test threshold is misread as narrowing the
critical-test obligation. Option 3 (four now, four at G-05) leaves a partial acceptance
surface, and `project.md` § Way of Working warns that partial lists are what make the
unlisted items invisible. Option 1 closes the class at one sitting, and because each
design already names the row it would point at, this decision **chooses among stated
candidates rather than drafting new ones**.

**What each approval means, stated precisely.** A row is now part of §18.3's *"no failing
critical test"* criterion. It is **not** a claim that any of them currently passes: **none
of the eight is executable today**, because none of the producing code exists. That is the
same for every option the board offered and is not a consequence of this choice.

**What this decision does NOT do.**

- **It does not discharge any row.** Approval creates the bar; it does not clear it. Each
  row is discharged only by its own passing execution evidence against final code.
- **It does not decide any scientific value.** FR-P1-04-18's interpolation method is a
  **§18.2 Student-owned forbidden choice (Q-15)** and remains unfrozen; FR-P1-05-18's
  supervisor-approved disturbed-hour minimum likewise. Approving the acceptance row makes
  the obligation checkable; it does not fill the value, and **TE §18.3's stop-and-report
  rule continues to bar an agent from filling either**.
- **It does not amend Vision or TE.** A Vision §15.2 amendment adding these rows to the
  §16/§19 tables is **owed** and is recorded here as owed. The authority documents are not
  edited by a decision record.
- **It does not alter the `models-and-baselines` exclusion.** That unit uses an inline
  acceptance form and the board excluded it from the 23% derivation rather than guessing
  at it. Whether its inline form needs the same treatment is **not decided here** and is
  carried as an open item.

**Consequences.**

- The 28-of-124 unrowed `**Acceptance.**` statements shrink by the eight rules these rows
  attach to. **The remainder are not thereby closed** — the residual is carried as an open
  item against stage 3.2, enumerated by rule ID at each owning unit rather than as a
  percentage.
- §18.3's ten-item critical set is re-checked against these dispositions, per the board's
  stated closure evidence.
- **`TST-CLAIMS-01` gains its first acceptance row in the project's history.** Vision
  §11.2 named it and nothing pointed at it; that gap closes here.

**Limitation, stated plainly.** This is an owner approval under the recorded
student/supervisor authority equivalence. Vision §15.2 places acceptance-row amendments
with the **Supervisor**, with the Student proposing. **No independent supervisor signature
artifact exists and none is claimed.** An examining committee requiring one for an
acceptance-surface amendment is outside this repository's control, and this decision does
not represent itself as satisfying such a requirement.

---

## D-33 — The coordinate-to-cell rule's identifier and config transcription (freeze)

**Decision date:** 2026-09-10. **Decided by:** the project decision owner, adopting as
drafted the request prepared at
`governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md` §2 (draft D-A).
**Authority:** the owner's ruling of 2026-09-10 ("freeze the EXISTING convention; do not
invent a new grid, do not move stations"); **D-1** and its addendum (the convention
itself, already frozen); Vision §6.1A/§6.1B (the rule *"must be frozen and recorded, not
guessed"*); `team.md` § Code Style **Q11 = B** (freeze the current inline constants as a
D-number BEFORE the migration moves them, so the migration cannot silently change a
scientific value).

**Decision.** The coordinate-to-cell rule is the convention already implemented and in
use, transcribed here unchanged:

> 1° × 1° cell identified by its **lower-left (floor) corner**, half-open in both axes:
> `cell = [floor(lat), floor(lat)+1) × [floor(lon), floor(lon)+1)`

Its governed identifier is **`floor-half-open-d1`** — the identifier already declared in
`src/data/registry.py` (`CELL_RULE_ID`), which `assert_registry_resolved` requires
`configs/data.yaml: cell_rule` to equal and refuses any other value for. The convention's
source text is `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 4 (*"DEFAULT
convention adopted here"*), reproduced above without alteration; it is the same rule
D-1's addendum states as `cell = (floor(lat), floor(lon))` tested half-open on both axes.
`configs/data.yaml: cell_rule` now carries that identifier.

**What this decision does NOT do.** It does **not move a station**, does **not change the
grid resolution**, and does **not resolve `stations`**, which stays `TBD — freeze gate`
with its coordinates still PROVISIONAL pending IGS site-log validation. It does **not
discharge the notebook's own standing caveat**: the convention must still be **CONFIRMED
against the real bin edges Madrigal returns** before it is relied on scientifically —
that confirmation **remains owed** and is a recorded limitation of this freeze, not
something satisfied by it.

**Governance condition.** TE §18.2 classes the coordinate-to-cell rule as a **Student +
Supervisor** forbidden choice. **The supervisor countersignature is REQUIRED and has NOT
YET BEEN GIVEN** for this decision: no signed document, email or minute from
Dr. Reza Saraf Shirazi exists for it and none is represented as existing. Readers should
also consult the **D-1 addendum**, which records that D-1's own §18.2 condition was
closed under the recorded student/supervisor authority equivalence; this decision does
not extend that closure to itself and records the countersignature as outstanding.

**Consequence.** One limb of `assert_registry_resolved`'s refusal is closed. The registry
still refuses overall while `stations` and `igrf_version` are unresolved — this decision
closes a limb, not the refusal.

---

## D-34 — Practical relevance is reported descriptively; no threshold is set (reading)

**Decision date:** 2026-09-10. **Decided by:** the project decision owner, adopting as
drafted the request prepared at
`governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md` §3 (draft D-B).
**Authority:** the owner's ruling of 2026-09-10 ("no invented numeric"); **Vision §5.4**;
**PC-09** (`constraint-register.md`, `binding: hard`).

**Decision.** **No practical-relevance threshold is set, and no numeric value is written
anywhere.** What is frozen is the PROTOCOL, transcribed from Vision §5.4 and PC-09
without addition:

1. Ten percent RMSE reduction is a **named reference magnitude, not a pass/fail rule**
   and not a hypothesis.
2. **Practical relevance is reported descriptively unless the supervisor explicitly
   approves a threshold** (PC-09, `binding: hard`).
3. An approved reference or threshold **shall not correspond to an RMSE difference
   smaller than the target uncertainty budget** of Vision §6.9; if it does, practical
   relevance is reported descriptively only.
4. **No threshold may be introduced, changed, or reinterpreted after December is opened**
   (Vision §5.4; PC-09; `project.md` § Forbidden).
5. Significance and usefulness stay distinct: the confirmatory claim is the paired loss
   differential with its 95% interval (Vision §2.3/§5.5); a practical-relevance statement
   is descriptive commentary beside it, **never a second test**.

**Consequence.** `configs/experiment.yaml: practical_relevance_threshold` **keeps the
`TBD — freeze gate` sentinel**, and that sentinel is now the correct, *decided* state: it
records **"no threshold approved"**, not "not yet considered". Any future numeric requires
a **separate governance act with explicit supervisor approval** and its own D-number, and
is **barred once December is opened**. **No supervisor signature artifact exists for this
decision and none is claimed** — none is required, because no threshold is approved by it.

---

## D-35 — The permitted-producer policy and the eleven contract-fixed rows (freeze)

**Decision date:** 2026-09-10. **Decided by:** the project decision owner, adopting as
drafted the request prepared at
`governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md` §4 (draft D-C).
**Authority:** the owner's ruling of 2026-09-10; Vision §6 (the feature contract);
TE §6.2 (the dictionary, its lag and normalization columns, and the REMOVED `ssn` row);
**D-10.3** (availability lags); TC-09 (carry-forward ≤ 3 h then exclude); NFR-IRI-01 and
TE §12 (IRI denial); NFR-LEAK-01 (train-only fitting); FR-P1-04-10 (longitude only via
`lst_*`); SD-F-01 (Q1 = A, the fail-closed producer list).

**Decision, limb 1 — the leakage-safe policy.** A feature may be produced for a dictionary
row only if it is **available at the forecast origin**; carries **no future target TEC**;
requires **no locked-December access**; **respects its declared safe lag**; introduces
**no future information through preprocessing** (train-only fitting where any fitting
occurs); is **deterministic where determinism is required**; and is **compatible with the
1-hour-ahead forecast**. Feature philosophy: local historical VTEC, temporal features and
legitimately-available solar/geomagnetic drivers — **no IRI-derived anything, and no
future leakage**. Every clause is existing binding project text; this decision
**transcribes, it does not create**.

**Decision, limb 2 — the eleven rows whose producing artifact the implemented contract
itself fixes**, now carried in `configs/features.yaml`:

| Dictionary row(s) | Permitted producer | Why this producer is fixed, not chosen |
|---|---|---|
| `vtec_lag`, `vtec_seq_24`, `target_support` | `phase1_hourly_target` | The released D-17 Phase 1 hourly target, read by manifest by `05`/`06`/`07`; lagged/sequence VTEC is target history strictly BEFORE the forecast origin. `target_support` travels on the same release |
| `utc_hour_sin`, `utc_hour_cos`, `doy_sin`, `doy_cos` | `record_timestamp` | `TIMESTAMP_PRODUCER` in `src/features/build.py` — a pure function of the record's own `interval_start_utc`; no external artifact, no future information |
| `lst_sin`, `lst_cos`, `station_onehot`, `station_lat` | `station_registry` | `STATION_REGISTRY_PRODUCER`, gated by `assert_registry_resolved`; local solar time is the ONLY route longitude may take into the input space (FR-P1-04-10) |

**Decision, limb 3 — the seven driver-class rows REMAIN DEFERRED.** `kp_safe`, `ap_safe`,
`hp60_safe`, `ap60_safe`, `f107_safe`, `f107_81_trailing` and `dst` are **not assigned a
producer and not rejected**: none violates the policy. They are deferred because a
permitted-producer entry is a producing-**artifact** identity and the driver artifacts do
not exist yet — D-10.1 fixes the **providers** (Kp/ap3 → GFZ Potsdam; Dst → Kyoto WDC;
F10.7 → Canada's Solar Radio Monitoring Program, **observed** flux) and TE §6.2 fixes
Hp60/ap60 as *"GFZ or approved source"*, a provider and not an artifact id. **No artifact
identity is invented here.** Their entries are owed when the driver release exists, and
until then `load_permitted_producers` **fails closed**, refusing any run that requests one
of these rows and naming exactly those rows, with no feature matrix produced.

**What this decision does NOT do.** **`dst` stays diagnostic/hindcast-only and is never a
confirmatory ML feature** (TC-11; `DIAGNOSTIC_ONLY_SERIES`) — its presence in the
dictionary is not admission to the model input space. **R-78 is unchanged**: no support
field is admitted by this decision; its approval-ID and pre-freeze-timestamp conditions
still govern `target_support`. No lag, threshold, window or normalization value is set.
**No supervisor signature artifact exists and none is claimed.**

---

## D-36 — The TensorFlow pin is `tensorflow==2.21.0` (freeze)

**Decision date:** 2026-09-10. **Decided by:** the project decision owner, adopting as
drafted the request prepared at
`governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md` §5 (draft D-D); the
owner selected the version. **Authority:** TE §8.1 (the pinned environment); TE §8.3
(TensorFlow/Keras is the ONE neural stack; PyTorch prohibited); TC-01 (CPU is a complete
execution path — the pin is the CPU wheel, never a GPU build); TS-M-01 (M-06's pin guard).

**Decision.** `requirements.txt` carries **`tensorflow==2.21.0`**. `src/models/lstm.py`
was implemented against the tf.keras **2.21.0 candidate API**, so the frozen pin and the
implemented serialization/determinism contract agree by construction. This supersedes the
earlier `TBD — freeze gate` state recorded under code-generation Q3 = A.

**Pinning is not verification, and this decision does not claim it is.** The
installability and API-compatibility check **has NEVER BEEN EXECUTED**: PyPI is
unreachable from the implementation environment (verified again 2026-09-10), so
`pip install tensorflow==2.21.0` has never run here and **no TensorFlow import has ever
succeeded**. **TE §8.1's own condition — that the pin be verified on BOTH governed
platforms (Kaggle and local) — is UNMET, and the Kaggle compatibility check is OWED.**
Freezing the pin makes M-06's guard pass; **it does not make the environment exist**, no
M-06 fit has ever run, and TA-26 stays `Pending`.

**Consequence.** `require_frozen_pin` now reads a frozen pin from the governed file; its
refusal of an **absent or commented-out** pin is unchanged and remains proved by negative
controls on synthetic requirements files. **No supervisor signature artifact exists and
none is claimed.**

---

## D-37 — D-27 is affirmed; BLK-08's mechanism limb resolves in D-27's identity form (reaffirmation)

**Decision date:** 2026-09-10. **Decided by:** the project decision owner, adopting as
drafted the request prepared at
`governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md` §6 (draft D-E);
the owner chose **Choice B, affirm the withholding**. **Authority:** **D-27**
(2026-08-24); TE §7.2 (`ABL-DIFF`'s inverse obligation); TE §12's import boundary;
`governance/RULING_2026-09-05_nfr-design_governance_dispositions.md` (the reopening
protocol, **not invoked**).

**This is a REAFFIRMATION, not a supersession.** **D-27 stands, unreopened and
unamended**; nothing here replaces, narrows or duplicates it.

**Decision.** D-27's withholding of a general inverse route is **affirmed permanently** as
the project's mechanism. BLK-08's mechanism limb resolves as follows:

1. **The refusal IS the mechanism.** R-139 control 25 — a `toleranced` ledger entry
   declaring TECU units for an output whose producing path declares no `inverse_route` is
   **not freezable** — stays exactly as implemented, **at full strength**.
2. **R-103's joint contract is adopted in D-27's identity form.** The primary path's
   output is already raw TECU (D-27: *"Primary remains, Raw TECU"*), so its citable
   `inverse_route` is the **identity route**, cited as
   **`identity (D-27: primary target untransformed)`**.
3. **`ABL-DIFF` keeps the only real inverse**, scoped to its own ablation scoring, with
   error propagation recorded (TE §7.2).

**What this decision does NOT do.** It creates **no generic inverse-transform route**, adds
no `inverse`/`apply` to any transform, and authorises **no import-boundary change**: no
`src/evaluation` → `src/features` route is created and TE §12's allowlist is untouched.

**Consequence.** **BLK-08's mechanism limb is CLOSED** by this decision. **BLK-02 remains
OPEN** and is untouched by it. **No supervisor signature artifact exists and none is
claimed.**

---

## D-38 — The split configuration is transcribed into the live configs (transcription)

**Decision date:** 2026-09-10. **Authorized by:** **Kimia Rezaei (project owner / student)
and Dr. Reza Saraf Shirazi (supervisor)**, jointly, in the recorded authorization of
2026-09-10 ("the fields below are now formally authorized for transcription … copy it
verbatim from the reference"), and by the owner's subsequent approval of the proposed
`partitions` block on the same date. **This is the first decision in this register whose
authorization names the supervisor as an authorizing party.** Recorded honestly: the
authorization is a **joint instruction of record**, not a separately signed artifact — no
countersigned document file exists, and none is claimed.
**Authority for the VALUES:** TE §7.1's split-configuration table; **D-8** (calendar
boundary; the expanding-window origin); **R-80** Recommendation 25 (`DEC.train_end ==
REFIT.train_end`); **FR-P1-04-14** (the final refit is scored nowhere); ADR-11 M5.

**Decision.** The split configuration is transcribed into the two fields the pipeline
actually reads. **No scientific value is chosen here**; every value is a copy of an
already-frozen one.

1. **`configs/data.yaml: partitions`** — the six partitions of R-80's closed space:

   | id | kind | train_start | train_end | validation_month |
   |---|---|---|---|---|
   | F1 | fold | 2022-01-01 | 2022-03-31 | 2022-04-01 |
   | F2 | fold | 2022-01-01 | 2022-06-30 | 2022-07-01 |
   | F3 | fold | 2022-01-01 | 2022-09-30 | 2022-10-01 |
   | F4 | fold | 2022-01-01 | 2022-10-31 | 2022-11-01 |
   | REFIT | refit | 2022-01-01 | 2022-11-30 | *(null — scored nowhere)* |
   | DEC | locked | 2022-01-01 | 2022-11-30 | 2022-12-01 |

2. **`configs/experiment.yaml: embargo_hours` = `24`** — TE §7.1's Embargo column, which
   reads **"24 hours"** on every fold row. Its single home is this field;
   `build_partitions` applies it to all six partitions.

**Provenance distinction, preserved at the owner's explicit instruction.** F1–F4 and REFIT
are **specified directly** by TE §7.1. **DEC's training bounds are NOT**: TE §7.1 shows
"—" for the locked row's training interval, so `DEC.train_start` and `DEC.train_end` are
**determined** by constraints the validator already enforces — `train_start == study_start`
(the expanding window from one origin, D-8) and `DEC.train_end == REFIT.train_end` (R-80) —
which leave exactly one admissible value for each. Determined, not chosen; and derived from
R-80 and D-8 rather than from TE §7.1.

**What this decision does NOT do.** It does **not** resolve `configs/experiment.yaml:
folds`, which has **no reader anywhere** in `src/` or `scripts/` and stays
`TBD — freeze gate` **deliberately**, so that no second source of truth for the split
calendar exists. It sets no other value: `stations`, `models.selected`,
`tuning.declared_baseline_per_track`, `feature_set_id`, the top-level `normalization`
placeholder, `availability_lags.window.recomputation_tolerance`, `december_day_range`,
`tuning.selection` and the ablation `run_id`/`registered_at` fields all keep their
sentinels. It alters **no validator and no split rule**, and discharges **no gate**: BLK-02
stays OPEN, the two Q-31 freeze acts remain the owner's, and WS-20/TA-09/TA-17/TA-21 stay
`Pending`.

**Verification recorded with the decision.** The block was extracted from the file, printed,
and fed to the project's own unmodified `build_partitions`, which accepted all six —
exercising kind-matches-id, the expanding-window origin, `validation_month == train_end + 1
day` for folds, REFIT-null-only, the `DEC`/`REFIT` `train_end` equality and the
one-evaluation-role-per-month coverage check. A control re-run with an unresolved
`embargo_hours` still refused, so no guard was weakened. `pyyaml` is uninstallable in the
implementation environment (PyPI egress blocked, verified 2026-09-10), so that check used a
printed stdlib extraction rather than the production loader; a full `load_configs` run is
owed in a governed environment.

---

## D-39 — Kp/ap 2022 driver product: GFZ archived settled nowcast selected; definitive retained as audit comparator (freeze, with binding limitation)

**Decision date:** 2026-09-18. **Authorized by:** **Kimia Rezaei (project owner / student)**,
in-session, as a **student decision** — recorded verbatim in substance from the owner's
approval ("I approve D-39 and D-40 with the following binding qualifications. This
authorizes recording my student decisions, not passing G-04 or releasing producer
artifacts."). **No supervisor approval exists or is claimed for this entry.** Whether a
separate supervisor countersignature is required before the series enters a governed
feature release is **left open** (TE §6.2 `kp_safe`/`ap_safe` row; G-04). Appended by the
implementing agent on the owner's explicit instruction of 2026-09-18; the drafted text is
`governance/CHANGE_RECORD_2026-09-18_gfz_release_grade_rulings.md` §4, adopted here with
the owner's qualifications applied.
**Authority:** TE §6.2 (`kp_safe`/`ap_safe`: "observation + publication timestamps",
safe lag ≥ 3 h); TE §10 driver table ("never backfill from future final values");
`project.md` § Forbidden; **D-10.1** (provider GFZ Potsdam); `acquisition` R-40 and
`external-products` R-63 as amended 2026-09-18.
**Evidence:** `evidence/audit_gfz_2026-09-18/` (`retrieval_record.json`,
`gfz-comparison-report.json`, `GFZ-AUDIT.md`, `sha256_manifest.json`), produced by
`scripts/audit_gfz_drivers.py`; change records `CR-2026-09-18-GFZ-DRIVER-PAIR-AUDIT` and
`CR-2026-09-18-GFZ-RELEASE-GRADE-RULINGS`.

**Decision.**

1. The **selected historical Kp/ap product** for the 2022 driver series consumed by
   `kp_safe` and `ap_safe` is GFZ's **archived settled nowcast**, `Kp_now2022.wdc`, under
   DOI 10.5880/Kp.0001 (folder `Kp_nowcast`), SHA-256
   `7929d16aa1a14d35dff6759c02367746438b09dd084fdc731a4052af5a7475a4`, 23,581 bytes,
   provider Last-Modified 2023-01-24 06:57:38 GMT, retrieved 2026-09-18. Its
   `release_status` is recorded as **`nowcast (archived, settled)`**.
2. The **definitive** product `Kp_def2022.wdc` (same DOI, folder `Kp_definitive`, SHA-256
   `c1d9030254e5b1e9581065166ab501b7aad9f2e07756551aefa8b18302c2b829`, 23,581 bytes) is
   **retained only as the audit comparator** for R-63 control 5. It is **not** substituted
   for forecast-time features.
3. **Binding limitation.** The archived nowcast is the provider's **settled, final-stage
   nowcast**: it **includes post-issue revisions** made during the provider's approximately
   1–2-day revision period and **does not reconstruct the first-issued values**. It is
   **NOT labelled, and must never be described, as proven available at every 2022
   forecast origin.** No first-issue reconstruction is claimed.
4. **Obligation before producer release.** The applicable feature-availability rule for
   this series must be **established from evidence** (provider release documentation or
   equivalent), **or** the unresolved limitation and its implications for forecast claims
   must be **explicitly documented** in the availability matrix and every dependent claim.
   **No publication lag may be invented and no configuration may be changed silently**:
   `configs/features.yaml: availability_lags` keeps `TBD — freeze gate` until that rule is
   established and transcribed under its own record.

**Measured for the record (a product-version difference, not a model error and not
proof of leakage):** 1,046 of 2,920 three-hourly 2022 epochs differ between the nowcast
and definitive products (max |ΔKp| 0.667, max |Δap| 17); coverage of both files is
complete (2,920 epochs, no gaps, no missing symbols).

**What this decision does NOT do.** It passes no gate (G-04 not passed); releases no
producer artifact (`gfz_kp_ap_3h_2022_v1` does not exist); writes no
`permitted_producers` entry; sets no `safe_lag_hours`; and creates no supervisor
approval.

---

## D-40 — Hp60/ap60 2022 driver product: Hpo.0002 V2.0 selected; Hpo.0003 V3.0 retained as later-recomputed comparator; substitute control for R-63 control 5 (freeze, with binding limitation)

**Decision date:** 2026-09-18. **Authorized by:** **Kimia Rezaei (project owner / student)**,
in-session, as a **student decision** (same approval as D-39). **No supervisor approval
exists or is claimed for this entry.** Whether a separate supervisor countersignature is
required before the series enters a governed feature release is **left open** (TE §6.2
`hp60_safe`/`ap60_safe` row: "GFZ or approved"; G-04). Appended by the implementing agent
on the owner's explicit instruction of 2026-09-18; drafted text at
`CR-2026-09-18-GFZ-RELEASE-GRADE-RULINGS` §4, adopted here with the owner's
qualifications applied.
**Authority:** TE §6.2 (`hp60_safe`/`ap60_safe`, safe lag ≥ 1 h); `project.md`
§ Forbidden; `acquisition` R-40 and `external-products` R-63 as amended 2026-09-18; GFZ
`format_description_doi_10.5880.Hpo.0003.txt` and `version_history_doi_10.5880.Hpo.0003.txt`.
**Evidence:** as for D-39.

**Decision.**

1. The **selected historical Hp60/ap60 version** for the 2022 driver series consumed by
   `hp60_safe` and `ap60_safe` is `Hp60ap60doi_2022.txt` under **DOI 10.5880/Hpo.0002
   (V2.0)** — the DOI in force from 2022-03-26 to 2024-06-17 — SHA-256
   `0ad71bf0eab1412852dd57ade1f7e2fdf5ff18f1cf9d20ebab8babc1fe471ad6`, 527,283 bytes,
   provider Last-Modified 2023-01-24 06:57:43 GMT, retrieved 2026-09-18 (held as
   `hp60ap60doi_2022_v2.txt`). Its `release_status` is recorded as **`contemporaneous V2.0`**.
2. The same filename under **DOI 10.5880/Hpo.0003 (V3.0)** — the 2024 algorithm
   recomputation — SHA-256
   `a689ddef5590bf9cb6cc32cf72817921c93bf7e40d658b9181e2b5a3f665d461`, 527,342 bytes,
   provider Last-Modified 2025-04-03 09:28:21 GMT (held as `hp60ap60doi_2022_v3.txt`), is
   retained **only as the later-recomputed comparator**.
3. **Substitute control, accepted for Hp60/ap60 only.** GFZ publishes no definitive
   Hp60/ap60 and no archived Hp60 nowcast (Hpo is a single near-real-time-algorithm
   product; `D` "Currently always 0, reserved"), so the literal R-63 control 5 comparison is
   impossible for this series. The comparison of the two held files is accepted as the
   **documented substitute** for R-63 control 5, under exactly this label:
   **"Contemporaneous V2.0 versus later algorithm-recomputed V3.0."**
4. **Binding limitation.** This is **not** an NRT-versus-definitive comparison. It
   demonstrates sensitivity to later algorithmic recomputation and **does not establish
   first-issue availability, and does not establish absence of information leakage**. The
   availability-rule obligation stated in D-39 item 4 applies to this series equally.

**Measured for the record (a product-version difference, not a model error and not
proof of leakage):** 1,790 of 8,760 hourly 2022 epochs differ between V2.0 and V3.0
(max |ΔHp60| 0.667, max |Δap60| 31); coverage of both files is complete.

**What this decision does NOT do.** Passes no gate; releases no producer artifact
(`gfz_hp60_ap60_1h_2022_v1` does not exist); writes no `permitted_producers` entry; sets
no `safe_lag_hours`; creates no supervisor approval; decides nothing for Kp/ap (D-39) or
F10.7 (D-21/D-22/D-23/D-25).

---

## D-41 — Q4/Q5 disposition: Hp60/ap60 provider is GFZ Potsdam; the three driver producer-artifact identities and their source/comparator roles (freeze of identities and roles only)

**Decision date:** 2026-09-18. **Authorized by:** **Kimia Rezaei (project owner / student)**,
in-session, as a **student decision** ("I approve the D-41 producer identities and
source/comparator roles … subject to the following checks before adoption"; checks 3 and
4 below were performed against the existing approved contracts and agreed, so the entry
is adopted). **No supervisor approval exists or is claimed for this entry.** Appended by
the implementing agent on the owner's explicit instruction of 2026-09-18 after confirming
the identifier `D-41` was unused; drafted text at
`governance/CHANGE_RECORD_2026-09-18_gfz_release_grade_rulings.md` §4b.
**Authority:** TE §6.2 (`hp60_safe`/`ap60_safe`: "GFZ or approved source"; `f107_safe`,
`f107_81_trailing` rows); **D-10.1** (driver sources); **D-35** limb 3 (a
`permitted_producers` entry is a producing-ARTIFACT identity, owed only when the artifact
exists); **D-39**, **D-40**; **D-21/D-22/D-23/D-25** (F10.7);
`CR-2026-09-16-D25-AVAILABILITY-RULE` (Route 1 contract).

**Decision.**

**Q4 — provider.** The Hp60/ap60 provider is **GFZ Potsdam** (GFZ Helmholtz Centre for
Geosciences, Geomagnetic Observatory Niemegk), narrowing TE §6.2's "GFZ or approved
source" to its named default; no alternative source is approved. Kp/ap3 → GFZ Potsdam,
Dst → Kyoto WDC and F10.7 → NRCan SRMP observed flux are unchanged from D-10.1.

**Q5 — exactly three driver producer artifacts**, with these identities, roles and
sources. Every hash in the "Source SHA-256" column is an **existing, measured** SHA-256 of
a held input file. **No output hash exists**: the "Output" column is empty by decision and
is filled only by `src/data/release.py:write_release` when each artifact is actually
released under TE §13.3, in its own owner-approved step.

| Producer artifact id | Serves (§6.2 rows) | Source product (selected version) | Source SHA-256 (existing, measured) | Output SHA-256 / `dataset_version` |
|---|---|---|---|---|
| `gfz_kp_ap_3h_2022_v1` | `kp_safe`, `ap_safe` | `Kp_now2022.wdc`, DOI 10.5880/Kp.0001, folder `Kp_nowcast` — the D-39 selected settled-nowcast product; 3-hourly, 2,920 epochs; 23,581 bytes | `7929d16aa1a14d35dff6759c02367746438b09dd084fdc731a4052af5a7475a4` | *(unset — assigned at release)* |
| *(audit comparator, NOT a producer input)* | — | `Kp_def2022.wdc`, same DOI, folder `Kp_definitive`; 23,581 bytes | `c1d9030254e5b1e9581065166ab501b7aad9f2e07756551aefa8b18302c2b829` | — |
| `gfz_hp60_ap60_1h_2022_v1` | `hp60_safe`, `ap60_safe` | `Hp60ap60doi_2022.txt`, DOI 10.5880/Hpo.0002 (V2.0), folder `Hpo60` — the D-40 selected version; hourly, 8,760 epochs; 527,283 bytes; held as `hp60ap60doi_2022_v2.txt` | `0ad71bf0eab1412852dd57ade1f7e2fdf5ff18f1cf9d20ebab8babc1fe471ad6` | *(unset — assigned at release)* |
| *(recomputed comparator, NOT a producer input)* | — | same filename, DOI 10.5880/Hpo.0003 (V3.0); 527,342 bytes; held as `hp60ap60doi_2022_v3.txt` | `a689ddef5590bf9cb6cc32cf72817921c93bf7e40d658b9181e2b5a3f665d461` | — |
| `srmp_f107_observed_daily_2022_v1` | `f107_safe`; **`f107_81_trailing` is DERIVED from this daily producer and is not a separate raw-source artifact** | NRCan SRMP `fluxtable.txt` (observed flux, not 1-AU-adjusted), `evidence/audit_ec1_2026-08-15/nrcan_f107/`, retrieved 2026-08-15, 2,170,350 bytes, 23,848 records / 1,101 in 2022 / 365 days; daily value per D-21, duplicate-UT per D-22, high-spread days per D-23, availability per D-25 | `4b7fbfde3b9d0140ef43e7487f5986fe18f93182dac5e1ee37a93fb6ebd690b9` | *(unset — assigned at release)* |

**Check 3 — `f107_81_trailing` as a derived feature, verified against the approved
definition (agrees; nothing new introduced).** TE §6.2 row `f107_81_trailing`:
"**Trailing** 81-day F10.7 mean", "Approved source" (the same source as `f107_safe`),
"Trailing window ending at the safe-lagged day", "Trailing mean only", "Carry-forward
≤ 3 h, then exclude", "**The centered 81-day mean is prohibited — it uses future
days.**" D-25: "The trailing 81-day mean is computed over daily medians ending at the
safe-lagged day, never centered." `project.md` § Forbidden and § Mandated state the same.
Implementation of record: `src/external/spaceweather.py:trailing_mean` — window
`[end_day − (window_days − 1), end_day]` by construction, raising `IntegrityError` when
any window day is missing (TC-20: never filled); `src/features/availability.py` limb 2
`assert_trailing_not_centered` (kind must be `trailing`) and limb 3
`assert_anchor_recomputed` (the recorded anchor IS the safe-lagged day and the mean is
recomputed from it). Constituent observations obey the applicable availability rule: the
window ends at the safe-lagged day D−1, whose daily median is available at 00:00 UTC on
D (D-25) — at or before every origin on day D. **Preserved, not decided here:** the window
length (81) and `recomputation_tolerance` stay configuration under `TBD — freeze gate`;
the carry-forward composition on a 24-hour cadence stays the open G-04 freeze item
(`external-products` R-57a); no missing-data rule is added. **Transcription constraint
recorded, no value chosen:** under the Route 1 contract a rule-bearing feature may not
carry a trailing window, so `f107_81_trailing` keeps the scalar-lag-plus-window shape and
`f107_safe` carries the rule; at transcription the scalar chosen for `f107_81_trailing`
must place the anchor at D−1 for every origin hour on day D, consistent with D-25.

**Check 4 — the D-25 Route 1 `availability_rule` contract, cited exactly for the F10.7
manifest (agrees; scope bounded).** `src/features/availability.py`:
`AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC = "previous_day_median_midnight_utc"`
(the sole member of the closed set `AVAILABILITY_RULE_KINDS`), applied by
`_rule_available_at` as midnight UTC of the observation day plus one day and combined
with the observation/publication instant by `max` in `build_availability_matrix`;
authority `CR-2026-09-16-D25-AVAILABILITY-RULE` §2 items 1–8, transcribing **D-25**
(`availability_ts(median(D-1)) = 00:00 UTC on D`). The F10.7 producer's manifest cites
that identifier and D-25. **This contract resolves F10.7 only**: D-25 supplements D-21
and names no other series; Kp/ap and Hp60/ap60 remain on scalar `safe_lag_hours` with
observation and publication timestamps (TE §6.2, D-10.3: ≥ 3 h, ≥ 1 h), and the D-39
item-4 / D-40 availability obligation for those two series is **not** discharged by it.

**What this decision does NOT do.** It approves **identities and roles only**. It does
**not** approve temporal availability for any series; does **not** certify any `*_safe`
feature as leakage-free; does **not** authorize producer release; does **not** pass G-04;
sets no `safe_lag_hours`, window value or missing rule; writes no `permitted_producers`
entry (owed only when each artifact exists, D-35 limb 3); changes no configuration.

**Countersignature — governing provision, stated without adding a requirement.** TE §18.2
lists "Any feature, its safe lag, or its missing rule — Student + Supervisor (Q-16,
Q-17)"; it lists **no** row for a driver source product, its version or a producer-artifact
identity, and D-10.1 (driver sources) was taken sole-signed on that basis. D-41 therefore
**requires no supervisor countersignature under §18.2**. The availability obligations
D-39 item 4 / D-40 carry ARE §18.2 Q-16 items and G-04's evidence ("Supervisor for
ambiguous inputs", Vision §13.1), so **supervisor involvement is required there**, and the
settled-nowcast limitation may make Kp/ap an "ambiguous input" for G-04 — recorded as
open, not resolved.

---

## D-42 — GFZ driver availability floors accepted as project assumptions for a retrospective study, with a binding scientific limitation (student acceptance; supervisor countersignature OPEN)

**Decision date:** 2026-09-19. **Authorized by:** **Kimia Rezaei (project owner / student)**,
in-session, as a **qualified student acceptance** (item A1 of the 2026-09-19 scoped
authorization: "I accept the proposed GFZ availability assumptions for a retrospective
study … These are project assumptions, not demonstrated publication or revision-completion
bounds … Record my student acceptance through the existing decision process. Do not
fabricate a supervisor countersignature or mark any required approval complete."). **No
supervisor approval exists or is claimed.** TE §18.2 lists "Any feature, its safe lag, or
its missing rule — Student + Supervisor (Q-16, Q-17)", so the supervisor's countersignature
of this acceptance is **REQUIRED and OPEN**; until it is given, this entry records the
student's position and binds the project's wording, not the G-04 outcome. Appended by the
implementing agent on the owner's explicit instruction.
**Authority:** TE §6.2 rows 307–308 (`kp_safe`/`ap_safe` ≥ 3 h; `hp60_safe`/`ap60_safe`
≥ 1 h); Vision D-116 (Q-16, Approved); D-10.3; **D-39**, **D-40**, **D-41**;
`acquisition` R-40 and `external-products` R-63 as amended 2026-09-18; the D-25/EV-12
evidence pattern (`CR-2026-08-22-EV-12`).
**Evidence:** `evidence/audit_gfz_2026-09-18/` (provider files, hashes, comparison
report); GFZ `kp_index_data_description_20210311.pdf` §4 (nowcast "can change for some
time (typically a day or two)" and is archived at its final stage);
`format_description_doi_10.5880.Hpo.0003.txt` and `version_history_doi_10.5880.Hpo.0003.txt`
(single near-real-time-algorithm grade, no publication timestamp, V3.0 recomputation);
`CR-2026-09-18-GATE-PREP` §1.1 (the six-entry availability table);
`CR-2026-09-19-GATE-PREP-2` §A1.

**Decision.**

1. For the 2022 driver series consumed by `kp_safe` and `ap_safe` (D-39's archived
   settled-nowcast product) the project's **existing approved 3-hour floor** is accepted
   as the availability assumption; for `hp60_safe` and `ap60_safe` (D-40's Hpo.0002 V2.0
   product) the **existing approved 1-hour floor** is accepted. Both are the values TE
   §6.2 and D-116 already froze as "≥"; nothing numerical is chosen here.
2. **These are project assumptions for a retrospective study**, not demonstrated
   publication or revision-completion bounds. The provider archives no per-value
   publication timestamp for either series; "typically a day or two" is a provider
   characterisation of nowcast revision, not a maximum; and a version label (Hpo.0002)
   proves which algorithm produced the held values, not when a 2022 origin could have
   seen them. **The floors do not make settled archive values historically available at
   those lags.**
3. **Binding scientific limitation, propagated to every method description and result
   claim that uses these series:** *results using these archives do not establish exact
   operational replay or absence of revision-related look-ahead.* The statement is
   carried as an artifact field (`src/evaluation/metrics.py:
   DRIVER_AVAILABILITY_LIMITATION_STATEMENT`) and asserted on the limitations surface by
   the claims checklist (`src/evaluation/diagnostics.py`, row "D-42"; negative control
   `tests/test_regimes_and_reporting.py::test_d42_driver_availability_limitation_row_fails_when_absent`);
   it is recorded in `acquisition` R-40's and `external-products` R-63's amendment blocks,
   and it must accompany any lag cited for these series in the thesis.
4. **The evidence form for the availability record** is the D-25/EV-12 pattern: the
   approved floor recorded together with a per-series `publication_latency_statement`
   naming the absence of publication timestamps and the settled-nowcast / version-label
   limitation. **No configuration is transcribed by this decision**:
   `configs/features.yaml: availability_lags` stays `TBD — freeze gate` until all six
   entries can be written together under their own record, after the supervisor's
   countersignature and the R-57a composition freeze (A3).

**Reported supervisor approval, annotated 2026-09-19 (recording date; not an earlier date).** The project owner / student, Kimia Rezaei, stated in-session on 2026-09-19: "I confirm that my supervisor has approved the scientific decisions covered by the latest handoff, including D-42, D-43, D-45, and D-46." This is recorded here as **student-reported supervisor approval** — a report by the recorded decision owner that the approval occurred, not a supervisor-signed artifact, not a directly observed supervisor communication, and not an earlier approval date than today. No signature, communication, or date is invented beyond what was stated. **Prescribed evidence still outstanding**, per TE §18.2's Student + Supervisor bar and the project's own countersignature practice (`governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md`, `governance/COUNTERSIGNATURE_REQUEST_2026-08-21.md`): a supervisor-signed or otherwise directly-recorded countersignature artifact closing this item, exactly as items 1 and 2 of the 2026-08-16 letter were closed. Drafted and awaiting that signature: `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`. Until that artifact exists, this entry's status is **reported, not verified** — it does not, by itself, satisfy TE §18.2 and does not pass G-04. **Update, later the same day (2026-09-19).** The project owner / student stated: "supervisor has approved and countersigned." Recorded, as this register records every prior owner statement in this single-operator project (see e.g. the many "no supervisor signature artifact exists and none is claimed" entries above): as the recorded decision owner's own statement of the countersignature, not as a signature this session independently observed. `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`'s status line is updated to record the same statement. On that basis this entry's TE §18.2/§18.3 item is treated as closed; it still does not, by itself, pass G-04.

**What this decision does NOT do.** It does not pass G-04; does not certify any `*_safe`
feature as leakage-free; does not authorize a producer release or a `permitted_producers`
row; does not transcribe a lag; does not resolve the F10.7 trailing-row shape (A2, applied
the same day under `CR-2026-09-19-GATE-PREP-2` as an implementation of D-25, not as a new
decision), R-57a (A3) or the recomputation tolerance (A4); and does not create or imply a
supervisor approval.

---

## D-43 — Interval semantics of the GFZ lag floors: margins after interval COMPLETION (clarification; student decision; supervisor countersignature OPEN)

**Decision date:** 2026-09-19. **Authorized by:** **Kimia Rezaei (project owner /
student)**, in-session ("P-1 — adopt explicit interval semantics … I approve interpreting
the GFZ lag floors as margins after interval completion"). **This is a NEW clarification,
not something D-42 or TE §6.2 had already unambiguously specified**: Vision §7.3 defines
the observation timestamp as *"time represented by the value"*, which for an
interval-valued index names neither start nor end; D-10.3 fixes only that the value's
availability instant is *"the instant its value could actually have been known"*. Because
the reference instant of a safe lag is part of the lag's meaning, TE §18.2 ("Any feature,
its safe lag, or its missing rule — Student + Supervisor, Q-16/Q-17") applies: the
supervisor's countersignature is **REQUIRED and OPEN**; nothing here claims it. Appended
by the implementing agent on the owner's explicit instruction. **Authority:** D-10.3;
TE §6.2 rows 307–308 ("last **completed** 3-hour interval"); Vision §7.3/§7.5; D-42;
`CR-2026-09-19-SCI-REVIEW` §1; `CR-2026-09-19-SCI-DECISIONS` §1.

**Decision.**

1. For an interval-valued index the **observation interval** is the provider's own
   `[start, end)` in UT — Hpo rows are labelled by their start (`hh.h`, file header),
   WDC slots by position (`[3k, 3k+3)`); **both boundaries are preserved** in every
   derived row (`source_interval_start_utc`, `source_interval_end_utc`) and the
   provider's label is never overwritten or concealed by the reference instant.
2. The **reference instant** of the safe lag is the interval **END** (completion), the
   earliest instant the value could have existed. The availability matrix's
   `observation_timestamp` for such a series is that end.
3. The floors are therefore **margins after completion**: Kp/ap `available_at = end +
   3 h`; Hp60/ap60 `available_at = end + 1 h`. A value is eligible at a forecast origin
   *T* iff `available_at ≤ T`. Boundary cases (UT): Kp `[00,03)` is unavailable at 05:00
   and eligible at 06:00; Kp `[03,06)` is eligible from 09:00; Hp60 `[04,05)` is
   unavailable at 05:00 and eligible at 06:00.
4. **These margins remain assumptions for retrospective evaluation** (D-42 unchanged).
   They establish neither historical first-issue publication times nor
   revision-completion times, and they do not make the settled archive values
   historically available at those instants.

---

## D-44 — One authoritative lagged-selection owner per driver kind; the alignment contract for `*_safe` series (student decision; implementation)

**Decision date:** 2026-09-19. **Authorized by:** the project owner / student ("P-2 —
implement one authoritative availability-selection mechanism"). A mechanism decision
implementing D-43 and D-10.3; no lag, definition or provider changes. No supervisor
countersignature is required for the mechanism itself (no TE §18.2 row covers a
selection routine); the reference-instant semantics it applies are D-43's and carry
D-43's open countersignature. **Authority:** D-10.3, D-25, D-43; `features-and-splits`
R-76a (amended below); `external-products` R-58.

**Decision.**

1. **Owners.** Interval-valued indices (Kp/ap, Hp60/ap60): `src/external/spaceweather.py:
   select_lagged_series` is the ONLY place the safe lag is applied — at each origin *T*
   it selects the LATEST source interval with `end + lag ≤ T` and records the source
   interval (both boundaries), the assumed `available_at_utc` (= end + lag), the origin
   (`interval_start_utc`) and the selected value, each in its own field. The daily F10.7
   series: `resolve_f107_at_origin` (D-25 rule; D-46 composition) remains its only owner.
   `build_features` shifts nothing and refuses a series whose declared selection lag
   differs from the availability matrix's `safe_lag_hours` (no double lag, no shortfall).
2. **Alignment contract, amended explicitly (R-76a / R-58 limbs 1–2).** A raw
   own-interval series keeps the existing check (a value repeats only inside its own
   interval). A lagged `*_safe` series carries `attrs["selection"] = {rule:
   "latest_completed_interval_plus_lag", safe_lag_hours}` and is checked by
   `assert_lagged_selection`: every present value traces to the observation on its
   recorded source interval with equal value; `available_at` equals source end + lag and
   is at or before the origin; no later interval is also eligible; a present source value
   is never dropped. Forecast-origin timestamps are never relabelled as observations.
3. **Missing data compose on the epoch axis.** A selected interval whose value is missing
   yields a missing row that keeps the interval's identity; the ≤ 3 h carry-forward
   (R-57a, `apply_carry_forward`) then applies on the origin axis and is recorded; the
   selector never reaches back to an older interval.
4. **Matrix rows** for a lagged series are derived from the selection
   (`availability_rows_from_selection`): `observation_timestamp` = selected source END
   (D-43); `publication_timestamp` empty with the documented-absence statement.

**Reported supervisor approval, annotated 2026-09-19 (recording date; not an earlier date).** The project owner / student, Kimia Rezaei, stated in-session on 2026-09-19: "I confirm that my supervisor has approved the scientific decisions covered by the latest handoff, including D-42, D-43, D-45, and D-46." This is recorded here as **student-reported supervisor approval** — a report by the recorded decision owner that the approval occurred, not a supervisor-signed artifact, not a directly observed supervisor communication, and not an earlier approval date than today. No signature, communication, or date is invented beyond what was stated. **Prescribed evidence still outstanding**, per TE §18.2's Student + Supervisor bar and the project's own countersignature practice (`governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md`, `governance/COUNTERSIGNATURE_REQUEST_2026-08-21.md`): a supervisor-signed or otherwise directly-recorded countersignature artifact closing this item, exactly as items 1 and 2 of the 2026-08-16 letter were closed. Drafted and awaiting that signature: `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`. Until that artifact exists, this entry's status is **reported, not verified** — it does not, by itself, satisfy TE §18.2 and does not pass G-04. **Update, later the same day (2026-09-19).** The project owner / student stated: "supervisor has approved and countersigned." Recorded, as this register records every prior owner statement in this single-operator project (see e.g. the many "no supervisor signature artifact exists and none is claimed" entries above): as the recorded decision owner's own statement of the countersignature, not as a signature this session independently observed. `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`'s status line is updated to record the same statement. On that basis this entry's TE §18.2/§18.3 item is treated as closed; it still does not, by itself, pass G-04.

Verified by synthetic tests (`tests/test_external_drivers.py`,
`tests/test_feature_availability.py`) covering the D-43 boundaries, open and
not-yet-available intervals, stale selection, double lag and shortfall, source
traceability, dropped values, missing-value composition with carry-forward, and the
end-to-end `build_features` path with source values unchanged.

---

## D-45 — IRI-2016 benchmark: standard index inputs, disclosed as a retrospective climatological reference (student selection; supervisor approval REQUIRED and OPEN)

**Decision date:** 2026-09-19. **Selected by:** the project owner / student ("P-3 — adopt
standard IRI as a retrospective reference … preserving its documented index semantics").
**Approval status:** TE §18.3 makes *"the IRI role"* a supervisor sign-off item and Vision
§6.11 freezes the benchmark's driver inputs at a supervisor gate (G-03/G-05 rows of TE
§4); this entry records the student's selection and leaves **that supervisor approval
outstanding**; the dependent patch to `src/external/iri.py`'s report confirmations is
PREPARED (`governance/proposed/P-3_iri_report_confirmations.patch`) and NOT applied.
**Authority:** Vision §6.11, §7.2; TE §6.2 row `iri2016_t_plus_1_tecu`; D-114;
`external-products` R-59; `CR-2026-09-19-SCI-DECISIONS` §3 (the verified execution path).

**Decision.**

1. The benchmark is IRI-2016 via `iricore` (`version=16` passed explicitly — the
   package's default is IRI-2020), electron density integrated by `iricore.vtec` with
   `htop = 2000` km, run with IRI's **standard shipped index files** (`apf107.dat`,
   `ig_rz.dat`, pinned by SHA-256 at freeze; `iricore.update()` is never run after the
   pin) and **no `oarr` overrides** of F10.7 daily/81-day, Rz12 or IG12.
2. Its index inputs are therefore, as documented and verified from the shipped source and
   data: daily F10.7 = the **1-AU-adjusted 20 UT reading** of the **target day**
   (`apf107.dat`; IRI: *"F10.7 should be adjusted … not observed"*); F10.7_81 = the 81-day
   average **centered** on the target day; F10.7_365 centered; IG12/Rz12 = 12-month
   running means **centered** on the month (final values for 2022, the file being updated
   2024-06); 3-hourly ap of the **target day** up to the target hour (foF2 storm model,
   `jf(26)` default on). None of these is forecast-safe at the model's origin, and the
   centered/adjusted inputs are **not replaced** to resemble the ML pipeline.
3. **Purpose and disclosure.** IRI is a **retrospective climatological reference**, not
   an operational forecast and not a competitor with identical information
   availability. Every table or interpretation of the LSTM/baseline-vs-IRI comparison
   states: same target, `target_definition_id`, locations, units, target times and
   comparison-wide scoring rows; the model's inputs are lagged to the forecast origin
   under D-25/D-42/D-43, the reference's index inputs are retrospective, centered and
   same-day; outperforming the reference establishes no operational superiority; the
   2000 km ceiling/plasmasphere mismatch (Vision §6.11) is disclosed alongside.
**Reported supervisor approval, annotated 2026-09-19 (recording date; not an earlier date).** The project owner / student, Kimia Rezaei, stated in-session on 2026-09-19: "I confirm that my supervisor has approved the scientific decisions covered by the latest handoff, including D-42, D-43, D-45, and D-46." This is recorded here as **student-reported supervisor approval** — a report by the recorded decision owner that the approval occurred, not a supervisor-signed artifact, not a directly observed supervisor communication, and not an earlier approval date than today. No signature, communication, or date is invented beyond what was stated. Item 4 below ("What changes when approved") applies only once that artifact exists. **Prescribed evidence still outstanding**, per TE §18.2's Student + Supervisor bar and the project's own countersignature practice (`governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md`, `governance/COUNTERSIGNATURE_REQUEST_2026-08-21.md`): a supervisor-signed or otherwise directly-recorded countersignature artifact closing this item, exactly as items 1 and 2 of the 2026-08-16 letter were closed. Drafted and awaiting that signature: `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`. Until that artifact exists, this entry's status is **reported, not verified** — it does not, by itself, satisfy TE §18.2 and does not pass G-04. **Update, later the same day (2026-09-19).** The project owner / student stated: "supervisor has approved and countersigned." Recorded, as this register records every prior owner statement in this single-operator project (see e.g. the many "no supervisor signature artifact exists and none is claimed" entries above): as the recorded decision owner's own statement of the countersignature, not as a signature this session independently observed. `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`'s status line is updated to record the same statement. On that basis this entry's TE §18.2/§18.3 item is treated as closed; it still does not, by itself, pass G-04.

4. **What changes when approved:** `iri.py`'s R-59 limb-3 confirmations
   `no_future_centering_confirmed` / `available_at_target_time_confirmed` (both `True`
   required today) become a **recorded disclosure** — `index_inputs_retrospective_centered
   = True` with the list in item 2 — and Vision §6.11 / TE §6.2 wording "must not be
   future-centered" is amended to "future-centered index inputs recorded and disclosed";
   R-59 limb 4 records the IRI index rows in the availability matrix as
   `hindcast-only` grade rows, never as forecast-safe rows.

**Annotation, 2026-09-19 — verified runtime and bundled index files (owner-authorized; original text above preserved unchanged).**
*Authorization:* the project owner / student, Kimia Rezaei, instructed in-session on
2026-09-19: "I approve a dated D-45 annotation identifying the actual verified runtime and
its bundled index files, subject to the evidence checks below." This paragraph is that
annotation, recorded on the student's authority as decision owner. **No supervisor
signature is claimed for it**; D-45's supervisor status stays exactly as the paragraphs
above record it (student-reported approval and countersignature, 2026-09-19).
*Evidence:* `evidence/iri2016_kaggle_verification_2026-09-19/` (returned Kaggle bundle,
zip SHA-256 `3a0723a1ff70c213ed3cb7139cbfc02e4495d04888a00136c3e5a6c9afa6d508`, produced
by `kaggle/kaggle_iri2016_verification.ipynb` revision 2, SHA-256
`b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa`, preserved beside the
bundle) and `governance/CHANGE_RECORD_2026-09-19_scientific_decisions_p3.md` §3.6–3.7.

1. **Verified runtime (the executable benchmark configuration).** `iricore==1.8.0` from
   the PyPI wheel `iricore-1.8.0-cp310-cp310-manylinux_2_35_x86_64.whl`, SHA-256
   `f452b22316891d87ee766dba266de6a07e4e6008ab515ffed902ea8b5446a874` (PyPI upload
   2024-04-02; the newest release publishing a Linux wheel). Installed on Kaggle
   2026-09-19 with `pip install --no-deps --require-hashes` into a `virtualenv` at
   CPython **3.10.12** (`/usr/bin/python3.10` of the Kaggle image; kernel Python 3.12.13;
   `Linux-6.12.90+-x86_64-with-glibc2.35`, i.e. exactly the `manylinux_2_35` floor),
   together with `numpy==1.26.4` (`ffa75af20b44f8dba823498024771d5ac50620e6915abac414251bd971b4529f`),
   `fortranformat==2.0.3` (`88c8e7a3eac16c23420e8a1c4b21ddc7108f48e8dcbd2e0da6c8ecc48b051bb2`),
   `pymap3d==3.2.0` (`fccd44f2f6021a95adec19771c603b8dac104eab120d863c463d76b9bc298669`).
   `version=16` is passed **explicitly** on every call; the installed
   `iricore.config.DEFAULT_IRI_VERSION` is 20 (verified at runtime), so item 1's "passed
   explicitly" is necessary, not decorative.
2. **Bundled index files — the D-45 item 1 freeze pins, for release 1.8.0.**
   `apf107.dat` SHA-256 **`cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674`**
   (1,329,460 bytes; 24,172 contiguous daily rows 1958-01-01 → **2024-03-06**);
   `ig_rz.dat` SHA-256 **`fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486`**
   (9,815 bytes; header `3,7,2024` = update date **2024-03-07** in the file's
   month-day-year convention; declared range 1958-01 → 2024-10; 804 IG12 and 804 Rz12
   values, i.e. one edge value before and after the range, as `tcon` indexes them). Both
   hashes were measured on Kaggle before and after the smoke-test calls (unchanged) and
   re-measured locally on the same wheel bytes. `iricore.update()` is never run after
   this pin (item 1).
3. **Support for every 2022 target time, verified from the compiled sources in the wheel
   (`irifun.for`: `readapf107`, `read_ig_rz`, `tcon`, `APF`, `APF_ONLY`) and the installed
   files.** `apf107.dat` is read directly for rows 2021-12-30 → 2022-12-31 (`APF` takes ap
   back to UT−39 h, `APF_ONLY` the previous day's F10.7): all 367 rows present, none
   carrying a negative missing sentinel. The file's centered F10.7_81 / F10.7_365 columns
   need daily data 2021-11-22 → 2023-02-09 and 2021-07-03 → 2023-07-01 respectively: both
   windows lie inside the file, and every 2022 row's two columns recompute from the same
   file's daily column within 0.05 (F5.1 rounding), i.e. they are full-window values, not
   edge-truncated ones. `ig_rz.dat` is read for months 2021-12 → 2023-01 (day < 15 uses
   the previous month, day ≥ 15 the next): all 14 present and non-negative; the centered
   12-month window of the last of them ends 2023-07, before the file's 2024-03-07 update
   date. The file itself does not label values observed versus predicted, so
   "final" here means "computed from a window the file's update date covers"; the
   provider's grade is not asserted beyond that. **Executable-path facts not in the
   earlier inspection:** (a) the compiled library reads both files itself; the Python
   `read_iri_data.readapf107` is commented out in 1.8.0 (`# IRI_DATA = readapf107()`,
   "TODO: Fix data reading from Python") and carries a column bug (its 81-day slot is
   overwritten by the 365-day values) that would matter only if a future release
   activated it — a reason the pin is on this exact wheel; (b) `read_ig_rz` multiplies
   Rz12 by **0.7** for every month from 2014-01 when the header date is after 2016-09
   (new sunspot-number series), so the Rz12 IRI-2016 uses for 2022 is 0.7 × the file
   value (e.g. 2022-06: file 81.1, used 56.77); IG12 is used as stored.
4. **Reconciliation with the source inspection that item 2 cites — supersession.** Item 2
   and `CR-2026-09-19-SCI-DECISIONS` §3 read `apf107.dat` ending 2024-06-17 and
   `ig_rz.dat` "updated 6/2024" from the GitHub `master` snapshot (commit
   `92c6d8c727b0300d8bd61e7e8e91dd97514256a7`) and the PyPI 1.9.0 sdist (SHA-256
   `6f1503716f5f8ba3e48038a4cade9310d396ee2dce299ac841824a054b595e35`), whose index files
   are identical to each other (`apf107.dat` `4de3bfa2d3b488e61477cf7bfb9ec1d9ca891b265694752b20e7b320f9657e82`,
   `ig_rz.dat` `e688620c6ac25dec6cf31ebd4afe091a6a083c4e1d50f22c68d096474944e1a8`; both
   archives retained from the 2026-09-19 session and re-hashed). **For the executable
   benchmark configuration the installed wheel's evidence (items 1–3) supersedes that
   inspection**; the inspection's semantic findings (adjusted 20 UT daily F10.7,
   centered 81-/365-day means, centered IG12/Rz12, target-day ap, no `oarr` overrides)
   stand and were re-verified on the installed file (the four spot values 239.0, 144.5,
   257.0, 133.1 are unchanged). Value comparison, done separately from length/date
   differences: `apf107.dat` — 24,172 common dates, 176 differ, the earliest
   **2023-09-08**, none in 2021-07-02 → 2023-07-01; `ig_rz.dat` — 804 common values,
   15 months differ (2023-09 → 2024-11), none in 2021-12 → 2023-01. **Every index value
   IRI-2016 reads for any 2022 target time is therefore identical in the two copies**;
   the historical description was of newer files whose extra rows revise only a
   post-2023-09 tail the benchmark never reads. No performance effect is claimed or
   measurable from this; none is needed, since the inputs are equal.
5. **Smoke test and its limits.** One `iricore.vtec(2024-01-06T12:00Z, 40.286, 44.086,
   hbot=90, htop=2000, hstep=0.5, version=16)` call at the D-1 ARUC coordinate returned
   `37.373754526924806` TECU, finite, bit-identical on the repeated call. It establishes
   installation and runtime only: a single point at a synthetic non-December date, no
   GNSS/VTEC target read, no 2022 target time evaluated, no comparison, **not a
   scientific result and not validation of the 2022 benchmark**.
6. **Material-change assessment.** This annotation changes no decision: the release and
   the pin values are the concrete form of item 1's "standard shipped index files,
   pinned by SHA-256 at freeze", and item 4 shows the 2022 inputs equal the copies the
   original text described. TE §18.2 therefore requires no additional approval for it.
   What remains supervisor-gated is unchanged: Vision §6.11 freezes the benchmark's
   driver inputs at G-03/G-05, and the two hashes in item 2 are presented there as part
   of D-45. G-04 is not passed by this annotation.

---

## D-46 — F10.7 missing-update composition: reading B, clock hours from the expected availability instant, inclusive 3-hour boundary (freeze; Student + Supervisor item — countersignature OPEN)

**Decision date:** 2026-09-19. **Decided by:** the project owner / student ("A3 — adopt
option B … I select the three-hour missing-update allowance, not the daily-step
extension"). TE §18.2 Q-16/Q-17 ("its missing rule") makes this a Student + Supervisor
item: the student's freeze is recorded; **supervisor countersignature OPEN**.
**Authority:** TE §6.2 ("Carry-forward ≤ 3 h, then exclude"); TC-09; D-21; D-25;
`external-products` R-57a; `CR-2026-09-19-SCI-REVIEW` §4.

**Decision.**

1. **Ordinary reuse is not carry-forward.** `median(D−1)` is the designated value for
   every origin on day *D* (available at 00:00 UTC on *D* under D-25); its use at
   00:00 … 23:00 of *D* is normal use within its validity period — staleness 0, not
   carried, not counted.
2. **Missing update.** When the designated `median(D−1)` is absent (no readings, NaN) or
   not yet available at 00:00 UTC on *D*, the previously available median is carried
   forward for origins *t* with `t − 00:00 UTC D ≤ 3 h` — **inclusive**: 00:00, 01:00,
   02:00 and 03:00 keep the carried value; origins **from 04:00 are excluded** (the row's
   F10.7 limb is unavailable) until a valid update becomes available. The clock starts at
   the EXPECTED availability instant of the missing value, never at the carried value's
   own availability or observation instant; on a second consecutive missing day the clock
   restarts at 00:00 of that day. The bound is `configs/features.yaml:
   carry_forward_bound_hours` (TC-09), never a literal; the vocabulary is
   `carry_forward_composition: clock_hours`.
3. **`f107_81_trailing`** keeps its exact 81-day window ending at the eligible anchor
   (*D*−1); a missing constituent is never imputed and no older window is substituted, so
   the derived feature is **unavailable for the whole affected day**, including the four
   origins where `f107_safe` is carried. Under the established feature-completeness rule
   (a row missing any driver value is excluded, `build_features`), a feature set carrying
   both rows loses all 24 origins of an affected day; a set carrying `f107_safe` alone
   loses 20. This distinction is documented, not smoothed over.
4. **Measured on the held file (Jan–Nov 2022, D-21/D-22/D-23 applied, December readings
   never read):** 365/365 days 2021-12-01 … 2022-11-30 carry a median (four duplicate
   days and four high-spread days reproduce D-22/D-23 exactly); over the **8016** hourly
   origins of 1 Jan–30 Nov 2022, **0** are carried and **0** excluded — every origin is
   ordinary reuse. The A3 sensitivity protocol therefore **stops at Step 0** (no affected
   origin); no model experiment is run. The result would change only if D-26's
   provenance resolution removed days.
**Reported supervisor approval, annotated 2026-09-19 (recording date; not an earlier date).** The project owner / student, Kimia Rezaei, stated in-session on 2026-09-19: "I confirm that my supervisor has approved the scientific decisions covered by the latest handoff, including D-42, D-43, D-45, and D-46." This is recorded here as **student-reported supervisor approval** — a report by the recorded decision owner that the approval occurred, not a supervisor-signed artifact, not a directly observed supervisor communication, and not an earlier approval date than today. No signature, communication, or date is invented beyond what was stated. **Prescribed evidence still outstanding**, per TE §18.2's Student + Supervisor bar and the project's own countersignature practice (`governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md`, `governance/COUNTERSIGNATURE_REQUEST_2026-08-21.md`): a supervisor-signed or otherwise directly-recorded countersignature artifact closing this item, exactly as items 1 and 2 of the 2026-08-16 letter were closed. Drafted and awaiting that signature: `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`. Until that artifact exists, this entry's status is **reported, not verified** — it does not, by itself, satisfy TE §18.2 and does not pass G-04. **Update, later the same day (2026-09-19).** The project owner / student stated: "supervisor has approved and countersigned." Recorded, as this register records every prior owner statement in this single-operator project (see e.g. the many "no supervisor signature artifact exists and none is claimed" entries above): as the recorded decision owner's own statement of the countersignature, not as a signature this session independently observed. `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`'s status line is updated to record the same statement. On that basis this entry's TE §18.2/§18.3 item is treated as closed; it still does not, by itself, pass G-04.

5. Implemented in `spaceweather.resolve_f107_at_origin` (returns `F107Selection` with
   `source_day`, `value`, `carried_forward`, `excluded`, `staleness_hours`); the field
   values themselves are transcribed with the six-entry configuration under item 9 of
   `CR-2026-09-19-SCI-DECISIONS`, not by this entry.

---

## D-47 — `f107_81_trailing` recomputation tolerance: 8.0e-12 sfu, certified for constituents |value| ≤ 400 sfu (freeze; conditional approval verified)

**Decision date:** 2026-09-19. **Decided by:** the project owner / student ("A4 —
conditionally approve 8.0e-12 sfu … only after verifying the proposed derivation"); the
verification is `CR-2026-09-19-SCI-DECISIONS` §5 and
`tests/test_feature_availability.py::test_d47_tolerance_derivation_against_an_exact_reference_and_the_certified_domain`.
Q6 (TE §18.2) is a numerical-reproducibility parameter of the Student's window contract;
no supervisor row covers it. **Authority:** D-21/D-22 (the constituents' grid); TE §6.2
`f107_81_trailing`; `CR-2026-09-19-SCI-REVIEW` §5.

**Decision.**

1. `window.recomputation_tolerance = 8.0e-12` sfu, **absolute**, for
   `|mean_recorded − mean_recomputed|` at every scored origin; derived as
   (N+1)·ε·B = 82 × 2⁻⁵² × 400 = 7.28 × 10⁻¹² rounded UP to one significant figure (the
   only adjustment; never a decade multiplier). ε = 2⁻⁵² is machine epsilon = 2u (u the
   unit round-off); the count (N+1) covers one rounding per parsed constituent, N−1
   sequential additions and one division; the ε-for-u substitution gives a factor ≈ 2 of
   margin, which makes the bound rigorous rather than first-order.
2. **Applicability condition:** the certificate holds for constituents with
   |value| ≤ **B = 400 sfu** (`window.recomputation_input_bound_sfu: 400`). B is a stated
   numerical domain, **not** a physical maximum; a reading or median above it is never
   deleted, clipped or declared invalid. If any constituent exceeds B the numerical
   certification **fails clearly** (`assert_recomputation_domain`, `IntegrityError`) and a
   justified wider bound under its own decision — or a more accurate implementation — is
   required; the tolerance is never raised silently. Held daily medians (2004–2026,
   December 2022 excluded) reach 311.7 sfu.
3. **Verified** against an exact rational reference (`Fraction`, no floating point):
   max |float − exact| = 1.9 × 10⁻¹³ over synthetic 0.05-sfu-grid windows (the
   project's own constituent grid: D-21 medians of 0.1-sfu readings, D-22 half-grid
   means); `json` `repr` round trip exact; a 6-decimal writer breaks the certificate
   (must be refused at freeze); 80-day and shifted-anchor perturbations differ by
   ≥ 10⁻³ sfu (≫ tolerance). Summation is plain sequential on the governed CPython 3.11;
   compensated summation on later interpreters only reduces the error.
4. **Numerical agreement only** — the tolerance says nothing about F10.7 measurement
   accuracy (readings are quantised at 0.1 sfu; flare-contaminated readings are retained
   under D-23). Transcription of the two values into `configs/features.yaml` is part of
   the six-entry configuration diff (item 9), not of this entry.

---

## D-48 — December custody scan: structural detection; driver-exclusion class 5 for the GFZ captures with content and provenance conditions (freeze; student decision under the D-30 precedent)

**Decision date:** 2026-09-19. **Decided by:** the project owner / student ("G-3/P-4 —
resolve December scanning transparently … I approve an additional driver-audit exclusion
only within this explicit scope"). **Authority to decide:** `governance-guards` R-26/R-27
are design rules whose class list the project decision owner already amended by D-30
(class 4, 2026-08-28, under the recorded authority equivalence); the same authority
applies. No target value is involved, so no locked-test access provision is engaged.
**Authority:** R-26, R-27, D-15, D-30, `project.md` § Forbidden (December-blind rule);
`CR-2026-09-19-SCI-REVIEW` §6; `CR-2026-09-19-SCI-DECISIONS` §6.

**Decision.**

1. **Detection is structural, per format** (`src/data/locked_test.py`): JSON by parsed
   structure — any string carrying `2022-12`/`202212`, any record with year 2022 and
   month 12 under `y`/`year` and `m`/`month` at any depth, any per-month mapping keyed by
   month numbers that carries `"12"`; WDC and Hpo files by their own date layouts;
   isprint tables by first/last record epoch; Madrigal CSVs by `ut1_unix` epochs or
   literals; other text by literal; Markdown = outside automated inspection, reported as
   such and never labelled clean. Every file outside the restricted root is inventoried
   with its detection method and disposition (`december_custody_inventory`); scanner
   coverage is reported separately from compliance.
2. **Class 5** — *raw GFZ geomagnetic-index captures and their source-version audit
   summary*: `audit_gfz_*/Kp_*.wdc`, `audit_gfz_*/hp60ap60doi_*.txt`,
   `audit_gfz_*/gfz-comparison-report.json`. Eligibility = exact path pattern **and**
   validated content (every raw data line parses as the provider format with no extra
   column; the report's schema is fixed and carries no target/prediction/metric key —
   `y` admitted only inside `{y, m, d, h}` epoch keys, `coverage` only under
   `validation`) **and** documented provenance (a sibling `retrieval_record.json` listing
   the raw file with a matching SHA-256, or the report's `run_id`). Mixed, unknown or
   unclassifiable content **fails closed** (flagged for review). This is **narrower**
   than the class 5 prepared on 2026-09-19 (which also named `GFZ-AUDIT.md`,
   `retrieval_record.json`, the manifests and `environment_supplemental.json` — files
   with no December content, now simply inventoried as such).
3. Classes 1–4 keep their paths and gain the same content validation (Dst pages must be
   Dst pages without target words; `fluxtable.txt` lines must parse; classes 3/4 remain
   key-token gated). No evidence file is relocated or reserialised.
4. **Excluded files are custody exclusions only**: inventoried with their reason and
   recorded as **exposure** — the December values in them were read for identification,
   parsing validation and version comparison; none informed a method, feature,
   threshold, lag, missingness-policy or model decision (`CR-2026-09-19-SCI-DECISIONS`
   §6.4). Holdout independence is not asserted "unaffected"; the December-blind rule is
   evidenced by the absence of any December-derived choice in the records.

---

## D-49 — B-01 execution-environment exception: CPython 3.10.12 for the isolated Kaggle IRI-2016 environment only (owner approval 2026-09-19)

**Decision date:** 2026-09-19. **Decided by:** the project owner / student ("I approve
CPython 3.10.12 for the isolated Kaggle B-01 IRI execution environment, using the verified,
pinned iricore installation. Record this as a B-01-specific exception to the Python 3.11
requirement. Keep the main project environment unchanged."). **Authority:** TE §8.1 / TC-03d
(Python 3.11, exact pins — TE §18.2 Q-29 environment row) as the rule being excepted; D-45
and its 2026-09-19 annotation (the verified runtime); `CR-2026-09-19-SCI-DECISIONS-P3`
§3.6–3.9. **Recorded on the owner's authority; no supervisor signature is claimed.**

**Decision.**

1. **Scope.** The exception covers exactly one environment: the `virtualenv` created on the
   Kaggle image from `/usr/bin/python3.10` (CPython **3.10.12**) in which
   `scripts/04_build_external_products.py` runs `--verify-runtime`,
   `--build-validation-report` and `--generate-benchmark` against the pinned
   `iricore==1.8.0` wheel. It does **not** extend to model training, the walking-skeleton
   fixture runs, any other stage script, or the governed local environment, all of which
   remain Python 3.11 with `requirements.txt`'s exact pins (TC-03d unchanged).
2. **Why.** `iricore==1.8.0` — the newest release with a Linux wheel — publishes that wheel
   for CPython 3.10 only (`cp310-cp310-manylinux_2_35_x86_64`); 1.8.1–1.9.0 publish
   macOS-arm64 only. The wheel installs and runs on Kaggle (verified 2026-09-19; no
   from-source Fortran build was attempted).
3. **Recorded identity.** `iricore==1.8.0` wheel SHA-256
   `f452b22316891d87ee766dba266de6a07e4e6008ab515ffed902ea8b5446a874`; `numpy==1.26.4`
   `ffa75af20b44f8dba823498024771d5ac50620e6915abac414251bd971b4529f`; `fortranformat==2.0.3`
   `88c8e7a3eac16c23420e8a1c4b21ddc7108f48e8dcbd2e0da6c8ecc48b051bb2`; `pymap3d==3.2.0`
   `fccd44f2f6021a95adec19771c603b8dac104eab120d863c463d76b9bc298669`; `pyyaml==6.0.1` (cp310
   manylinux wheel) `ba336e390cd8e4d1739f42dfe9bb83a3cc2e80f567d8805e11b46f4a943f5515`; index
   files `apf107.dat` `cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674`,
   `ig_rz.dat` `fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486`; IGRF-13
   compiled in (`igrf2020.dat` `5c5288ede8987252…`, `igrf2020s.dat` `40abaa5990a20487…`,
   `dgrf2015.dat` `bfa50177d289f007…`); Kaggle kernel 3.12.13, `Linux-6.12.90+-x86_64-with-glibc2.35`;
   virtualenv seeds `pip==26.2.1`, `setuptools==84.0.0`. Every B-01 run's environment lock
   records the 3.10.12 interpreter and the environment's own `pip freeze`
   (`configs/experiment.yaml: benchmark_b01.runtime.interpreter_exception`).
4. **Interaction with the fixture gate — preserved, not waived.** `fixture_gate.verify_receipt`
   (SD-X-02, Q2 = A) accepts a receipt only when its recorded environment identity
   (requirements hash, pip freeze, versions, code commit, config hashes, platform) equals
   the caller run's lock. A full-year `--generate-benchmark` run inside this 3.10
   environment therefore **cannot** consume receipts produced by fixture runs in the
   3.11 environment. This decision does not resolve that; two admissible resolutions are
   recorded for a later, separate decision: (a) extend this exception to the two fixture
   runs executed inside the same B-01 environment — an extension to the fixtures'
   training step, hence NOT granted here; (b) build `iricore` for Python 3.11 from its
   sdist (`iricore-1.8.0.tar.gz`, SHA-256
   `e5c4a71e3639879b48c3c091f2c543d750a23cca50eafeca1bdc62fb9d206d77`; TC-04 anticipates a
   Fortran build re-established from pins) so B-01 runs in the governed environment and
   this exception becomes a fallback. The bounded checks (`--verify-runtime`,
   `--build-validation-report`) need no receipts and run under this exception now.
5. **Not changed.** No scientific value; no gate; D-45 as annotated stands; G-04 is not
   passed.

**Addendum 2026-09-20 — item 4 resolved by resolution (a): the exception EXTENDS to the two
walking-skeleton fixture runs executed inside the same B-01 environment.** Owner authorization,
quoted: *"I authorize extending the Python 3.10 exception to the prerequisite fixture runs
specifically required for B-01, provided their required dependencies and scientific behavior are
compatible. Keep the main training/stage environment on Python 3.11. Preserve the receipt
requirement: the B-01 fixtures and benchmark must use the same applicable environment identity.
Do not bypass or weaken receipt checks."* Recorded on the owner's authority; no supervisor
signature is claimed. Prepared at `governance/CHANGE_RECORD_2026-09-20_b01_prerequisites.md` §1.

1. **Scope of the extension.** The `plumbing_7day` and `scientific_1month` runs of
   `scripts/run_walking_skeleton.py` — measuring runs (`--emit-candidate`) and verification
   runs alike, together with the seven Phase 1 stage-script subprocesses and the M10 contract
   fixture they invoke — MAY execute inside the item-1 environment when, and only when, that
   run's purpose is to produce the TE 9.2 receipts a B-01 `--generate-benchmark` run consumes.
   The environment is the item-1 `virtualenv` (CPython 3.10.12) carrying, in addition to the
   item-3 hash-pinned IRI set, every pin of `requirements.txt` installed unchanged. Model
   training as a deliverable, every other stage run, and the governed local environment stay
   on Python 3.11 with `requirements.txt`'s exact pins (TC-03d unchanged).
2. **Compatibility condition — checked, not assumed.** A `pip` dry-run resolution for
   `cp310` / `manylinux_2_17..2_35` x86-64 of `requirements.txt` plus `iricore==1.8.0`,
   `fortranformat==2.0.3`, `pymap3d==3.2.0` resolved **50** packages with no conflict: every
   one of the eight `requirements.txt` pins publishes a cp310 Linux wheel
   (`tensorflow==2.21.0` requires-python `>=3.10`, wheel `manylinux_2_27`, satisfied by the
   image's glibc 2.35); `iricore`'s own constraints (`numpy<2.0,>=1.25`, `fortranformat<3`,
   `pymap3d[core]<4`) are met by the same `numpy==1.26.4` pin. No pin was altered. Two
   limitations are recorded rather than hidden: (i) `requirements.txt` pins no transitive
   dependency, so the resolved `keras` differs between interpreters (3.12.4 under 3.10 in the
   dry run; 3.15.1 in the local 3.11 environment) — the environment lock's `pip freeze` records
   what actually ran, and a receipt binds to it; (ii) "scientific behaviour compatible" is
   asserted at the pin level (same TensorFlow, scikit-learn, numpy, pandas wheels for cp310
   as for cp311) and is NOT a claim of bit-identical outputs across interpreters — which is
   exactly why the receipt requirement below is preserved rather than relaxed.
3. **Receipt requirement — preserved by construction, not by exemption.**
   `fixture_gate.verify_receipt` is unchanged: a receipt is accepted only when its recorded
   TE 13.1 environment identity (requirements hash, `pip freeze`, runtime versions, code
   commit, config hashes, platform, nondeterministic ops) equals the consuming run's lock.
   Running the fixtures and the benchmark in ONE environment is what makes that identity
   satisfiable; nothing in the gate was widened, and a fixture receipt produced in any other
   environment (the local 3.11 one included) still refuses a 3.10 generation run.
4. **Mirrored in configuration.** `configs/experiment.yaml: benchmark_b01.runtime.interpreter_exception`
   now lists the two fixture runs under `applies_to` with this addendum as their authority and
   keeps model training and every other stage under `excluded`.
5. **Consequence for the fixtures, stated so it is not misread.** The extension makes the
   environment identity satisfiable; it does not make a receipt exist. Every other fixture
   prerequisite — the walking-skeleton freeze acts (Q-31) and the stage-script refusal gates
   enumerated in `CHANGE_RECORD_2026-09-20_b01_prerequisites.md` §2 — stands exactly as
   before.

---

## D-50 — B-01 IRI-2016 validation tolerance: 1.0 TECU absolute per case (freeze; student decision)

**Decision date:** 2026-09-20T12:27:01Z (the approval instant is the declaration time recorded
below, never backdated — R-59 limb 2). **Decided by:** the project owner / student ("1.
approved"). **Authority:** R-59 area 7 assigns the predeclared tolerance to the student;
`governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md` (revision 2) is the full derivation.
No supervisor signature is claimed or required for this item.

**Decision.** `|adapter − official| ≤ 1.0 TECU` for every one of the eight R-59 cases, absolute,
per case; the validation report also records the mean and maximum signed difference across the
eight. Status `passed` only if all eight hold.

**Basis (measured, not asserted; full detail in the proposal).** 288 non-December, non-R-59-case
profiles on the pinned `iricore==1.8.0` wheel (Kaggle smoke-test value reproduced bit-identically)
give: adapter − converged reference +0.004…+0.062 TECU; adapter − official under IRI's own
`iri_tec` scheme at its "standard"/"best" step settings +0.006…+0.14 TECU; under its "fast"
setting −0.06…−0.82 TECU at ≤ 38 TECU (the server's exact setting is unknown and declared as
the one open assumption, with a predeclared sign-and-proportionality signature to recognise it
without post-hoc reasoning). Configuration mismatches the validation exists to catch (wrong foF2
model, topside option, B0 model, storm switch, integration ceiling) shift TEC by 1–7 TECU on at
least half the profiles; the one exception is the hmF2 model (the form's default AMTB versus the
IRI-2016-standard Shubin-COSMIC), which shifts TEC by at most 0.45 TECU and is therefore not
caught by any per-case tolerance in the plausible range — handled procedurally (Shubin selected
on the form; the collection sheet fixes this) rather than by tolerance.

**What this does not do.** It does not absorb a scientific mismatch. If any of the eight cases
fails, the report is written `status: failed`, generation stays blocked, and the cause is
investigated from the recorded output headers (server index version, echoed integration limits)
and, where the hmF2 column was recorded, that model choice — the implementation is never switched
and the tolerance never widened after the fact (TE §18.2). D-47's `8.0e-12 sfu` F10.7
recomputation tolerance is a distinct quantity (sfu, floating-point reproduction) and is not
reused here.

**Recorded.** `configs/experiment.yaml: benchmark_b01.validation_report.tolerance_tecu = 1.0`,
`tolerance_declared_at_utc = "2026-09-20T12:27:01Z"`. The report builder (`build_validation_report`)
refuses to run while either field is `TBD` and refuses a declaration that does not precede the
comparison; both conditions are now satisfied for a comparison run FROM this instant forward.

---

## D-51 — `experiment.yaml: horizons: [1]` is transcribed from TE §2.1 (transcription)

**Decision date:** 2026-09-20. **Authorized by:** the project decision owner ("3. approved",
given against `governance/CHANGE_RECORD_2026-09-20_b01_prerequisites.md` §2.5 item 5, which
presented the value and its source), exercised under the standing student/supervisor authority
equivalence recorded for this workspace (D-1 addendum). **Authority for the VALUE:** TE §2.1,
row "Optional horizon": *"`experiment.yaml` shall expose `horizons: [1]` with `24` implemented
and testable but **not** included in the default run list."* (Q-03, Q-33).

**Decision.** `configs/experiment.yaml: horizons = [1]`. **No scientific value is chosen here**;
the list is a verbatim copy of TE §2.1's already-frozen text, exactly as D-38 copied
`embargo_hours` from TE §7.1. `src/models/train.py: read_horizons` reads it and refuses while
absent or `TBD` (R-99: the horizon reaches every model from this field, never from a literal).
The +24 h horizon stays implemented and testable but outside the default list; adding it is a
config change only, and TE §2.1 bars it from the default list before the minimum thesis is
complete and frozen.

**Governance condition, stated precisely — same pattern as D-1's addendum and D-31.** TE §18.3
precondition 3 (and D-31's table) names *horizons* among the six items the supervisor signs
before affected components run. D-38's `embargo_hours` transcription carried a joint
owner-and-supervisor instruction of record; this transcription carries the owner's approval
under the recorded delegation. **No signed document, email or minute from Dr. Reza Saraf
Shirazi exists for this item, and none is represented as existing.** If the examining
committee requires an independent supervisor signature distinct from the delegation, that
requirement is outside this repository's control and is recorded here so a reader can judge it.

**Effect on the fixture ladder.** Stage 06's first refusal ("`horizons` absent or unresolved",
`CR-2026-09-20-B01-PREREQS` §2.2 row k) is cleared; its next refusal, `models.selected`, is the
tuning run's output and not a freeze item.

---

## D-52 — Stage 00 on a fixture run READS the scope's verified derived artifacts; no transport (ruling; option (a))

**Decision date:** 2026-09-20. **Ruled by:** the project decision owner ("for item 1 i choose a",
against `governance/CHANGE_RECORD_2026-09-20_b01_prerequisites.md` §2.5 item 1, which offered
two mutually exclusive rulings). **Authority:** TE §15.1 (a walking-skeleton fixture "reads
prepared provider VTEC only"); TE §9.2 (both fixtures before any full-year job); `team.md`
§ Walking Skeleton (eligibility judged on derived-artifact verification; the DATA-07 caveat);
R-31 / Option B (`CR-2026-09-13-000102-FIXTURE-WINDOW`); R-36 (`provenance_class` closed set,
"the twelve pre-TC-06 months are 'derived_only'"); R-135 control 12 (declared inputs verified
at use).

**Decision.** On a fixture run (`--fixture-manifest` given), `scripts/00_acquire_prepared_vtec.py`
constructs **no** provider transport. It re-executes the orchestrator's declared-input
verification (`verify_declared_inputs`, now housed once in `src/data/acquisition.py` and
imported by both), reads the scope's cited records file, SELECTS the cited station(s)' records
inside the cited window on record dates, ASSERTS the assembled set (no locked-month record;
every record inside the window), and writes `artifacts/acquisition/fixture_read_manifest.json`
(`retrieval_performed: false`; the month's own recorded `madrigalWeb_version` copied verbatim —
`"unknown"` for the pre-TC-06 months, never replaced by a plausible value) plus
`sha256_manifest.json` with `provenance_class = "derived_only"`, zero provider files and
exactly the verified artifacts. **No `request_manifest.json` is written on this path**: nothing
was requested, so R-35's retrieval check (a non-empty `madrigalWeb_version`) is neither applied
nor imitated. A retrieval run (no `--fixture-manifest`) is unchanged and still refuses at
`_build_transport` until the DATA-07 re-acquisition is authorised.

**What this does not do.** It does not verify retrieval (DATA-07's caveat stands on every
fixture artifact); it does not authorise any provider call; it does not change the fixture
windows, stations or any cited value. Option (b) — exempting stage 00 from the fixture sequence
— was offered and not chosen.

**Measured effect.** Plumbing measuring-run probe (governed 3.11 environment, isolated copy):
stage 00 completes (`records_read_from_month_file` 18,183; `records_in_window` 1,810 for
`BSHM`, D-11's own figure), stage 01 completes, and the ladder now stops at **stage 02**
(`configs/data.yaml: qc_operations` absent — freeze item 2, the supervisor's). Tests:
`tests/test_clean_run.py::test_item1_option_a_00_fixture_run_reads_verified_artifacts_and_writes_derived_only`,
`::test_item1_option_a_00_fixture_run_refuses_a_tampered_artifact_before_reading`.

---

---

## D-53 — The documented-QC operation list is closed at five operations (freeze)

**Decision date:** 2026-09-21. **Approved by:** the project decision owner ("approved,
proceed"; "Transcribe existing approvals now"), and **countersigned by the supervisor on the
student's report of the same date**. No separately signed document artifact exists in the
workspace and none is claimed. **Authority:** FR-P1-03-1 (the closed four-transformation set);
R-64; TE §7.0A P1-03 ("preserve provider values; apply only documented QC, UTC normalization,
cell selection and frozen hourly aggregation; never … silently interpolate missing cells");
R-71 content 2 / NFR-DQ-01; **D-19** (all four threshold values); **D-5** and **D-10.2** (gaps).

**Decision.** `configs/data.yaml: qc_operations` is frozen as the closed list of exactly five
documented-QC operations, the first of FR-P1-03-1's four permitted transformations:

| # | Operation | Effect | Governing record |
|---|---|---|---|
| 1 | `reject_unexplained_negative_vtec` | **Rejects** the row unless a recorded explanation accompanies it; an explained negative is accepted with its explanation carried in the data-quality block | R-71 content 2; NFR-DQ-01 |
| 2 | `flag_valid_observation_count_below_minimum` | Marks `target_valid: false` with the reason, below **3** samples | D-19 |
| 3 | `flag_within_hour_spread_above_range_bound` | Marks `target_valid: false` above a **10.0 TECU** range | D-19 |
| 4 | `flag_largest_internal_gap_above_maximum` | Marks `target_valid: false` above **1800 s** | D-19 |
| 5 | `flag_provider_dtec_summary_above_level` | Records a **quality flag only**; does not invalidate the row, above **1.5 TECU** median `dtec` | D-19 |

**What is new here, stated exactly.** All five operations were already approved and already
implemented in `src/data/prepared.py: standardize_hourly_target`. **The only new act is the
closure of the list** — naming these five as the complete documented-QC set, so that an
operation outside it fails exactly as a fifth transformation would
(`assert_qc_operation_permitted`; R-64). **No threshold was invented and no provider value is
modified**: three of the five only flag or record, and none alters `vtec_tecu`.

Two facts are recorded in the block so their absence is not misread as an omission:
`preserves_provider_values: true`, and `gap_policy: explicit_nan_never_filled` (D-5; D-10.2) —
there is no gap-filling operation to enumerate because gaps are never filled, at acquisition or
at standardization.

**Also transcribed under this act:** `configs/data.yaml: target.support_thresholds`, all four of
**D-19's** rows with their measured basis and `basis_window: "January-November 2022"`. Copies of
values approved 2026-08-21; December was excluded by construction in D-19's own measurement, and
`resolve_support_thresholds` refuses a basis that references December.

**Verified by execution** (2026-09-21, CPython 3.11.16): `assert_qc_operations_frozen` accepts
the block and reports five operations; all four thresholds resolve with their statistics and
roles; and a control confirms an operation outside the list is refused by name. Change record:
`governance/CHANGE_RECORD_2026-09-21_qc_and_support.md`.

---

## D-54 — The top-1% sensitivity: 1% of absolute errors, comparison-wide, one retained set (freeze)

**Decision date:** 2026-09-21. **Decided by:** the project decision owner; **countersigned by the
supervisor on the student's report of the same date**. No separately signed document artifact
exists and none is claimed. **Authority:** FR-P1-05-10; Vision §2.3 (equal-station weighting);
Vision §2.4 (the binding honesty rule); Vision §8.3 (the selection channel). Closes
`GOV-2026-09-20-CG-01` **Recommendation 21** and dispositions §5 item 14.

**Decision.** `removed_fraction: 0.01`, `scope: comparison_wide`, with:

* the **same retained rows applied to every compared model**;
* the established **equal-station-weighted** metrics recomputed on the remainder;
* **removed and retained counts reported per station**;
* an **undefined comparison refused** when any station retains no rows;
* the figure bounded as a **supplementary sensitivity only** — it never changes the primary
  results, never selects a model, and never tunes a parameter.

**Unchanged and not re-decided** (each already implemented): the ranking variable is the absolute
error |ŷ − y| of each masked row; ties break by `(station, interval_start_utc)` ascending;
`k = ceil(removed_fraction × n)`, never `round` or `floor`; removed rows are dropped and every
metric **recomputed** on the remainder; a support the rule would empty refuses.

**The consequence of `comparison_wide`, recorded rather than glossed.** Ranking all three stations
together is the literal reading of FR-P1-05-10's wording. It is also **not proportionate**: a
station with systematically larger errors loses a larger share of its rows, so the equal-station
mean is then taken over unequal per-station supports. That is precisely why the per-station counts
are mandatory output rather than optional — the asymmetry is made visible instead of inferred.

**The combination rule (decided 2026-09-21, same act).** The decision fixes that the retained rows
are shared; **how** several members' rankings become that one set was a second choice, resolved as
`rank_by_max_member_error`: each masked row is ranked once by its worst absolute error across the
compared members, and the top `k` removed. Exactly `k` rows go, so the declared 1% holds exactly
and no single member's ranking decides the set alone. The alternative, `union_of_member_top_k`,
was not chosen; it would have removed more than the declared fraction.

**What had to be built.** `top1pct_removed_keys` ranked a **single member's** own errors, so each
model would have been scored on a **different support** — the very thing the comparison-wide mask
exists to prevent (NFR-FAIR-01). Four functions were added to `src/evaluation/diagnostics.py`:
`top1pct_comparison_removed_keys`, `_assert_no_station_emptied`, `top1pct_station_counts` and
`top1pct_comparison_block`, the last carrying `role: supplementary_sensitivity_only` and
`may_inform_selection_or_tuning: false` as data. Seven controls, including negative controls for
the station-emptied refusal and for an undeclared combination rule.

**Recorded before locked evaluation**, as required. Change record:
`governance/CHANGE_RECORD_2026-09-21_top1pct.md`.

---

## D-55 — M-03 climatology: station-and-hour mean, fitted on training partitions only (freeze)

**Decision date:** 2026-09-21 (reaffirming the previously approved key). **Approved by:** the
project decision owner; **countersigned by the supervisor on the student's report of the same
date**. No separately signed document artifact exists and none is claimed. **Authority:** Vision
§2.4 tier 2 and PC-03/PC-04 (M-03 is a mandatory difficulty control); R-98 / NFR-LEAK-01;
D-16/D-17 (the hourly interval and the target row); D-38 / R-80 (the expanding-window splits).
Closes `GOV-2026-09-20-CG-01` **Recommendation 2**.

**Decision.** M-03's climatology key is the mean of the target grouped by **station and hour**,
fitted **exclusively on each partition's own training data**. **Month is removed from the key.**

**Why month is removed.** A month-bearing key can predict for **no** scored month: under the
expanding-window splits every partition's validation month lies strictly after its own training
range, so every scored row looked up a key the training data cannot contain. Because M-03 is one
of the three mandatory difficulty controls, an M-03 that yields no prediction empties the
comparison-wide mask for every comparison it belongs to.

**Limitation, mandatory wherever M-03 is reported.** A station-and-hour mean carries **no seasonal
term**. It cannot represent December's diurnal amplitude or level differing from the
January–November training mean, and it is **not** a seasonal climatology. This is the deliberate
cost of a key that can predict for every scored month at all.

**Time convention unchanged:** `hour` is the UTC hour of `interval_start_utc` (D-16's hourly
interval; D-17's target row). No local-solar-time variant is introduced; longitude reaches the
model only through `lst_sin`/`lst_cos` (TE §7.2).

**Enforcement.** `src/models/climatology.py` refuses a key field it cannot compute **by name**, so
a month-bearing key cannot be re-adopted by editing configuration alone; refuses a key in a
different order; and refuses any `fitted_on` other than `training_partition_only` as a
`LeakageError`. Missing keys at prediction time stay **missing** (`missing_climatology_keys` on the
frame), never interpolated or filled. Change record:
`governance/CHANGE_RECORD_2026-09-21_climatology_refit_and_reconciliation.md` §1.

---

## D-56 — The refit epoch rule: median best-validation epoch across folds and seeds, rounded half up (freeze)

**Decision date:** 2026-09-21 (reaffirming the previously approved rule). **Approved by:** the
project decision owner; **countersigned by the supervisor on the student's report of the same
date**. No separately signed document artifact exists and none is claimed. **Authority:** Vision
§8.3 (December never informs selection); TE §7.0B; R-94 (best-checkpoint restoration).
Closes `GOV-2026-09-20-CG-01` **Recommendation 5**'s rule limb.

**Decision.** The final refit's epoch count is the **median best-validation epoch across the
predefined pre-December folds (F1–F4) and the final seeds, for the selected configuration, rounded
half upward**.

**The rule is the frozen object; the number is its output.** The inputs are the epochs the fold
fits actually restored (`Checkpoint.epoch`, the lowest-validation-RMSE epoch, R-94) — one per
(fold, seed) pair, all pre-December. The resulting integer is transcribed into
`configs/experiment.yaml: models.refit.epochs` under its own D-number **before the final refit and
before G-05**. It is **not required before the validation runs that produce it**: nothing but the
refit reads the field, so the folds run with it unset.

**December's role.** The refit trains for exactly that many epochs on the permitted
January–November REFIT training data, with **no validation set and no early stopping**, so no
December row can reach a stopping decision. **December is inference-only.**

**Enforcement.** `refit_epoch_count` implements the rule once; `assert_refit_epochs_match_rule`
re-derives it from the recorded fold/seed epochs and refuses a transcribed value that is not the
rule's own output. Rounding is half **up** by integer arithmetic, not `round()` (which rounds half
to even). **Verified by execution** 2026-09-21: the rule over `[5, 7, 8, 10]` returns **8**
(median 7.5). Change record: `…_climatology_refit_and_reconciliation.md` §2.

---

## D-57 — `window_length_hours` is 24 (transcription)

**Decision date:** 2026-09-21. **Authorized by:** the project decision owner ("transcribe approved
values without asking again"); **countersigned by the supervisor on the student's report of the
same date**. No separately signed document artifact exists and none is claimed. **Authority:**
Vision §8.1 — *"History window: 24 hours primary … **History length is not a tuned
hyperparameter**"*; TE §7.2's ablation table, where ABL-HIST48's `primary_remains` reads 24 h.

**Decision.** `configs/experiment.yaml: window_length_hours = 24`. **No scientific value is chosen
here**: this is a copy of an already-frozen one, the same class of act as **D-38**
(`embargo_hours`) and **D-51** (`horizons`). The 48-hour variant reaches the pipeline only as
**ABL-HIST48**, and only after the primary configuration is frozen.

**Verified by execution** 2026-09-21: `read_window_length(snapshot, sequence_steps=24)` returns 24,
and the leakage guard still refuses a mismatched sequence length (`sequence_steps=48` raises
`LeakageError`) — transcribing the value did not disarm the check that protected it. Change
record: `…_climatology_refit_and_reconciliation.md` § `CR-2026-09-21-RECONCILIATION` §1.

---

## D-58 — The declared baseline per track is persistence (freeze)

**Decision date:** 2026-09-21. **Decided by:** the project decision owner; **countersigned by the
supervisor on the student's report of the same date**. No separately signed document artifact
exists and none is claimed. **Authority:** Vision §8.7 — *"The declared baseline per track is named
in configuration before tuning begins"* — and **D-124**, which approves the selection rule without
naming a baseline; Vision §2.4 tier 2 and PC-03/PC-04 (persistence as a mandatory control).

**Decision.** **Persistence** is the declared baseline for every track.

**Why.** It is already one of the three mandatory difficulty controls, it is defined on every
partition, and it requires no fit — so the selection criterion can never be compared against a
baseline that itself failed to fit. Vision §8.7 fixes the obligation to name a baseline in
configuration; this decision supplies the name it left open.

**Transcribed alongside it** (a copy of **D-124**, recorded as *Approved* in Vision §14.2): the
selection rule itself — select on mean per-fold skill versus the declared baseline across F1–F4;
prefer the simpler configuration within **1%**; refit without changing any hyperparameter; and no
December result may influence the criterion (Vision §8.7; Vision §8.3).

---

## D-59 — The December day range governing D-13's comparison count is 2–31 December 2022 (freeze)

**Decision date:** 2026-09-21. **Decided by:** the project decision owner **and the supervisor**
(the student reports the supervisor's countersignature of the same date); this is the **Student +
Supervisor** gate item `GOV-2026-08-28-FD-01` **Recommendation 15** routed. No separately signed
document artifact exists and none is claimed. **Authority:** **D-28** (the locked scored set);
D-13 (the independent-storm-event threshold); Vision §9.3.

**Decision.** `configs/experiment.yaml: regimes.december_day_range = "2022-12-02..2022-12-31"`.

**Why this range.** It matches **D-28's locked scored set exactly** — 2–31 December 2022, thirty
days — so D-13's comparison count describes precisely the set that is scored, rather than a
different December. D-28's own three grounds for the 30-day set (physical, statistical, and the
load-bearing arithmetic that 720 hours is divisible by both 24 and 48, which 744 is not) carry
over unchanged; nothing about the scored set is reopened here.

**This is not a locked-test access.** Fixing a day range reads no December target value. The
required pre-G-05 December coverage and regime audit remains performance-blind and remains a
precondition of G-05 (Vision §8.3; Vision §11; R-13).

**Verified by execution** 2026-09-21: `read_december_day_range` resolves the field to
2022-12-02 … 2022-12-31, thirty days inclusive. The refusal that protected the field while it was
unfrozen is **kept as a negative control** on a synthetic config — a sentinel, an absent value and
an unparseable string each still refuse by name.

---

## D-60 — The Phase 1 feature set: `FS-P1-2022-v1`, 21 fields over 13 dictionary rows (freeze)

**Decision date:** 2026-09-21. **Approved by:** the project decision owner ("i approve of all the 7
train_only_standardize feature names"), against the proposal at
`governance/proposed/FEATURE_IDS_PROPOSAL_2026-09-21.md`; **countersigned by the supervisor on the
student's report of the same date**. No separately signed document artifact exists and none is
claimed. **Authority:** TE §6.2 (the dictionary table); `src/features/build.py:
SECTION_6_2_ROWS` (the same row identities as a frozen constant); NFR-LEAK-01; TE §7.2.

**Decision.** `configs/features.yaml` takes `feature_set_id: "FS-P1-2022-v1"`, the 21-field
`feature_dictionary` below, and `normalization: "train_only_standardize"` as the declared default
posture.

**What is transcription and what was chosen.** The input space was already closed in two places
that agree — TE §6.2's table and `SECTION_6_2_ROWS`. The rows, the exact lag set `[1,2,3,24]`, and
the `none` normalizations are **copies**. **One thing was chosen**: the seven rows whose TE §6.2
Normalization column reads the conditional *"Train-only if scaled"* — `station_lat`, `kp_safe`,
`ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe`, `f107_81_trailing` — resolve to
`train_only_standardize`, because Ridge and the LSTM are scale-sensitive across drivers spanning
Kp 0–9 to F10.7 in the hundreds; Random Forest is scale-invariant so it costs nothing; and
train-only fitting is the leakage-safe direction, fitted per fold on training rows only.

**The 21 fields.** `vtec_lag_1h/2h/3h/24h` (row `vtec_lag`, exact lags 1/2/3/24);
`vtec_seq_24` (24 steps); `utc_hour_sin`, `utc_hour_cos`, `doy_sin`, `doy_cos`, `lst_sin`,
`lst_cos`; `station_onehot_ARUC/BSHM/NICO`; `station_lat`; `kp_safe`, `ap_safe`, `hp60_safe`,
`ap60_safe`, `f107_safe`, `f107_81_trailing`. Thirteen rows expand to 21 fields because
`vtec_lag` yields four and `station_onehot` three.

**Deliberately absent, each a decision rather than an omission.** `dst` — diagnostic/hindcast-only,
never a confirmatory feature. `ssn_*` — removed; `REMOVED_ROWS` refuses it by name.
`target_support` (`valid_observation_count`, spread/gap/QC fields) — diagnostic by default; model
use *"requires explicit G-04 approval"*, and **G-04 is not passed**; target-hour quality fields are
permanently forbidden as features regardless. Raw longitude in any form — it enters only through
`lst_sin`/`lst_cos`. Anything IRI-bearing — refused by the denial mechanism WS-10 proves.

**A change to this dictionary means a NEW `feature_set_id`** (`FS-P1-2022-v2`), never an edit of
this one.

**Verified by execution** 2026-09-21: `load_feature_dictionary` accepts all 21 fields
(12 `train_only_standardize`, 9 `none`).

**What this does NOT discharge.** G-04 is not passed; no support field becomes a feature; the
target contract is unchanged; and `configs/data.yaml: stations.*.observable_codes` remains
untranscribed, so `assert_registry_resolved` still refuses on that one field.

---

## D-61 — Stage 00 publishes the release the downstream stages consume (option A; freeze)

**Decision date:** 2026-09-21. **Ruled by:** the project decision owner ("for release issue i
choose option A and based on D-52 is okay to be written like this"), against the four options at
`governance/proposed/RELEASE_PRODUCER_OPTIONS_2026-09-21.md`; **countersigned by the supervisor on
the student's report of the same date**. No separately signed document artifact exists and none is
claimed. **Authority:** TE §13.3 (the release field contract); **D-29** (`dataset_version`
derivation); R-13 (no overwrite); R-44 (releases consumed by manifest and hash, never bare paths);
**D-52**, as read below.

**The defect this closes.** `src/data/release.py: write_release` was a complete, tested,
TE §13.3-conformant writer with **no production caller anywhere** — verified 2026-09-21 by grep
over `scripts/`, `src/`, `notebooks/` and `kaggle/`: only two test modules called it. Meanwhile
`01_inventory_and_registry.py` reported `release_manifests_found: 0` and
`02_standardize_prepared_target.py` **refused** ("no released provider input exists under the
release root … refusing rather than fabricating input"). Both refusals were correct; the producer
had simply never been wired, so the Phase 1 sequence could not advance past stage 01.

**Decision.** **Stage 00 releases what it acquired.** After every existing assertion — the
declared inputs re-verified, the records selected on record dates, no locked-month record present,
every record inside the cited window — the fixture path publishes the verified rows as an
immutable release under `artifacts/releases/<fixture_id>_<utc stamp>/`.

**The D-52 reading, as ruled.** D-52's "no transport" prohibits **transport of provider bytes**,
not writes as such. A fixture run still contacts no provider and still reads only the scope's
verified derived artifacts; what it now also does is publish those verified rows so the stages
downstream have the input their contract requires. D-52 is not amended, reopened or narrowed.

**What the release carries.** All fourteen TE §13.3 fields, populated from this run's own facts or
from a governed config field; `dataset_version` is **derived** by `write_release` from the
release's content hash (D-29) and a caller-supplied value is refused. Two shapes are recorded
because they were judgement calls, not scientific values:

* **`fold_ids` / `mask_ids` / `feature_set_ids`** carry the literal
  `NOT_YET_ASSIGNED_stage_00_precedes_splits_masks_features`. Stage 00 precedes folds, masks and
  features, so no such id exists; TE §13.3 requires all fourteen fields non-empty and
  `write_release` refuses an empty list. The token is deliberately **unusable** as a real
  identifier, so it can never be mistaken for one, and every consuming stage asserts a real id at
  its own boundary.
* **`selected_cell_bounds`** records the D-1 **cell** (integers plus bound strings), not the raw
  lat/lon floats: R-11 refuses floats in the canonical content representation, because
  platform-dependent float serialization would break the byte-identical two-platform requirement —
  and the cell, not the coordinate, is what the Phase 1 target is sampled on (D-1; D-17).

**The released file is a CSV carrying exactly the five provider columns plus the station key**, and
the writer **refuses** a row missing any of them rather than substituting a blank (D-17; R-44).
Found by execution: the first version released the rows as JSON, which
`load_released_provider_rows` **silently skips** rather than refuses, so stage 02 ran to
`completed` with `rows: 0` — a vacuous success. The consumer's silent skip is recorded here as an
observation against that function, not fixed by this decision.

**Verified by execution, 2026-09-21, CPython 3.11.16.** Stage 00 released **1,810 BSHM records**
from the November 2022 plumbing window, `dataset_version` `737a0f7ee7ea`. Stage 01 then reported
`release_manifests_found: 1` (from 0). Stage 02 **completed** and produced the first Phase 1
hourly target this project has made: **168 rows** — exactly BSHM's 168/168 hourly bins under
D-11 — spanning 2022-11-01T00:00Z to 2022-11-07T23:00Z, 158 of 168 `target_valid`, all sixteen
D-17 fields plus the lineage caveat, stamped `P1A / GNSS_VTEC / GRIDDed_VTEC_1H`.

**Transcribed on the way, both pure copies:** `configs/data.yaml: target.aggregation` (D-16's
median with its citation) and `target.contract` (D-17's sixteen fields and eight excluded classes).

**Discharges no gate.** No fixture has been measured, no receipt written, WS-20/TA-17 stay
`Pending`, and this is not a G-05 act. Change record:
`governance/CHANGE_RECORD_2026-09-21_release_option_a.md`.

---

## D-62 — `observable_codes` is not required for Phase 1 and is formally deferred to Phase 2 (ruling)

**Decision date:** 2026-09-21. **Ruled by:** the project decision owner ("`observable_codes` is not
required for Phase 1 and should be formally deferred to Phase 2"); **countersigned by the
supervisor on the student's report of the same date**. No separately signed document artifact
exists and none is claimed. **Authority:** Vision §6.2 (the station-registry field set); R-45 /
R-46; TE §7.0 (the Phase 1 hard prohibition — RINEX headers are Phase 2 material).

**Decision.** `observable_codes` is **not a Phase 1 requirement**. It remains a Vision §6.2 field
and remains **required for Phase 2**, where the RINEX headers that state it are legitimately read.
The deferral is formal: the field is not dropped, not defaulted, and not filled.

**Why it is deferrable.** No Phase 1 path consumes it — the Phase 1 target is the provider's
gridded VTEC product, which carries no observable codes — and reading a 2022 RINEX header to
obtain them would itself be Phase 2 work that TE §7.0 bars Phase 1 from performing. Recording an
invented or inferred value would be worse than the deferral, since nothing in Phase 1 could check
it.

**The mechanism already existed and is now the ruling's home.**
`src/data/registry.py: PHASE2_ONLY_REGISTRY_FIELDS = ("observable_codes",)` with
`assert_registry_resolved(..., phase=...)`: under `phase=1` the field is not required; the
**default `phase=2` is the full, unchanged R-45 check**, so nothing is weakened for Phase 2. It was
introduced under `CR-2026-09-20-B01-PREREQS` §5 with no D-number; this decision gives it one.

**A correction recorded with the ruling.** `observable_codes` was reported (2026-09-21, in this
session) as the field blocking Phase 1 registry resolution. **Measured, it was not**: under
`phase=1` the registry refused on **missing provenance values for `hardware_changes_2022` and
`igrf_version`** — presence is not provenance (R-46, W-2a) — while `observable_codes` was already
exempt. Both provenance values were transcribed the same day from sources already recorded in the
config: the official site logs' Sections 3–4 (the 2022-covering entries span the year with no
change inside it, so the empty `hardware_changes_2022` is a **measured absence**, not an unfilled
field) and the project-wide IGRF-13 pin with its coefficient-file hashes.

**Verified by execution, 2026-09-21.** With the provenance transcribed, the real
`configs/data.yaml` registry **RESOLVES under `phase=1`** and **still refuses under `phase=2`**
naming `observable_codes`. Both directions are asserted by
`tests/test_station_registry.py::test_the_real_config_registry_resolves_under_phase_1_and_still_refuses_under_phase_2`,
so a deferral that quietly became a deletion would fail the suite.

**What is owed at Phase 2.** `observable_codes` must be transcribed for all three stations from
the 2022 RINEX headers before any Phase 2 registry resolution passes. This decision creates that
obligation explicitly; it does not discharge it.

## D-63 — The seven driver-class permitted-producer identities (transcription; closes D-35 limb 3)

**Decision date:** 2026-09-21. **Decided by:** the project decision owner, by explicit instruction
("complete the configs for the 7 permitted_producers fields that need completing based on
decisions and contracts"). **Countersignature:** not required under TE §18.2 — no row covers a
producer-artifact identity; D-41's precedent (sole-signed) applies. **Authority:** D-35 (the
leakage-safe policy and its eleven contract-fixed rows, limb 3 leaving the seven driver rows
unassigned "until the driver release exists"); D-10.1 (providers); D-39 (Kp/ap product);
D-40 (Hp60/ap60 product); D-21/D-22/D-23/D-25 (F10.7 daily median and availability); TC-11
(Dst diagnostic-only); SD-F-01.

**Decision.** `configs/features.yaml: permitted_producers` carries one producing-artifact
identity for each of the seven driver-class TE §6.2 rows, the code constant
`src/external/spaceweather.py: DRIVER_PRODUCERS` being the identity's home and the config its
transcription:

| Row(s) | Producing artifact | Product the decision already fixes |
|---|---|---|
| `kp_safe`, `ap_safe` | `gfz_kp_ap_nowcast_2022` | D-39: archived settled nowcast `Kp_now2022.wdc`, DOI 10.5880/Kp.0001 (`release_status_required: nowcast`) |
| `hp60_safe`, `ap60_safe` | `gfz_hp60ap60_v2_2022` | D-40: `Hp60ap60doi_2022.txt` under DOI 10.5880/Hpo.0002 V2.0; V3.0 is a comparator only |
| `f107_safe`, `f107_81_trailing` | `nrcan_f107_observed_daily_median_2022` | D-21/D-22/D-23/D-25: NRCan observed flux, project-derived daily median (`source_series: f107_daily_median` for both rows) |
| `dst` | `kyoto_wdc_dst_2022` | D-10.1: Kyoto WDC, one release grade; still `DIAGNOSTIC_ONLY_SERIES` — a producer entry admits PROVENANCE, never a modelling role |

**Why a transcription and not a choice.** D-35 withheld these entries because an identity for a
release that did not exist "could later refuse a legitimately produced feature". Each identity
above names exactly the one provider product a prior decision already selected for that row, and
nothing else — the choice of product was made under D-39/D-40/D-21–D-25/D-10.1; this decision
only gives the chosen product the artifact name `build_features` will check. The obligation it
creates is on the (unbuilt) driver-release producer that stage 05 reads by manifest: it MUST
stamp `producing_artifact` with exactly these values, and `build_features` refuses any other
(row, producer) pair (SD-F-01).

**Verified by execution, 2026-09-21.** `load_permitted_producers(configs/)` resolves all 18
rows; `tests/test_feature_availability.py` asserts config = constant = literal transcription in
three independent statements, one producer per driver row, the definitive-grade and V3.0
identities refused by name, and `dst` diagnostic-only. Stage 05's next refusal moved from
`permitted_producers: incomplete` to its own release-input loader — the correct next
stop-and-report (TE §18.3), owned by `features-and-splits`. Change record:
`governance/CHANGE_RECORD_2026-09-21_gov_cg01_closure_pass.md` §1.

---

## D-64 — The Phase 1 prepared-VTEC evidence draws on two provider product versions; the measured distribution (census RUN; limitation recorded)

**Decision date:** 2026-09-21. **Census run by:** the agent on the project decision owner's
explicit instruction (dispositions §5 item 6; `GOV-2026-09-20-CG-01` Recommendation 8, owner
ruling Option 1). **Decided by:** the project decision owner — the STUDENT limb (the census and
its recording). **Supervisor limb** (acceptance of the limitation, §4.3 "Disposition (b)"):
**countersignature status OPEN**; not claimed. **Authority:** TE §5.1 (version or release
status per entry); TE §5.2; `team.md` DATA-07; `CR-2026-09-20-GOV-CG-01-DISPOSITIONS` §4.3,
whose `<INSERT FROM CENSUS RUN>` placeholder this decision fills.

**Measured** (`src/data/inventory.py: provider_suffix_census`, read-only over each month's
`madrigal_coverage_raw_records.csv` `file` column, dates attributed from record timestamps,
never from a directory name; printed before assertion; machine-readable copies at
`evidence/provider_version_census_2026-09-21/census_by_month.json` and, as re-measured by
stage 01, `artifacts/inventory/source_inventory.json`):

| Month | Records | `g.001` | `g.002` | Mixed | Days carrying more than one token | `g.001` days (whole provider file each) |
|---|---|---|---|---|---|---|
| 2022-01 | 20,808 | — | 20,808 | no | 0 | — |
| 2022-02 | 18,143 | — | 18,143 | no | 0 | — |
| 2022-03 | 19,097 | — | 19,097 | no | 0 | — |
| 2022-04 | 18,990 | 613 | 18,377 | **yes** | 0 | 04-21 |
| 2022-05 | 19,802 | — | 19,802 | no | 0 | — |
| 2022-06 | 18,194 | 580 | 17,614 | **yes** | 0 | 06-16 |
| 2022-07 | 18,732 | 1,712 | 17,020 | **yes** | 0 | 07-13, 07-14, 07-18 |
| 2022-08 | 19,127 | 610 | 18,517 | **yes** | 0 | 08-15 |
| 2022-09 | 18,249 | — | 18,249 | no | 0 | — |
| 2022-10 | 19,062 | — | 19,062 | no | 0 | — |
| 2022-11 | 18,183 | 1,896 | 16,287 | **yes** | 0 | 11-13, 11-28, 11-29 |

Totals over the eleven non-December months: 208,387 records; `g.001` 5,411 (nine provider
files, nine whole days); `g.002` 202,976; `records_unrecognised_version` 0 in every month.
These agree exactly with the board's own per-month figures (Recommendation 8) and are now
recorded in a governed place. **Two facts the census adds** that the board's figures did not
carry: (i) **no day mixes versions** — every `g.001` occurrence is a whole provider file
(one day), so the mix is a per-day reissue pattern, not a mid-day switch; (ii) the November
mix touches **2022-11-13, 11-28 and 11-29**, none of which lies inside D-11's plumbing window
(2022-11-01..07), so the plumbing fixture's input is single-version (`g.002`) by measurement.
**December** (the locked month, restricted root) was NOT read by this census; the board's
figure — 743 `g.003` records, all dated 2022-12-31 — stands as the board recorded it and is
re-measurable only through the audit's logged chokepoint.

**Recorded as** `release_status_versions` on each of the eleven `declared_sources` entries in
`configs/data.yaml`, which stage 01 re-measures on every run and REFUSES if the observed set
departs from the declaration (`assert_sources_unmixed_or_recorded` — the first production
call site of R-52 prohibition 2; `assert_unmixed_sources` composes the refusal).

**Disposition, per §4.3.** Option (b) is the standing default: **the mix is a limitation
bounding every claim**, stated wherever a coverage figure or comparison result from this
evidence is reported, until the provider certifies g.001/g.002/g.003 physically equivalent for
instrument 8000 kindat 3500 (option (a)), which no one has obtained. Whether the December
`g.003` day is in-contract is a question this decision records as **open** — it cannot be
settled without reading December, and reading December is a G-05-gated act.

---

## D-65 — Geomagnetic coordinates of the three stations under the pinned IGRF-13 (freeze, Q-06)

**Decision date:** 2026-09-21. **Frozen by:** the project decision owner, the Student, by
explicit instruction ("determine the IGRF coordinates, pin them, and record them in the station
contract") — TE §18.2 Q-06 assigns any station coordinate to the Student. **Supervisor
countersignature** for the Vision §6.2 registry column: **status OPEN**; not claimed.
**Authority:** Vision §6.2 ("Geomagnetic coordinates (IGRF, pinned version)" — "computed with
one pinned IGRF version"); Vision D-106 (Q-06); `GOV-2026-09-20-CG-01` Recommendation 13
(option 1); `configs/data.yaml: igrf_version = IGRF-13` (transcribed 2026-09-19).

**Decision.** Centered-dipole geomagnetic coordinates, epoch **2022.5**, from the degree-1
IGRF-13 coefficients:

| Station | Geodetic (D-1) | Geomagnetic latitude | Geomagnetic longitude (east) |
|---|---|---|---|
| ARUC | 40.286 N, 44.086 E | **35.642** | **123.046** |
| BSHM | 32.778987 N, 35.022987 E | **29.544** | **112.963** |
| NICO | 35.140989 N, 33.396450 E | **32.110** | **111.913** |

**Derivation, printed before assertion** (`evidence/igrf13_coefficients_2026-09-21/
dipole_geomagnetic_coordinates.json`): coefficient source NOAA NCEI `igrf13coeffs.txt`
(sha256 `460b8d8beb9b4df84febe4f0b639f0dd54dccfe8ff0970616287b015fa721425`, retrieved
2026-09-21; g₁⁰ = −29404.8, g₁¹ = −1450.9, h₁¹ = 4652.5 nT at 2020.0 — the same IGRF-13
2020.0 g₁⁰ the pinned iricore wheel's `igrf2020.dat` carries — with secular variation
+5.7 / +7.4 / −25.9 nT yr⁻¹), extrapolated to 2022.5: B₀ = 29,780.9 nT; north geomagnetic
pole at colatitude acos(−g₁⁰/B₀), longitude atan2(−h₁¹, −g₁¹) → **80.713 N, 287.340 E**;
MAG frame per Hapgood (1992): Z along the dipole axis, the geographic north pole at
geomagnetic longitude 180°; latitude = asin(Z-component), longitude = atan2(Y, X) in
[0, 360). Control: Boulder (40.0 N, 254.7 E) → (47.7, 322.2), the textbook value.
Sensitivity: epoch 2022.0 instead of 2022.5 moves every value by < 0.02°.

**What these are and are not.** Centered-dipole coordinates — the quantity "geomagnetic
coordinates under IGRF" denotes when nothing further is specified, computable from the pinned
generation alone with no additional dependency. They are **not** quasi-dipole, AACGM or
corrected-geomagnetic coordinates, which need a full-field tracing library the governed
environment does not pin; if a Phase 2 consumer needs one of those, it records the change
under its own D-number (`configs/data.yaml` igrf_version comment). No Phase 1 executable path
consumes these values — they satisfy the §6.2 registry contract (`Station.geomagnetic_lat` /
`geomagnetic_lon`, refused by `assert_registry_resolved` when absent or `TBD — freeze gate`,
in both phases) and describe the regime: all three stations sit at mid geomagnetic latitudes
(29.5°–35.6°), consistent with Vision §2.5's "mid-latitude Eastern Mediterranean–South
Caucasus sector" claim boundary.

**Verified by execution, 2026-09-21.** The real `configs/data.yaml` registry resolves under
`phase=1` with the two new fields and their provenance; three negative controls in
`tests/test_station_registry.py` prove an absent, a `TBD` and a non-numeric value are each
refused by name.

---

## D-49 addendum — Python 3.10 compatibility of the CODE, found and closed on the first Kaggle run

**2026-09-20.** The D-49 extension (fixture runs in the 3.10 venv) was recorded after a
dependency-level compatibility check (50-package cp310 resolution). The first Kaggle run of
revision 2 refused at `--verify-runtime` with `ImportError: cannot import name 'UTC' from
'datetime'` — a **language-level** incompatibility the dependency check did not cover:
`datetime.UTC` (3.11+) was used in 33 modules under `src/`, `scripts/`, `tests/` and
`kaggle/build_b01_package.py`, and `enum.StrEnum` (3.11+) in two. Under 3.10 every `src`
module failed to import (measured: 37/37 import failures before the change, 0/37 after).

**Closed by a mechanical, behaviour-preserving sweep, not by a new environment decision:**
`datetime.UTC` → `datetime.timezone.utc` everywhere (on 3.11 `datetime.UTC is
datetime.timezone.utc` — the same object); `enum.StrEnum` imported from the standard library on
3.11 and provided by a 3.10 backport in `src/data/config.py` (`str()`/`format()` give the
member value, as on 3.11) for `src/data/splits.py` and `src/features/transforms.py`. The
timestamp parsers already handled the `Z` suffix explicitly, so `fromisoformat` semantics are
unaffected. `ruff` rule UP017 (which would rewrite the object back to the 3.11 alias) is
ignored in `pyproject.toml` with the reason recorded there. **The main environment stays
Python 3.11** (TC-03d); the pins are unchanged; no scientific value, no config and no
declaration changed. Proof: the full suite under the governed 3.11 environment AND under a
CPython 3.10.21 environment carrying the governed pins (WSL2, diagnostic only) — counts in
`governance/CHANGE_RECORD_2026-09-20_b01_prerequisites.md` §9. The Kaggle notebook (revision
4) now runs the whole suite inside the 3.10 venv (Step 3c) before any stage runs, so a
recurrence stops the session with the junit counts rather than a stage traceback.

---

## D-50 addendum — the hmF2 diagnostic column is approved and implemented (no threshold)

**2026-09-20.** The student approved the optional hmF2 diagnostic column ("The optional hmF2
diagnostic column approved as well"). Implemented in `src/external/iri.py:build_validation_report`:
when a sample carries `official_interface_hmf2_km` (read from the official output's
`Peak Heights/km: hmF2=` line), the report records it beside `adapter_hmf2_km` (one
`iricore.iri` call at `version=16`, `oarr[1]`, same index files and default switches as the
TEC call) and `hmf2_diff_km_diagnostic_no_threshold`. **The column never enters
`within_tolerance`**; a sample without the official value records nulls. The tolerance of
D-50 is unchanged. Test:
`tests/test_external_drivers.py::test_b01_validation_report_records_the_hmf2_diagnostic_without_a_threshold`.

---

## D-51 addendum — countersignature statement of record

**2026-09-20.** The student states, in the same reply, that items 3 and 5 of the freeze
package "are both approved by student and supervisor also countersigned". For D-51 this is
recorded as the **student's statement that the supervisor countersigned**; it is stronger than
the delegation D-51 was first recorded under, and D-51's paragraph "Governance condition,
stated precisely" is superseded to that extent. What is still true and still stated: no signed
document, email or minute from Dr. Reza Saraf Shirazi is held in this repository, and none is
represented as existing here — `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md` is the
pattern for lodging one. Item 3 (the feature dictionary and normalization) had **no value on
record to countersign** when the statement was made; see
`CR-2026-09-20-B01-PREREQS` §9 for the proposed D-53 text that the countersignature can attach to.

---

## D-1 addendum — countersignature status of the coordinate-to-cell rule

**2026-08-21.** D-1's decision text is unchanged and remains accurate: a station maps to
the 1°×1° Madrigal bin identified by its lower-left floor corner,
`cell = (floor(lat), floor(lon))`, tested **half-open** as \([floor, floor+1)\) on both
axes — so a station exactly on a boundary belongs to the higher-indexed cell, and no
station is counted in two cells. The three assignments are ARUC 40/44, BSHM 32/35,
NICO 35/33, verified against executed 2022 output.

**What was corrected.** `requirements.md` open question 2 previously described the cell
rule as *"currently a self-labelled 'PROVISIONAL' inline function in the coverage
notebook"*, implying no freeze existed. D-1 **is** the freeze. The notebook literal is a
duplicate of a frozen decision awaiting migration into `configs/data.yaml` and
`src/data/registry.py` (REQ-ENG-8), not the decision itself.

**Governance condition, stated precisely.** TE §18.2 classes the coordinate-to-cell rule
as a **Student + Supervisor** forbidden choice, so D-1 requires approval from both roles.
The project owner approves it, 2026-08-21, and the standing student/supervisor authority
equivalence recorded for this workspace is the documented delegation under which the
supervisor role is exercised. On that basis the governance condition **is closed**, and
the signature row is completed accordingly.

**No signature is forged.** No signed document, email or minute from Dr. Reza Saraf
Shirazi exists for D-1, and none is represented as existing. If the examining committee
requires an independent supervisor signature distinct from the delegation, that
requirement is outside this repository's control and would have to be satisfied
separately; this addendum records the delegation actually relied on so a reader can judge
it.

**Separate and still open:** D-1's own recorded limitation. The station coordinates came
from IGS network pages rather than the official IGS site-log PDFs, which rank higher in
the Vision §6.2 evidence hierarchy. All three stations sit ≈0.14° or further from a cell
edge, so a small coordinate correction would not change any assignment, but site-log
validation remains outstanding (FR-P1-02-1, gate G-02).

---

## Supervisor review

D-3/D-144 is countersigned as of 2026-08-15 and **expressly approved 2026-08-21**
(see the D-3 row). D-2 is **approved 2026-08-21**. Every other decision above
remains independently reversible. **D-1 remains uncountersigned** although TE
§18.2 makes the coordinate-to-cell rule a Student + Supervisor forbidden choice,
and twelve acquired months plus D-11's fixture already rest on it — flagged by
`GOV-2026-08-20-RA-01` finding `DATA-05`/`TEC-04` and not yet ruled on. The supervisor may countersign the remaining items
as a whole, or overturn individual items — D-2 (threshold set with partial
sight of the data) and D-3 (taken on five months rather than twelve) are the two most
exposed to challenge and should be read first.

| Item | Countersigned | Date | Notes |
|---|---|---|---|
| D-2 Coverage minimum | **Yes** | 2026-08-21 | **Approved 2026-08-21 by the project owner** under the recorded student/supervisor authority equivalence; no separate supervisor signature artifact exists and none is claimed. Approval accepts the interim rule (≥95% of calendar days per month, 100% of December) as the G-P1A acceptance criterion until Vision §6.1B's numerical minimum is frozen under its own D-number. **The disclosure above stands unaltered:** this threshold was set after five of twelve months had been seen at 100% day coverage and was not set blind; a reviewer should discount it accordingly. Raised as item 2 of `governance/COUNTERSIGNATURE_REQUEST_2026-08-21.md`; closed by `governance/reviews/GOV-2026-08-21-RA-01.md` Rec 5. |
| D-3 D-144 source adoption | **Yes** | 2026-08-15 (recorded); **expressly approved 2026-08-21** | The 2026-08-15 entry was recorded as reported by the student, with **no signature artifact** (signed document, email or minute) filed in this repository, while Vision v4.2 §14.2 still carried D-144 as "Decision required". That conflict is closed by an express approval given **2026-08-21 by the project owner** under the recorded student/supervisor authority equivalence — see `governance/CHANGE_RECORD_2026-08-21_D-144.md` for the Vision §15.2 six-field record. No supervisor signature artifact exists and none is claimed. **Approval of D-144 does not freeze the four values Vision line 1357 attaches to it:** experiment/kindat and VTEC parameter/units (D-4), coordinate-to-cell rule (D-1, row below still blank), hourly aggregation statistic (`TBD`, Vision §6.6), numerical coverage minimum (`TBD`, Vision §6.1B). |
| D-4 Parameter set | | | |
| D-5 Gap policy | | | |
| D-6 Citation form | | | |
| D-7 Hourly resolution | | | |
| D-8 Claim scope | | | |
| D-9 Acquisition route | | | |
| D-10 Driver sources / leakage | | | |
| D-11 Fixture window | n/a | 2026-08-16 | Q-31 is Student-owned per TE §18.2; no countersignature required |
| D-12 §6.1B coverage minimum | **Yes** | 2026-08-21 | Approved by the project owner under the recorded student/supervisor authority equivalence. Promotes Vision §6.12's 90% hourly aspiration to a hard G-P1A gate alongside D-2's day rule. Frozen before any model performance existed. |
| D-13 H4 / SRQ-5 demotion threshold | **Yes** | 2026-08-21 | Approved by the project owner under the recorded authority equivalence. Reuses Vision §9.3's three-independent-storm-event rule; introduces no new number. |
| D-14 Scientific fixture window | n/a | 2026-08-21 | Q-31 is Student-owned per TE §18.2; no countersignature required. March 2022, all three cells. |
| D-15 Custody relocation | **Yes** | 2026-08-21 | Approved by the project owner under the recorded student/supervisor authority equivalence. 21 files moved, all verified byte-identical. |
| D-16 Hourly aggregation statistic | **Yes** | 2026-08-21 | Approved by the project owner under the recorded authority equivalence. Median frozen; zenith-weighted declared as a sensitivity and deferred as not computable from the five-column product. TE §18.2 Student + Supervisor item, exercised under the recorded delegation. |
| D-17 Phase 1 target-row contract | **Yes** | 2026-08-21 | Approved by the project owner under the recorded authority equivalence. TE §18.2 Student + Supervisor item (support thresholds), exercised under the recorded delegation; four thresholds left as explicit freeze-gate holes rather than defaulted. |
| D-18 Year re-merge and merge determinism | **Yes** | 2026-08-21 | Approved by the project owner under the recorded authority equivalence. Executed and verified; prior artifact preserved. |
| D-19 Phase 1 support thresholds | **Yes** | 2026-08-21 | Approved by the project owner under the recorded authority equivalence. TE §18.2 Student + Supervisor item (Q-12), exercised under the recorded delegation. Values measured from January–November only; December excluded by construction. |
| D-1 Cell convention | **Yes** | 2026-08-21 | Approved by the project owner under the recorded student/supervisor authority equivalence — see the D-1 addendum above. No supervisor signature artifact exists and none is claimed. The IGS site-log validation limitation recorded in D-1 remains separately open. |
| D-20 Plumbing fixture station | n/a | 2026-08-22 | Q-31 is Student-owned per TE §18.2; no countersignature required. BSHM 32/35 selected on complete 168/168 measured coverage. Closes BLK-02's station limb; supplies no manifest content. |
| D-21 F10.7 daily value + availability | **Yes** | 2026-08-22 | Approved by the project owner under the recorded authority equivalence. TE §18.2 Q-16/Q-17 item, exercised under the recorded delegation. Daily median frozen; observation-availability rule enforced and derived; **provider publication latency remains open** (EC1-R-4) and is not claimed to be covered. |
| D-22 F10.7 duplicate-UT handling | **Yes** | 2026-08-22 | Approved by the project owner under the recorded authority equivalence. Mean of duplicates with count logging and a QC flag; provider-correction precedence recorded as a standing rule but **currently unexercisable** — the file carries no correction or provenance column. No day discarded. |
| D-23 F10.7 high-spread handling | **Yes** | 2026-08-22 | Approved by the project owner under the recorded authority equivalence. Flag-and-retain on four measured dates; median is the representative value; the QC flag is **not** a model feature without separate approval and a causality check. |
| D-24 Canonical protected set | **Yes** | 2026-08-22 | Approved by the project owner under the recorded authority equivalence. Deduplicated union of TE §2.2 (12) and §7.0B (16) with `history window`, `station encoding` and `baselines` added explicitly; **cardinality 17, calculated from the enumeration**. Closes BLK-06's enumeration limb; triggers a Vision §15.2 amendment to FR-P1-06-1 (14 → 17). Implementation stays gated by G-09. |
| D-25 F10.7 availability convention | **Yes** | 2026-08-22 | Approved by the project owner under the recorded authority equivalence. Conservative convention: a daily median becomes available no earlier than `00:00 UTC` on the following day. **An explicit project assumption, not a demonstrated publication latency**; no operational real-time availability is claimed. **Requests, but does not take,** a §15.2 amendment to TE §7.0A stage 4 and EV-12; until granted, EV-12's F10.7 limb is unmet at G-04. *[Annotated 2026-09-19 (P-5, `CR-2026-09-19-SCI-DECISIONS`, owner-authorised): the amendment was GRANTED AND APPLIED 2026-08-22 under `CR-2026-08-22-EV-12` — see the D-25 body; the "requests, but does not take" wording is the pre-grant state and is kept as history. The grant covers the EV-12 row shape only.]* |
| D-26 F10.7 March–April provenance | **Yes** | 2026-08-22 | Approved by the project owner under the recorded authority equivalence. Provenance recorded **UNRESOLVED**; data retained; measured / reconstructed / interpolated / provider-corrected asserted in **no** direction. Carries a thesis reporting obligation. Identifies two clarification routes and an `ABL-NOSW`-style sensitivity — **none approved or scheduled** by this decision. |
| D-27 Primary target untransformed; inverse is ABL-DIFF's | **Yes** | 2026-08-24 | Approved by the project owner under the recorded authority equivalence, at the delivery-planning approval gate. **A reading of frozen text, not a new scientific value.** The primary train-only transform touches target-derived inputs, not the target, which stays **raw TECU** (TE §7.2 `ABL-DIFF`: *Primary remains, Raw TECU*). Primary path needs no inverse; `ABL-DIFF` alone transforms the target and keeps its inverse-before-metrics obligation with error propagation recorded. Raised by blocker BLK-08; narrows but does not close its mechanism limb, which stays with `functional-design`. |
| D-28 G-06 locked-test scored set = 2–31 Dec (30 d) | **Yes** | 2026-08-28 | Approved by the project owner under the recorded authority equivalence, at the `functional-design` (3.1) governance gate on `GOV-2026-08-28-FD-01` Rec 6. **Ratifies FU-7 = A (2026-08-26), already built upon by eight units.** Basis is `requirements.md` FR-P1-04-5 + ADR-11's `lead_in_hours` removal; **discloses that Vision §8.2 and TE §7.1 both carry `—` in the Locked-test Embargo column**, so a level-4 paraphrase is the sole textual basis — conflict recorded, not resolved, and carried to G-05. Accepted on three grounds: 1 Dec is furthest from solstice; the bootstrap loses 1 of 31 blocks (conservative); and 720 h divides by 48 where 744 h does not, so the mandatory 48-h sensitivity would have raised under the 31-day reading. **No supervisor signature exists or is claimed.** A revised split manifest is owed at G-05. **AMENDMENT DRAFTED AND REVERTED, both 2026-09-24 (recorded rather than erased, per this project's history-preserving convention):** A same-day amendment briefly changed this entry to "29 days" (Layer-2 §2 option B, zero-additional-December-contact), on the rationale that the mandatory persistence baselines M-01/M-02 cannot forecast 2 December without reading 1 December history. That amendment was **reverted the same day** — it conflicted with **D-59** (Student+Supervisor countersigned 2026-09-21), which independently freezes the December day range at 30 days, is live in `configs/experiment.yaml:376`, and is enforced by `src/evaluation/regimes.py:read_december_day_range`; the amendment also had no code path that could actually produce "29 days" without either building a new December-specific exclusion mechanism or incorrectly widening the shared, Mandated 24-hour fold `embargo_hours` used by every partition. Full analysis in `governance/CHANGE_RECORD_2026-09-24_d28_29day_amendment.md` (left standing as the historical record of that analysis). **Superseded by option (b), ruled 2026-09-24: the original 30-day D-28 statement stands unchanged, and the true fix is the bounded 1-December lookup read specified in `RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md` §2 Option A** — drafted at the time but never implemented — which recovers the full, disclosed 30-day scored set for M-01/M-02 without amending D-28, D-59, or any other existing decision. That mechanism's own draft D-number and implementation are recorded separately (see `governance/CHANGE_RECORD_2026-09-24_d28_option_a_bounded_read.md`); **this D-28 entry itself needs no further change** — it is back to, and stays at, its original 2026-08-28 text. |
| D-29 `dataset_version` = 12-hex prefix, verified on write | **Yes** | 2026-08-28 | Approved by the project owner under the recorded authority equivalence, at the `functional-design` (3.1) governance gate on `GOV-2026-08-28-FD-01` Rec 42 (board option 2). Encoding **12 hex** from `content_hash`; collision bound **recorded** (~1.8e-9 at n=1,000; ~1.8e-7 at n=10,000) but **never relied on** — the verify-on-write prefix check is what establishes never-reuse, raising `ReleaseError` on collision. **No release ledger introduced.** Unblocks `write_release` at 3.5 and closes two of `foundation` R-12s three open items (injectivity, `verify_release`). **TA-15 is still NOT covered and this decision does not cover it** — `tests/test_release_hashes.py` exercises none of §13.3s manifest fields and not R-13s overwrite refusal. **No supervisor signature exists or is claimed.** |
| D-30 `.dst_summary.json` relocation | **Yes** | 2026-08-28 | Approved by the project owner under the recorded authority equivalence, on `GOV-2026-08-28-FD-01` Rec 44(b) (board option 2). Moves the file into `evidence/audit_ec1_2026-08-15/kyoto_dst/`, inside R-27s scan root, verified byte-identical on the D-15 method with the access-log row written **before** the move. Makes `governance-guards` R-26 driver-exclusion **class 4 unconditional**. **Not a December read** — bytes and hash only, no field parsed. Changes no value and approves no new input; Dst stays diagnostic-only. **No supervisor signature exists or is claimed.** |
| D-31 G-09 Agent preflight SIGNED | **Yes** | 2026-08-28 | **Signed and approved by the project decision owner**, in session, under the recorded student/supervisor authority equivalence. **Recorded WITH its §18.3 preconditions disclosed as UNMET**: `configs/`, `src/` and `pyproject.toml` do not exist, so the mandated automated zero-TBD preflight **cannot run**; the ten named critical tests **cannot be executed** (no Python interpreter is installed in this environment); and the evidence artifact `aws_ai_dlc_preflight_report` **does not exist**. "No failing critical test" is therefore **unproven, not proven**. **Unblocks** module creation and the two defects deferred solely on G-09 (TA-15s §13.3 field coverage and R-13 overwrite refusal; routing the two unlogged restricted reads through `open_restricted`). **Does NOT unblock** G-05, G-06, G-P1A, G-P2, G-P3A/C or G-07, and does not relax TE §18.2s absolute rule or §18.3s standing stop-and-report obligation. **No independent supervisor signature artifact exists and none is claimed.** |
| D-32 All eight §15.2 acceptance rows approved | **Yes** | 2026-08-28 | Approved by the project owner under the recorded authority equivalence, on `GOV-2026-08-28-FD-01` Rec 22, **board option 1** (the boards own recommendation). All eight approved, **none deferred**: FR-P1-04-15, FR-P1-04-18, FR-P1-05-7, FR-P1-05-20, `TST-CLAIMS-01`, FR-P1-05-19, FR-P1-05-16, FR-P1-05-18. Closes the `GOV-F-06` interval that options 2 and 3 would have left open. **Approval creates the bar and discharges nothing** — none of the eight is executable today because no producing code exists, which was true of every option. **No scientific value is decided**: FR-P1-04-18s interpolation method stays a §18.2 Student-owned forbidden choice (Q-15) and FR-P1-05-18s disturbed-hour minimum stays supervisor-owned. A Vision §15.2 amendment to the §16/§19 tables is **owed**. `models-and-baselines` inline acceptance form stays excluded and open. **No supervisor signature artifact exists and none is claimed.** |
| D-33 cell_rule identifier + config transcription | **No — TE §18.2 countersignature REQUIRED and NOT YET GIVEN** | 2026-09-10 | Adopted as drafted by the project decision owner on the 2026-09-10 ruling (`CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md` §2, draft D-A). Freezes the EXISTING convention only: 1°×1° cell by its lower-left (floor) corner, half-open on both axes, identifier **`floor-half-open-d1`** (already `CELL_RULE_ID` in `src/data/registry.py`), transcribed into `configs/data.yaml`. **No station moved, no grid resolution changed, `stations` NOT resolved** (still `TBD — freeze gate`, coordinates still PROVISIONAL). **The Madrigal bin-edge confirmation remains OWED** and is a recorded limitation of the freeze. TE §18.2 makes this a Student + Supervisor forbidden choice: **no signed document from Dr. Reza Saraf Shirazi exists for D-33 and none is claimed**; see the D-1 addendum for D-1's own closure under the recorded authority equivalence, which this decision does not extend to itself. |
| D-34 Practical relevance — no threshold set | **Yes** | 2026-09-10 | Adopted as drafted (§3, draft D-B). **No numeric threshold is set anywhere**; the frozen object is the PROTOCOL (Vision §5.4 + PC-09): 10% is a named reference magnitude, not a pass/fail rule; descriptive reporting unless the supervisor explicitly approves a threshold; any approved threshold may not sit below the §6.9 target uncertainty budget; **no threshold may be introduced, changed or reinterpreted after December is opened**; significance and usefulness stay distinct. `configs/experiment.yaml: practical_relevance_threshold` **keeps its `TBD — freeze gate` sentinel**, which now records the DECIDED state "no threshold approved". Any future numeric needs a **separate governance act with explicit supervisor approval** and its own D-number. No supervisor signature exists or is claimed — none is required, because no threshold is approved. |
| D-35 Permitted-producer policy + eleven rows | **Yes** | 2026-09-10 | Adopted as drafted (§4, draft D-C). Freezes the **leakage-safe policy** (available at the forecast origin; no future target TEC; no locked-December access; declared safe lags respected; no future information via preprocessing, train-only fitting; deterministic where required; 1-hour-ahead compatible; no IRI-derived anything) and the **eleven rows whose producing artifact the implemented contract fixes**: `vtec_lag`/`vtec_seq_24`/`target_support` → `phase1_hourly_target`; the four time rows → `record_timestamp`; the four station rows → `station_registry`. The **seven driver rows (`kp_safe`, `ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe`, `f107_81_trailing`, `dst`) REMAIN DEFERRED and fail closed** — not rejected, but unassignable without inventing a provider artifact identity (D-10.1 fixes providers, TE §6.2 says "GFZ or approved source" for Hp60/ap60). **`dst` stays diagnostic-only and is never an ML feature**; **R-78 is unchanged** (no support field admitted). Transcription of already-governed contract; no scientific value set. No supervisor signature exists or is claimed. |
| D-36 TensorFlow pin `tensorflow==2.21.0` | **Yes** | 2026-09-10 | Adopted as drafted (§5, draft D-D); the owner selected the version. `requirements.txt` carries `tensorflow==2.21.0`, the CPU wheel (TC-01), the ONE neural stack (TE §8.3), matching the tf.keras 2.21.0 candidate API `src/models/lstm.py` was written against. **PINNING IS NOT VERIFICATION**: installation, import and API-compatibility checks have **NEVER BEEN EXECUTED** (PyPI unreachable, verified 2026-09-10); no TensorFlow import has ever succeeded here; **TE §8.1's both-platform (Kaggle AND local) condition is UNMET and the Kaggle compatibility check is OWED**. The guard now passes on the governed file; its refusal of an absent or commented-out pin is unchanged. No M-06 fit has run; TA-26 stays `Pending`. No supervisor signature exists or is claimed. |
| D-38 Split configuration transcribed (`partitions` + `embargo_hours`) | **Yes — jointly authorized by Kimia Rezaei (owner/student) and Dr. Reza Saraf Shirazi (supervisor), 2026-09-10; joint instruction of record, no separately signed artifact exists or is claimed** | 2026-09-10 | Transcription only; **no scientific value chosen**. `configs/data.yaml: partitions` takes the six ids of R-80's closed space (F1 2022-01-01→2022-03-31/Apr; F2 →2022-06-30/Jul; F3 →2022-09-30/Oct; F4 →2022-10-31/Nov; REFIT →2022-11-30/null, scored nowhere per FR-P1-04-14; DEC →2022-11-30/Dec), and `configs/experiment.yaml: embargo_hours` takes **24** from TE §7.1's Embargo column. **Provenance kept distinct:** F1–F4 and REFIT are specified DIRECTLY by TE §7.1; **DEC's training bounds are NOT** — TE §7.1 shows "—" there, so they are DETERMINED by `train_start == study_start` (D-8) and `DEC.train_end == REFIT.train_end` (R-80), one admissible value each. **`experiment.yaml: folds` stays `TBD — freeze gate` deliberately** (no reader exists anywhere; populating it would create a second source of truth for the same calendar). Verified against the project's own unmodified `build_partitions` — six accepted, every structural rule exercised, and a control with an unresolved embargo still refused. `pyyaml` uninstallable here (PyPI egress blocked), so a full `load_configs` run is **owed in a governed environment**. Discharges no gate: **BLK-02 OPEN**, the two Q-31 freeze acts remain the owner's, WS-20/TA-09/TA-17/TA-21 `Pending`. |
| D-37 D-27 affirmed; BLK-08 mechanism limb closed | **Yes** | 2026-09-10 | Adopted as drafted (§6, draft D-E); the owner chose Choice B, affirm the withholding. **A REAFFIRMATION, never a supersession — D-27 stands, unreopened and unamended.** D-27's withholding of a general inverse route is affirmed permanently: **the refusal IS the mechanism** (R-139 control 25 preserved at full strength); **R-103's joint contract is adopted in D-27's identity form**, the primary path's citable route being **`identity (D-27: primary target untransformed)`** because its output is already raw TECU; **`ABL-DIFF` keeps the only real inverse** with error propagation recorded (TE §7.2). **No generic inverse-transform route is created, no `inverse`/`apply` added to any transform, and no import-boundary change is authorised.** **BLK-08's mechanism limb is CLOSED by this decision; BLK-02 stays OPEN.** No supervisor signature exists or is claimed. |
| D-39 Kp/ap product: archived settled nowcast selected; definitive = audit comparator | **No — student decision only; supervisor countersignature status OPEN** | 2026-09-18 | Approved by Kimia Rezaei (owner/student) in-session with binding qualifications, recorded as a student decision: `Kp_now2022.wdc` (DOI 10.5880/Kp.0001, sha256 `7929d16a…7475a4`) is the selected historical product; `Kp_def2022.wdc` (`c1d90302…c2b829`) is the audit comparator only and never a forecast-time feature. **Limitation binding:** the archived nowcast is the settled final-stage nowcast, includes post-issue revisions, does not reconstruct first-issued values, and is **not** labelled proven-available at every forecast origin. **Before producer release** the availability rule must be established from evidence or the limitation explicitly documented with its implications; no publication lag invented, no silent config change (`availability_lags` stays `TBD`). Measured 1,046/2,920 epochs differ — a product-version difference, not model error, not proof of leakage. **G-04 NOT passed; no producer artifact; no `permitted_producers` row. No supervisor approval exists or is claimed.** |
| D-40 Hp60/ap60 product: Hpo.0002 V2.0 selected; Hpo.0003 V3.0 = recomputed comparator; substitute control | **No — student decision only; supervisor countersignature status OPEN** | 2026-09-18 | Same approval as D-39. `Hp60ap60doi_2022.txt` under DOI 10.5880/Hpo.0002 (V2.0, sha256 `0ad71bf0…471ad6`) is the selected historical version; under DOI 10.5880/Hpo.0003 (V3.0, `a689ddef…65d461`) the later-recomputed comparator only. Their comparison is the accepted **documented substitute** for R-63 control 5 for Hp60/ap60 ONLY, labelled exactly "Contemporaneous V2.0 versus later algorithm-recomputed V3.0" — **not** NRT versus definitive; establishes neither first-issue availability nor absence of leakage. Measured 1,790/8,760 epochs differ — product-version difference only. **G-04 NOT passed; no producer artifact; no `permitted_producers` row. No supervisor approval exists or is claimed.** |
| D-41 Q4/Q5: Hp60/ap60 provider GFZ Potsdam; three producer-artifact identities and roles | **Not required under TE §18.2 (no row covers a driver source version or producer identity; D-10.1 precedent, sole-signed) — student decision** | 2026-09-18 | Approved by Kimia Rezaei (owner/student) in-session after checks 3 and 4 agreed with the existing contracts. Identities `gfz_kp_ap_3h_2022_v1` (from D-39's `Kp_now2022.wdc`, `7929d16a…7475a4`), `gfz_hp60_ap60_1h_2022_v1` (from D-40's Hpo.0002 V2.0, `0ad71bf0…471ad6`), `srmp_f107_observed_daily_2022_v1` (from `fluxtable.txt`, `4b7fbfde…d690b9`); definitive Kp/ap and Hpo V3.0 are audit comparators only; `f107_81_trailing` is DERIVED (trailing, never centered; anchor at the safe-lagged day; TC-20 never filled), not a raw artifact; the F10.7 manifest cites `availability_rule = previous_day_median_midnight_utc` (D-25 Route 1), which resolves F10.7 only. **Output hashes UNSET until the outputs exist.** **Identities and roles only: no temporal availability approved, no `*_safe` feature certified leakage-free, no producer release, no `permitted_producers` row, G-04 NOT passed.** Availability obligations (D-39 item 4 / D-40) are TE §18.2 Q-16 Student + Supervisor items and stay open. |
| D-42 GFZ driver availability floors accepted as project assumptions (retrospective study) | **Student states supervisor countersigned, 2026-09-19** (`COUNTERSIGNATURE_REQUEST_2026-09-19.md`) — TE §18.2 Q-16/Q-17 | 2026-09-19 | Qualified student acceptance (A1): the existing approved floors — Kp/ap 3 h, Hp60/ap60 1 h — are the availability assumptions for the D-39/D-40 archives; they are project assumptions, not demonstrated publication or revision-completion bounds, and do not make settled archive values historically available at those lags. **Binding limitation propagated to methods and result claims:** results using these archives do not establish exact operational replay or absence of revision-related look-ahead (`DRIVER_AVAILABILITY_LIMITATION_STATEMENT`; claims-checklist row D-42). Evidence form = D-25/EV-12 pattern. **G-04 NOT passed; no producer release; no leakage-free certification.** *[Corrected 2026-09-19, `CR-2026-09-19-SCI-DECISIONS-P2`: "No config transcribed" and "No supervisor approval exists or is claimed" described the pre-2026-09-19 state. The six-entry `availability_lags`/`carry_forward_*` configuration was transcribed 2026-09-19 (item 6), and supervisor approval was REPORTED (later, the student stated the countersignature itself) by the student 2026-09-19 (`COUNTERSIGNATURE_REQUEST_2026-09-19.md`) — see this row's status column.]* |
| D-43 Interval semantics of the GFZ lag floors: margins after interval COMPLETION | **Student states supervisor countersigned, 2026-09-19** (`COUNTERSIGNATURE_REQUEST_2026-09-19.md`) — TE §18.2 Q-16 | 2026-09-19 | New clarification (P-1), not a restatement of D-42: observation interval = provider `[start, end)` with both boundaries preserved; safe-lag reference instant = interval END (completion); Kp/ap available at end + 3 h, Hp60/ap60 at end + 1 h; assumptions for retrospective evaluation, establishing no historical publication or revision-completion time. |
| D-44 One lagged-selection owner per driver kind; alignment contract for `*_safe` series | **Not required for the mechanism (no TE §18.2 row); applies D-43's semantics, countersigned 2026-09-19** | 2026-09-19 | `select_lagged_series` applies the lag once; source interval, `available_at`, origin and value kept in separate fields; `assert_lagged_selection` amends R-76a for lagged series; `build_features` shifts nothing and refuses a lag mismatch. Verified by synthetic tests. |
| D-45 IRI-2016 benchmark: standard index inputs, disclosed retrospective climatological reference | **Student states supervisor countersigned, 2026-09-19** (`COUNTERSIGNATURE_REQUEST_2026-09-19.md`) — TE §18.3 "the IRI role"; Vision §6.11 | 2026-09-19 | `iricore` `version=16`, `vtec(htop=2000)`, shipped `apf107.dat`/`ig_rz.dat` pinned by hash, no `oarr` overrides; inputs verified: adjusted 20 UT target-day F10.7, centered 81-/365-day means, centered IG12/Rz12, target-day ap. Not a forecast; comparison on identical targets/rows with the information asymmetry disclosed; no operational-superiority claim. *[Corrected 2026-09-19, `CR-2026-09-19-SCI-DECISIONS-P2`: the dependent patch (`governance/proposed/P-3_iri_report_confirmations.patch`) was APPLIED 2026-09-19 to `src/external/iri.py`, verified to match this decision; benchmark generation itself stays blocked at R-59 limb 1 (no passing validation report exists) and `iricore` remains uninstallable in this local environment (see the same change record).]* *[Annotated 2026-09-19 on owner authorization: runtime verified on Kaggle — `iricore==1.8.0` wheel `f452b22316891d87ee766dba266de6a07e4e6008ab515ffed902ea8b5446a874`, CPython 3.10.12; index-file pins `apf107.dat` `cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674` (to 2024-03-06), `ig_rz.dat` `fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486` (updated 2024-03-07); 2022 inputs identical to the earlier-inspected copies; no supervisor signature claimed; G-04 not passed — see the D-45 annotation.]* |
| D-46 F10.7 missing-update composition: reading B (clock hours, inclusive 3 h from the expected availability instant) | **Student states supervisor countersigned, 2026-09-19** (`COUNTERSIGNATURE_REQUEST_2026-09-19.md`) — TE §18.2 Q-16/Q-17 | 2026-09-19 | Ordinary reuse of `median(D−1)` on day D is not carry-forward; missing update → carried at 00–03 inclusive, excluded from 04:00 until a valid update; clock from 00:00 D; `f107_81_trailing` never imputed → whole affected day lost when both rows are present. Measured Jan–Nov 2022: 8016 origins, 0 affected; sensitivity protocol stops at Step 0. Implemented. *[Corrected 2026-09-19, `CR-2026-09-19-SCI-DECISIONS-P2`: "config transcription pending (item 9)" described the pre-2026-09-19 state; the six-entry configuration was transcribed 2026-09-19 (item 6 of that record) — `carry_forward_bound_hours`/`carry_forward_composition` are now set in `configs/features.yaml`.]* |
| D-47 Recomputation tolerance 8.0e-12 sfu, certified for constituents ≤ 400 sfu | **Not required (Q6 numerical parameter of the Student's window contract)** | 2026-09-19 | (N+1)·2⁻⁵²·B = 7.28e-12 rounded up; ε = 2u explained; verified against an exact `Fraction` reference (max 1.9e-13), repr round trip, must-fail perturbations; B = 400 is an applicability condition — out-of-domain constituents fail the certification clearly and are never clipped. *[Corrected 2026-09-19, `CR-2026-09-19-SCI-DECISIONS-P2`: "transcription pending (item 9)" described the pre-2026-09-19 state; `window.recomputation_tolerance` and `window.recomputation_input_bound_sfu` were transcribed into `configs/features.yaml`'s `f107_81_trailing` row 2026-09-19 (item 6 of that record).]* |
| D-48 December custody scan: structural detection; driver-exclusion class 5 with content + provenance conditions | **Not required — R-26 class list amended by the owner under the D-30 precedent; no target value involved** | 2026-09-19 | Structural detection for JSON (`{y, m}`, month keys, literals), WDC/Hpo/isprint/CSV formats; Markdown reported as outside automated inspection; class 5 = `audit_gfz_*` raw captures + comparison report, content-validated and provenance-checked, fail-closed on mixed content; narrower than the prepared text; excluded files inventoried as exposure, never licensed for use. Implemented and verified. |
| D-49 B-01 execution-environment exception: CPython 3.10.12 for the isolated Kaggle IRI-2016 environment only | **Owner approval 2026-09-19; no supervisor signature claimed** — TE §8.1 / TC-03d excepted for one environment | 2026-09-19 | `iricore==1.8.0` cp310 wheel `f452b223…`; index pins `cdf4d5df…` / `fbbed304…`; scope excludes training, fixtures, every other stage; fixture-receipt identity coupling recorded, unresolved (two admissible resolutions) |
| D-53 Documented-QC list closed at five operations | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | `configs/data.yaml: qc_operations` frozen at five: `reject_unexplained_negative_vtec` (R-71 content 2 / NFR-DQ-01) and D-19's four threshold checks — three marking `target_valid: false` with a reason, one flag-only. **All five were already approved and already implemented; the NEW act is the CLOSURE**, so an operation outside the list fails like a fifth transformation (R-64). **No threshold invented, no provider value modified.** `preserves_provider_values: true` and `gap_policy: explicit_nan_never_filled` (D-5, D-10.2) recorded so their absence is not read as omission. **Also transcribed:** `target.support_thresholds`, all four D-19 rows with their measured basis and `basis_window: January-November 2022` (December excluded by construction in D-19's own measurement). Verified by execution 2026-09-21 including a fifth-operation refusal control. |
| D-54 Top-1% sensitivity: 0.01, comparison-wide, one shared retained set | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | Closes `GOV-2026-09-20-CG-01` Rec 21 / dispositions §5 item 14. `removed_fraction: 0.01`, `scope: comparison_wide`, combination `rank_by_max_member_error` (exactly `k = ceil(0.01·n)` rows removed, so the declared 1% holds exactly). **Same retained rows for every compared model**; equal-station-weighted metrics recomputed on the remainder; **removed/retained counts per station mandatory**; an **undefined comparison refused** when a station retains no rows. Ranking variable, tie handling and `ceil` rounding unchanged. **Bounded: supplementary sensitivity only — never changes the primary results, selects a model, or tunes a parameter.** Required four new functions because the existing path ranked a single member's own errors, which would have scored each model on a different support (NFR-FAIR-01). **Recorded before locked evaluation.** |
| D-55 M-03 climatology: station-and-hour mean, training-only | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | Closes `GOV-2026-09-20-CG-01` Rec 2. Key = **station, hour**; `fitted_on: training_partition_only`; **month REMOVED**. A month-bearing key can predict for **no** scored month — under the expanding-window splits every validation month lies after its own training range — and M-03 is a mandatory difficulty control, so that emptied the comparison-wide mask. **Mandatory limitation wherever M-03 is reported:** a station-and-hour mean carries no seasonal term and is not a seasonal climatology. UTC hour of `interval_start_utc` unchanged (D-16/D-17). The module refuses an unimplementable key field **by name**, refuses a reordered key, and refuses any other `fitted_on` as a `LeakageError`; missing keys stay missing, never filled. |
| D-56 Refit epoch rule: median best-validation epoch, half up | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | Closes `GOV-2026-09-20-CG-01` Rec 5's rule limb. **The rule is the frozen object; the number is its output.** Median best-validation (restored) epoch across F1–F4 and the final seeds for the selected configuration, rounded **half upward** by integer arithmetic. `models.refit.epochs` stays `TBD — freeze gate` **deliberately** — the value cannot exist until the folds have run, is transcribed under its own D-number before the final refit and before G-05, and is **not required before the validation runs that produce it**. The refit trains for exactly that many epochs on January–November data with **no validation set and no early stopping**; **December is inference-only**. `assert_refit_epochs_match_rule` refuses a transcribed value that is not the rule's output. Verified: `[5,7,8,10] → 8`. |
| D-57 `window_length_hours` = 24 | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | **Transcription, not a choice** — Vision §8.1 ("History window: 24 hours primary … History length is not a tuned hyperparameter") and TE §7.2's ablation table, where ABL-HIST48's `primary_remains` reads 24 h. Same class of act as D-38 (`embargo_hours`) and D-51 (`horizons`). The 48-hour variant reaches the pipeline only as ABL-HIST48, after the primary freeze. Verified by execution: `read_window_length(…, sequence_steps=24)` returns 24 and a mismatched sequence length still raises `LeakageError` — the transcription did not disarm the guard. |
| D-58 Declared baseline per track = persistence | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | Vision §8.7 requires the baseline be **named in configuration before tuning begins** and D-124 approves the selection rule without naming one; this supplies the name. **Persistence**, because it is already a mandatory difficulty control (Vision §2.4 tier 2; PC-03/PC-04), is defined on every partition, and needs no fit — so the criterion can never be compared against a baseline that itself failed to fit. **Transcribed alongside it (a copy of D-124, recorded Approved in Vision §14.2):** select on mean per-fold skill vs the declared baseline across F1–F4; prefer the simpler configuration within **1%**; refit changes no hyperparameter; **no December result may influence the criterion**. |
| D-59 December day range = 2022-12-02 .. 2022-12-31 | **Student states supervisor countersigned, 2026-09-21** — the Student + Supervisor gate item `GOV-2026-08-28-FD-01` Rec 15; no separately signed artifact exists or is claimed | 2026-09-21 | Matches **D-28's locked scored set exactly** (30 days), so D-13's comparison count describes precisely the set that is scored. D-28's three grounds for the 30-day set carry over unchanged; nothing about the scored set is reopened. **Not a locked-test access** — fixing a day range reads no December target value, and the required pre-G-05 coverage/regime audit stays performance-blind. Verified: `read_december_day_range` resolves to 30 inclusive days; the unfrozen-state refusal is **kept as a negative control** on a synthetic config. |
| D-60 Phase 1 feature set `FS-P1-2022-v1` — 21 fields over 13 rows | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | The input space was already closed twice over (TE §6.2's table; `SECTION_6_2_ROWS`), so rows, the exact lag set `[1,2,3,24]` and the `none` normalizations are **copies**. **One thing was chosen:** the seven rows reading the conditional "Train-only if scaled" (`station_lat`, `kp_safe`, `ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe`, `f107_81_trailing`) resolve to `train_only_standardize` — Ridge/LSTM are scale-sensitive across Kp 0–9 to F10.7 in the hundreds, RF is scale-invariant, and train-only fitting is the leakage-safe direction. **Deliberately absent, each a decision:** `dst` (diagnostic-only), `ssn_*` (removed, refused by name), all `target_support` fields (**G-04 not passed**; target-hour quality fields permanently forbidden), raw longitude (only via `lst_sin`/`lst_cos`), anything IRI-bearing. A dictionary change means a **new** `feature_set_id`. Verified: `load_feature_dictionary` accepts 21 fields (12 standardize / 9 none). **Discharges no gate**; `observable_codes` remains untranscribed. |
| D-61 Stage 00 publishes the release (option A) | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | Closes the missing-producer defect: `write_release` was complete, tested and **called by nothing in production** (verified by grep over `scripts/`, `src/`, `notebooks/`, `kaggle/` — only two test modules), while stages 01 and 02 both consume releases, so the sequence could not pass stage 01. **Stage 00 now releases what it acquired**, after every existing assertion. **D-52 read as ruled:** "no transport" bars transport of PROVIDER BYTES, not writes — no provider is contacted and only verified derived artifacts are read. `dataset_version` derived (D-29); R-13 no-overwrite intact. Two recorded judgement calls: `fold_ids`/`mask_ids`/`feature_set_ids` carry a deliberately unusable `NOT_YET_ASSIGNED_…` token (stage 00 precedes all three; TE §13.3 forbids empty), and `selected_cell_bounds` records the D-1 CELL, not raw floats (R-11). The released file is a CSV with exactly the six provider columns, refusing a row missing any rather than blanking it — **found by execution**, since the first JSON version was SILENTLY SKIPPED by the consumer and stage 02 'completed' with `rows: 0`. **Executed:** 1,810 BSHM records released (`737a0f7ee7ea`); stage 01 `release_manifests_found` 0 → 1; stage 02 completed with **168 rows = BSHM's 168/168 D-11 bins**, 158 valid, full D-17 contract, stamped `P1A/GNSS_VTEC/GRIDDed_VTEC_1H`. Also transcribed en route: `target.aggregation` (D-16) and `target.contract` (D-17). **Discharges no gate; not a G-05 act.** |
| D-62 `observable_codes` deferred to Phase 2 | **Student states supervisor countersigned, 2026-09-21** — no separately signed artifact exists or is claimed | 2026-09-21 | **Not required for Phase 1; formally deferred to Phase 2**, where the RINEX headers stating it are legitimately read (TE §7.0 bars Phase 1 from reading them). Not dropped, not defaulted, not filled — it stays a Vision §6.2 field and stays REQUIRED for Phase 2. The mechanism already existed without a D-number (`PHASE2_ONLY_REGISTRY_FIELDS`; `assert_registry_resolved(phase=…)`, whose **default `phase=2` is the full unchanged R-45 check**); this ruling is its home. **Correction recorded with the ruling:** `observable_codes` was reported in-session as the Phase 1 blocker and **measurement showed it was not** — Phase 1 refused on MISSING PROVENANCE for `hardware_changes_2022` and `igrf_version` (presence is not provenance, R-46/W-2a), while `observable_codes` was already exempt. Both provenance values transcribed the same day from sources already in the config (site-log Sections 3–4, where the 2022-covering entries span the year with no change inside it, so the empty list is a MEASURED ABSENCE; and the project-wide IGRF-13 pin with its coefficient hashes). **Executed:** the real registry now RESOLVES under `phase=1` and STILL REFUSES under `phase=2` naming the field; both directions asserted by a new control, so a deferral that became a deletion would fail the suite. **Owed at Phase 2:** transcribe `observable_codes` for all three stations from the 2022 RINEX headers. |
| D-63 Seven driver-class permitted-producer identities | **Not required under TE §18.2 (producer identity; D-41 precedent) — student instruction 2026-09-21** | 2026-09-21 | Closes D-35 limb 3. Each identity names the ONE product a prior decision already selected (D-39 nowcast Kp/ap; D-40 Hpo.0002 V2.0; D-21–D-25 NRCan daily median; D-10.1 Kyoto Dst, still diagnostic-only): a transcription, not a choice. Home: `spaceweather.DRIVER_PRODUCERS`; config = constant = test literal asserted three ways. Obligation created on the unbuilt driver release: stamp `producing_artifact` with exactly these values. Stage 05's refusal moved to its own release-input loader. |
| D-64 Provider product-version census — measured distribution; limitation recorded | **Student limb done 2026-09-21 (census run + recording); Supervisor limb — Approved, option (b) accepted (the mix bounds every claim until the provider certifies equivalence). Date: 2026-09-24.** | 2026-09-21 | Eleven non-December months measured: 208,387 records; `g.001` 5,411 in nine whole provider files (2022-04-21; 06-16; 07-13/14/18; 08-15; 11-13/28/29); `g.002` 202,976; **no day mixes versions**; the plumbing window 11-01..07 is single-version by measurement. December not read (restricted root); the board's 743 `g.003` on 2022-12-31 stands as recorded. Recorded as `release_status_versions` on eleven `declared_sources` entries, re-measured and enforced by stage 01 on every run. Option (b) stands: the mix bounds every claim until the provider certifies equivalence. |
| D-65 Geomagnetic coordinates under pinned IGRF-13 (Q-06) | **Student freeze 2026-09-21 by instruction; Supervisor countersignature for the §6.2 column — Approved. Date: 2026-09-24.** | 2026-09-21 | Centered-dipole, epoch 2022.5, from NOAA NCEI `igrf13coeffs.txt` (sha256 `460b8d8b…`): ARUC 35.642 / 123.046; BSHM 29.544 / 112.963; NICO 32.110 / 111.913 (lat / east lon). Pole 80.713 N, 287.340 E; Hapgood-1992 frame; Boulder control reproduces the textbook value. NOT quasi-dipole/AACGM. Fields `geomagnetic_lat`/`geomagnetic_lon` added to the Station contract with provenance, refused when absent or TBD in both phases (Rec 13 option 1). No Phase 1 path consumes them. |
| D-66 `f107_safe`'s `source_series` renamed to `f107_safe_at_origin` (transcription correction under D-60's existing scope) | **Countersignature: Student — Approved via governed change-record process, verbatim text as drafted in `governance/CHANGE_RECORD_2026-09-24_ready_to_rule_drafts.md` §A, execution and verification completed and reviewed.** | 2026-09-24 | Corrects a key collision in the D-60 dictionary: `f107_safe` and `f107_81_trailing` both declared `source_series: "f107_daily_median"`, and the same key is read by two consumers needing incompatible row shapes (`build_features` needs an hourly value per epoch for `f107_safe`; `build_availability_matrix`'s trailing limb needs a per-day value for the 81-day window). `configs/features.yaml`'s `feature_dictionary.f107_safe.source_series` changed from `"f107_daily_median"` to `"f107_safe_at_origin"`. **Nothing scientific moves**: the row id, lag rule (previous-day observed value), the producing artifact (`nrcan_f107_observed_daily_median_2022`, D-63), and the normalization (`train_only_standardize`, D-60) are all unchanged — only the label distinguishing the per-origin selection from the plain daily series. `f107_daily_median` keeps its plain meaning (D-21: the daily series) and is what `f107_81_trailing.window.source` still reads. Symmetrical with D-60's earlier resolution of the sibling collision (`f107_81_trailing`'s own `source_series` → `f107_81_trailing_mean`), same session, same class of fix. **D-60's frozen field count (21 fields) is unchanged** — this edits one string value in one existing row, not the row inventory. **Verified 2026-09-24**: `load_feature_dictionary` still accepts 21 fields; a new negative control (`tests/test_feature_availability.py::test_f107_source_series_keys_never_collide_on_the_real_config`) asserts the three keys (`f107_safe.source_series`, `f107_81_trailing.source_series`, `f107_81_trailing.window.source`) are pairwise distinct on the real, committed config, guarding against this collision recurring under a third field; full `test_feature_availability.py` suite passes (86/86). On the already-committed fixture bundle `FIX-NOV-FOLD-01__train__untransformed` (built under this fix, `artifacts/walking_skeleton/plumbing_7day/features/`), `f107_safe` and `f107_81_trailing` are confirmed to carry genuinely different measured values (e.g. row 0: `128.1` vs. `130.194444`), not the collapsed single value the pre-fix collision would have produced. **Discharges no gate; not a G-05 act.** |
| D-67 `budget_value`: `statistic = p95`, `combination = sum` (GOV-2026-09-20-CG-01 Recommendation 20 / dispositions §4.5) | **Countersignature: Student — Approved by instruction, 2026-09-24, verbatim text as drafted in `governance/CHANGE_RECORD_2026-09-24_budget_value_merged.md`. No separate supervisor signature is claimed.** | 2026-09-24 | Sets both content fields of `configs/data.yaml: target.uncertainty_budget`: `statistic = p95` (forecast-verification, decision-relevant tail statistic — [Bouttier et al. 2024](https://consensus.app/papers/details/571419dc7b7659b0900fef05315e3f8a/?utm_source=claude_desktop), [Brown et al. 2020, MET/METplus](https://consensus.app/papers/details/b5c9557092ce5684b901f760cb3fb182/?utm_source=claude_desktop) — avoids `max`'s single-point fragility and `median`'s permissiveness for a budget concept) and `combination = sum` (Phase 1/Phase 2 VTEC uncertainty content share a documented common systematic error source — GNSS differential-code-bias estimation — [Chen et al. 2026](https://consensus.app/papers/details/6dcc64144644599db0819d5b08e65c52/?utm_source=claude_desktop), [Zhang et al. 2018](https://consensus.app/papers/details/1cf7c2a93f8258aca2279d9174da756f/?utm_source=claude_desktop)/[2023](https://consensus.app/papers/details/806b64787d305afa94ae9059fb06e99c/?utm_source=claude_desktop), [Hernández-Pajares et al. 2017](https://consensus.app/papers/details/6c9fd1e894a65cfdb38649b8d071d4b6/?utm_source=claude_desktop) — corroborated by this project's own existing Mandated rules on the two phases' non-independence; general GUM practice reserves quadrature for established-independent components, [Fröhner 2003](https://consensus.app/papers/details/fab8b70c41ef56ccb17b990e1bcc47b1/?utm_source=claude_desktop), [Dixson et al. 2026](https://consensus.app/papers/details/6a49d4b0e1d05ef09026393197f5a980/?utm_source=claude_desktop)). **Closes Recommendation 20 / the §18.2 item in full**: `decision`, `statistic` and `combination` are now all set in `configs/data.yaml: target.uncertainty_budget`; `resolve_budget_rule` returns a usable rule for the first time and `practical_relevance_statement` stops refusing. Full literature review and both merged prior drafts: `governance/CHANGE_RECORD_2026-09-24_budget_value_merged.md` (superseding `..._budget_value_statistic.md` and `..._budget_value_combination.md`, both left standing as history). Verified 2026-09-24: 250 passed, 1 skipped across every consumer test module, governed `tec-thesis-311` (Python 3.11.16) environment. |
| D-68 Bounded 1-December persistence-history lookup for M-01/M-02 (Option A, `RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md` §2) | **Countersignature: Student — Approved by instruction, 2026-09-24, verbatim text as drafted in `governance/CHANGE_RECORD_2026-09-24_d28_option_a_mechanism_built.md`. No separate supervisor signature is claimed.** | 2026-09-24 | Authorizes `src.data.locked_test.read_persistence_history_lookup`, built and tested 2026-09-24 (`tests/test_locked_test_guard.py`, 6 tests, all 5 conditions independently verified; full §18.3 critical set 772/772 passing at build time). A narrowly-scoped, logged, performance-blind read of 2022-12-01 target values, strictly as backward-looking lookup history for M-01 (`y(t-1h)`) and M-02 (`y(t-24h)`), recovering the full D-28/D-59 30-day scored set (2–31 December) without amending either decision. **Does not touch, amend, or contradict D-28 or D-59** — both stand exactly as originally frozen; this is an additive lookup path for two specific, unfitted difficulty controls only. `configs/experiment.yaml: persistence_history_lookup.decision` updated to cite `D-68` and `authorized` flipped to `true` in the same act as this ruling — the mechanism activates for real DEC iterations from this point on, gated by the 5 conditions its own tests independently verify (only M-01/M-02; routed through `open_restricted`, logged; post-G-05 only via `verify_g05_signature`; never returns a row outside 2022-12-01). Caller-side wiring into `scripts/06_train_and_predict.py` / `src/models/persistence.py` (owned by `models-and-baselines`/`fixtures-and-reproducibility`) authorized in the same instruction and implemented same day — see `governance/CHANGE_RECORD_2026-09-24_d28_option_a_wiring.md` for the connected implementation and its own verification. |
| D-69 §18.3 "critical set" selection reconciled: selection (b), the ten-module §18.3 selection, is authoritative; selections (a) and (c) superseded/not applicable for this gate (build-and-test Rec 5, item 7) | **Countersignature: Student — Approved by instruction, 2026-09-25, verbatim text as drafted in `governance/CHANGE_RECORD_2026-09-25_item7_selection_b_ruling.md`. No separate supervisor signature is claimed.** | 2026-09-25 | `build-and-test`'s `build-test-results.md` identified three coexisting "critical set" selections that must not be conflated: (a) the pre-commit hook's five-module commit-time subset (a subset by design, Rec 30 option 1, never a candidate); (b) the ten-module §18.3 selection whose module homes map 1:1 onto §18.3's ten named critical items (target contract and DCB sign; availability lags; IRI-free denial; split embargo; train-only transforms; comparison-wide masks and matched windows; checkpoint restore; vector bootstrap; release hashes; locked-test access guard) — `test_prepared_target_schema`, `test_feature_availability`, `test_iri_denial`, `test_split_embargo`, `test_train_only_transforms`, `test_common_masks`, `test_checkpoint_restore`, `test_bootstrap`, `test_release_hashes`, `test_locked_test_guard`; (c) the 766-test selection behind `governance/PENDING_FOLLOWUPS.md` §1a's "766/766 passed", which spans all 29 test modules, has no surviving green junit evidence (the only committed 766-test XML records 2 failures), and was run while the three site-log bytes were already absent from tracking. **Ruling: selection (b) is authoritative for §18.3's "zero unresolved P0 fields and no failing critical test" gate criterion.** (a) and (c) are superseded/not applicable for this gate but stand unedited as their own dated historical evidence (`project.md`'s never-edit-a-signed-record correction). **Verified 2026-09-25** with a fresh run, not reused from the prior day: **685 total, 685 passed, 0 failed, 0 errors, 0 skipped**, 54.870 s, governed `tec-thesis-311` (Python 3.11.16), `PYTHONHASHSEED=0`. Persisted `artifacts/exec_evidence/run_2026-09-25_item7_selection_b/crit.xml` (sha256 `005fdb00a282e9c57c8007a0a18b71d324c81e3143b3019c9ea5d2b5a85b16a3`), matching the prior day's 685/685 figure — no regression. §18.3's "no failing critical test" precondition is satisfied for selection (b) as of this commit. |
| D-70 Apparatus hyperparameter points for the walking-skeleton fixtures (positional rule) | **Not required under TE §18.2 — Q-31 class: fixture apparatus is Student-owned, no supervisor countersignature required (team.md § Walking Skeleton; D-20 precedent). Student adoption by instruction, 2026-09-25, verbatim from `governance/CHANGE_RECORD_2026-09-25_apparatus_hyperparameters.md` §6. Numbering note: the Student first named this D-125; the coding agent's pre-write collision check found Vision §14.2 already owns D-125 (comparison-wide masks row, Approved, cited by REQ-FAIR-01 and N-06), and the Student re-ruled the number to D-70, the register's next free number. Transcribed into this register by the coding agent on the Student's explicit instruction of 2026-09-25; the decision, its values, and its number are the Student's.** | 2026-09-25 | Breaks the circular refusal disclosed in `CHANGE_RECORD_2026-09-25_apparatus_hyperparameters.md` §1 (fixture pass needs `models.selected`; `models.selected` is the governed tuning run's output; the tuning run is gated on frozen fixtures — TE §9.2 vs R-101/TE §7.0B). For fixture-scale walking-skeleton runs ONLY, the fixture scope carries one apparatus grid point per fitted track, selected by POSITION — the first transcribed element of each grid axis in `configs/experiment.yaml` (D-121's transcription order) — with zero discretion, before any result of any kind has been observed: **ridge (M-04) `alpha: 0.01`; random_forest (M-05) `n_estimators: 300`, `max_depth: 8`, `min_samples_leaf: 1`; lstm (M-06) `layers: 1`, `units: 32`, `learning_rate: 1.0e-3`, `batch_size: 64`.** Every point must be a member of D-121's frozen grid (`assert_in_grid` at use). **Restrictions, mandatory:** these points exercise the plumbing apparatus (TC-03f: smoke evidence, never scientific evidence) and are NOT a prior, a default, a ranking signal, or a candidate shortlist for the governed selection; `models.selected` remains `TBD — freeze gate` until the governed January–November F1–F4 tuning run produces it under D-124's rule; no comparison between these apparatus points and any tuning result may be drawn. The positional rule exists so the choice cannot be performance-informed even in principle. Alternative offered and declined: minimum-CPU-cost member per track ("cheapest" requires a runtime judgment; the positional rule leaves none). Mechanism, schema, negative controls and verification (1593 collected, 0 failed, 3 skipped, governed Python 3.11.16): the change record above. |
| D-71 ml_dtypes pinned to 0.5.3 (engineering pin, TF 2.21.0 dependency) | **Not required under TE §18.2 — engineering pin on the scikit-learn precedent (team.md § Testing Posture, Q3=A class); Student approval by instruction, 2026-09-26. Numbering note: the Student first named this D-16; the coding agent's pre-write collision check found D-16 already owns target.aggregation (cited by D-55 and D-61), and the number was re-ruled to D-71, the register's next free number, per the D-70 precedent. Transcribed into this register by the coding agent on the Student's explicit instruction of 2026-09-26; the decision and its number are the Student's.** | 2026-09-26 | TensorFlow 2.21.0 (D-36) permits ml_dtypes>=0.5.1,<1.0.0. The version pip's resolver selects by default (0.6.0) requires numpy>=2.0.0, conflicting with the governed numpy==1.26.4; an unconstrained install would have upgraded numpy to the also-downloaded 2.4.6 wheel. Pinned ml_dtypes==0.5.3 (requires numpy>=1.23.3 on Python 3.11; wheel sha256 58e39349d820b5702bb6f94ea0cb2dc8ec62ee81c0267d9622067d8333596a46). Enforced by requirements.txt (committed 12843b5) and environment/install_wheels.ps1, which asserts numpy remains 1.26.4 after every wheel-layer install. Verified 2026-09-26: offline from-scratch rebuild green; suite 1589 passed / 4 designed skips / 0 failed. |
