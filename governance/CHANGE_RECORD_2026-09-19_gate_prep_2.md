# Change Record — 2026-09-19 — Gate preparation 2: A1 acceptance, A2 rule-plus-window repair, A3/A4/G-3 proposals, G-1/G-2/G-4 and G-7…G-11 repairs, governed-suite result

**Change ID:** `CR-2026-09-19-GATE-PREP-2`
**Authority:** the project decision owner's scoped authorization of 2026-09-19 (ten
numbered items). Items authorised for implementation: A1 (record the qualified student
acceptance through the decision process; propagate the limitation), A2 (approve and
implement the rule-plus-window repair), A4 (prepare and validate the tolerance
procedure, no value), G-1 (narrow compatibility correction consistent with the
authoritative manifest contract), G-2 (review and narrow the allowlist change), G-4
(implement exclusions already granted by R-26 classes), G-5/G-6 (already applied
2026-09-18), G-7…G-11 (narrow fixes consistent with the runtime and reproducibility
contracts, no weakened tests). Items left OPEN by the same instruction: A3 (proposal
only), G-3 (proposal only), any change to an approved contract not covered above.
Forbidden and not done: config changes, producer artifacts, `write_release`,
`permitted_producers` entries, dataset registration, commit, push, declaring G-04 passed.
**Repository state:** HEAD `18843aa`; working tree as listed in §10. **No commit.**

---

## A1 — recorded as **D-42** (student acceptance; supervisor countersignature OPEN)

`evidence/DECISIONS.md` § D-42 + review-table row (appended, CRLF preserved; `D-42`
confirmed unused first). Scope: the existing approved floors — Kp/ap 3 h, Hp60/ap60 1 h —
accepted for a retrospective study as **project assumptions, not demonstrated publication
or revision-completion bounds**; they do not make settled archive values historically
available at those lags. **Binding limitation propagated:** "results using these archives
do not establish exact operational replay or absence of revision-related look-ahead" —
now an artifact field (`src/evaluation/metrics.py:DRIVER_AVAILABILITY_LIMITATION_STATEMENT`),
a claims-checklist disclosure row on the limitations surface
(`src/evaluation/diagnostics.py`, row "D-42", fragment `revision-related look-ahead`),
with the negative control
`tests/test_regimes_and_reporting.py::test_d42_driver_availability_limitation_row_fails_when_absent`
and the happy-path fixture carrying the statement; mirrored into `acquisition` R-40's and
`external-products` R-63's dated blocks. **No supervisor approval fabricated**: TE §18.2
Q-16 makes the countersignature REQUIRED, recorded as OPEN in the register. No config
transcribed.

## A2 — approved and implemented: the D-25 rule composes with the trailing window

