# Change Record — 2026-09-18 — Gate preparation: six-feature availability proposal, F10.7 window verification, G-1…G-6 dispositions, governed environment

**Change ID:** `CR-2026-09-18-GATE-PREP`
**Authority:** the project decision owner's instruction of 2026-09-18 ("Continue from the
current repository state and adopted D-39, D-40, and D-41 … turn the remaining release
blockers into evidence-backed, reviewable proposals and complete routine technical
preparation"), which authorises narrow, reversible technical fixes and factual
documentation updates that preserve approved behaviour, and forbids: new decision
adoption, config changes, producer artifacts, `write_release`, `permitted_producers`
entries, dataset registration, commit, push, and declaring G-04 passed.
**Repository state:** HEAD `18843aa`; working tree carries the D-25 Route 1
reconstruction, the GFZ driver-pair audit, D-39/D-40/D-41 in the register, and this
pass's edits (§3, §7). **No commit is made by this pass.**

---

## 1. The six `availability_lags` entries — derived, not recalled

`src/features/build.py:SECTION_6_2_ROWS` classifies exactly six rows as
`FieldClass.driver` — `kp_safe`, `ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe`,
`f107_81_trailing` — and `build_features` refuses any driver-class field without an
availability-matrix row (`build.py:791-799`). `dst` is `FieldClass.diagnostic`
(`DIAGNOSTIC_ONLY_SERIES`, TC-11) and needs no entry. `read_availability_lags` reads the
block per feature; TE §6.2 rows 307–310 and Vision D-116 (Q-16, Approved) fix the
contract: "Kp/ap lag ≥ 3 h, Hp60/ap60 lag ≥ 1 h, observed F10.7 lag 1 day, trailing
81-day mean, Dst diagnostic-only, SSN removed, carry-forward ≤ 3 h".

### 1.1 Per-entry proposal

Legend — **Approved assumption** = a value or rule the project has frozen without
independent evidence of historical publication timing; **Demonstrated** = supported by
provider evidence held in the repository.

