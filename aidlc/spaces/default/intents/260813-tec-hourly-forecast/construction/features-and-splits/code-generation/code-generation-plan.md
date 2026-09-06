# Code Generation Plan — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (W-1…W-10; R-74…R-84, R-76a), `nfr-design/security-design.md` (SD-F-00…SD-F-07), `nfr-design/logical-components.md`, `unit-of-work.md` §7, `requirements.md`, `application-design/component-methods.md` (ADR-11: `FrameSpec`, `Transform`, `FeatureBundle`, `build_features`, `fit_transforms`, `Partition`/`build_partitions`), `services.md` (bundle on-disk form `<partition_id>__<role>__<transform_id>/`). Answers: Q1=A (**R-74 approved** — BLK-04 contract), Q2=A (**R-83 approved** — BLK-09 amendment), Q3=A (separate-loader accessor), Q4=A (BLK-08 defer stands) — receipted.
**Authority**: G-09 signed (D-31); the Q1=A/Q2=A rulings lift the implementation bar; the change record recording both is Step 1 and precedes everything else.

## Ground rules binding every step

Same as prior units (3.11 target; in-place edits; no scientific constant in source; two-tier errors; docstrings; ruff clean; negative control per hard rule; nothing discharged; smoke ≠ governed; **no git commit**). Plus this unit's own: **no feature matrix is produced** (permitted-producer list unauthored — the fail-closed raise is the deliverable); **no December execution** (`materialise_locked_partition` refuses without a verifying G-05 signature; no test touches December content or the restricted root); **no inverse path and no `src/evaluation` → `src/features` edge** (Q4=A, D-27); raw longitude never a predictor; window length 24 asserted grid-free; membership from record timestamps; no random/shuffled CV; `scikit-learn` splitters unused; no windowing package; December never informs a threshold.

## Recorded input — nfr-design review Minors (human ruling 2026-09-05)

This unit's terminal READY (1 Major — the `snapshot.permitted_producers` owed-interface finding, resolved by Q3=A's separate loader; 1 Minor) findings are addressed by the receipted rulings or record-only; quoted at the stage gate.

## Steps

- [ ] **Step 1 — Change record FIRST: `governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md`** [Q1=A, Q2=A; GOV-2026-08-22-REM-01 exit ruling]
  Records the owner's approval of **R-74** (the ADR-11 train-only fitting contract: identity check `transform.partition_id == spec.partition_id` with the single enumerated `REFIT`→`DEC`/`role="score"` exception; `fit_transforms` raising on non-train role, non-None transform_id, scored range ≠ training range, id disagreement; untransformed bundles never consumable) and **R-83** (`Partition.train_start` + `train_end` both from `configs/data.yaml`, strict-subset control) as the governed BLK-04/BLK-09 contracts. BLK-08 recorded as deferred per D-27 (Q4=A). Blocker-register status updates routed to the gate (register lives in an approved Inception artifact — annotate-in-place needs the owner there).

