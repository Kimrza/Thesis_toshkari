# Change Record — 2026-09-19 — Scientific review incorporated into gate preparation: timestamp semantics, F10.7/benchmark definitions, A2 mutant disposition, A3/A4 decision packages, G-3/G-4 reconciliation, claim wording

**Change ID:** `CR-2026-09-19-SCI-REVIEW`
**Authority:** the project decision owner's instruction of 2026-09-19 ("Incorporate the
scientific review below into the remaining gate preparation", items 1–9). Authorised and
done: routine, reversible fixes and documentation alignment; focused verification.
Prepared, NOT adopted: every contract amendment (P-1 … P-5 below), the A3 decision and its
sensitivity protocol, the A4 value, the G-3 class-5 text, the scanner repair, the claim
wording. Forbidden and not done: new scientific decision adoption, configuration changes,
producer artifacts, `write_release`, `permitted_producers` entries, dataset registration,
model training, commit, push, declaring G-04 passed, fabricating supervisor approval.
**Preserved:** D-39 … D-42 and every fix of `CR-2026-09-19-GATE-PREP-2`; no contradiction
with them was found. **Repository state:** HEAD `18843aa`; no commit.

Three evidence classes are kept apart throughout: **[VERIFIED]** = read from a held file,
the governing text, or executed code this pass; **[ASSUMED]** = an approved project
assumption (D-25, D-42) restated as such; **[OPEN]** = an unresolved question routed to the
owner or supervisor.

---

## 1 — Timestamp semantics, end to end, for the six driver features

### 1.1 File contracts, verified separately per product