`src/features/availability.py` (+279/−39 vs HEAD in total; A2's part):

- `AVAILABILITY_RULE_SCOPE = {previous_day_median_midnight_utc: {f107_safe, f107_81_trailing}}`
  — the rule is confined to the F10.7 rows; a rule on any other feature is refused at
  config read ("governs only …"). **Never extended to GFZ series.**
- `AVAILABILITY_RULES_WITH_WINDOW = {previous_day_median_midnight_utc}` — only a rule that
  can derive a window end day may carry a `window`; the four window fields are validated
  on the rule branch exactly as on the scalar branch (`_validate_window_fields`).
- The four concepts kept distinct in code and docstrings: **observation day** (the daily
  median's UT day), **constituent availability time** (`_constituent_available_at`: 00:00
  UTC of the following day under D-25), **window end day** (`latest_eligible_window_end`:
  the latest observation day whose constituent availability time is at or before the
  origin — derived, never conventional), **forecast origin**.
- `assert_anchor_recomputed` takes exactly one of `safe_lag_hours` / `availability_rule`
  (neither or both → `IntegrityError`); under the rule the recorded anchor must equal the
  derived end day (same-day AND stale earlier anchors refused), **every window constituent's
  availability time is verified against the origin**, the mean is recomputed from the
  anchor over 81 days, and a missing constituent still raises `IntegrityError` (TC-20).
  Scalar path unchanged. Limb 1 for the trailing row uses the rule semantics via the
  existing `max(observation/publication instant, rule instant)`; a later
  `publication_timestamp` on the trailing row still governs. `observation_timestamp` is
  never overwritten; no anchor-day-midnight convention remains.
- Daily source rows carry `day` and `value` only (existing contract), so a later publication
  of a constituent can reach the limb only through the trailing row's own
  `publication_timestamp` — stated in the docstring, not silently assumed.

Tests (`tests/test_feature_availability.py`, now 74 test functions, all green): rule +
trailing window accepted only for the D-25 rule (centered window refused; rule + scalar
refused; rule on `kp_safe` refused; a synthetic rule kind without window support refused);
anchor at D−1 for **all 24 origin hours** with the honest constituent instant (D−1 23:00),
measured lag = hour; end day derived across the **month boundary (1 Feb → 31 Jan) and the
year boundary (1 Jan → 31 Dec)** at 00:00 and 23:00; same-day anchor refused (by limb 1 at
build and by the anchor limb directly); stale D−2 anchor refused; missing constituent →
`IntegrityError`; recomputation mismatch refused; later publication timestamp governs;
scalar path unchanged. Mutation controls: 5 mutants, **4 killed** (same-day end day; scope
not enforced; any rule may carry a window; stale anchor accepted); the un-killed mutant
removes the per-constituent availability loop, which is defence-in-depth behind the
end-day equality and is unreachable by black-box behaviour today — stated, not hidden.
The superseded test `test_d25_rule_beside_a_trailing_window_is_refused` was replaced (its
assertion was the item-6 blanket exclusion this approval narrows); no other test weakened.
Contract text: `CR-2026-09-16-D25-AVAILABILITY-RULE` carries a dated A2 amendment.

## A3 — R-57a: complete proposal for review (NOT approved, nothing implemented)

**Governing wording.** TE §6.2 dictionary column for every driver row, `f107_safe` and
`f107_81_trailing` included: **"Carry-forward ≤ 3 h, then exclude."** TC-09 (`binding:
hard`, "the central leakage-prevention rule"). `external-products` R-57a: "A missing
external-driver value at an epoch may be filled by carrying the last observed value
forward for **at most 3 hours**; beyond that bound the row is **excluded**, never filled";
and its 2026-08-28 Constraint: the bound "has NO STATED MEANING on the one daily-cadence
series", the mechanism raises `FeatureAvailabilityError` while
`features.carry_forward_composition` is `TBD`, and two readings are tabled for the Student
at G-04. D-21: F10.7's carry-forward "composes with, and does not override, the ≤ 3 h
carry-forward bound". D-25: `availability_ts(median(D)) = 00:00 UTC on D+1`.
`spaceweather.resolve_f107_at_origin` implements the stop and never adopts a reading.

**The distinction the rule must make.** *Normal hourly reuse* of a valid daily value is
NOT carry-forward: `median(D−1)` is the designated value for every origin on day D by
D-10.3/D-25 — it is fresh at 00:00 D and equally designated at 23:00 D, because the series'
native step is one day. *Carry-forward* begins only when the designated value is itself
unavailable — `median(D−1)` missing (D-26's March–April 2022 provenance question is the
live instance) or not yet published under the rule — and the last available earlier
median is used instead.

**Reading A, as tabled (the proposal).** Bound staleness in the series' own axis: **one
daily step = one carry-forward step.** With concrete timestamps (all UTC):

| Origin | Designated value | Available? | Under reading A | Under reading B (literal clock hours) |
|---|---|---|---|---|
| 2022-03-15 00:00 … 23:00 (normal day) | `median(03-14)`, available 00:00 03-15 | yes | used at every hour — reuse, not carry-forward; staleness 0 daily steps | same |
| 2022-03-16 00:00 … 23:00, `median(03-15)` **missing** | `median(03-15)` | no | `median(03-14)` carried forward: 1 daily step (clock staleness 24–47 h past its availability instant); all 24 rows survive | rows 00:00–03:00 keep `median(03-14)` (≤ 3 clock hours past the *expected* availability instant 00:00 03-16); rows 04:00–23:00 **excluded** → 20 of 24 rows lost, all three cells |
| 2022-03-17, `median(03-16)` also missing | `median(03-16)` | no | second consecutive missing daily step → **exclude** all 24 rows of 03-17 | all 24 rows excluded |
| At the allowance under A: 1 step used | | | within | — |
| Beyond the allowance under A: 2nd step | | | excluded, never filled | — |

**What reading A changes, stated exactly.** It **re-expresses the frozen numeral "3 h" in
a different unit** ("1 daily step") for one series; the approved *missingness semantics*
(carry the last observed value, then exclude, never interpolate — D-5, TC-20) are
unchanged, but the approved *duration* is not applied literally: a carried value can be
up to 47 clock hours past its availability instant at hour 23. That is a §18.2 Q-16/Q-17
(Student + Supervisor) item. **Proposed replacement wording** for the `f107_safe` /
`f107_81_trailing` rows' carry-forward cell and for `configs/features.yaml:
carry_forward_composition` (value `daily_step`): *"F10.7 is a daily series (D-10.2); a
missing or not-yet-available daily median is carried forward for at most **one daily
step** (the previous day's median serves every origin of the affected day, up to 47 clock
hours after its availability instant); a second consecutive missing daily median excludes
the affected rows, never fills them. This is the daily-cadence composition of TE §6.2's
'≤ 3 h, then exclude' (D-21), frozen by the Student at G-04 as reading A."* Reading B's
replacement wording, if chosen instead (`carry_forward_composition: clock_hours`): *"the
3-hour bound is applied in clock hours from the expected availability instant 00:00 D;
rows at 04:00–23:00 of a day whose designated median is unavailable are excluded and the
excluded count is recorded as a split-manifest field."* **No reinterpretation of "≤ 3 h"
as "≤ 3 daily steps" is proposed.** Not implemented; `carry_forward_composition` stays
`TBD`; the resolver keeps raising.

## A4 — recomputation-tolerance procedure (prepared and validated on synthetic data; no value frozen)

- **Quantity compared.** For every scored origin, the recorded `mean_value` of
  `f107_81_trailing` (produced by the feature build) against the mean recomputed by
  `spaceweather.trailing_mean` from the released daily medians over the 81 days ending at
  the derived anchor (limb 3).
- **Units and precision.** Solar flux units (sfu); the provider records daily readings to
  **0.1 sfu** (`fluxtable.txt`, e.g. `000132.7`); daily medians are medians of 0.1-sfu
  readings, so every constituent is an exact decimal with one fractional digit; the mean
  of 81 such values is an exact rational.
- **Reference calculation (independent of the implementation).** Exact rational
  arithmetic: `Fraction(str(value))` per constituent, summed, divided by 81 — no floating
  point anywhere in the reference. The implementation under test is the float64
  `trailing_mean`; the recorded value is whatever the producing path wrote.
- **Tolerance semantics.** **Absolute**, in sfu (values are O(100), never near zero, and the
  discrepancy of interest is rounding, not scale). The a-priori float64 bound for an 81-term
  sum of values ≤ 300 sfu is 81 × 2⁻⁵² × 300 ≈ **5.4 × 10⁻¹²** sfu; the recording precision
  is 0.1 sfu, six orders above any rounding effect.
- **Acceptance criteria.** (i) Measured max |float − exact| over every scored origin of the
  governed run must be **below the a-priori bound** (5.4 × 10⁻¹²); any excess is an
  implementation defect, not tolerance to absorb. (ii) The frozen `recomputation_tolerance`
  is then set **from the a-priori bound, not from the observed discrepancy** (proposal: the
  a-priori bound itself, or one decade above it — the owner's Q6 choice), so a tolerance is
  never widened to accommodate an observed error. (iii) Two must-fire controls are part of
  the measurement run: an 80-day window and a one-day-shifted anchor must produce
  discrepancies ≫ tolerance.
- **Synthetic validation (this pass, scratchpad, no repository file):** 500 synthetic daily
  medians at 0.1-sfu resolution in 60–300 sfu, 419 windows: **max |float − exact| =
  1.05 × 10⁻¹³ sfu** (< 5.4 × 10⁻¹² bound); 80-day window differs by 0.706 sfu; anchor
  shifted one day differs by 0.993 sfu — both ≫ 10⁻¹¹.
- **Not done:** no measurement on production data; `recomputation_tolerance` stays `TBD`;
  no config change. **Further approval needed:** Q6 — the owner freezes the numeric value
  after the first governed recomputation, choosing between "= a-priori bound" and "one decade
  above", with the measurement report attached.

## G-1 — implemented: canonical manifest = TE §13.3 path-to-hash; metadata separated

Canonical representation established: **TE §13.3 `output_files` — "Relative artifact path
and SHA-256 for every release file"** — a flat `{relative path: sha256}` mapping. Its
consumers already agree: the twelve pre-TC-06 monthly `sha256_manifest.json` files,
`src/data/release.py:write_release` (`output_files`), TA-15's reader
(`tests/test_release_hashes.py`, every `evidence/**/sha256_manifest.json`), and
`scripts/run_walking_skeleton.py:_month_manifest_entries` (accepts flat). The one producer
that deviated was `acquisition.write_sha256_manifest`, whose nested payload mixed
metadata keys into the mapping. **Correction:** `write_sha256_manifest` now writes the flat
mapping under `sha256_manifest.json`, keyed by the on-disk name (`logical_name`, falling
back to `provider_filename`), and the W-4 metadata — provider identity with version
suffix per file, `provenance_class`, `producing_interpreter`, and the hash arithmetic
(`hash_count = provider_file_count + derived_artifact_count`) — in a sidecar
`sha256_manifest_meta.json` (`SHA256_MANIFEST_META_NAME`). **One format, no dual support**;
historical monthly manifests are unchanged and already canonical. Refusals verified by
test: hash-less provider record; unknown provenance class; empty interpreter; `full` with
no provider entries; **digest not 64 lower-case hex; ambiguous mapping** (two records to one
path; a derived artifact colliding with a provider file) — nothing written on refusal.
`tests/test_acquisition.py` updated accordingly (59 passed). `scripts/audit_gfz_drivers.py`
uses the writer directly; regenerated `evidence/audit_gfz_2026-09-18/sha256_manifest.json`
(flat, 8 entries) + `sha256_manifest_meta.json`; the interim
`w4_provider_sha256_manifest.json` of 2026-09-18 (a derived output of the same script,
not provider evidence) was removed — provider bytes and their hashes unchanged;
TA-15 green over the directory. Byte-change detection is TA-15's existing check (recorded
vs recomputed digest per declared file); missing declared files fail there.

## G-2 — reviewed and NARROWED

**Exact rule now in force** (`REDACTION_ALLOWLIST`, last entry): `^(?=.{1,48}$)RUN(?:[._-]RUN)+\.(txt|wdc|csv|tsv|json|jsonl|html|htm|hdf5|h5|nc|dat|zip|gz|tar|tgz|yaml|yml|md|log|xml|parquet|npy|ipynb|pdf)$` where `RUN = [a-z0-9]+ | [A-Z0-9]+ | [A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)?` — at least two word-shaped runs joined by `.`/`_`/`-`, a data extension, ≤ 48 chars; known credential **prefixes are checked before the allowlist**.
**Newly accepted** (vs HEAD): provider filenames of 20+ chars mixing upper/lower/digits, e.g. `Hp60ap60doi_2022.txt`, `Kp_ap_Ap_SN_F107_since_1932.txt`, `madrigal_coverage_summary_2022-FULL.csv`.
**Downstream handling inspected:** `guard_egress_value` runs the two structural carriers (signed URL, auth header) unconditionally first, then prefixes, then the allowlist, then the entropy heuristic; `guard_egress_free_text` tokenises prose and applies structural+prefix checks per token (no heuristic) — an embedded filename passes, an embedded `ghp_…` token still fails. **Representative unintended inputs verified refused** (tests): prefix-dressed (`AKIA…_2022.txt`, `ghp_…_notes.md`, `xoxb-…_2022.txt`), 3-class token without extension, **49-char boundary** (48 passes), 3-class runs with a separator (`Q7r8S9t0U1v2_W3x4Y5z6A1b2.txt` — accepted by the 2026-09-18 rule, refused now), AWS-secret-shaped runs with extension, consecutive separators, upper-case extension, path-like mixed-case strings.
**Remaining limitations:** (i) a secret composed only of lower-case+digit runs with separators and a data extension under 48 chars would pass — no known provider issues that shape; (ii) path-like values (`evidence/…/Kp_now2022.wdc`) are still refused by the heuristic when mixed-case — callers must pass bare filenames (the audit script does); (iii) this is one allowlist entry, structural, not a name list.

## G-3 — proposed fifth R-26 class (NOT adopted)

**Class 5 — "Raw GFZ geomagnetic-index captures and their derived audit reports."**
Path pattern (evidence-relative): `audit_gfz_*/Kp_*.wdc`, `audit_gfz_*/hp60ap60doi_*.txt`,
`audit_gfz_*/retrieval_record.json`, `audit_gfz_*/gfz-comparison-report.json`,
`audit_gfz_*/sha256_manifest*.json`, `audit_gfz_*/environment_supplemental.json`,
`audit_gfz_*/GFZ-AUDIT.md`. **The folder name alone never qualifies content**: eligibility
= exact path pattern **AND** content check — for JSON, no key token in
`TARGET_INDICATOR_KEYS` (vtec/tec/target/y_hat/prediction/metric/rmse/mae/paired/estimand/
coverage/madrigal/station/cell/aruc/bshm/nico/mask/fold/model, …) at any depth; for raw
`.wdc`/`.txt`, the provider header must be present (`# PURPOSE: … Kp index` / `Hp60 index`)
and every data line must parse as the provider's index format with no extra columns. A
target value, a model prediction, an evaluation metric or a mixed-content file at any of
these paths is **flagged**, exactly as the G-4 implementation already flags mixed content
at class-3/4 paths. **Safeguards:** (1) driver-only content, enforced by the two-condition
eligibility above and pinned by a negative control (a `vtec_tecu` key or a prediction file
placed in `audit_gfz_*/` is flagged); (2) the enumeration test pins **five** classes exactly
— no glob over `evidence/`; (3) D-39/D-40's roles ride the class: `Kp_def2022.wdc` and
`hp60ap60doi_2022_v3.txt` are audit comparators, never inputs — the class excludes them
from *custody* only, never licenses their use (R-26: "a custody exclusion is never a
licence to use"); (4) December driver values in these files are "seen" under `project.md`
§ Forbidden — recorded as exposure; no selection, threshold, hyperparameter or feature
choice may be made from them, and the comparison report's month-12 counts are driver
aggregates only. **Adoption requires** the owner's edit of R-26's design table (a
completed-stage artifact) and the corresponding code entry; until then the GFZ files
remain outside any exclusion — and, being `.wdc`/`.txt` plus integer-keyed JSON, they are
neither flagged nor excluded by the scan, which is the ambiguity this proposal resolves.

## G-4 — implemented: R-26's four classes, content-gated

`src/data/locked_test.py`: `DECEMBER_DRIVER_EXCLUSION_CLASSES` (exactly R-26's four:
`dst_provisional_*.html`, `fluxtable.txt`, `ec1-audit-report.json`, `.dst_summary.json`),
`TARGET_INDICATOR_KEYS`, `december_driver_exclusion_class(candidate, root, text)` — exact
path match **and** driver-only JSON content (no target-indicator key at any depth);
`assert_no_december_outside_restricted` consults it only for a December-bearing JSON, and
an unparseable JSON still fails via `fail_unparseable`. No field renamed, nothing
reserialized, no class added. Verified: the real `evidence/` tree scans **clean**
(`ec1-audit-report.json` excluded by class 3 with its F10.7 date range; `.dst_summary.json`
by class 4); a mixed-content file at the class-3 path (`december_coverage_pct` or
`vtec_tecu` beside the driver keys) is **flagged**; any December-bearing JSON outside the
four classes — including one under `audit_gfz_*` — is flagged; the enumeration is pinned
at four (`tests/test_locked_test_guard.py::test_r26_driver_exclusions_are_exactly_four_and_content_gated`).
**Ambiguity returned, not assumed:** R-26 class 1 and 2 are non-JSON and the scan reads
`*.json` only — their exclusion is path-only and never exercised by the scan (the guard's
own disclosed narrowing).

## G-5 / G-6 — applied 2026-09-18 (`CR-2026-09-18-GATE-PREP` §3); unchanged.

## G-7 … G-11 — diagnosed and repaired under the governed pin

| Item | Diagnosis (inspected) | Repair | Why it is not a weakening |
|---|---|---|---|
| **G-7** | Production: every stage script calls `ensure_process_determinism` then `seed_everything` **once, first, per process** (R-05); no production workflow re-seeds in one process. `seed_everything` performs its own deferred `import tensorflow`, so in ONE pytest process the first call makes every later call refuse — correct under R-05, but six `test_determinism` tests and `test_clean_run`'s stage-entry test (which called `_stage_entry`, hence `seed_everything`, **three times in one test**) assumed re-entry; three `test_models_smoke` assertions measured `"tensorflow" not in sys.modules` in a process where earlier tests had imported it. | `tests/_fresh_process.py::in_fresh_process` — re-runs the decorated test in a **fresh interpreter** via `pytest <nodeid>` (the stage script's execution model), child failure fails the parent, output relayed. Applied to the six determinism tests, the three models_smoke purity tests, and the stage-entry test **split into three one-process tests** (the `BEYOND_ENUMERATION_CONTROLS` ledger updated; the control count stays outside the 39/11 ledger). | Test bodies unchanged; every assertion executes in a process that matches how the code actually runs; no skip, no marker, no ordering assumption hidden. Reproducibility is asserted by the child run itself. `seed_everything`'s contract untouched. |
| **G-8** | `tests/test_bootstrap.py::test_real_config_confirmatory_shape_rereads_never_literal`: the fixture `_prediction` built April timestamps (default `month=4`) for days 2–31 before the test rewrote them to December; day 31 does not exist in April. A **fixture date bug**, unreachable until pyyaml/numpy let the test run. Not production date handling. | `_prediction(..., month=12)`; the post-hoc rewrite removed. | Same assertions, same D-28 window; the fixture now builds the dates it always intended. |
| **G-9** | `test_real_repository_configs_refuse_today` asserted the pre-D-38 state. D-38 (2026-09-10) transcribed the six partitions; the governed loader now accepts them — the governed-environment check D-38 recorded as owed. | Renamed `test_real_repository_configs_carry_the_d38_transcription`: asserts exactly the six R-80 ids with D-38's bounds and `embargo_hours == 24`, and **keeps the refusal checks on the same real files** (block removed → refuse; `TBD` embargo → refuse); synthetic-block refusals unchanged above it. | The negative checks are preserved on real inputs; the positive assertion is D-38's own table. |
| **G-10** | Intended semantics established from D-5/D-10.2 (a gap is an explicit missing value) and the persistence module's own contract ("a missing source value yields a missing `y_hat`, counted"): missing is `None` in a record sequence and `NaN` once pandas materialises the frame (a float column cannot hold `None`). **Real defect found downstream:** `src/evaluation/masks.py:_prediction_keys` tested `y_hat is not None`, so under pandas a missing member prediction (`NaN`) entered the comparison-wide intersection as present — a NFR-FAIR-01 correctness bug, exposed only now. `persistence_rows` likewise counted only `None`. | `masks._is_missing` (None or NaN) used by `_prediction_keys`; `persistence_rows` counts `None` **or** `NaN` and normalises to missing; the models test asserts *missing* in either representation; new control `tests/test_common_masks.py::test_a_missing_member_prediction_is_excluded_whether_none_or_nan` — **proven to bite on the pre-repair masks.py** (mutation run, restore SHA-verified). | Scientific behaviour restored to the approved contract (missing never enters the mask), not altered for green. `models-and-baselines` and `evaluation-and-comparison` code-summaries stale for this edit (gf-3, disclosed). |
| **G-11** | `test_m06_fit_refuses_at_the_guard_before_any_tensorflow_import` ended by asserting `ModuleNotFoundError` — an environment fact (TF absent), not the guard property. | Both supported states asserted: TF absent → `ModuleNotFoundError` and TF still not imported; TF present (the governed environment) → `build_keras_model` builds `m06_compact_direct_lstm` and TF is observed imported **only after** the guard; the guard refusals before it unchanged; run in a fresh process. | The "no import before the guard" property is now proved in the environment the thesis actually runs in. |

## Suite results (governed pin: conda `tec-thesis-311`, CPython 3.11.16, every `requirements.txt` pin)

Focused runs during repair: `test_feature_availability` 74 tests green (A2 mutants 4/5);
`test_acquisition` 59; `test_locked_test_guard` 58; `test_common_masks` + `test_models_smoke`
green; `test_determinism` 46; `test_bootstrap`, `test_split_embargo`, `test_clean_run`,
`test_regimes_and_reporting` green; `compileall` 0; `ruff check` clean on every touched
module (pre-existing findings at HEAD left as found and listed in
`CR-2026-09-18-GATE-PREP` §6). **Full suite: 1256 passed, 4 skipped, 0 failed** (skips:
no fixture manifest yet — BLK-02; scikit-learn present so its refusal path is unreachable;
no hourly target artifact yet; `dataset_version` derived by `write_release`). The
2026-09-18 baseline was 13 failed. Registry rows appended by the offline audit re-runs and
the suite: 28 (append-only; none deleted). `artifacts/run_snapshots/`: 2 directories.

## §9 — records, access, tracking recommendation

- **Access:** no December target value read by any step; synthetic data throughout; the
  only real-evidence reads were the R-26 class-3/4 files (driver aggregates) and the GFZ
  audit's own outputs. No access-log row owed; none written. Registry rows and run snapshots
  untouched except by append.
- **Contents inspected:** `artifacts/registry/experiment_registry.jsonl` — 28 JSONL rows,
  every one a `gfz-driver-audit-*` run (5 failed with reasons, the rest started/completed
  pairs), `locked_test_accessed = false`, supplemental lock hashes (stated in `notes`).
  `artifacts/run_snapshots/<stamp>-<hash>/` — the four governed config files as read by
  `load_configs` (TE §13.1 per-run config snapshot), 2 directories, 88 KB.
- **Tracking policy:** `.gitignore` line 29 states the artifacts tree "is committed";
  `artifacts/exec_evidence/*` is tracked; `evidence/**` and `artifacts/**` are `-text`
  (DATA-01). **Recommendation:** commit `evidence/audit_gfz_2026-09-18/` (provider bytes +
  manifests + retrieval record: TE §13.3 provenance), `artifacts/registry/experiment_registry.jsonl`
  (NFR-AUD-01: failed runs stay visible), `scripts/audit_gfz_drivers.py`,
  `tests/_fresh_process.py`, the three change records and the register; commit the two
  run-snapshot directories only if the student wants the preflight probes of 2026-09-18
  reproducible by hash — they carry no data and are regenerated by every `load_configs`
  call, so a `.gitignore` rule for `artifacts/run_snapshots/` with a documented exception
  for governed runs is the cleaner policy (owner's call, listed in §11). Commit messages
  must cite D-25 (Route 1), D-39/D-40/D-41/D-42 and the CR ids per `team.md`.

## §10 — files changed by this pass (measured)

`src/features/availability.py` (A2), `src/data/acquisition.py` (G-1, G-2),
`src/data/locked_test.py` (G-4), `src/evaluation/masks.py`, `src/models/persistence.py`
(G-10), `src/evaluation/metrics.py`, `src/evaluation/diagnostics.py` (A1 disclosure),
`tests/_fresh_process.py` (new, G-7), `tests/test_feature_availability.py`,
`tests/test_acquisition.py`, `tests/test_locked_test_guard.py`, `tests/test_common_masks.py`,
`tests/test_models_smoke.py`, `tests/test_determinism.py`, `tests/test_clean_run.py`,
`tests/test_bootstrap.py`, `tests/test_split_embargo.py`, `tests/test_regimes_and_reporting.py`,
`scripts/audit_gfz_drivers.py` (G-1 writer), `evidence/DECISIONS.md` (+D-42),
`evidence/audit_gfz_2026-09-18/` (regenerated manifests; provider bytes unchanged; interim
W-4 file removed), `governance/CHANGE_RECORD_2026-09-16_d25_availability_rule.md` (A2
pointer), the two design files (D-42 blocks), the diary, this record. **Untouched:**
`configs/`, `scripts/00…07` except the 2026-09-18 G-6 string, `src/data/config.py`
(`seed_everything` contract), all D-25 Route 1 semantics other than A2.

## §11 — decisions still needed (smallest consolidated set)

1. **Supervisor countersignature of D-42** (TE §18.2 Q-16) — required before any
   `availability_lags` transcription or G-04 evidence is accepted. Outstanding.
2. **A3 — R-57a reading** (Student, with the supervisor under Q-16/Q-17): A (proposed,
   wording above) or B. Consequence of A: 24 rows survive on a one-day-stale median (up to
   47 h); of B: 20 of 24 rows lost per affected day in all cells.
3. **A4 — Q6 value rule**: freeze `recomputation_tolerance` at the a-priori bound
   (5.4 × 10⁻¹² sfu) or one decade above, after the first governed measurement.
4. **G-3 — adopt class 5** as proposed (R-26 table edit + code entry + negative control),
   or leave the GFZ evidence outside any exclusion.
5. **Transcription go-ahead** for the six `availability_lags` entries together, once 1–3
   are settled (F10.7 rows via the rule; GFZ rows via floors + statements).
6. **Tracking policy** for `artifacts/run_snapshots/` (ignore-with-exception vs commit).
