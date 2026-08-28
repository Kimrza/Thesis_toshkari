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
| D-25 F10.7 availability convention | **Yes** | 2026-08-22 | Approved by the project owner under the recorded authority equivalence. Conservative convention: a daily median becomes available no earlier than `00:00 UTC` on the following day. **An explicit project assumption, not a demonstrated publication latency**; no operational real-time availability is claimed. **Requests, but does not take,** a §15.2 amendment to TE §7.0A stage 4 and EV-12; until granted, EV-12's F10.7 limb is unmet at G-04. |
| D-26 F10.7 March–April provenance | **Yes** | 2026-08-22 | Approved by the project owner under the recorded authority equivalence. Provenance recorded **UNRESOLVED**; data retained; measured / reconstructed / interpolated / provider-corrected asserted in **no** direction. Carries a thesis reporting obligation. Identifies two clarification routes and an `ABL-NOSW`-style sensitivity — **none approved or scheduled** by this decision. |
| D-27 Primary target untransformed; inverse is ABL-DIFF's | **Yes** | 2026-08-24 | Approved by the project owner under the recorded authority equivalence, at the delivery-planning approval gate. **A reading of frozen text, not a new scientific value.** The primary train-only transform touches target-derived inputs, not the target, which stays **raw TECU** (TE §7.2 `ABL-DIFF`: *Primary remains, Raw TECU*). Primary path needs no inverse; `ABL-DIFF` alone transforms the target and keeps its inverse-before-metrics obligation with error propagation recorded. Raised by blocker BLK-08; narrows but does not close its mechanism limb, which stays with `functional-design`. |
| D-28 G-06 locked-test scored set = 2–31 Dec (30 d) | **Yes** | 2026-08-28 | Approved by the project owner under the recorded authority equivalence, at the `functional-design` (3.1) governance gate on `GOV-2026-08-28-FD-01` Rec 6. **Ratifies FU-7 = A (2026-08-26), already built upon by eight units.** Basis is `requirements.md` FR-P1-04-5 + ADR-11's `lead_in_hours` removal; **discloses that Vision §8.2 and TE §7.1 both carry `—` in the Locked-test Embargo column**, so a level-4 paraphrase is the sole textual basis — conflict recorded, not resolved, and carried to G-05. Accepted on three grounds: 1 Dec is furthest from solstice; the bootstrap loses 1 of 31 blocks (conservative); and 720 h divides by 48 where 744 h does not, so the mandatory 48-h sensitivity would have raised under the 31-day reading. **No supervisor signature exists or is claimed.** A revised split manifest is owed at G-05. |
| D-29 `dataset_version` = 12-hex prefix, verified on write | **Yes** | 2026-08-28 | Approved by the project owner under the recorded authority equivalence, at the `functional-design` (3.1) governance gate on `GOV-2026-08-28-FD-01` Rec 42 (board option 2). Encoding **12 hex** from `content_hash`; collision bound **recorded** (~1.8e-9 at n=1,000; ~1.8e-7 at n=10,000) but **never relied on** — the verify-on-write prefix check is what establishes never-reuse, raising `ReleaseError` on collision. **No release ledger introduced.** Unblocks `write_release` at 3.5 and closes two of `foundation` R-12s three open items (injectivity, `verify_release`). **TA-15 is still NOT covered and this decision does not cover it** — `tests/test_release_hashes.py` exercises none of §13.3s manifest fields and not R-13s overwrite refusal. **No supervisor signature exists or is claimed.** |
| D-30 `.dst_summary.json` relocation | **Yes** | 2026-08-28 | Approved by the project owner under the recorded authority equivalence, on `GOV-2026-08-28-FD-01` Rec 44(b) (board option 2). Moves the file into `evidence/audit_ec1_2026-08-15/kyoto_dst/`, inside R-27s scan root, verified byte-identical on the D-15 method with the access-log row written **before** the move. Makes `governance-guards` R-26 driver-exclusion **class 4 unconditional**. **Not a December read** — bytes and hash only, no field parsed. Changes no value and approves no new input; Dst stays diagnostic-only. **No supervisor signature exists or is claimed.** |
