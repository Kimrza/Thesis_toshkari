# Code Generation Plan — `statistical-inference`

**Unit** `statistical-inference` (Bolt 10) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (R-113…R-122; W-1…W-8; `domain-entities.md`), `nfr-design/` (SD-S-01…SD-S-04; B1…B7), `unit-of-work.md` § 10 (Owns: `src/evaluation/bootstrap.py`, `tests/test_bootstrap.py`), `requirements.md` (FR-P1-05-8; context FR-P1-04-5, NFR-DET-01, NFR-REP-01, NFR-AUD-01). Consumed code: `src/evaluation/guards.py` (the six SD-C-01 refusals incl. `require_mask_member_alignment`), `src/evaluation/masks.py`/`metrics.py` (registered masks, `EstimandResult`, the estimand pipeline — one copy, R-114), `src/data/config.py` (`ConfigSnapshot`, `BootstrapError` if declared there else declared here per R-01's any-future clause), `configs/seeds.yaml` (`bootstrap: 20221201`, D-122).
**Answers (receipted)**: Q1 = A (percentile interval confirmed), Q2 = A (fixed non-overlapping 24-hour partition confirmed), Q3 = A (paired-error correlation series confirmed), Q4 = A (both `estimand` and `bootstrap` blocks transcribed).
**Authority**: D-122 (seed), D-28 (30-day DEC window; 720 h = 30 × 24 h), D-31 (module creation authorised), TE §13.6 / TC-19 (24-h vector blocks, 10,000 replicates, 95%, cross-station correlation reported, within-station variant rejected at Q-27); the three Q1–Q3 confirmations recorded in Step 1's change record with a proposed D-number. G-05/G-06 stay `Blocked`; BLK-08's ABL-DIFF limb open (D-27 unreopened).

## Ground rules binding every step

Same as prior units (3.11 target; in-place edits; no scientific constant in source — 24 h,
10,000, 0.95, 48 h, the seed and the confirmed method/scheme/series reach code ONLY from
`configs/`; two-tier errors; module docstrings; ruff or recorded substitute; a negative
control per hard rule; nothing discharged; smoke ≠ governed; **no commit**). Plus this
unit's own: the seed is a REQUIRED parameter read from `ConfigSnapshot.seeds` at the call
site (`TypeError` by signature when absent; ADR-05 carve-out — `seed_everything` never
touches it); PCG64 with seed-sequence spawns, child 0 = 48-h sensitivity, child 1 =
widening comparator, assignments recorded in `BootstrapResult`; NEVER a within-station or
naive bootstrap on any load-bearing path — the Q-27 variant exists only as the quarantined
comparator, never serialized as a reported interval; the estimand is NEVER reimplemented
(import `metrics.paired_loss_differential`'s pieces — R-114 one-copy); preconditions via
the sibling's `guards.py`, nothing duplicated; `numpy` imported lazily, absence refuses
naming the `numpy==1.26.4` pin; replicate hash = SHA-256 over the replicate vector's raw
IEEE-754 bytes with the four canonical-form facts (float64, little-endian, C-order, draw
order) recorded beside it; append-safe emission (never overwrite a prior `BootstrapResult`);
no completed sibling artifact edited (the sibling's naming of `vector_block_bootstrap`
among its guarded entry points stays OWED at its next touch).

## Steps

- [x] **Step 1 — Change record FIRST: `governance/CHANGE_RECORD_2026-09-06_R119_bootstrap_confirmations.md`** [Q1–Q4]
  Records the owner's three scientific confirmations (percentile interval — R-119; fixed
  non-overlapping 24-hour partition — R-115/Rec 26; cross-station paired-error correlation
  series — R-121) with ONE proposed D-number text for `evidence/DECISIONS.md` covering all
  three (owner adopts or edits; no agent writes the register), the Q4 transcription scope,
  and the honest limits (no supervisor signature exists or is claimed; WS-17/TA-13/TA-14/
  TA-26 stay `Pending`; the G-06 abort policy for a failed widening comparison stays owed to
  the Supervisor at G-05 per Rec 23).

- [x] **Step 2 — Config transcription: `configs/experiment.yaml` `estimand` + `bootstrap` blocks** [Q4 = A; R-118]
  `estimand`: orientation `benchmark_minus_model`, weighting `equal_station`, the sign
  sentence — citing Vision §2.3 / TE §1.3. `bootstrap`: block_hours 24, replicates 10000,
  confidence_level 0.95, sensitivity_block_hours 48, seed_key `seeds.bootstrap` (D-122),
  interval_method `percentile` (Q1), block_scheme `fixed_nonoverlapping` (Q2),
  correlation_series `paired_error_pearson_all_pairs` (Q3) — citing TE §13.6 / TC-19 / the
  Step 1 record. Nothing either authority does not fix is written; every other field
  untouched.

- [x] **Step 3 — `src/evaluation/bootstrap.py` (new)** [R-113…R-122; W-1…W-7; SD-S-01…SD-S-04]
  `vector_block_bootstrap(...)` with `seed` required (TypeError by signature): preconditions
  re-asserted via the sibling's guard module (registered mask, stamps, mask-member
  alignment, DEC receipt+containment, target space — one copy each); precompute the per-pair
  paired-difference array ONCE (W-2); block grid per the confirmed fixed non-overlapping
  24-hour partition with R-115's boundary raises (a block crossing a fold/embargo boundary
  or the scored window refuses; grid derived from the mask's window, no calendar constant in
  source); missing-pair handling per R-116 (declared rule or `BootstrapError`); PCG64 +
  seed-sequence spawns with the fixed child assignments; 10,000 replicate draws of 24-hour
  vector blocks (all three stations together); percentile interval from config
  (unrecognised/absent/unconfirmed method refuses naming the field — control (18));
  48-hour sensitivity on child 0 (15 blocks on DEC); widening comparator on child 1 — the
  Q-27 within-station method, exact parameters, same replicate count, QUARANTINED (guard
  evidence only: width, count, derived seed, outcome; fixture-time failure raises
  `BootstrapError`, real-data failure emits the mandatory machine-readable disclosure
  carrying both widths, the comparator parameters, block length/realised count, and the Q3
  correlations); cross-station paired-error Pearson correlations, all three pairs, on the
  masked rows; `BootstrapResult` with the replicate vector materialised in full, the SHA-256
  raw-bytes replicate hash + the four canonical-form facts + generator identity + seed key +
  stream assignments, append-safe write (never overwrite; atomic idiom). `BootstrapError`
  declared per R-01's any-future clause at the single declaration site (check
  `src/data/config.py` first; declare there ONLY if foundation's pattern requires it,
  else in `bootstrap.py` deriving from `IntegrityError` — record which).

