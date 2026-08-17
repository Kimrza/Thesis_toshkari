# EC-1 Driver Audit — Kyoto WDC Dst grade span and Canadian F10.7 archive coverage

**Performed:** 2026-08-15
**Discharges:** intent-statement scoped verification obligations 1 and 2; initiative-brief entry condition **EC-1**; governance residual GOV-R-03.
**Tooling:** `scripts/audit_ec1_drivers.py`, run against the retrieved files listed below. Machine-readable output: `ec1-audit-report.json`.

**Headline:** both obligations are discharged, and the F10.7 result is **not** what the intent statement anticipated. The Canadian archive has **no missing dates in 2022** — the documented March 2022 outage is not present as a gap. Four data-quality items and one previously unrecorded decision are surfaced instead.

## Method and Integrity

Files were retrieved once over HTTPS and hashed. The audit script reads only the local copies, so re-running it reproduces the same report from the same bytes.

The `fluxtable.txt` transfer was interrupted on the first attempt at 491,209 bytes (ending mid-record at 2009-10-14) and completed by byte-range resume. Integrity of the joined file is evidenced by the parse itself: **23,848 records, zero unparsed lines, and dates monotonically non-decreasing across the whole file** from 2004-10-28 to 2026-08-15. A truncation or a duplicated seam would break at least one of those three.

## Retrieved Files

| File | Bytes | SHA-256 |
|---|---|---|
| `nrcan_f107/fluxtable.txt` | 2,170,350 | `4b7fbfde3b9d0140ef43e7487f5986fe18f93182dac5e1ee37a93fb6ebd690b9` |
| `kyoto_dst/dst_provisional_202201.html` | 5,714 | `98319fa4aa04ca3c3acb3aa476e0d81e8a958cd246d46118c90a9640b51ca1a0` |
| `kyoto_dst/dst_provisional_202202.html` | 5,407 | `f6561832f996c3905b88587f16d5d0d5276ea6977843f7c1acdcf0c563cefdaa` |
| `kyoto_dst/dst_provisional_202203.html` | 5,714 | `c4c96eff798eb539d4c4bafe34e1fabcb7d1d1716b4955d496445cb96ecb3ba4` |
| `kyoto_dst/dst_provisional_202204.html` | 5,612 | `69656d10c05a4a6795346d06b1ca3a2879143117cc1b9f7e6d8966da70b08395` |
| `kyoto_dst/dst_provisional_202205.html` | 5,714 | `70015482a17247347bdab4e38ad23c75080a3c1715e602e9f5ac90a4020370cc` |
| `kyoto_dst/dst_provisional_202206.html` | 5,612 | `939d5149d0119eb523a9d0c5a5e2dfb9b23660d353cecf7126ae99ff25e7faea` |
| `kyoto_dst/dst_provisional_202207.html` | 5,714 | `e5f1e10e2e0c82f518a866c1ed00a73bfb10353e2e754e3a3ff8943a4d1e8b8f` |
| `kyoto_dst/dst_provisional_202208.html` | 5,714 | `272d8310eb4440d9f671596b7960918001a5d260bfbd767458c3b4752925f5f1` |
| `kyoto_dst/dst_provisional_202209.html` | 5,612 | `477405ab43a8179196308bb3de61f1aa2beb859982183d8c820b0e7710d8e1ef` |
| `kyoto_dst/dst_provisional_202210.html` | 5,714 | `a9ddc03aefdc7bd3a69a70cef2a20093186981e3ac62367c08b61406ec502240` |
| `kyoto_dst/dst_provisional_202211.html` | 5,612 | `56562cf040e1b12b7fae5156d2bd1e4f5d2489fb215071fdd5883143864fb592` |
| `kyoto_dst/dst_provisional_202212.html` | 5,741 | `0edd417ae93550d1ff91da8d4c8dd240472cd98a0909f827c425417ec7f9c26c` |
| `kyoto_dst/onDstindex.html` | 27,896 | `09ab7ba7a9cb3fc0cc3fb3b5fcc75fb4d138608ca27cfe8e0424d20a8c827fe6` |
| `kyoto_dst/wdc_index.html` | 4,391 | `091123f70b547dbe7a109ef88ccbd3162f80b3ca90a2b97b4fd197ec72a4b29c` |