| Entry | Selected source / grade | Observation timestamp semantics | Publication / revision timing (provider evidence) | Existing approved contract | Proposed value | Missing-data / carry-forward | Uncertainty and forecast-claim implication | Needs |
|---|---|---|---|---|---|---|---|---|
| `kp_safe` | `Kp_now2022.wdc`, DOI 10.5880/Kp.0001, `nowcast (archived, settled)` — **D-39**; definitive = audit comparator only | Start of the 3-hour UT interval the index describes (WDC cols 1–6 + slot; `hh.h` in the since-1932 file); the value characterises the whole interval, so it is not *observed* before the interval ends | **No per-value publication timestamp is archived.** Provider states only that nowcast values "can change for some time (typically a day or two)" and are archived at their final stage when the definitive month is computed (`kp_index_data_description_20210311.pdf` §4). No first-issue timestamp, no revision log per epoch. **"Typically a day or two" is a provider characterisation, not a maximum, and adding it as a delay does not reconstruct the issue history.** | TE §6.2: "last completed 3-hour interval … observation + publication timestamps … **≥ 3 h**"; D-10.3; Vision D-116 (Q-16 Approved); Q1 owner-approved value **3** | `safe_lag_hours: 3` as the **approved floor** (already frozen as ≥ 3 h; 3 is the transcription the owner approved as Q1). Whether 3 h reflects actual 2022 availability is **unverified** | TE §6.2 / TC-09: carry-forward ≤ 3 h then exclude; D-5/D-10.2: gaps stored as NaN (`-1` → NaN at acquisition) | The series is the **settled** nowcast: any 2022 forecast origin may have seen a value later revised. A 3 h floor measured against the interval start does not prove the value was published by then. Forecast claims must carry: "driver values are the provider's settled nowcast; point-in-time availability at 2022 origins is an approved assumption, not demonstrated". | **Owner decision (Student + Supervisor, TE §18.2 Q-16):** accept the D-25/EV-12 pattern for this series — record the approved 3 h floor plus a `publication_latency_statement` naming the absence and the settled-nowcast limitation — OR obtain provider release documentation (EC1-R-4-style request to GFZ) first. Then transcription. |
| `ap_safe` | same file, same grade (ap column) — **D-39** | as `kp_safe` | as `kp_safe` | as `kp_safe` (TE §6.2 row shared) | `safe_lag_hours: 3` (Q1) | as `kp_safe` | as `kp_safe` | same decision as `kp_safe` |
| `hp60_safe` | `Hp60ap60doi_2022.txt`, DOI 10.5880/Hpo.0002, `contemporaneous V2.0` — **D-40**; V3.0 = recomputed comparator only | Start of the 1-hour UT interval (`hh.h`); value characterises the hour | **No publication timestamp; no grade marker** (`D` "always 0, reserved"); Hpo is computed by a near-real-time algorithm from observatory data (`format_description_doi_10.5880.Hpo.0003.txt`); no per-value issue time is archived. The DOI-version label proves which algorithm produced the held values, **not** when a 2022 origin could have seen them. | TE §6.2: "Hourly-cadence … **≥ 1 h**"; D-116; Q2 owner-approved value **1** | `safe_lag_hours: 1` as the **approved floor** | TC-09 carry-forward ≤ 3 h then exclude; NaN at acquisition | Point-in-time availability **undemonstrated**; V2.0 is contemporaneous *by version*, not by issue time. Same claim caveat as Kp. | same decision shape as `kp_safe` (EV-12 pattern or provider documentation), then transcription |
| `ap60_safe` | same file (ap60 column) — **D-40** | as `hp60_safe` | as `hp60_safe` | as `hp60_safe` | `safe_lag_hours: 1` (Q2) | as `hp60_safe` | as `hp60_safe` | same decision as `hp60_safe` |
| `f107_safe` | NRCan SRMP `fluxtable.txt`, observed flux; daily median (D-21); duplicate-UT (D-22); high-spread (D-23) — **D-41** identity `srmp_f107_observed_daily_2022_v1` | Daily value of UT day D; observation completion 22–23 UT (D-25, measured from the held file: 22 UT on 120 days, 23 UT on 245 days) | **No publication timestamp in the archive** (D-21 "not derivable"; D-22 seven columns, no provenance column). **Approved project assumption** D-25: `availability_ts(median(D)) = 00:00 UTC on D+1`, explicitly "not a demonstrated fact"; EV-12 satisfied for F10.7 by recording the convention + absence + unverified statement (`CR-2026-08-22-EV-12`) | TE §6.2 `f107_safe` "1 day"; D-10.3 previous-day; **D-25**; Route 1 contract (`CR-2026-09-16-D25-AVAILABILITY-RULE`) | `availability_rule: previous_day_median_midnight_utc` (no scalar; Route 1 items 3–5) + `publication_latency_statement` (EV-12 form) | TE §6.2 carry-forward ≤ 3 h then exclude — **its composition on a 24-h cadence is the open G-04 freeze item R-57a** (`spaceweather.resolve_f107_at_origin` refuses while `features["carry_forward_composition"]` is unset); TC-20 never impute the outage window | Availability rests on D-25's assumption; claims must state "conservative convention, publication latency unverified". | **Transcription only** (rule identity exists in code; D-25 frozen) — but transcription is blocked until all six entries can be written together (owner rule), and R-57a's composition freeze is still owed. |
| `f107_81_trailing` | derived from `f107_safe`'s daily series — **D-41** (no raw artifact) | Window of 81 daily medians ending at the safe-lagged day D−1 (TE §6.2; D-25) | inherits `f107_safe`'s (no publication timestamps; D-25 assumption for the last constituent) | TE §6.2 row 310: trailing only, centered prohibited, "ending at the safe-lagged day"; D-25; limbs 2–3 in `availability.py`; `trailing_mean` (TC-20 never filled) | **Unresolved shape — see §2.** Under Route 1 the row may not carry the rule, so it needs `safe_lag_hours` + `window{kind: trailing, days: 81, source, recomputation_tolerance}`; `days: 81` is TE §6.2's frozen length; `recomputation_tolerance` is **measured then frozen** (TE §15.1; Q6 — not chosen here). The scalar value is a convention (see §2 counterexample), not an availability measurement | as `f107_safe`; a missing window day refuses the mean (never filled) | Same as `f107_safe`, plus: the scalar lag on this row is an anchor convention, so it must never be reported as a measured availability lag. | **Owner decision** on §2's proposed repair (rule + window on the trailing row) **or** an explicit convention ruling for the scalar; then Q6 measurement; then transcription. |