| Product | Timestamp label in the file | Verified how | Interval semantics |
|---|---|---|---|
| Hpo `Hp60ap60doi_2022.txt` V2.0 (`hp60ap60doi_2022_v2.txt`) | `YYYY MM DD hh.h hh._m days days_m` | **[VERIFIED]** header lines 24–27 of the held V2.0 file: *"YYYY MM DD is date of UT day. hh.h is starting time in hours of interval for which Hp60 and ap60 are given. hh._m is mid time in hours of interval … days is days since 1932-01-01 00:00 UT to start of interval"* | Row labelled by interval **START**; the value covers `[hh, hh+1)` UT; completion at `hh+1` |
| Hpo V3.0 (`hp60ap60doi_2022_v3.txt`) | same columns | **[VERIFIED]** held V3.0 header: *"hh.h is starting time in hours of interval"* | identical labelling; V3.0 is the later recomputation (D-40 comparator only) |
| WDC `Kp_now2022.wdc` / `Kp_def2022.wdc` | `YYMMDD` + eight fixed-width Kp slots + eight ap slots per day; **no hour field** | **[VERIFIED]** held files (first data line `22 1 1…`, 62+ chars, eight slots); parser `scripts/audit_gfz_drivers.py:parse_wdc` keys slot *k* as start hour `3k`. The GFZ PDF (`kp_index_data_description_20210311.pdf` §5) cited on 2026-09-18 is **not held locally** — the eight-slot day is the WDC format's positional convention (`[0,3), [3,6), …, [21,24)` UT), consistent with IRI-2016's reading of the same eight slots (`irifun.for` `readapf107`: *"3-hour Ap indices for the UT intervals (0-3(,(3-6(,…(21-24("*) | Slot identity is positional: slot *k* covers `[3k, 3k+3)` UT; completion at `3k+3` |
| NRCan `fluxtable.txt` | `fluxdate fluxtime` (e.g. `20220315 170000`) | **[VERIFIED]** held file, per month for 2022: **17/20/23 UT on 245 days (Mar–Oct), 18/20/22 UT on 120 days (Nov–Feb)**; 360 days with 3 readings, 4 with 4, 1 with 5 (D-21's figures reproduced) | Instantaneous readings; the day's median is complete at the **last** reading: 23:00 UT (245 d) / 22:00 UT (120 d) |

GFZ's web-service documentation labelling by interval start therefore agrees with the Hpo
file header and with the WDC positional convention — but each was checked on its own file
rather than assumed identical. The WDC PDF §5 remains cited-not-held (routine follow-up:
retrieve and hash it into `evidence/audit_gfz_2026-09-18/` on the next authorised
retrieval; no scientific consequence, since the positional convention is the WDC format's).

### 1.2 The chain for each feature (all UT)

| Feature | Source timestamp → parsed observation interval | Interval end (completion) | Availability instant used by the project | Selected value at forecast origin *T* |
|---|---|---|---|---|
| `kp_safe`, `ap_safe` | day + slot *k* → `[3k, 3k+3)` | `3k+3` | **[ASSUMED, D-42]** completion + 3 h floor | latest interval with `end + 3 h ≤ T`: at *T* = 06:00 → `[00,03)`; 07:00, 08:00 → still `[00,03)`; 09:00 → `[03,06)`. Staleness after completion 3–5 h. |
| `hp60_safe`, `ap60_safe` | day + `hh.h` → `[hh, hh+1)` | `hh+1` | **[ASSUMED, D-42]** completion + 1 h floor | latest interval with `end + 1 h ≤ T`: at *T* = 06:00 → `[04,05)`. Staleness after completion 1 h exactly at every whole-hour origin. |
| `f107_safe` | readings at 17/20/23 (or 18/20/22) → project-derived **daily median** of UT day *D* (D-21, D-22) | 23:00 or 22:00 on *D* | **[ASSUMED, D-25]** `00:00 UTC on D+1` (1–2 h after completion) | `median(D−1)` at every origin on day *D* (`resolve_f107_at_origin`; Route 1 rule). Staleness past availability 0–23 h; past completion 1–26 h. |
| `f107_81_trailing` | 81 daily medians ending at anchor *E* | *E*'s last reading | **[ASSUMED, D-25]** `00:00 UTC on E+1`, the maximum over constituents (monotone, §3) | anchor *E* = *D*−1 for every origin on day *D* (`latest_eligible_window_end`, A2); no observation-timestamp convention. |

### 1.3 The four instants that must not be conflated (synthetic boundary case, Kp interval `[03,06)`)

| Instant | Kp `[03,06)` example | Where the project's evidence stands |
|---|---|---|
| **Interval completion** | 06:00 UT | **[VERIFIED]** from the file label (start 03:00 + 3 h) |
| **Initial publication** (first issue of the nowcast) | unknown; provider states the nowcast *"can change for some time (typically a day or two)"* | **NOT held**; the archive carries no per-value publication timestamp (D-39, D-42). **Not reconstructed. No timestamp invented.** |
| **Subsequent revision** | unknown (nowcast revisions) | 1046 of 2920 nowcast epochs differ from definitive in 2022 — a product-version difference count, **not** a revision-timing record and not a leakage measure |
| **Archived settled value** | `Kp_now2022.wdc` (Last-Modified 24 Jan 2023) | **[VERIFIED]** the bytes the project holds (D-39) |

**The 3-hour and 1-hour floors are margins AFTER completion, and they are project
assumptions.** With `observation_timestamp` = interval END, a 3 h lag admits the `[03,06)`
value from 09:00, three hours after it could first have existed. It is **not** a
demonstrated publication delay: nothing held shows when the first-issued value appeared or
when its revisions ended. D-42's wording stands unchanged: *"do not make settled archive
values historically available at those lags"*.

**The trap, pinned executably.** The same `[03,06)` value labelled by its interval START
(03:00 — the provider file's own label) clears a 3-hour lag at 06:00, i.e. at the moment
the interval completes, with **zero** publication margin; the matrix arithmetic cannot
distinguish the two labellings. New test
`tests/test_feature_availability.py::test_interval_end_observation_timestamps_make_the_lag_a_post_completion_margin`
asserts the refusals at 06/07/08 and admission at 09 (Kp), refusal at 05 and admission at
06 (Hp60), **and** that the start-labelled row passes — the last assertion is there so the
proposal below cannot be forgotten.

### 1.4 What the approved contracts say, and where they are silent — **[VERIFIED]**

- D-10.3: *"each predictor is assigned an availability timestamp — the instant its value
  could actually have been known … A 3-hour interval that has not closed by the origin is
  not available."* → the observation instant can be no earlier than **completion**.
- TE §6.2 row `kp_safe`/`ap_safe`: *"Geomagnetic indices from the **last completed**
  3-hour interval … observation + publication timestamps … ≥ 3 h"*; Vision §7.5: *"Last
  **completed** 3-hour interval; lag ≥ 3 h"*.
- Vision §7.3: *"Observation timestamp — Time represented by the value"* — for an
  interval-valued index this phrase does not say start, mid or end. **Silent.**
- `src/features/availability.py` measures `actual_lag_hours = origin − max(observation,
  publication[, rule])` from whatever `observation_timestamp` the driver rows carry. **No
  code fixes the convention.**
- `src/features/build.py::build_features` selects `driver_values[name][origin]` from the
  hourly `source_series` and **applies no lag** (**[VERIFIED]** by a scratchpad run through
  `build_features` with a synthetic own-interval-aligned Kp series: at origin 04:00 the
  matrix row carried the value of `[03,06)` — the interval still OPEN at the origin). A
  lagged series with the raw observation intervals attached is refused by
  `AlignmentError` (R-76a's own-interval check); a lagged series whose attached
  `observations` are its **usable windows** (`[end+lag, next end+lag)`) is accepted and
  yields the `[03,06)` value at 09:00. The Stage 05 loader (`_load_release_inputs`) is
  unimplemented, so this path is unreachable today — the gap is in the **contract**, not in
  a running pipeline.

**Conclusion.** The contracts do not conflict with each other; they are jointly **silent**
on (a) which instant an interval-valued `observation_timestamp` records and (b) which
component performs the lagged selection. The implementation is consistent with the
contracts as written and would accept a leaking series because the contracts leave the
choice to the producer. Smallest explicit amendments (prepared, not applied):

> **P-1 (observation-timestamp convention; TE §6.2 / Vision §7.3 gloss, Student +
> Supervisor under Q-16):** *"For an interval-valued index (Kp/ap 3-hour, Hp60/ap60 1-hour)
> the availability matrix's `observation_timestamp` is the interval **END** in UT — the
> completion instant, the earliest instant the value could have existed (D-10.3). The safe
> lag is measured from it. Provider labels by interval start are converted at production
> and the conversion is recorded in the driver manifest."*
>
> **P-2 (lagged-selection ownership; `external-products` R-63 / feature dictionary
> `source_series` gloss):** *"A `*_safe` hourly series released under a producer artifact is
> the LAGGED selection: its value at epoch *T* is the value of the latest source interval
> whose completion instant plus the declared safe lag is at or before *T*; its attached
> `observations` are the usable windows `[end + safe_lag, next_end + safe_lag)`, so R-76a's
> own-interval check verifies that a lagged value repeats only inside its usable window.
> `build_features` performs no shift and must not; the matrix row's `observation_timestamp`
> for epoch *T* is the selected interval's END."* Enforcement to add with P-2 (not now): a
> `build_features` cross-check that each driver field's matrix row lag is consistent with
> the selected series' usable windows — one negative control per entry point.

Neither amendment changes a lag, a definition or a provider; both fix wording the contracts
left open. Until P-1/P-2 are adopted no producer artifact can be specified unambiguously,
which is one more reason `permitted_producers` stays empty.

---

## 2 — F10.7 definitions and benchmark compatibility

### 2.1 The project's F10.7 — **[VERIFIED]**

- **Observed, not adjusted.** D-10.3 and D-21: `fluxobsflux` (column 5), *"observed and
  not 1-AU-adjusted"*; the file also carries `fluxadjflux` and `fluxursi`, neither used.
- **The daily value is a project-derived aggregation**, not a provider product: the
  **median of the UT day's readings** (D-21), after D-22's mean-of-duplicates at one UT
  stamp; high-spread days flagged and retained (D-23). The provider issues no daily value;
  `srmp_f107_observed_daily_2022_v1` (D-41) will be the project's derivation and must say so.
- **Seasonal measurement times** verified from the file (§1.1): completion of the median
  is the day's last reading, 23:00 UT (Mar–Oct) or 22:00 UT (Nov–Feb).
- **Completion ≠ publication.** D-25's `00:00 UTC on D+1` delays availability 1–2 h past
  completion and is an **[ASSUMED]** convention; no evidence of publication by midnight is
  held (`fluxtable.txt` has no publication column; EC1-R-4 open). Preserved verbatim.
- **Trailing 81-day mean** over daily medians ending at the anchor, never centered; anchor
  derived per origin (A2).

### 2.2 The IRI-2016 benchmark's own F10.7 definition — **[VERIFIED]** from the wrapped source

`iricore` (not installed in `tec-thesis-311`; TE §8.1 requires it) wraps IRI-2016 and reads
its indices from IRI's own `apf107.dat` / `ig_rz.dat` (`read_iri_data.py:read_apf107`,
format `(13I3, 3F5.1)`), with caller overrides `oarr40` (daily F10.7), `oarr45` (81-day
F10.7), `oarr32` (Rz12), `oarr38` (IG12); **no override for the 3-hourly ap**. The Fortran
the package ships documents the defaults (`irifun.for`, quoted):

| IRI input | Documented definition (IRI-2016 source) | Project feature | Same? |
|---|---|---|---|
| `F107D` | *"F10.7 index for the day (adjusted to 1AU)"* (`APF_ONLY`); read for the **target** date | `f107_safe` = observed median of *D−1* | **No** — day (target vs previous), possibly observed vs adjusted (file content not verified locally: **[OPEN]**), single reading vs project median |
| `F107_81` | *"F10.7 average over 3 solar rotations (81 days, **centered** on the current day)"* | `f107_81_trailing` (trailing, ends *D−1*) | **No** — centered uses 40 future days |
| `F107_365` | *"365-day average of F10.7 **centered** on the date of interest"* | none | — (future 182 days) |
| `IG12`, `Rz12` | *"12-month-running mean … requires the indices for the six months preceding M and the six months following M … based on indices predictions"* near the file's update date | none | — (future 6 months, or predictions) |
| 3-hourly `ap` | `[0,3)…[21,24)` of the **target** day (storm model history up to the target time) | `ap_safe` (completion + 3 h before the **origin**) | **No** — the interval containing the target hour is not complete at the origin |

Vision §6.11 requires the frozen benchmark configuration to confirm *"no driver is
future-centered or unavailable at target time"*; TE §6.2 row `iri2016_t_plus_1_tecu`: *"Drivers
must be forecast-safe and must not be future-centered"*; `src/external/iri.py` enforces
`driver_inputs.no_future_centering_confirmed is True` and `available_at_target_time_confirmed
is True`. **Forecast origin and target hour are distinct** (Vision §7.2: information
available by *t* for a forecast of *t+1*): the report's own criterion is stated at the
**target** time, the model's at the **origin**; the two are one hour apart at *h* = 1 and
the confirmation as worded does not test origin-availability at all.

**Finding F-2.** IRI-2016 as documented is driven by centered and same-day indices. Run
with its own index files it cannot truthfully confirm "not future-centered"; run with
project overrides (`oarr40` = `median(D−1)`, `oarr45` = trailing mean) its **documented input
semantics are modified** — its coefficients were fitted against centered `F107_81`/`IG12`,
and `IG12`/`Rz12`/`ap` cannot be overridden into forecast-safe form without changing what the
model is. **No substitution is made here.** This is a supervisor-level decision (§18.3
preflight: supervisor sign-off covers *"the IRI role"*):

> **P-3 (IRI index-input disposition; Supervisor):** choose ONE and record it with its
> disclosure — **(a)** *IRI-2016 with its standard index files, labelled a climatological
> reference whose index inputs are retrospective and centered by construction; the
> comparison is "forecast vs climatology with retrospective indices", the asymmetry
> disclosed wherever the primary comparison is interpreted; `driver_inputs` in the
> validation report records `future_centered_indices = true` with the list above, and
> Vision §6.11 / TE §6.2 / `iri.py`'s two `True` confirmations are amended to "recorded and
> disclosed" rather than "confirmed absent"*; or **(b)** *overrides `oarr40`/`oarr45` from
> the project's forecast-safe series with `IG12`/`Rz12`/`ap` left standard, recorded as a
> documented deviation from IRI's input semantics, with (a) retained as the reference
> configuration*. **Recommendation: (a)** — it keeps the benchmark equal to its published
> definition and makes the asymmetry a disclosed fact rather than a hidden modification;
> (b) is admissible only as a separately predeclared sensitivity, never as the primary.
> **Consequence of deciding nothing:** R-59 limb 3 refuses generation on the two
> confirmations, so the benchmark cannot be produced.

Also **[VERIFIED]** and routed, not fixed: `src/external/iri.py` (docstring and the R-59
limb-4 error text) and the D-25 review-table row (`evidence/DECISIONS.md` line 2380) still
say D-25 *"requests, but does not take"* the EV-12 amendment, while the D-25 body records
**"Amendment GRANTED and APPLIED 2026-08-22 — `CR-2026-08-22-EV-12`"** and TE §7.0A stage 4
carries the applied text. The register row is a human-signed record (not edited); `iri.py`
is a READY unit's module (not edited without a ruling). **P-5:** align both to the granted
status — owner's one-line ruling.

---

## 3 — A2 verification completed; mutant disposition

- **Can an interior window day be available later than the origin under the supported
  contract?** **No.** The daily source rows carry `day` and `value` only — no per-day
  publication timestamp exists (and none is introduced); the D-25 constituent instant is
  `00:00 UTC of day+1`, **strictly increasing in the observation day**; the anchor limb
  first enforces `recorded_anchor == latest_eligible_window_end(origin)`, whose instant is
  `≤ origin`; every earlier day's instant is therefore `< origin`. The per-constituent loop
  is **redundant by that invariant**, which is now pinned:
  `test_d25_constituent_availability_is_monotone_so_the_anchor_bounds_the_window` (400
  consecutive days across month/year boundaries; anchor and all window members at three
  origin hours). **Disposition:** the loop is kept as defence in depth with a comment naming
  the invariant and the test; the surviving mutant is explained, not silenced.
- **Exact 81-day membership** (the fixture's N): perturbing day `anchor − N` leaves the
  check passing; perturbing `anchor − (N−1)` or the anchor itself fails on the
  recomputation; a missing interior member raises `IntegrityError` and never shifts to an
  older window (`test_trailing_window_membership_is_exactly_the_declared_days_ending_at_the_anchor`).
- **Eligible anchor:** `latest_eligible_window_end` = *D*−1 for all 24 origin hours and at
  month/year boundaries (existing A2 tests, re-run).
- **Pre-2022 coverage, real file:** the 81 UT days ending 2021-12-31 (from 2021-10-12) are
  all present in `fluxtable.txt`, reading only dates `< 20220101`
  (`test_real_fluxtable_carries_every_day_of_the_window_ending_before_2022`).
- No fictitious timestamp field, no older-window fallback.

---

## 4 — A3 decision package (policy unchanged; nothing implemented)

**Standing policy:** TE §6.2 *"Carry-forward ≤ 3 h, then exclude"* on every driver row;
D-21 composes it with the daily series; `carry_forward_composition` is `TBD`;
`resolve_f107_at_origin` raises the R-57a stop. Unchanged by this record.

**Normal use vs extension — the boundary, stated exactly.** `median(D−1)` is the
*designated* value for every origin on day *D* (D-10.3, D-25): using it at 00:00 … 23:00 of
*D* is **normal use of a daily value**, staleness 0 daily steps, not carry-forward.
**Extension** begins only when the *next expected daily update is missing*: at 00:00 UTC on
*D* the designated `median(D−1)` should have become available and did not (the day has no
readings, or the value is refused/unresolved). The **clock starts at 00:00 UTC on D** — the
expected availability instant of the missing designated value — never at the previous
value's own availability instant and never at its observation-completion instant.

**Reading B — exact wording** (`carry_forward_composition: clock_hours`):
> *"When the designated daily median `median(D−1)` is not available at 00:00 UTC on D, the
> last available earlier median is carried forward for origins *t* on day *D* with
> `t − 00:00 UTC D ≤ 3 h` — the boundary is **inclusive**: origins 00:00, 01:00, 02:00 and
> 03:00 keep the carried value; origins from 04:00 through 23:00 are **excluded**, never
> filled; the excluded count per day and per cell is recorded as a split-manifest field.
> Rows are excluded, not the day: an origin whose other inputs are valid is dropped for
> the F10.7 limb alone."*

**Reading A — exact wording** (`carry_forward_composition: daily_step`): as tabled in
`CR-2026-09-19-GATE-PREP-2` § A3 — one daily step of extension (the last available median
serves every origin of the affected day, up to 47 clock hours after its availability
instant); a second consecutive missing daily median excludes all 24 origins.

**Timestamped examples (2022-03-15 … 03-17 synthetic, all UTC):**

| Origin | Designated value | Available? | A | B |
|---|---|---|---|---|
| 03-15 00:00 … 23:00 | `median(03-14)`, available 00:00 03-15 | yes | used — normal use | used — normal use |
| 03-16 00:00 | `median(03-15)` | **no** | `median(03-14)`, step 1 | `median(03-14)`, 0 h into the clock — kept |
| 03-16 03:00 | " | no | kept | 3 h — kept (inclusive boundary) |
| 03-16 04:00 … 23:00 | " | no | kept (20 rows) | **excluded** (20 rows, every cell) |
| 03-17 00:00 … 23:00 | `median(03-16)` | **no** | **excluded** (2nd consecutive step) | excluded |

**Neither reading is claimed optimal.** B preserves the frozen numeral literally and loses
20 of 24 rows per affected day; A preserves the series' own step and admits up to 47 h of
staleness. Preserving the contract is not a scientific argument for B; retaining rows is
not one for A. **What is decisive on this data — [VERIFIED]:** D-21 counts at least one
reading on **365 of 365** days of 2022, so under the held file **no 2022 origin has a
missing designated median** and A and B are **extensionally identical on 2022** unless D-26
(March–April provenance) later removes days. The choice therefore governs (i) the D-26
outcome and (ii) the contract's meaning for any future series — not the 2022 row count.

**Sensitivity-analysis protocol — for approval before execution (nothing run):**

1. **Policies compared:** A (one daily step), B (≤ 3 clock hours inclusive from 00:00 *D*),
   B0 (no extension: exclude every origin of an affected day) as the strict reference.
   Rationale: A and B are the two tabled readings; B0 bounds the cost of any extension.
2. **Scope:** training/validation folds F1–F4 (January–November 2022 only), the frozen
   primary feature set and frozen model configurations; **no new model family, no grid,
   no threshold** — the same fitted procedure re-run per policy only if any affected origin
   exists. **Step 0 is a count:** affected origins per fold and cell under the D-26
   resolution; if zero, the analysis is reported as "no affected origin; policies
   extensionally identical" and stops.
3. **Coverage and exclusion reporting:** per policy, fold, cell: rows retained, rows
   excluded for the F10.7 limb, carried-forward rows, maximum staleness (clock hours and
   daily steps) — as manifest fields, not prose.
4. **Common evaluation timestamps:** paired comparisons are scored on the **intersection**
   of origins retained by every policy compared (one comparison-wide mask per comparison
   set, NFR-FAIR-01); the estimand is the approved paired loss differential with
   equal-station weighting.
5. **Differing sample sets:** origins retained by A but not B (03-16 04:00–23:00 in the
   example) are reported **separately** as a descriptive table (count, staleness, error
   distribution) — never merged into the paired result.
6. **December independence:** no December origin, driver value or result is read; the
   policy is selected on F1–F4 validation only, recorded with its D-number **before** G-05;
   after G-05 the field is frozen (Vision §8.3, §8.7).
7. **Not a research programme:** one comparison, three policies, one predeclared table.

---

## 5 — A4 numerical justification and proposed tolerance

**Quantity.** `|mean_recorded − mean_recomputed|` for `f107_81_trailing` at every scored
origin, in sfu. **Numerical reproducibility tolerance only** — it says nothing about the
physical accuracy of F10.7 (readings are quantised at 0.1 sfu and within-day spreads reach
234 sfu on flare-contaminated days, D-23); it bounds arithmetic, not measurement.

**Reference representation.** Each reading is decimal text with one fractional digit
(`000132.7`); D-22's mean of duplicated readings and D-21's median keep every daily
constituent on the **0.05-sfu grid** (a median of an odd count is a grid value; a mean of
two is a half-grid value). The reference is exact rational arithmetic —
`Fraction(text)` per reading, exact median, exact 81-term sum, exact division by 81 — with
no floating point anywhere. **[VERIFIED]** by the scratchpad script `a4_derivation.py`.

**Implementation under test.** `spaceweather.trailing_mean`: parse to float64, sequential
`sum()` of 81 terms, divide by 81. Under the governed pin (CPython 3.11.16) `sum()` is
plain sequential; CPython ≥ 3.12 uses compensated (Neumaier) summation, which only reduces
the error, so the bound below holds on both.

**Arithmetic (float64, unit round-off u = 2⁻⁵³, machine epsilon ε = 2⁻⁵² = 2u; N = 81;
B = an a-priori bound on any daily median):**

| Step | Error contribution to the mean |
|---|---|
| decimal → float64 per constituent (81 roundings) | ≤ u·B each → ≤ u·B on the mean |
| sequential sum of 81 terms | ≤ (N−1)·u·Σ|xᵢ| ≤ (N−1)·u·N·B on the sum → ≤ (N−1)·u·B on the mean |
| division by 81 | ≤ u·B |
| **total (first order)** | **≤ (N+1)·u·B**; stated conservatively with ε: **(N+1)·ε·B = 82·2⁻⁵²·B** |

**Input bound B.** Daily medians over the whole held file (2004-10 … 2026-08, **December
2022 excluded from the read**) never exceed **311.7 sfu** (2024-10-03; four days > 300, none
> 400). The a-priori bound is set at **B = 400 sfu**, above every held daily median with
≥ 28 % margin and above the historical daily F10.7 record; it is an input assumption
stated in the open, not tuned to data.

**Proposed value:** (N+1)·ε·B = 82 × 2.220446e-16 × 400 = **7.28 × 10⁻¹² sfu**, **rounded UP
to one significant figure → `recomputation_tolerance: 8.0e-12`** (sfu). The rounding is the
only adjustment: it never lowers the bound and inflates it by < 10 % so the config literal
is short; it is not a decade multiplier. (Unrounded alternative: `7.29e-12`.)

**Serialization and parsing effects.** `json.dumps(float)` writes `repr` (shortest
round-trip) and `float()` reads it back exactly — **[VERIFIED]** on 201 values; a
fixed-precision writer (`%.6f`) would add up to 4.9 × 10⁻⁷ sfu and would **violate** the
tolerance by five orders of magnitude, so the freeze procedure below makes round-trip
serialization a requirement, not an assumption.

**Synthetic checks — [VERIFIED]:** 1 120 windows of 0.05-grid constituents in 60–400 sfu:
max |float − exact| = **1.91 × 10⁻¹³ sfu** (38× inside the bound); must-fire controls: an
80-day window differs by 0.68 sfu, an anchor shifted one day by 3.02 sfu — both ≫ 10⁻¹¹.

**Freeze procedure (for approval; no config transcription now):** (1) owner records the
value under a D-number citing this derivation; (2) the first governed recomputation over
production Jan–Nov origins (December untouched) must measure max |float − exact| **below
7.28 × 10⁻¹²** — any excess is an implementation defect to fix, never tolerance to widen;
(3) the two must-fire controls run in the same job; (4) the recorded `mean_value` field is
asserted to round-trip (`json.loads(json.dumps(v)) == v`); (5) then `8.0e-12` is
transcribed into `configs/features.yaml` under that D-number. The value is fixed by the
bound, not by the measurement (Q6's "measured then frozen" is satisfied by step 2 as a
*check*, not as the source of the number).

---

## 6 — G-3 / G-4 reconciliation and December exposure

### 6.1 Exact fifth-class proposal (NOT adopted) — unchanged from `CR-2026-09-19-GATE-PREP-2` § G-3

Class 5 — *"Raw GFZ geomagnetic-index captures and their derived audit reports"*, path
patterns `audit_gfz_*/Kp_*.wdc`, `audit_gfz_*/hp60ap60doi_*.txt`,
`audit_gfz_*/retrieval_record.json`, `audit_gfz_*/gfz-comparison-report.json`,
`audit_gfz_*/sha256_manifest*.json`, `audit_gfz_*/environment_supplemental.json`,
`audit_gfz_*/GFZ-AUDIT.md`; eligibility = exact path **and** driver-only content (JSON: no
`TARGET_INDICATOR_KEYS` token at any depth; raw `.wdc`/`.txt`: provider header present and
every data line parses as the provider's index format with no extra column); safeguards
(1) negative control with a `vtec_tecu` key or a prediction file placed under
`audit_gfz_*/` → flagged; (2) enumeration test pins **five** classes exactly; (3) the class
excludes from *custody* only — `Kp_def2022.wdc` and `hp60ap60doi_2022_v3.txt` remain audit
comparators, never inputs; (4) December driver values in these files are *seen* — recorded
as exposure, never a basis for any selection. The folder name never qualifies content.

### 6.2 Why the current scan is clean — file by file — **[VERIFIED]** (`dec_census2.py`)

The scan (`assert_no_december_outside_restricted`) reads `*.json` outside the restricted
root, looks for a **quoted** `"2022-12` / `'2022-12` literal, and consults the four R-26
classes only for such a file. Result on the real tree: **0 offenders**. Why, exactly:

| File (evidence-relative) | December content | Scan disposition |
|---|---|---|
| `audit_ec1_2026-08-15/ec1-audit-report.json` | quoted `2022-12` (F10.7 date range) | **Examined and permitted — class 3** (content driver-only) |
| `audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json` | December **provisional-Dst aggregates** under the month key `"12"` (31 days parsed; daily minima, storm-day lists) — no `2022-12` literal | **Examined, NOT DETECTED** (month-number keys, same gap as the GFZ report). **Correction to `CR-2026-09-19-GATE-PREP-2` § G-4**, which said this file was *"excluded by class 4"*: the class check is never reached for it because no literal is present; class 4 would apply only under P-4a's structural detection |
| `audit_gfz_2026-09-18/gfz-comparison-report.json` | **229 integer-keyed `{y:2022, m:12, d, h}` differing-epoch records** with both versions' Kp/ap and Hp60/ap60 values — December **driver** values | **Examined, NOT DETECTED**: no quoted literal, so the scan never reaches the class check. This is the undetected-content case; integer keys were chosen on 2026-09-18 to pass the W-9 lexical guard, and this record states plainly that passing a lexical scan is not compliance |
| `audit_gfz_2026-09-18/Kp_now2022.wdc`, `Kp_def2022.wdc` | 31 December day lines each (8 Kp/ap slots per line) | **Outside scan scope** (non-JSON) |
| `audit_gfz_2026-09-18/hp60ap60doi_2022_v2.txt`, `_v3.txt` | 744 December hourly lines each | **Outside scan scope** (non-JSON) |
| `audit_gfz_2026-09-18/retrieval_record.json`, `sha256_manifest*.json`, `environment_supplemental.json` | none (hashes, identities, environment) | Examined; no December content |
| `audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt` | 95 December-2022 reading lines | **Outside scan scope**; R-26 class 2 by path, never exercised by the scan (disclosed narrowing) |
| `audit_ec1_2026-08-15/kyoto_dst/dst_provisional_202211.html` | one navigation link `202212/index.htm`, no values | Outside scope; not data |
| `audit_ec1_2026-08-15/EC1-AUDIT.md`, `DECISIONS.md`, `experiment_registry.md`, `CORRECTION_2026-08-16_acquisition_window.md` | prose mentions of the locked month | Outside scope; governance prose |
| `audit_evidence_2022-01 … -11/madrigal_coverage_raw_records.csv` | **none** (`2022-12` count 0 in every file; a broad numeric regex matched digit runs such as `22125`, a false positive corrected before reporting) | Outside scope; target data with no December record |
| `evidence/locked_test_restricted/**` | the locked month | Excluded by root, as designed |

**Therefore:** the clean result is (i) one file permitted by class 3, (ii) two December-bearing
JSON files the scan **cannot see** (integer/month-number keys), (iii) six December-bearing
non-JSON files the scan **does not read**. None of (ii)/(iii) is a class-4-style permission; they are scope gaps, stated as such.
A clean scan is not proof of compliance; the exposure below is.

### 6.3 Scanner repair and policy amendment — proposed, not applied

> **P-4a (scanner, `governance-guards` R-27 widening):** detect December by **structure**
> as well as by literal — a JSON object carrying `y == 2022` and `m == 12` (any nesting), a
> top-level month-number key `"12"` in a per-month summary, the compact form `202212`, and per-format raw walks for the R-26/G-3 classes (`.wdc` lines
> starting `2212`, Hpo lines starting `2022 12`, `fluxtable` lines starting `202212`). A
> hit outside the restricted root is then permitted only through a class whose content
> check passes. **Consequence:** with P-4a alone the real tree **fails** on
> `gfz-comparison-report.json` and the four GFZ raw files (no class covers them; `.dst_summary.json`
> and `fluxtable.txt` would then pass through classes 4 and 2 on content), so P-4a is
> adopted together with **exactly one** of: G-3 class 5, **or** relocation of
> `evidence/audit_gfz_2026-09-18/` under `evidence/locked_test_restricted/` on the D-15/D-30
> byte-identical method with its access-log obligation. Recommendation: **class 5 + P-4a**
> — the files are driver-only by content and relocation would put audit comparators under
> the target seal, blurring what the seal means.
> **P-4b (policy, `project.md` § Forbidden gloss):** *"Reading December driver values for
> product identification, hashing, parsing validation and version comparison is exposure,
> recorded in the run's change record; using them to choose a method, feature, threshold,
> lag, missingness policy or model is a violation of the December-blind rule regardless of
> whether the locked target was opened."*

### 6.4 Access record — factual completeness — **[VERIFIED]**

- `evidence/test_run_access_log.jsonl`: **+407 rows** in the working tree, all dated
  2026-09-18, all `purpose = coverage_audit`, `performance_inspected = false`,
  `locked_test_accessed = true`; 395 from `test_release_hashes` (*"restricted-root
  manifests and declared artifacts, bytes and hashes only"*, TA-15) and 12 from
  `test_acquisition_window` (*"acquisition record dates, for the out-of-window containment
  invariant"*). These are the governed suite's integrity reads across the day's runs —
  complete for what the tests do; no target value was inspected by any of them.
- **What was actually examined this pass and on 2026-09-18 (driver exposure, not a
  locked-test access under Vision §8.3 — the D-22 precedent):** the four GFZ files were
  parsed in full (calendar 2022, December included) for validation and version
  comparison; `gfz-comparison-report.json` records December differing epochs with values;
  `fluxtable.txt` was read this pass for (a) per-month measurement times (all 2022 months,
  December's slot times included), (b) the pre-2022 window test (dates `< 20220101` only),
  (c) the A4 bound (December 2022 **excluded**).
- **What was used:** nothing for any selection. No feature, lag, threshold, hyperparameter,
  missingness policy or model choice was derived from any December value; the A3 examples
  are March 2022 synthetic; the A4 bound excludes December; D-42's floors predate the
  retrieval. **What cannot be asserted:** that the holdout is "unaffected" — exposure of
  December driver aggregates to the implementing agent is a fact, recorded here; the
  December-blind rule is satisfied by the absence of any December-derived choice, which
  this record and the earlier ones evidence, not by the disclaimer.
- Historical records preserved: no registry row, log row, evidence file or earlier change
  record was edited.

---

## 7 — Scientific claim wording (prepared; adoption is the owner's)

**Core statement, adapted to the approved scope (D-8, Vision §2.5, D-25, D-42):**

> *"This is a retrospective forecasting study of hourly location-sampled gridded VTEC at
> the ARUC, BSHM and NICO cells for calendar 2022, tested on December 2022 only. External
> driver inputs are archived products — GFZ Kp/ap (archived settled nowcast, DOI
> 10.5880/Kp.0001), GFZ Hp60/ap60 (Hpo.0002 V2.0) and NRCan observed F10.7 (project-derived
> daily median) — lagged under explicitly stated availability assumptions (Kp/ap: interval
> completion + 3 h; Hp60/ap60: completion + 1 h; F10.7 daily median: 00:00 UTC of the
> following day). The study does not reconstruct the historical first-issued values of
> any driver and does not establish operational real-time performance; results using
> these archives do not establish exact operational replay or absence of revision-related
> look-ahead."*

**Four things the wording keeps apart — required in every methods/limitations/results
check:**

| Distinction | Say | Never say |
|---|---|---|
| Source-version differences | "1046/2920 Kp epochs and 1790/8760 Hp60 epochs differ between the held product version and its later comparator" | that these percentages are model error, or leakage, or bound its effect |
| Numerical implementation correctness | "the recomputation agrees within 8 × 10⁻¹² sfu (A4)"; "alignment and lag assertions pass" | that passing tests prove the drivers were available at the origin |
| Effect on model performance | only what a predeclared sensitivity (A3 protocol, or a version-swap sensitivity if ever approved) measures | any inference of performance effect from a differing-value percentage |
| Operational availability | "assumed floors; not demonstrated publication bounds" | "real-time", "operationally available", "replay" |

**Fair-comparison requirements retained verbatim from the approved contract:** identical
target and `target_definition_id`, identical forecast origins and horizons, one
comparison-wide intersection mask per comparison set with common scoring timestamps, the
paired loss differential with equal-station weighting; any comparator whose input
assumptions differ intentionally (IRI under P-3(a): retrospective, centered indices; GIM:
final product) is **disclosed as such in the primary table**, and the disclaimer never
substitutes for that disclosure.

**Where it lands (proposal):** D-42's `DRIVER_AVAILABILITY_LIMITATION_STATEMENT` already
carries the final clause; the fuller statement above is proposed as the methods-section
text and as an extension of the claims-checklist row, adopted by the owner with the D-42
countersignature rather than edited into the recorded constant now.

---

## 8 — Files changed by this pass and focused verification

| File | Change | Why |
|---|---|---|
| `src/features/availability.py` | docstrings aligned to A2 (a window may accompany a rule in `AVAILABILITY_RULES_WITH_WINDOW`; refusal text names the actual condition); comment on the per-constituent loop naming the invariant and its test | documentation alignment; A2 mutant disposition. No behaviour change |
| `tests/test_feature_availability.py` | +4 tests: monotone-invariant, exact window membership, real-file pre-2022 coverage, interval-end boundary cases (Kp/Hp60) incl. the start-label trap; `ruff format` applied to the module (reflowed A2 tests only) | §1.3, §3 |
| `governance/CHANGE_RECORD_2026-09-19_scientific_review.md` | this record | — |
| `aidlc/…/construction/build-and-test/memory.md` | diary entries under the four standard headings | protocol |

Scratchpad only (not repository files): `a4_derivation.py`, `medmax.py`, `dec_census2.py`,
`t1_demo.py`, `irifun.for`/`irisub.for` (downloaded IRI-2016 source for §2.2 quotes).

**Focused verification (governed pin, conda `tec-thesis-311`, CPython 3.11.16):**
`tests/test_feature_availability.py` (78 tests) + `tests/test_external_drivers.py`: **134
passed, 0 failed**. `ruff check` on the two touched modules: no new finding (the five
pre-existing findings at HEAD are unchanged); `tests/test_feature_availability.py` + `tests/test_locked_test_guard.py`: 136 passed, 0 failed. Working-tree note: a `git stash`/`pop` used for the lint baseline rewrote the checked-out endings of six modified files to the repository's CRLF (they had carried LF on lines written yesterday); content unchanged (`git diff --numstat` identical), `git -c core.whitespace=cr-at-eol diff --check` clean, `configs/` zero diff. Full suite not re-run: no production
behaviour changed (docstrings, a comment, additive tests); the last full governed run
(`CR-2026-09-19-GATE-PREP-2`: 1256 passed / 4 skipped / 0 failed) stands.

---

## 9 — Owner decisions still needed (smallest set), each with recommendation, rationale, consequence

| # | Decision | Recommendation | Scientific rationale | Consequence of deciding / not deciding |
|---|---|---|---|---|
| 1 | **D-42 supervisor countersignature** (Q-16) | obtain | the floors are Student + Supervisor items | without it no `availability_lags` transcription and no G-04 evidence is acceptable |
| 2 | **P-1 + P-2**: interval-END observation timestamp; lagged selection owned by the producer with usable-window `observations` | adopt both as a §15.2 gloss (Student + Supervisor) | D-10.3 says "instant the value could have been known" — completion is the earliest defensible instant; without P-2 the consumer would accept an open-interval value | with: producer artifacts become specifiable and a build-time cross-check can be added; without: no `*_safe` series can be released unambiguously |
| 3 | **P-3**: IRI index-input disposition | **(a)** standard IRI indices, disclosed as retrospective/centered; (b) only as a predeclared sensitivity | keeps the benchmark equal to its published definition; the asymmetry becomes a disclosed fact | without: R-59 limb 3 refuses benchmark generation; (b)-as-primary changes what "IRI" means in the thesis |
| 4 | **A3 reading** (Student + Supervisor, Q-16/Q-17) | **A** as tabled — *with the finding that A and B are extensionally identical on 2022 unless D-26 removes days*; approve the §4 protocol to run only if Step 0 counts ≥ 1 affected origin | the series' native step is the honest unit of staleness; B's literal clock has no empirical bite on 2022 and would drop 20/24 rows on any future affected day | either reading unblocks `carry_forward_composition`; deferring keeps `resolve_f107_at_origin` raising |
| 5 | **A4 value**: `recomputation_tolerance = 8.0e-12` sfu, B = 400 sfu, freeze procedure §5 | adopt the bound and procedure now; transcribe after the first governed measurement | derived from float64 round-off, not from observed error; serialization made a requirement | without: the anchor limb cannot run on production data |
| 6 | **G-3 class 5 + P-4a scanner widening + P-4b policy gloss** | adopt together | the GFZ files are driver-only by content; a lexical scan that cannot see them is the ambiguity, not the compliance | without: `gfz-comparison-report.json` stays invisible to the guard and the guard's "clean" is hollow |
| 7 | **P-5**: align `iri.py` text and the D-25 review-table row to "amendment granted 2026-08-22" | one-line ruling to annotate | the register body and TE already say granted | stale text misinforms the next reviewer of EV-12's status |
| 8 | Six-entry `availability_lags` transcription; `artifacts/run_snapshots/` tracking | as in `CR-2026-09-19-GATE-PREP-2` §11 items 5–6, after 1, 2, 4 | — | — |

**Unresolved questions (not decisions, facts still missing):** whether IRI's `apf107.dat`
F10.7 column is observed or 1-AU-adjusted (source comment says adjusted; file content not
verified — needs `iricore` installed); GFZ Kp PDF §5 not held locally (positional
convention used); NRCan publication latency (EC1-R-4, open since 2026-08-22).

**G-04 remains OPEN. No supervisor approval exists or is claimed.**
