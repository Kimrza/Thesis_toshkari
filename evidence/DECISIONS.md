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

---

## Supervisor review

D-3/D-144 is countersigned as of 2026-08-15. Every other decision above remains
independently reversible. The supervisor may countersign the remaining items
as a whole, or overturn individual items — D-2 (threshold set with partial
sight of the data) and D-3 (taken on five months rather than twelve) are the two most
exposed to challenge and should be read first.

| Item | Countersigned | Date | Notes |
|---|---|---|---|
| D-1 Cell convention | | | |
| D-2 Coverage minimum | | | |
| D-3 D-144 source adoption | **Yes** | 2026-08-15 (recorded) | Countersigned by the supervisor. Recorded 2026-08-15 as reported by the student; no signature artifact (signed document, email or minute) is filed in this repository. Attach the evidence here when available. |
| D-4 Parameter set | | | |
| D-5 Gap policy | | | |
| D-6 Citation form | | | |
| D-7 Hourly resolution | | | |
| D-8 Claim scope | | | |
| D-9 Acquisition route | | | |
| D-10 Driver sources / leakage | | | |
| D-11 Fixture window | n/a | 2026-08-16 | Q-31 is Student-owned per TE §18.2; no countersignature required |