### 1.2 The smallest decisions this table needs (no numbers invented)

- **A1 (Student + Supervisor, TE §18.2 Q-16):** for the four GFZ rows, accept the
  EV-12/D-25 evidence pattern — approved floor (3 h / 1 h, already frozen as ≥) recorded
  together with a per-series `publication_latency_statement` that names the absence of
  publication timestamps and the settled-nowcast / version-label limitation — as the G-04
  availability record; or require GFZ release documentation before transcription.
  *Recommended: accept the pattern* (it is the sanctioned shape for an unobtainable
  provider field, and it keeps every forecast claim honest); consequence: the four
  `*_safe` GFZ features are governed by an approved assumption, and the thesis must say so
  wherever a lag is cited.
- **A2 (Owner):** §2's repair for `f107_81_trailing` (rule + window) or a recorded
  scalar convention.
- **A3 (Student, G-04 freeze item):** R-57a's carry-forward composition on the 24-h
  F10.7 cadence (reading A or B, as tabled in `external-products` R-57a).
- **A4 (Student, Q6):** `recomputation_tolerance` measured on the first governed
  recomputation, then frozen.

Only after A1–A4 can the six entries be transcribed **together** into
`configs/features.yaml: availability_lags` under a single record. Nothing was written
to `configs/` by this pass.

## 2. F10.7 trailing-window verification (executable, synthetic data, real code)

Script: scratchpad `f107_window_check.py` (not a repository file; its assertions are
reproduced in prose here). 293 checks, 0 failures. Origin days 2022-01-01 (year
boundary), 2022-03-01 (month boundary after non-leap February), 2022-07-15, 2022-12-31;
all 24 origin hours each.

| Check | Result | What it establishes |
|---|---|---|
| A — `trailing_mean(end_day=D−1, window_days=81)` | 96/96: exactly 81 consecutive days, last = D−1, first = D−81, mean identifies the window uniquely | Code behaviour: window is trailing, closed on D−1, no centred or future day |
| B — `assert_anchor_recomputed` with `safe_lag_hours = 24` | 96/96 accept anchor D−1 at every hour incl. 00:00; 96/96 refuse an anchor AT D | Code behaviour: the scalar 24 h places the anchor at D−1 for every hourly origin (`(origin − 24 h).date()`); a same-day anchor is refused |
| C — a missing day inside the window | `IntegrityError` raised | TC-20 behaviour: never filled |
| E — `f107_safe` under the Route 1 rule | availability instant = 00:00 UTC on D for all 24 hours | Code behaviour of the D-25 rule |
| **D — limb 1 on the `f107_81_trailing` row** | D1 fixture convention (`observation_timestamp` = anchor-day 00:00): passes, recorded lag 24.0 h. **D2 honest constituent instant (D−1 23:00): FAILS at 23/24 hours** (min lag 1.0 h < 24). **D3 availability instant (00:00 D): FAILS at 24/24** (min lag 0.0 h) | **Counterexample.** The scalar-plus-window shape passes limb 1 only when the trailing row's `observation_timestamp` is set to the anchor-day midnight — a convention, not the instant the last constituent became available. Under D-25 the last constituent is available at 00:00 D, so a true lag at origin hour h is h hours; no scalar ≥ 24 can pass that honestly, and any scalar that passes it (≤ 0) would defeat limb 1's purpose. |

**What the checks establish vs what stays assumed.** They establish that the code
selects exactly the 81 days ending D−1, refuses centred/same-day anchors and missing
days, and that the rule instant for `f107_safe` is correct. They establish nothing
about when NRCan actually published any 2022 value: D-25 remains an approved assumption.

