# Supervisor countersignature request — 2026-09-19

**To:** Dr. Reza Saraf Shirazi
**From:** Kimia Rezaei
**Concerning:** four Student + Supervisor items (TE §18.2 Q-16/Q-17; TE §18.3 "the IRI
role") arising from the 2026-09-19 scientific review and decision pass
(`CR-2026-09-19-SCI-REVIEW`, `CR-2026-09-19-SCI-DECISIONS`)

**Status, 2026-09-19 — items 1–4 are countersigned by the supervisor**, recorded on
the student's report, matching the mechanism `COUNTERSIGNATURE_REQUEST_2026-08-16.md`
items 1–2 established. All four items below therefore close their TE §18.2/§18.3
Student + Supervisor requirement as of 2026-09-19. (Earlier text of this status line,
preserved for the audit trail: *"The student reported, in the session that produced this
letter, that the supervisor has approved all four items below... This letter is the
prescribed evidence form still outstanding... Until countersigned, each item below stays
reported, not verified."* That interim state closed the same day.) **Countersigning an
item does not itself register a producer artifact, transcribe a config value, or pass
G-04** — G-04 needs every P0 decision resolved (many beyond these four) plus the
executable preflight of TE §18.3, neither of which this letter closes.

| # | Item | Status |
|---|---|---|
| 1 | D-42 — GFZ driver availability floors (Kp/ap 3 h, Hp60/ap60 1 h) accepted as project assumptions for a retrospective study | **Countersigned 2026-09-19** |
| 2 | D-43 — Interval semantics of the GFZ lag floors: margin measured from interval COMPLETION, not start | **Countersigned 2026-09-19** |
| 3 | D-45 — IRI-2016 benchmark run with standard (unmodified) index inputs, disclosed as a retrospective climatological reference, never as an operational forecast | **Countersigned 2026-09-19** |
| 4 | D-46 — F10.7 missing-update composition: reading B (carry-forward bound applied in clock hours, inclusive, from the missing value's expected availability instant) | **Countersigned 2026-09-19** |

Each item below states what is asked, why, and the evidence already produced. All four
were implemented and verified this session; none required an actual value not already
frozen elsewhere (D-10.3, D-21, D-25, D-116). Countersigning closes the TE §18.2/§18.3
requirement; it does not itself register a producer artifact, transcribe a config value,
or pass G-04 — those remain separate, later steps.

---

## Item 1 — D-42: GFZ driver availability floors as project assumptions

### What is asked

Countersign that the existing approved lag floors (Kp/ap ≥ 3 h, Hp60/ap60 ≥ 1 h, TE §6.2
rows 307–308, D-116) may be used as the **availability assumption** for the D-39/D-40
archived series, explicitly as a project assumption for a retrospective study — not a
demonstrated publication or revision-completion bound.

### Why it is needed

TE §18.2 lists "Any feature, its safe lag, or its missing rule" as a Student + Supervisor
item (Q-16, Q-17). No numeric value is chosen here — both floors were already frozen by
D-116 — but the *application* of an existing floor to an archived, no-publication-timestamp
product is itself a Q-16 reading and needs the same sign-off.

### Evidence

`evidence/audit_gfz_2026-09-18/` (provider files, hashes, comparison report); GFZ Kp
documentation (nowcast "can change for some time (typically a day or two)", archived at
its final stage); Hpo format/version-history files (single near-real-time algorithm grade,
no publication timestamp). Full text: `evidence/DECISIONS.md` D-42.

### If left open

`configs/features.yaml: availability_lags`'s `publication_latency_statement` fields for
`kp_safe`/`ap_safe`/`hp60_safe`/`ap60_safe` are prepared but their TE §18.2 basis stays
unverified.

---

## Item 2 — D-43: interval-completion reference instant for the GFZ lag floors

### What is asked

Countersign that the safe-lag floors in item 1 are measured from the **interval END**
(completion) of each 3-hour/1-hour observation window, not its start — i.e. Kp/ap
`available_at = interval_end + 3 h`, Hp60/ap60 `available_at = interval_end + 1 h`.

### Why it is needed

Vision §7.3 defines the observation timestamp only as "time represented by the value" —
it does not say start or end for an interval-valued index, and D-42 did not resolve this
either. The reference instant changes the honest lag: a value labelled by interval START
would clear the same numeric floor at the moment the interval merely *completes*, with no
margin at all (demonstrated in
`tests/test_feature_availability.py::test_interval_end_observation_timestamps_make_the_lag_a_post_completion_margin`).
This is a Q-16 item under the same TE §18.2 row as item 1.

### Evidence

Provider file headers verified directly: GFZ Hpo file, `hh.h is starting time in hours of
interval`; WDC file, positional 3-hour slots. `evidence/DECISIONS.md` D-43; implementation
in `src/external/spaceweather.py: select_lagged_series`, `src/features/build.py`.

### If left open

`select_lagged_series`/`assert_lagged_selection` (already implemented and tested) has no
frozen reference instant to cite in the six-entry configuration, and the producer
artifacts for `kp_safe`/`ap_safe`/`hp60_safe`/`ap60_safe` cannot be built unambiguously.

---

## Item 3 — D-45: IRI-2016 benchmark disposition

### What is asked

Countersign that the IRI-2016 benchmark is generated with its **standard, unmodified**
index inputs (shipped `apf107.dat`/`ig_rz.dat`, `version=16`, no `oarr` overrides),
disclosed in every table and interpretation as a **retrospective climatological
reference** — never as an operational forecast, never claimed to share the model's
information availability, and never used to claim operational superiority when
outperformed.

### Why it is needed

TE §18.3 names "the IRI role" a supervisor sign-off item; Vision §6.11 freezes the
benchmark's driver inputs before generation. This session's inspection of the actual
`iricore` package source (v1.9.0; `master` branch downloaded and read; see
`governance/CHANGE_RECORD_2026-09-19_scientific_decisions.md` §3) established, from the
Fortran source and the shipped index files, that IRI's own inputs are same-day-adjusted
F10.7 and centered 81-/365-day/IG12/Rz12 means, target-day ap — none of them
forecast-safe. Overriding them to look forecast-safe would change IRI's fitted
coefficients' input regime; the recommended and adopted reading is to leave them
standard and disclose the asymmetry instead.

### Evidence

`governance/CHANGE_RECORD_2026-09-19_scientific_decisions.md` §3 (full inspection table:
wrapper signature, version default, index file format, observed-vs-adjusted verification
against `fluxtable.txt`, override coupling, target-day ap, IG12/Rz12 windows).
`evidence/DECISIONS.md` D-45. Dependent patch (`governance/proposed/
P-3_iri_report_confirmations.patch`) was verified against this decision and APPLIED
2026-09-19 (`CR-2026-09-19-SCI-DECISIONS-P2` §1); it changes no runtime behaviour reachable
today (benchmark generation stays blocked at R-59 limb 1 regardless).

### If left open

**Superseded by the patch application above** (kept for the audit trail): `iri.py`'s
R-59 limb-3 confirmations previously kept the pre-D-45 wording
(`no_future_centering_confirmed = True` required); they were replaced 2026-09-19 to match
this decision. Benchmark generation itself stays blocked at R-59 limb 1 regardless (no
passing validation report exists) until an actual Kaggle run produces one.

---

## Item 4 — D-46: F10.7 missing-update composition, reading B

### What is asked

Countersign reading B for the daily-cadence composition of TE §6.2's "carry-forward ≤ 3 h,
then exclude" bound: when the designated `median(D−1)` is missing at 00:00 UTC on day *D*,
the previous median is carried for origins within 3 clock hours of that instant
(00:00–03:00, inclusive), and origins from 04:00 are excluded until a valid update
arrives — never a "one daily step" extension.

### Why it is needed

TE §18.2 Q-16/Q-17 names "its missing rule" a Student + Supervisor item. D-21 already
bound the composition question but never resolved what "≤ 3 h" means on a series whose
native step is 24 hours; `external-products` R-57a tabled two readings (A: one daily step;
B: literal clock hours) and adopted neither. This item adopts B.

### Evidence

Measured on the held provider file (D-21/D-22/D-23 applied, December readings never
read): 8016 hourly origins in Jan–Nov 2022, **0 carried, 0 excluded** — reading A and B
are extensionally identical on 2022 unless D-26's March–April provenance question later
removes days. `evidence/DECISIONS.md` D-46; implementation in
`src/external/spaceweather.py: resolve_f107_at_origin` (returns `F107Selection`).

### If left open

`configs/features.yaml: carry_forward_composition` stays unfrozen at the TE §18.2 level
even though its value (`clock_hours`) is otherwise ready to transcribe.

---

## Summary

None of the four items is gate-blocking for anything already completed this session —
each was implemented and verified as a prepared decision regardless. They block: (a) the
six-entry `availability_lags`/`carry_forward_*` transcription's claim to satisfy TE §18.2;
(b) applying the D-45 dependent patch to `src/external/iri.py`'s R-59 confirmations with a
verified basis; (c) G-04 itself, which needs every P0 decision resolved, not merely
implemented. No academic approval beyond these four items is requested or granted by
countersigning this letter.