- [x] **Step 4 — `tests/test_bootstrap.py` (new)** [W-8; SD-S-01 controls; TA-14's fixture shape]
  W-8's eight checks plus the per-entry controls: same-seed rerun → identical replicate hash
  (equality, not tolerance); different seed → different hash; a `BootstrapResult` missing
  any canonical-form fact / generator identity / seed key fails; stream-isolation control
  (removing the sensitivity consumer does not perturb the primary hash); block-grid boundary
  violations raise; missing-pair rule; unconfirmed/unrecognised method refuses naming the
  config field; fixture-time widening raise on a synthetic dataset with known cross-station
  correlation (widening holds by construction) and the quarantine control (comparator never
  in any serialized interval field); real-data-mode failure emits the disclosure with the
  correlations (absent disclosure fails — control (22)); missing `seed` is a `TypeError`;
  per-entry guard controls through `vector_block_bootstrap` (stamp-less prediction,
  unregistered mask, mask-mismatched `partition_id` set, receipt-less `DEC` call,
  transformed-space `ABL-DIFF` frame — this unit's half of the entry-point contract);
  append-safety (second write never clobbers). Config values re-read from
  `experiment.yaml`/`seeds.yaml`, never literal; synthetic year only; numpy-absent paths
  refuse by name (tests skip draws gracefully under the shim, refusals still assert).

- [x] **Step 5 — Smoke + lint** — scratchpad Python 3.11.16 + pytest shim (numpy/pyyaml
  uninstallable — PyPI unreachable; numpy-dependent draw tests will skip/refuse by name and
  that is recorded, not hidden); `compileall` on touched files; ruff owed, stdlib substitute
  run.

- [x] **Step 6 — Governance stop before commit (student acts)**
  Step 1's record exists FIRST. Gate items: the proposed D-number (adopt or edit); the
  sibling's OWED naming of `vector_block_bootstrap` among its guarded entry points (its next
  touch); the Rec 23 G-06 abort policy (Supervisor, at G-05); the Rec 40 change record
  against `services.md`/`unit-of-work.md` (storage-vs-memory conflation — owed, not made
  here); TE §15.3's reduced replicate count (fixtures-and-reproducibility's manifest); TA-21
  ownership dispute (carried); full pytest + numpy smoke owed when PyPI reachable; commit
  citing **D-122, D-28, TC-19** plus the new D-number if adopted. Nothing discharged:
  WS-17, TA-13, TA-14, TA-26 stay `Pending`.

## Out of scope

Executing any real bootstrap (no released features/predictions exist); the estimand itself
(sibling's, one copy); breakdown tables/figures (regimes-diagnostics-reporting); the
ABL-DIFF inverse (D-27 unreopened); any G-06/DEC execution; fixture manifests
(fixtures-and-reproducibility); editing any completed sibling artifact.