**Pre-2022 coverage (verified on the held source, no download):** the first 2022 window
(origin 2022-01-01, anchor 2021-12-31) needs 2021-10-12 … 2021-12-31; `fluxtable.txt`
holds **81/81** of those days, 3 readings each (file starts 2004-10-28; 364 of 365 days
present in 2021, the absent day outside the window). No history shortfall; the scoring
period is untouched.

**Composition of the 24-h cadence with "carry-forward ≤ 3 h" (R-57a).** Not resolved
here. `spaceweather.resolve_f107_at_origin` refuses while `features["carry_forward_composition"]`
is unset; the trailing mean refuses a missing window day. The two compose consistently
only once R-57a's reading (A or B) is frozen; nothing in this pass chooses it.

**Minimal proposed repair (not implemented — semantic change, owner ruling A2):** let a
rule-bearing feature ALSO carry a `window` when its rule is
`previous_day_median_midnight_utc`, and have `assert_anchor_recomputed` derive the
expected anchor from the rule (anchor = availability-instant day − 1 = the observation
day) instead of from a scalar; limb 1 then uses the rule semantics (non-negative lag)
for the trailing row exactly as for `f107_safe`. This removes Route 1 item 6's blanket
exclusion for that one rule kind, adds one negative control (rule + `centered` window
still refused), and leaves scalar-lag features untouched. Alternative (no code change):
an owner ruling that the trailing row's `observation_timestamp` is *defined* as the
anchor-day 00:00 and its scalar as an anchor convention, recorded in the manifest as a
convention and never reported as a measured lag.

## 3. G-1 … G-6 dispositions

