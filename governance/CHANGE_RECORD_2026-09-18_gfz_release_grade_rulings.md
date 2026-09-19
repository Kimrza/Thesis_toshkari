# Change Record — 2026-09-18 — GFZ release-grade rulings, R-63 control-5 disposition, Q4/Q5 disposition

**Change ID:** `CR-2026-09-18-GFZ-RELEASE-GRADE-RULINGS`
**Authority:** the project decision owner's rulings of **2026-09-18**, given in-session
after `CR-2026-09-18-GFZ-DRIVER-PAIR-AUDIT` reported its measured results ("Approved with
the following rulings", five numbered items, reproduced in §1). Vision §15.2 change
control applies to the design amendment in §3; the owner's ruling 3 ("Amend the design
text accordingly") is the approval that permits an annotation to two completed-stage
artifacts (`CHANGE_RECORD_PROCEDURE.md` § Files a sweep may not edit).
**Repository state:** HEAD `18843aa`, working tree carrying the uncommitted D-25 Route 1
reconstruction and the GFZ driver-pair audit. **No commit is made by this pass.**
**Register discipline:** no agent writes `evidence/DECISIONS.md`. The release grades and
the Q4/Q5 disposition ARE decisions (they fix which provider grade a feature contract
consumes and name producer-artifact identities), so **D-number texts are DRAFTED in §4
for the student to adopt** (`project.md` `code-generation:c31`); until adopted they bind
nothing, and the owner's own condition holds: **no producer artifact is created and no
`permitted_producers` row is written until the G-04 release-grade record, the Q4/Q5
record and the amended Hp60 R-63 text are complete** — the first two of which complete
only on the student's adoption.

> **Adoption status, 2026-09-18 (later the same day).** The student approved D-39 and
> D-40 **with binding qualifications** and instructed that the qualified decisions be
> appended to `evidence/DECISIONS.md` ("This authorizes recording my student decisions,
> not passing G-04 or releasing producer artifacts"). Both entries were appended, as
> **student decisions** (§4a); **no supervisor approval exists or is claimed** and the
> countersignature requirement is left OPEN in the register's review table. **D-41 is NOT
> approved** — it stays the proposal in §4b, revised to the student's requested shape.
> **G-04 is NOT passed.**

---

## 1. The rulings, as given (owner, 2026-09-18)

1. **Kp/ap release grade.** `Kp_now2022.wdc` (DOI 10.5880/Kp.0001) is approved as the
   historical forecast-available grade for the 2022 driver series. `Kp_def2022.wdc` is
   retained only as the definitive audit comparator and is not substituted for
   forecast-time features. The limitation is preserved: the archived nowcast is the settled
   final-stage nowcast, not an exact reconstruction of each first-issued value.
2. **Hp60/ap60 release grade.** Hpo.0002 V2.0 is approved as the contemporaneous 2022
   grade. Hpo.0003 V3.0 is treated only as a later algorithm-recomputed comparison series.
   V2.0 versus V3.0 is never described as NRT versus definitive.
3. **R-63 control 5.** Kp/ap satisfies the literal control through the nowcast-versus-
   definitive comparison. For Hp60/ap60 the V2.0-versus-V3.0 comparison is formally
   accepted as a documented substitute control because no provider-native NRT/definitive
   pair exists; the design text is amended accordingly; the substitute demonstrates
   sensitivity to later algorithmic recomputation, not definitive backfill.
4. **Q4/Q5.** The required Q4/Q5 disposition is recorded consistently with these rulings
   before any governed artifact is produced or registered.
5. **Open gate items.** The W-4 manifest incompatibility, the W-9 identity-shape false
   positives, the fifth R-26 exclusion class and the pre-existing
   `ec1-audit-report.json` December-scan finding stay open for explicit gate disposition.
   The W-9 allowlist is not expanded merely to suppress legitimate provider identities.

## 2. Evidence the rulings rest on

`evidence/audit_gfz_2026-09-18/` (`CR-2026-09-18-GFZ-DRIVER-PAIR-AUDIT` §1–§3): four
provider files with SHA-256; 2022 coverage complete on all four; Kp nowcast vs definitive
1,046 / 2,920 epochs differ; Hp60 V2.0 vs V3.0 1,790 / 8,760 differ; provider
documentation quoted for the nowcast's settled status and for Hpo's single grade.

## 3. Design amendment applied (ruling 3) — dated blocks, nothing rewritten

- `construction/acquisition/functional-design/business-rules.md`, § "Constraint — THE
  REANALYSED-VALUE CHECK, DEFINED", immediately after the "re-acquired in BOTH grades"
  constraint: a dated **"Amended 2026-09-18"** block recording, per series, how the
  constraint resolved (Kp/ap: satisfied literally, grades ruled; Hp60/ap60: impossible as
  written, substitute control accepted, label fixed). The original constraint text is left
  standing as the specification that governed the retrieval. This is the authoritative
  site per the rule's own coordination clause.
- `construction/external-products/functional-design/business-rules.md`, § R-63, before
  the "Stated as a residual" box: the mirror block, same day, same content, plus the
  binding on `assert_gfz_cross_products`'s argument roles for Hp60 (`near_real_time` :=
  V2.0, `definitive` := V3.0) and the requirement that every artifact reporting it carries
  the substitute label.
- NOT amended: `scripts/04_build_external_products.py:751-759` (the "never retrieved"
  completeness entry — code under `external-products`' READY receipt; it will become
  wrong only when Stage 04 is pointed at the new evidence, and that is a code change owed
  to the gate, not a comment fix), `src/external/spaceweather.py` (the function is
  generic and unchanged), the story map and requirements (FR-P1-01-8 stays `UNTESTED`:
  the audit exercised the mechanism on real bytes, but no acceptance row exists).

## 4a. D-39 and D-40 — ADOPTED 2026-09-18 (student decisions; supervisor status OPEN)

The adopted texts are in `evidence/DECISIONS.md` § D-39 and § D-40 (appended after
D-38, before the D-1 addendum) with two rows in the § Supervisor review table. The
student's qualifications applied on adoption, beyond the §1 rulings:

- D-39: the archived nowcast is **not labelled proven available at every forecast
  origin**; it **includes post-issue revisions** and **does not reconstruct first-issued
  values**; **before producer release** the applicable feature-availability rule is
  established from evidence **or** the unresolved limitation and its implications for
  forecast claims are explicitly documented — **no publication lag is invented and no
  configuration is changed silently** (`availability_lags` stays `TBD — freeze gate`).
- D-40: the substitute applies to **Hp60/ap60 only**, under exactly the label
  **"Contemporaneous V2.0 versus later algorithm-recomputed V3.0"**; it is **not**
  NRT-versus-definitive and **establishes neither first-issue availability nor absence
  of information leakage**.
- Both: the reported percentages are **product-version differences**, never model-error
  percentages and never proof of leakage. Authorization is the **student's**; no separate
  supervisor approval is fabricated; whether one is required before a governed feature
  release is left open.

Wording aligned the same day, without broadening scope: `acquisition` R-40 and
`external-products` R-63 amendment blocks (the D-39/D-40 qualifications replace the
earlier "forecast-available grade" phrasing); `scripts/audit_gfz_drivers.py` driver
inventory `release_status` strings, and the regenerated `retrieval_record.json` /
`GFZ-AUDIT.md` (offline re-run; provider hashes unchanged).

## 4b. D-41 — PROPOSAL ONLY (not approved, not adopted; no artifact created)

> **Adoption status, 2026-09-18 (third ruling of the day).** The student approved the
> identities and source/comparator roles subject to checks 3 (`f107_81_trailing` derived,
> trailing, availability-obeying, existing window/missing rules preserved) and 4 (the
> D-25 Route 1 `availability_rule` contract cited exactly; scope F10.7 only). Both checks
> agreed with the existing approved contracts; `D-41` was confirmed unused; the entry was
> **appended to `evidence/DECISIONS.md`** with the checks' evidence inside it, as a
> **student decision**. Countersignature: **not required under TE §18.2** for D-41 (no row
> covers a source version or producer identity; D-10.1 precedent); the availability
> obligations remain §18.2 Q-16 Student + Supervisor items. **D-41 approves identities and
> roles only** — no temporal availability, no leakage-free certification, no producer
> release, no `permitted_producers` row, G-04 NOT passed. The proposal text below is
> retained as drafted; the adopted text (with the check evidence) is the register's.

### D-41 (proposed) — Q4/Q5 disposition: Hp60/ap60 provider is GFZ Potsdam; the three driver producer-artifact identities (freeze)

**Decided by:** (to be) the project decision owner. **Authority:** TE §6.2 ("GFZ or
approved source"), D-10.1, D-35 limb 3, D-39, D-40, D-21/D-22/D-23/D-25 (F10.7).

> **Q4 — provider.** The Hp60/ap60 provider is **GFZ Potsdam** (GFZ Helmholtz Centre for
> Geosciences, Geomagnetic Observatory Niemegk), narrowing TE §6.2's "GFZ or approved
> source" to its named default; no alternative source is approved. (Kp/ap3 → GFZ Potsdam,
> Dst → Kyoto WDC and F10.7 → NRCan SRMP observed flux are unchanged from D-10.1.)
>
> **Q5 — exactly three driver producer artifacts**, with these identities, roles and
> sources. **Every hash in the "Source SHA-256" column is an EXISTING, measured SHA-256 of
> a held input file. No output hash exists yet: the "Output" column is deliberately empty
> and is filled only by `src/data/release.py:write_release` when each artifact is actually
> released under TE §13.3, in its own owner-approved step.**
>
> | Producer artifact id | Serves (§6.2 rows) | Source product (selected version) | Source SHA-256 (existing, measured) | Output SHA-256 / `dataset_version` |
> |---|---|---|---|---|
> | `gfz_kp_ap_3h_2022_v1` | `kp_safe`, `ap_safe` | `Kp_now2022.wdc`, DOI 10.5880/Kp.0001, folder `Kp_nowcast` — the D-39 selected settled-nowcast product; 3-hourly, 2,920 epochs; 23,581 bytes | `7929d16aa1a14d35dff6759c02367746438b09dd084fdc731a4052af5a7475a4` | *(none yet — assigned at release)* |
> | *(audit comparator, NOT a producer input)* | — | `Kp_def2022.wdc`, same DOI, folder `Kp_definitive`; 23,581 bytes | `c1d9030254e5b1e9581065166ab501b7aad9f2e07756551aefa8b18302c2b829` | — |
> | `gfz_hp60_ap60_1h_2022_v1` | `hp60_safe`, `ap60_safe` | `Hp60ap60doi_2022.txt`, DOI 10.5880/Hpo.0002 (V2.0), folder `Hpo60` — the D-40 selected version; hourly, 8,760 epochs; 527,283 bytes; held as `hp60ap60doi_2022_v2.txt` | `0ad71bf0eab1412852dd57ade1f7e2fdf5ff18f1cf9d20ebab8babc1fe471ad6` | *(none yet — assigned at release)* |
> | *(recomputed comparator, NOT a producer input)* | — | same filename, DOI 10.5880/Hpo.0003 (V3.0); 527,342 bytes; held as `hp60ap60doi_2022_v3.txt` | `a689ddef5590bf9cb6cc32cf72817921c93bf7e40d658b9181e2b5a3f665d461` | — |
> | `srmp_f107_observed_daily_2022_v1` | `f107_safe`; `f107_81_trailing` is DERIVED from this daily producer, never a separate raw artifact | NRCan SRMP `fluxtable.txt` (observed flux, not 1-AU-adjusted), `evidence/audit_ec1_2026-08-15/nrcan_f107/`, retrieved 2026-08-15, 2,170,350 bytes, 23,848 records / 1,101 in 2022 / 365 days; daily value per D-21 (median), duplicate-UT per D-22, high-spread days per D-23, availability per D-25 (as reconstructed under `CR-2026-09-16-D25-AVAILABILITY-RULE`) | `4b7fbfde3b9d0140ef43e7487f5986fe18f93182dac5e1ee37a93fb6ebd690b9` | *(none yet — assigned at release)* |
>
> Each artifact, when released, records the full TE §13.3 manifest (`dataset_version`,
> `created_at_utc`, `source_manifest_id`, `source_files` with the source hash above,
> `processing`, `schema_version`/`units`, `row_counts`, `exclusions_qc_summary`,
> `fold_ids`/`mask_ids`/`feature_set_ids`, `output_files`, `change_record_id`) and the
> D-39/D-40 limitations verbatim. **No `permitted_producers` entry is written until the
> artifact it names exists** (D-35 limb 3), and no artifact is built until D-41 is
> approved, the D-39 item-4 availability obligation is discharged or documented, and the
> Hp60 R-63 design text (amended 2026-09-18) stands.

**Open before D-41 can be adopted:** the student's review of the identities and roles
above; confirmation that `f107_81_trailing`'s derived status (no separate raw artifact)
is the intended reading of Q5; and whether the D-25 Route 1 `availability_rule` contract
is the mechanism the F10.7 producer's manifest will cite.

## 5. Open gate items (ruling 5) — explicitly NOT disposed here

| # | Item | Owner of the disposition | Where recorded |
|---|---|---|---|
| G-1 | W-4 `write_sha256_manifest` shape fails TA-15's flat reader (`tests/test_release_hashes.py`) | `acquisition` / `fixtures-and-reproducibility`, at the `build-and-test` gate | `CR-2026-09-18-GFZ-DRIVER-PAIR-AUDIT` §5.1 |
| G-2 | W-9 heuristic refuses ordinary provider identities (≥20-char three-class tokens); allowlist NOT to be grown for that | `acquisition` | §5.3 there |
| G-3 | R-26 driver-exclusion table needs a fifth class (raw GFZ files + derived audit JSON) | `governance-guards` design | §5.2 there |
| G-4 | Pre-existing `evidence/audit_ec1_2026-08-15/ec1-audit-report.json` December-scan offender (`"2022-12-31"`) | `governance-guards` / R-26 class 3 | §5.4 there |
| G-5 | `features-and-splits` code-summary stale under its receipt (D-25 Route 1) | gate finding, `gf-3` | `CR-2026-09-16-D25-AVAILABILITY-RULE` §5 |
| G-6 | Script 04's "GFZ never retrieved" completeness entry is now historical | `external-products` | §3 above |

## 5a. December driver access — verification against the actual policy (ruling 5)

Lexical cleanliness of the JSON outputs is **not** the compliance argument; the policy
sources are:

- **Vision §8.3** governs *December target values* ("may be audited for coverage and
  regime counts without inspecting model performance") and *locked-test access*
  ("recorded in the experiment registry with `locked_test_accessed = true`"); TE §13.4
  defines the column for the locked test set. The audit read **no target value** — the
  four files are provider geomagnetic-index series — so `locked_test_accessed = false` is
  the truthful value and no access-log row is owed under §8.3 as written.
- **`governance-guards` R-26** (design): a December *hit* is a target value or a
  target-derived aggregate; December-dated **driver** captures are excluded by "a
  recorded and tested exclusion … pinned to exactly that set", enumerated exhaustively at
  **four classes** on 2026-08-28. The new raw GFZ files and `gfz-comparison-report.json`
  (which carries per-month mismatch counts including month 12 — a **driver** aggregate,
  not a target aggregate) are December-bearing driver artifacts inside R-27's scan root
  that **no enumerated class covers**. Strictly read, R-26's exclusion does not yet reach
  them: they are neither hits nor enumerated exclusions. That is gate item **G-3**, kept
  open; this record does **not** broaden the exclusion. The integer-keyed serialization
  keeps driver epochs mechanically distinct from target-date literals; it is not offered
  as the compliance argument, and the scan's `*.json`/literal narrowing is the guard's
  own disclosed limit, untouched.
- **`project.md` § Forbidden** ("NEVER let December inform model selection, feature
  selection, thresholds or hyperparameters; the trigger is December being seen"):
  December driver values *were* seen by the comparison. No selection, threshold,
  hyperparameter or feature choice was made from them; the mismatch statistics are
  reported per month without any use. Recorded as exposure, not as a violation, and
  carried to the gate.
- **Registry:** every run appended through `append_registry_event` with `code_commit`
  and a supplemental `environment_lock_hash` (not `capture_environment_lock`; stated in
  `notes`); the `exploratory` derivation found no access-log row for these run ids,
  consistent with no locked-test access. 22 rows at the time of writing (5 failed, 1
  online completed, 5 offline completed), none deleted.

**Conclusion:** `locked_test_accessed = false` complies with Vision §8.3 / TE §13.4;
**R-26 compliance is not claimed** until G-3 is disposed with an enumerated class.

## 6. Propagation sweep (CHANGE_RECORD_PROCEDURE step 2)

Superseded literal: "never retrieved" (GFZ). Sites: `scripts/04_build_external_products.py:751`
(code, left, G-6); `external-products/functional-design/business-rules.md` R-63 table
("⚠ NEVER RETRIEVED", two rows) and `business-logic-model.md:664-672` (same) —
completed-stage artifacts; R-63 carries the dated amendment block immediately below its
table and is therefore self-correcting to its reader; `business-logic-model.md` is NOT
annotated (owner approved amendment of the "design text" for control 5, which lives in
`business-rules.md`) and is listed as a residual; `acquisition/functional-design/
business-rules.md` R-40 table rows "never been retrieved" — the dated block sits directly
beneath. No count or ID range is amended by this record.

## 7. What remains before producer artifacts

> **Updated 2026-09-18 after D-41 adoption.** Items 1–2 below are superseded: D-39, D-40
> and D-41 are adopted (student decisions). Remaining before any producer artifact:
> (i) the D-39 item-4 / D-40 availability obligation — the rule established from evidence
> or the limitation documented, a TE §18.2 Q-16 Student + Supervisor item, then the
> `availability_lags` transcription (all six entries together, D-25 rule for F10.7 via
> `previous_day_median_midnight_utc`, scalar lags for the four GFZ rows) under its own
> record; (ii) G-04's supervisor involvement for ambiguous inputs (Kp/ap settled-nowcast
> limitation); (iii) G-1…G-6; (iv) a governed environment (Python 3.11 + pyyaml) for
> `capture_environment_lock` / `load_configs`; (v) the owner's explicit release
> instruction per artifact, each writing its TE §13.3 manifest through `write_release`
> and only then its `permitted_producers` row.

1. Student adopts D-39, D-40, D-41 (or amends them) in `evidence/DECISIONS.md` and records
   countersignature status.
2. The G-04 release-grade record is then complete for Kp/ap and Hp60/ap60; F10.7's grade
   remains the D-25 pattern (recorded absence + unverified statement), unchanged.
3. Only then: producer construction under TE §13.3 via `src/data/release.py`, followed
   by the `permitted_producers` transcription — each its own owner-approved step.