- [ ] **Step 2 — `src/data/splits.py` (new)** [FR-P1-04-5/WS-12/TA-11 subjects; SD-F-04, SD-F-05; R-80, R-83; W-5, W-6]
  `Partition` (both bounds per R-83), `build_partitions(snapshot)` returning 6 (`F1`…`F4`, `REFIT`, `DEC`; `DEC.train_end = 2022-11-30` — structural December-fit bar); calendar VALUES read from `configs/data.yaml` (absent/TBD → refusal — they enter only at their freeze); split manifest enumerating exactly 5 rows (six fails, four fails); 24 h embargo excluded **and counted**; `assert_membership_from_timestamps` (validates, derives nothing); the evaluation-ROLE exactly-one reading carried to the gate, not adopted; `materialise_locked_partition(snapshot, *, g05_signature)` — `LockedTestError` when `None` or unverified (execution limb; read limb stays `open_restricted`'s).

- [ ] **Step 3 — `src/features/availability.py` (new)** [FR-P1-04-2/WS-11/TA-08 subjects; SD-F-03; R-75; W-1/W-1a]
  Availability matrix (six recorded fields per feature: observation ts, publication ts or documented absence + unverified-latency statement, release status, safe lag, actual lag, anchor); three limbs: lag assertion (Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 previous-day), trailing-not-centered, and the **anchor recomputation** (mean recomputed from the recorded anchor and compared — catches a recorded-but-wrong anchor); Dst diagnostic-only; SSN absent (grep-class assert); no backfill.

- [ ] **Step 4 — `src/features/build.py` + the separate loader (new)** [FR-P1-04-1/WS-10/TA-07 data-flow limb, FR-P1-04-16; SD-F-01, SD-F-02; R-76, R-78; W-2; Q3=A]
  `load_permitted_producers(configs_dir)` reading `configs/features.yaml`'s `permitted_producers` block — **unset/incomplete → `LeakageError` naming WHICH §6.2 rows lack entries; no feature matrix produced**; closed-dictionary construction (outside-dictionary name raises; `iri_*` raises); per-(row, producer) provenance resolution; support fields default-excluded unless an approval ID with a timestamp **preceding** the feature-set freeze (three separate assertions); raw-longitude raise (`lst_sin`/`lst_cos` only — blocked pending station-registry provenance, refusal states it); window length from `experiment.yaml` == 24 and in no grid (grid placement fails).

- [ ] **Step 5 — `src/features/transforms.py` (new)** [NFR-LEAK-01/TA-11 subject; SD-F-03; R-74; W-3; BLK-04 contract now approved]
  `fit_transforms(bundle, *, partition)` with the four raises; `Transform` with fitted state + `transform_id` (no inverse — Q4=A); identity check with the one enumerated exception; untransformed bundle (`transform_id is None`) never consumable; the R-77 two-class carry-forward boundary (field class a required argument; `vtec_lag_*` rejected at it; the two classes partition the feature set; every excluded window counted).

- [ ] **Step 6 — `src/features/windows.py` (new)** [FR-P1-04-8/WS-13 subject; SD-F-06; R-81; W-4; Q4=A upstream]
  One window definition emitting both representations in one `FeatureBundle` (`matrix.parquet`, `tensor.npy`, `spec.json` with identity fields + per-column `provenance` map — key set EQUAL to column set, both directions raise; dropped stamp = load failure); WS-13 parity as two ordered assertions (shape/ordering precondition, then value-level reconstruction within the fixture-manifest tolerance — **unrunnable until that tolerance is frozen; the check exists and stops naming the TE §15.2 field**); comparison-wide mask computed once per comparison set, stored, three ID stamps.

- [ ] **Step 7 — `scripts/05_build_features_and_splits.py` (new)** [W-10; §12/§13.2]
  Position 05; six-step entry (`ensure_process_determinism` first; `assert_no_raw_fields` before first write); orchestrates 2–6; registry rows via foundation's writer; honest `aborted` row on the permitted-producer refusal; no December path.

- [ ] **Step 8 — Tests** [Q12=C M10 fixture; Q3=C limb-1 placement]
  `tests/test_feature_availability.py` (§12-mandated; three limbs + negative controls incl. same-day-F10.7-through-trailing-mean caught by the anchor), `tests/test_split_embargo.py` (§12-mandated; exact boundaries, embargo excluded-and-counted, manifest row counts 4/5/6, strict-subset control, M10 part), `tests/test_train_only_transforms.py` (§12-mandated; manifest/bundle-based — full-dataset fit raises, train-role bundle at evaluation fails, cross-partition transform fails, untransformed-consumer fails, strict-subset fails; the **M10 synthetic fixture** over synthetic partition dates asserting (a) every ordered id pair raises except `REFIT`→`DEC` by enumeration, (b) that pair passes score/raises train, (c) scored-range mismatch raises, (d) `transform_id is None` consumers raise); **limb-1 cases added to `tests/test_locked_test_guard.py`** (Q3=C: signature-absent refusal, signature-invalid refusal, no December content; two-unit ownership block added to its docstring; existing cases untouched).

- [ ] **Step 9 — Full-suite smoke + lint** — green under 3.11.9 (smoke only); ruff clean on touched files.

- [ ] **Step 10 — Governance stop before commit (student acts)**
  The Step 1 change record exists FIRST. Gate items restated: blocker-register annotations (BLK-04/BLK-09 contracts approved, BLK-08 deferred); the permitted-producer LIST authorship assignment (assigned to nobody — needs an owner); the evaluation-ROLE exactly-one reading; FR-P1-04-10's proposed-not-approved acceptance row; the R-84/R-103 naming divergence (evaluation-and-comparison's pass); WS-13's TE §16 criterion reading. Commit cites **D-27, D-28, D-10.3** as touched context. **No governed commit before the records exist.**

## Out of scope

Producing any feature matrix or mask artifact (list unset), authoring the permitted-producer list (assigned to nobody — gate item), the inverse path + evaluation edge (D-27), December execution, the fixture-manifest tolerance, `test_common_masks.py` (TA-11's other module — evaluation-and-comparison's), every acceptance-row discharge (WS-10…WS-13, WS-18, TA-07/08/11/18/33/34/35 stay `Pending`; FR-P1-04-10 stays rowless).