| Item | Root cause (files inspected) | Governing requirement | Proposed resolution | Class | Status / evidence to close |
|---|---|---|---|---|---|
| **G-1** manifest contract | `src/data/acquisition.py:write_sha256_manifest` emits `{provider_files{provider_filename: sha}, derived_artifacts, hash_count, provenance_class, producing_interpreter}`; `tests/test_release_hashes.py:_declared_artifacts` flattens EVERY `evidence/**/sha256_manifest.json` as `{on-disk filename: sha}`; `src/data/release.py:write_release` (`output_files`) is flat `{relative path: sha}` | **TE §13.3 `output_files`: "Relative artifact path and SHA-256 for every release file"** — the canonical contract is *path → hash*, which `write_release` and the TA-15 reader already follow. W-4's design (acquisition domain-entities § "sha256_manifest.json contents") keys provider files by provider identity and adds metadata keys, which TA-15 cannot read | (a) `write_sha256_manifest` keys provider entries by the on-disk `logical_name` (relative path) — provider identity already lives in `request_manifest.json`; (b) TA-15's reader recognises the W-4 shape by its `hash_count` key and flattens `provider_files` + `derived_artifacts`, ignoring the three metadata keys. Both keep TE §13.3 semantics. | **Owner ruling** — changes a READY unit's designed contract (W-4) and a governed test's reader | **Proposed, open.** Evidence to close: the GFZ audit's W-4 manifest re-emitted by the fixed writer under the governed filename, `test_release_hashes` green over it without the flat duplicate, one negative control (a metadata key is never treated as a file) |
| **G-2** W-9 false positives | `_heuristic_reason`: any 20+-char token with upper+lower+digits refused; five recorded refusals on ordinary provider filenames | SD-A-02: "A false positive lands on the allowlist under review"; owner: fix ordinary provider-identity false positives only, do not broadly expand | **FIXED (narrow, reversible):** one structural `REDACTION_ALLOWLIST` entry — separator-joined alphanumeric stem + known data extension, ≤ 48 chars — and the known-credential-**prefix** check moved BEFORE the allowlist so `AKIA…_2022.txt` is still refused. Two tests added (five filenames pass; prefix-dressed, extension-less, over-long, separator-less and signed-URL shapes all still refused). | Routine technical fix under the owner's explicit G-2 instruction | **Fixed.** `tests/test_acquisition.py`: 59 passed. Residual stated: a random 3-class secret that happens to carry a data extension and a separator would pass; no published credential format has that shape. `acquisition` code-summary now stale for this edit (disclosed here, gf-3) |
| **G-3** fifth R-26 class | `governance-guards` R-26 enumerates four excluded driver classes (2026-08-28); no coded list exists (`locked_test.py` has no exclusion structure); new December-bearing driver artifacts: `evidence/audit_gfz_2026-09-18/{Kp_now2022.wdc, Kp_def2022.wdc, hp60ap60doi_2022_v2.txt, hp60ap60doi_2022_v3.txt}` (raw indices, 2022-12 rows) and `gfz-comparison-report.json` (per-month driver mismatch counts, month 12 included) | R-26: exclusion "pinned to exactly that set", enumerated; custody exclusion is never a licence to use | **Proposed class 5 — "Raw GFZ geomagnetic-index captures and their derived audit reports"**, path `evidence/audit_gfz_*/` (raw `.wdc`/`.txt` + `retrieval_record.json`, `gfz-comparison-report.json`, `GFZ-AUDIT.md`, manifests). Safeguards: (i) driver-only — no target value or target-derived aggregate may ever be written there (a test asserts no `vtec`/target column and no target file); (ii) the enumeration test pins five classes exactly; (iii) D-39/D-40's "audit comparator only" roles ride the class (definitive Kp / Hpo V3.0 never become inputs); (iv) December driver values remain "seen" under `project.md` § Forbidden — recorded exposure, no selection from them | **Owner ruling** (design table + a governance-guards test) | **Proposed, open** |
| **G-4** `ec1-audit-report.json` | Content: `obligation_2_canadian_f107.first_2022_date = "2022-01-01"`, `last_2022_date = "2022-12-31"` (F10.7 date range — a driver-coverage aggregate) plus Kyoto month key `"12"`; no target value. `assert_no_december_outside_restricted` flags it on the literal `"2022-12` because the scan implements **no** R-26 exclusion; the scan has no production caller and its only tests run on synthetic roots | R-26 class 3 ("Derived driver audit report", this exact file) excludes it by design | Implement R-26's enumerated exclusion in `locked_test.py` (a pinned tuple of classes → path globs) consumed by the scan, with a test that the four (or five) classes are excluded and any other December-bearing JSON is still flagged | **Owner ruling** (governance-guards READY unit; a guard's scope) | **Proposed, open.** No field renamed, no serialization changed |
| **G-5** stale code-summary | `features-and-splits/code-generation/code-summary.md` described the pre-Route-1 module and "54 test functions" | `gf-3`: update the owning record or carry staleness explicitly | **FIXED (factual, dated post-receipt amendment appended; history preserved)** | Routine documentation update | **Fixed** |
| **G-6** script 04 "never retrieved" | `scripts/04_build_external_products.py:751-759` emitted a `missing_months` entry stating the GFZ series were never retrieved | R-61: completeness recorded machine-readably, truthfully | **FIXED (factual):** the entry now states "retrieved 2026-09-18 into `evidence/audit_gfz_2026-09-18/` but not yet consumed by this stage … integration owed under D-39/D-40/D-41"; superseded wording preserved in the comment. Behaviour (non-fatal completeness entry) unchanged; no integration performed | Routine factual update | **Fixed.** `tests/test_external_drivers.py`: 56 passed. `external-products` code-summary stale for this edit (disclosed) |

## 4. Governed environment (Python 3.11 + pinned requirements)

Runtimes found: system `C:\Python314` (3.14.7, untouched); conda 24.11.1 with envs
`base` (3.12.3), `ci` (3.10.13), `tensorflow_env` (3.8.20) — none 3.11. PyPI and
`repo.anaconda.com` reachable from this clone (unlike the earlier clone).
**Created** the isolated conda env `tec-thesis-311` (`conda create -n tec-thesis-311
python=3.11` → CPython **3.11.16**, the same patch level the 2026-09-13 session
installed via `uv`), then `pip install -r requirements.txt` into it — the pinned set
(numpy 1.26.4, pandas 2.1.4, **pyyaml 6.0.1**, scikit-learn 1.4.2, tensorflow 2.21.0,
pytest 8.2.2, ruff 0.4.8). No system Python replaced, no global package modified, no
version invented. Results of the install and the non-mutating checks are appended in
§6 once the install completes (network ≈ 100 kB/s at the time of writing).