Sources: `https://wdc.kugi.kyoto-u.ac.jp/dst_provisional/2022MM/index.html` and `https://www.spaceweather.gc.ca/solar_flux_data/daily_flux_values/fluxtable.txt`.

## Obligation 1 — Kyoto WDC Dst grade span for 2022

**Result: DISCHARGED. Provisional grade is published for the full span 2022-01-01 to 2022-12-31 as a single grade. No span is at a different grade, so no grade mixing is possible.**

Every month of 2022 was probed at all three grade paths:

| Grade path | 2022-01 … 2022-12 |
|---|---|
| `dst_final/2022MM/` | **404 for all twelve months** — no final-grade data exists for any month of 2022 |
| `dst_provisional/2022MM/` | **200 for all twelve months** |
| `dst_realtime/2022MM/` | 403 for all twelve months — access forbidden, and irrelevant since provisional supersedes it |

Day-row coverage parsed from the twelve retrieved pages:

| Month | Day rows / expected | Missing |
|---|---|---|
| 2022-01 | 31 / 31 | none |
| 2022-02 | 28 / 28 | none |
| 2022-03 | 31 / 31 | none |
| 2022-04 | 30 / 30 | none |
| 2022-05 | 31 / 31 | none |
| 2022-06 | 30 / 30 | none |
| 2022-07 | 31 / 31 | none |
| 2022-08 | 31 / 31 | none |
| 2022-09 | 30 / 30 | none |
| 2022-10 | 31 / 31 | none |
| 2022-11 | 30 / 30 | none |
| 2022-12 | 31 / 31 | none |

**365 / 365 days, 24 hourly values each.** Each page carries the header "Hourly Equatorial Dst Values (PROVISIONAL)". The December page records `[Updated at 2023-07-18 03:55UT]`.

**Provisional status is recorded** as required, and is consistent with the driver contract's treatment of Dst as diagnostic and hindcast-only rather than a confirmatory forecast feature — a grade change to final later would not disturb the primary estimand.

**Acknowledgement text, verbatim from the monthly pages:**

> Acknowledgments: We thank the geomagnetic observatories (Kakioka [JMA], Honolulu and San Juan [USGS], Hermanus [RSA], Alibag [IIG]), NiCT, INTERMAGNET, and many others for their cooperation to make the provisional Dst index.

**Residual — the non-commercial-use notice was not located.** It is not present on the twelve monthly pages, on `onDstindex.html`, or on the WDC index page, all of which were retrieved and hashed. The obligation to record it therefore remains open until the notice is found on the Kyoto data-use page and captured verbatim. Its existence is asserted upstream in the intent statement; this audit neither confirms nor contradicts it, and the notice text is **not** reproduced here from memory.

## Obligation 2 — Canadian observed F10.7 archive, from 2022-03-18

**Result: DISCHARGED, with a finding that changes the premise. There are ZERO missing dates in 2022. The month-long outage documented for March 2022 does not appear in this archive as absent dates.**

| Measure | Value |
|---|---|
| Days expected in 2022 | 365 |
| Days present | **365** |
| Missing dates, whole year | **none** |
| Missing dates from 2022-03-18 onward | **none** |
| Contiguous missing runs | none |
| Records for 2022 | 1,101 |
| Readings per day | 3 on 360 days, 4 on 4 days, 5 on 1 day |
| Observed flux range | 82.4 to 357.1 |
| Zero or negative readings | none |

Values across the outage window are continuous and physically ordinary — a smooth decline from ~121 on 2022-03-10 to ~94 on 2022-03-21, then a rise through ~150 by month end, with three readings on nearly every day.

**What this does and does not establish.** It establishes that no imputation or substitution is needed for missing dates, because none are missing — the intent statement's instruction to record the measured gap before choosing a handling rule is satisfied by a measured gap of zero. It does **not** establish that every value in the outage window is an original Penticton measurement. The archive was retrieved in 2026, four years after the incident, and `fluxtable.txt` carries no qualifier, flag or provenance column — only date, time, Julian date, Carrington rotation, and the observed, adjusted and URSI-adjusted fluxes. Whether values spanning the incident were measured, recovered, or reconstructed **cannot be distinguished from this file**, and this audit does not assert either way.

### Qualifiers found — days needing a handling rule

**Duplicate UT timestamps (5 days).** Two readings share one timestamp:

| Date | Readings (UT : observed flux) |
|---|---|
| 2022-03-26 | 17:119.4, 20:118.7, **23:117.7, 23:118.7** |
| 2022-09-20 | 17:137.6, 20:137.2, **23:134.9, 23:133.3** |
| 2022-10-17 | 17:123.4, 20:125.6, **23:120.5, 23:121.4** |
| 2022-10-23 | 17:106.4, **20:108.4, 20:105.5**, 23:108.7 |
| 2022-12-08 | **18:141.8, 18:140.1**, 20:143.0, **22:144.9, 22:143.5** |

**Within-day spread above 20% of the day's median (4 days)** — the signature of flare contamination in a single reading:

| Date | Readings | Median | Spread |
|---|---|---|---|
| 2022-01-18 | 18:148.8, 20:114.5, 22:111.6 | 114.5 | 32.5% |
| 2022-03-31 | 17:148.7, **20:239.5**, 23:149.8 | 149.8 | 60.6% |
| 2022-08-28 | 17:151.6, **20:251.9**, 23:133.5 | 151.6 | 78.1% |
| 2022-08-29 | **17:357.1**, 20:130.6, 23:123.0 | 130.6 | 179.2% |

Three of the four contaminated readings fall at 20 UT — local noon at Penticton, which is the conventional daily value — so a naive "take the 20 UT reading" rule would import a flare spike on 2022-03-31 and 2022-08-28.

### Decision this surfaces, not previously recorded

The driver contract fixes F10.7 as *previous-day observed value, lagged one day, with a trailing 81-day mean*. It does not state **which of the three daily readings is the daily value**, and this audit shows the choice is not cosmetic: the 20 UT convention collides with flare contamination on two days and with a duplicate stamp on 2022-10-23. A selection rule must be decided and frozen — candidates being the 20 UT reading, the daily median, or the 20 UT reading with a flare-rejection fallback — together with a tie-break for duplicate stamps.

This belongs in the frozen feature contract at **G-04 Feature safety** and must be settled before it can be part of the G-05 freeze. It is a driver-side specification decision, not a modelling choice made after seeing results.

### Locked-test boundary

One flagged day, 2022-12-08, falls inside the locked test month. **No seal is touched by this audit.** What was examined is the F10.7 *driver* archive — a public predictor series, retrieved and audited before the freeze exactly as the acquisition-freeze obligations require. No VTEC target value, no model, no prediction and no December performance quantity was accessed, computed or looked at. The December date appears here only because a year-wide data-quality scan cannot skip a month without leaving an unaudited hole in the predictor series.

## Summary Against the Obligations

| Obligation | Requirement | Status |
|---|---|---|
| 1 | Confirm provisional-grade Dst published for the full 2022 span as a single grade | **Discharged** — provisional for all twelve months, final non-existent, 365/365 days |
| 1 | Record provisional status | **Discharged** |
| 1 | Record the non-commercial-use notice | **Open** — notice not located on the pages retrieved; not reproduced from memory |
| 1 | Hash the retrieved files | **Discharged** — fifteen files hashed above |
| 2 | Audit the archive from 2022-03-18 for the outage | **Discharged** — zero missing dates |
| 2 | Report exact missing dates | **Discharged** — there are none |
| 2 | Report any qualifiers or reconstructed values | **Discharged in part** — 5 duplicate-stamp days and 4 high-spread days reported; the file carries no provenance column, so measured-versus-reconstructed is not determinable from it |
| 2 | Do not impute or substitute before the gap is recorded | **Honoured** — no imputation proposed; the measured gap is zero |

## Residuals Carried Forward

| # | Item | Owner | Due |
|---|---|---|---|
| EC1-R-1 | Locate and record the Kyoto non-commercial-use notice verbatim | Student | Before citation is finalised |
| EC1-R-2 | Decide and freeze the F10.7 daily-value selection rule and its duplicate-stamp tie-break | Student | G-04, before G-05 |
| EC1-R-3 | Decide the handling of the four high-spread days; a flare-rejection rule is a frozen feature-contract decision, not a post-hoc filter | Student | G-04, before G-05 |
| EC1-R-4 | If the provenance of March–April 2022 F10.7 values matters to the thesis narrative, ask NRCan directly; it is not recoverable from `fluxtable.txt` | Student | Optional, before claims |