## 5. Access controls and countersignature

No December target value was read by any step of this pass; synthetic data was used for
every behavioural check; the only real-evidence reads were `fluxtable.txt` day counts
(F10.7 driver, R-26 class 2) and `ec1-audit-report.json` (class 3). No access-log row is
owed and none was written. Registry: unchanged by this pass (the GFZ audit script was not
re-run). Decisions requiring countersignature, by provision: **A1** and **A3** (TE §18.2
"Any feature, its safe lag, or its missing rule — Student + Supervisor"); **A2** if it
changes the availability contract's semantics (same row); D-39/D-40/D-41 need none
(recorded 2026-09-18). G-04 itself: "Supervisor for ambiguous inputs" (Vision §13.1).

## 6. Verification appended after execution (2026-09-18, governed pin)

**Environment `tec-thesis-311` (conda, isolated):** CPython **3.11.16**; `pip install -r
requirements.txt` completed on the second attempt (the first failed with `WinError 32`
while the 350 MB TensorFlow wheel was being unpacked from a slow link; the retry used the
cached wheels). Verified imports: pyyaml **6.0.1**, numpy 1.26.4, pandas 2.1.4,
scikit-learn 1.4.2, tensorflow **2.21.0** (import succeeds, CPU), pytest 8.2.2, ruff
0.4.8 — every pin as written, none invented. System Python 3.14 and the three existing
conda envs untouched.

**Non-mutating preflight, first ever run through the production loader:**
`load_configs(Path("configs"), phase=1)` **succeeds** (all four governed files parse;
hashes `data.yaml 6093fcf18c82…`, `features.yaml b4d94b5f6383…`, `experiment.yaml
ca0cb2660c16…`, `seeds.yaml c951f949ae60…`); `assert_no_tbd(snapshot,
required=[features.availability_lags, feature_dictionary, feature_set_id, normalization])`
**refuses with `PreflightError`** naming all four as `TBD — freeze gate` — the expected
TE §18.3 stop, now produced by the governed mechanism rather than a stdlib shim.

**ruff 0.4.8 (pinned), on the files this session touched:** `ruff check` clean on
`src/features/availability.py`, `src/data/acquisition.py`, `scripts/audit_gfz_drivers.py`
after formatting the two files this session authored (`availability.py`: one constant
re-wrapped; `audit_gfz_drivers.py`: formatted, one `F541` fixed, `S310` scoped by pinning
the URL scheme+host to `https://datapub.gfz.de/`). Pre-existing findings left as found
(not this session's): `S101` in `availability.py` (present at HEAD), `I001`/`B015` and
"would reformat" in `tests/test_feature_availability.py` and `tests/test_acquisition.py`
(present at HEAD), "would reformat" in `scripts/04_build_external_products.py` (present
at HEAD). `compileall` under 3.11: exit 0. `scripts/audit_gfz_drivers.py --offline`
under 3.11: identical comparison counts (1046/2920; 1790/8760); two more append-only
registry rows.

**Full suite under the governed pin — `pytest tests` (pytest 8.2.2, py 3.11.16,
`PYTHONHASHSEED=0`): 13 failed, 4 skipped, remainder passed** (the same tree passes
1192/0 on 3.14 without TensorFlow/pyyaml/pandas — every failure below is *exposed by the
governed environment*, not introduced by this session's edits; none touches the D-25 or
GFZ modules, whose modules pass: `test_feature_availability` 68 passed / 0 skipped,
`test_acquisition` 59, `test_external_drivers` 56, `test_release_hashes`,
`test_locked_test_guard` all green). Isolated re-runs per module reduce 13 to **10**
(three `"tensorflow" not in sys.modules` assertions in `test_models_smoke` pass in
isolation — cross-module ordering).

| New gate item | Failures | Root cause (inspected) | Class |
|---|---|---|---|
| **G-7** `seed_everything` is not re-entrant within one process once TensorFlow is installed | `test_determinism` ×5 (isolated) / ×6 (full), `test_clean_run::test_optionb_00_stage_entry_real_invocation`, and the 3 ordering-dependent `sys.modules` asserts | `src/data/config.py:1072-1080`: R-05 refuses when `"tensorflow" in sys.modules` BEFORE its own deferred `import tensorflow`; the first successful call imports TF, so every later call in the same pytest process refuses. Correct for a stage script (one call per process); the test modules call it repeatedly. Never observable before because TF was never installed anywhere the suite ran. | **Owner ruling** (foundation READY unit / test harness): run those tests in subprocesses (the `test_determinism` re-exec tests already do), or a test-only reset hook — proposal, not applied |
| **G-8** `test_bootstrap::test_real_config_confirmatory_shape_rereads_never_literal` | 1 | `ValueError: day is out of range for month` at `tests/test_bootstrap.py:161 _ts` — with pyyaml present the test reads the REAL `configs/` for the first time and builds synthetic timestamps from a month/day it never exercised before (a latent test bug, reachable only now) | Routine test correction — **proposed**, not applied (`statistical-inference` READY unit) |
| **G-9** `test_split_embargo::test_real_repository_configs_refuse_today` | 1 | Expects `PartitionError` from the real configs; **D-38 (2026-09-10) transcribed `partitions` + `embargo_hours`**, so the real configs now load and the six partitions are accepted — exactly the D-38 verification that could not run then ("a full `load_configs` run is owed in a governed environment"). The test's "refuse today" fact is superseded by D-38. | Routine factual test update — **proposed** (asserting the D-38 state), not applied without the owner's word since it is a §12-mandated module |
| **G-10** `test_models_smoke::test_persistence_counts_a_missing_source_value_and_refuses_hyperparameters` | 1 | `assert nan is None`: with pandas installed the persistence baseline's frame carries `NaN` where the stdlib-records path carried `None`; the test was written against the stdlib representation | **Proposed**: decide the canonical missing-value representation across both representations (`models-and-baselines`); a real behavioural difference, not only a test artefact |
| **G-11** `test_models_smoke::test_m06_fit_refuses_at_the_guard_before_any_tensorflow_import` | 1 | `DID NOT RAISE ModuleNotFoundError` — the test expected TF to be absent; it is now installed. The guard-before-import property must be re-expressed without relying on absence | **Proposed** test re-expression (`models-and-baselines`) |

**D-38 verification closed by this run:** `load_configs(phase=1)` accepting the real
`partitions` block is the governed-environment check D-38 recorded as owed; recorded here
as evidence for the student to cite, not as a new decision.

**Side effect disclosed:** `load_configs` snapshots the four governed configs per call under `artifacts/run_snapshots/<stamp>-<hash>/` (TE §13.1 config snapshot; `src/data/config.py:787`); the preflight probes and the 3.11 suite left such snapshot directories there (88 KB, untracked, config copies only — no data). Left in place as run evidence; the student decides whether they are committed.

**Registry:** `artifacts/registry/experiment_registry.jsonl` now 24 rows (two more
append-only `started`/`completed` rows from the 3.11 offline audit run). No December
target value read; `locked_test_accessed = false` throughout.


## 7. Files changed by this pass

`src/data/acquisition.py` (G-2: +1 allowlist entry, prefix-check reordering; comments),
`src/features/availability.py` (ruff format only: one constant re-wrapped, no semantic change),
`scripts/audit_gfz_drivers.py` (ruff format, F541, URL scheme+host pinned; two regenerated
audit outputs `retrieval_record.json`/`GFZ-AUDIT.md` under 3.11, provider hashes unchanged),
`tests/test_acquisition.py` (+2 tests), `scripts/04_build_external_products.py` (G-6:
comment + one emitted string), `construction/features-and-splits/code-generation/
code-summary.md` (G-5: dated addendum), `construction/build-and-test/memory.md`
(diary), this record. Untouched: `configs/`, `evidence/DECISIONS.md`,
`evidence/audit_gfz_2026-09-18/`, `artifacts/registry/`, all D-25 Route 1 files.
