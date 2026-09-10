# Freeze / Decision REQUEST — 2026-09-10

**Status: DECISION REQUEST ONLY.** This file contains inventories, options and
RECOMMENDATIONS prepared on the owner's gate worklist of 2026-09-10. **No value below is
adopted, no config file is edited by this request, no D-number is minted or proposed as
already existing, and nothing here is a decision.** Every choice belongs to the project
decision owner (and, where a governing document says so, the supervisor). Prepared by the
code-generation lane from repository state `cdc61f7`; refusal behavior on every listed
sentinel was probed live on 2026-09-10 and fires (see §1.3).

---

## 1. The `TBD — freeze gate` inventory (Q-31 / BLK-02 preparation)

### 1.1 Inventory table

Legend for "Mints a new decision?": **transcription** = the value is already frozen under a
cited D-number or governing-document text and only needs its owner's transcription into the
config (no new scientific choice); **new decision** = choosing it is a new governed act.

| # | File | Key path | Current value | What it controls | Expected/allowed choices (from the design docs) | RECOMMENDED value + source (NOT written anywhere) | Mints a new decision? |
|---|---|---|---|---|---|---|---|
| 1 | `configs/data.yaml` | `stations` | `TBD — freeze gate` | Station registry: coordinates + cells for ARUC/BSHM/NICO | The D-1/D-8 frozen set: ARUC 40/44, BSHM 32/35, NICO 35/33 | Transcribe D-1/D-8's three entries, validated against the official IGS site logs first (team.md § Code Style, Q11 = B) | Transcription, at the ONE pre-G-P1A freeze event (data.yaml's own Q2 = A note); owner: `inventory-and-registry` |
| 2 | `configs/data.yaml` | `cell_rule` | `TBD — freeze gate` | Coordinate→cell selection rule | The notebook cell-4 "DEFAULT convention" — a §18.2 forbidden-choice item (Student + Supervisor) | Freeze the current inline rule as its own D-number FIRST (team.md Q11 = B), then transcribe; IGS-validated | **New decision** (the Q11 = B D-number freeze) unless that D-number already exists — none was found in `evidence/DECISIONS.md` on 2026-09-10 |
| 3 | `configs/experiment.yaml` | `folds` | `TBD — freeze gate` | The four expanding folds F1–F4 | TE §7.1 / Vision §8.2 exact calendar boundaries (F1: Jan–Mar/Apr; F2: Jan–Jun/Jul; F3: Jan–Sep/Oct; F4: Jan–Oct/Nov; December locked) | Transcribe TE §7.1's table verbatim; the month-boundary variant in each pair is TE §7.1's own text — transcribe it as written, never resolved by an implementer | Transcription; owner: `features-and-splits`. NOTE: D-28 records a Vision §8.2 / TE §7.1 embargo-column conflict "recorded, not resolved" — that conflict rides into this transcription and is the owner's to resolve at G-05 |
| 4 | `configs/experiment.yaml` | `embargo_hours` | `TBD — freeze gate` | The per-fold embargo | 24 (TE §7.1; project.md § Mandated: "each with a 24-hour embargo") | **24** — source: TE §7.1 as carried in project.md's affirmed Mandated rule | Transcription; owner: `features-and-splits` (same D-28 conflict note as #3) |
| 5 | `configs/experiment.yaml` | `tuning.declared_baseline_per_track` | `TBD — freeze gate` | Per-track simplicity baseline for the 1% rule | Vision §8.7 / D-124's named baselines | Transcribe D-124 / Vision §8.7 verbatim | Transcription; owner: `models-and-baselines` |
| 6 | `configs/experiment.yaml` | `tuning.selection` | `TBD — freeze gate` | The selection criterion | Vision §8.7 / D-124: mean per-fold skill over F1–F4 + the 1% simplicity rule | Transcribe D-124 / Vision §8.7 verbatim | Transcription; owner: `models-and-baselines` |
| 7 | `configs/experiment.yaml` | `models.selected` | `TBD — freeze gate` | The selected grid point per track (R-101) | A member of the D-121 grids, chosen by the tuning runs' recorded results | **No recommendation possible or permissible**: this is a RESULT of the not-yet-run tuning (mean per-fold skill over F1–F4), frozen before G-05 — not a transcription | **Blocked on execution**, then an owner freeze before G-05 |
| 8 | `configs/experiment.yaml` | `ablations.<5 ids>.run_id` / `registered_at` (10 fields) | `TBD — freeze gate` | Registration of the five predeclared ablations | TE §7.2: named runs registered with run IDs at registration time | None — these are registration ACTS, filled when each ablation is registered (ABL-HIST48 only after the primary configuration freezes) | Owner registration acts, per run |
| 9 | `configs/experiment.yaml` | `…december_day_range` | `TBD — freeze gate` | The locked-test scored window | D-28: **2–31 December 2022 (30 days)** — already owner-approved | Transcribe **D-28** verbatim ("2–31 December 2022, 30 days"); the revised split manifest D-28 owes at G-05 travels with it | Transcription of D-28; owner: `features-and-splits` / gate G-05 |
| 10 | `configs/experiment.yaml` | `practical_relevance_threshold` | `TBD — freeze gate` | The practical-relevance bar (PC-09) | Any value chosen BEFORE the locked test opens; never introduced/changed/reinterpreted after (Vision §5.4) | **No recommendation** — a genuinely new scientific choice (owner + supervisor); no governing document names a candidate value and none is invented here | **New decision**, hard-gated before G-06 |
| 11 | `configs/features.yaml` | `feature_set_id` | `TBD — freeze gate` | The frozen feature-set identity | An identifier minted at the feature-set freeze (features.yaml's own freeze-event note) | Mint at the feature-set freeze event | **New decision** (identity mint); owner: `features-and-splits` |
| 12 | `configs/features.yaml` | `feature_dictionary` | `TBD — freeze gate` | The TE §6.2 dictionary transcription | TE §6.2's table, verbatim | Transcribe TE §6.2 verbatim | Transcription; owner: `features-and-splits` |
| 13 | `configs/features.yaml` | `availability_lags` | `TBD — freeze gate` | Per-driver safe lags | TE §6.2 / D-10.3 / TC-10: Kp/ap3 ≥ 3 h; Hp60/ap60 ≥ 1 h; F10.7 previous-day observed with TRAILING 81-day mean | Transcribe D-10.3 / TE §6.2 verbatim | Transcription; owner: `features-and-splits` |
| 14 | `configs/features.yaml` | `normalization` | `TBD — freeze gate` | Train-only standardization declaration | TE §6.2 Normalization column: train-only for ridge/LSTM inputs, none for RF; the target itself untouched (D-27) | Transcribe TE §6.2's column verbatim | Transcription; owner: `features-and-splits` |
| 15 | `configs/features.yaml` | `permitted_producers` | `TBD — freeze gate` | SD-F-01's per-TE-6.2-row producer allowlist | One producer entry per TE §6.2 row | **No recommendation** — SD-F-01 assigns this to nobody yet; assigning producers is a new governed choice | **New decision**; owner: `features-and-splits` gate |
| 16 | `requirements.txt` | the TensorFlow pin (EXCLUDED by comment) | absent, "`TBD — freeze gate`" per the file's own header | M-06/LSTM runnability; the plumbing fixture's minimal M-06; the whole clean-run completion | A single `tensorflow==X` CPU pin, reproducible on Kaggle AND local (TE §8.1/§9.1) | **`tensorflow==2.21.0`** — source: `src/models/lstm.py` was implemented against "the tf.keras 2.21.0 candidate API" (models-and-baselines code-summary; FU-1 = C). NOT decided anywhere: `evidence/DECISIONS.md` carries no TensorFlow pin and the requirements.txt header says "added here only under an approved D-number" — **flagged as undecided** | **New decision** (a D-number), owner + supervisor per the §18.3 sign-off scope |

### 1.2 The Q-31 freeze acts themselves (BLK-02)

Q-31 (TE §18.2) assigns **fixture station, dates and acceptance tolerances** to the
Student. Already frozen: the plumbing window (**D-11**), the plumbing station (**D-20**,
BSHM 32/35), the scientific month (**D-14**, March 2022, all three cells). Still owed under
Q-31, in dependency order:

1. **The owner's identity declarations** (`kind: identity_declaration`, one per fixture) —
   citation-only transcriptions of D-11/D-20 and D-14 plus the apparatus-partition and
   `fixture_bootstrap` constants (R-122 test apparatus). Blocked only on the owner's act.
2. **Measuring runs** (`run_walking_skeleton.py --emit-candidate --identity <decl>`, at
   least TWO per fixture — composition refuses a zero-width runtime/storage range, board
   Rec 5). Blocked on: rows #3/#4 (partitions/embargo), #12–#15 (features), #16 (the TF
   pin, for the plumbing fixture's minimal M-06), plus pyyaml/numpy/pandas on the machine.
3. **The two freeze acts**: `status: frozen` + sibling `fixture_manifest.sha256` + the
   freeze D-number recording `fixture_manifest_sha256:` — the owner's, never an agent's.
   Acceptance tolerances are MEASURED at step 2 and frozen here, never invented (TE §15.1).

No proposed Q-31 freeze text pre-exists in `governance/` or `evidence/` beyond
`CR-2026-09-07` §10's enumeration of the acts as owed (searched 2026-09-10); the sequence
above IS the prepared request.

### 1.3 Refusal verification (probed live, 2026-09-10)

Every inventory row's sentinel class refuses today, probed directly on the scratchpad
CPython 3.11.16 (stdlib only): `assert_no_tbd` refused each of
`data.stations`, `data.cell_rule`, `experiment.folds`, `experiment.embargo_hours`,
`features.feature_set_id`, `features.permitted_producers`,
`experiment.practical_relevance_threshold` ("TE 18.3 requires zero unresolved required
fields"); `fixture_manifest.read_embargo_hours` refused naming
`configs/experiment.yaml: embargo_hours`. Suite-hosted refusals (models.selected,
availability lags, permitted producers, the TF-pin guard in `src/models/lstm.py`) are green
in the full-suite run recorded in the accompanying report (stdlib pytest stand-in).

---

## 2. D-27 / BLK-08 mechanism limb (preparation, NO reopening)

**D-27 IS explicitly resolved** (`evidence/DECISIONS.md`, 2026-08-24, "reading"): the
primary target is untransformed raw TECU; the inverse obligation is `ABL-DIFF`'s alone; the
general `src/evaluation` → `src/features` inverse route was withheld. The register ends at
**D-32**; nothing reopens D-27. `RULING_2026-09-05` states the reopening protocol verbatim:
a new D-number that states its new argument and honours D-27's reasoning.

**RESOLVED 2026-09-10 — the owner adopted Choice B, recorded as D-37** (this section is kept
as the record of what was requested). BLK-08's mechanism limb is **CLOSED by D-37**, which
reaffirms D-27; the checked refusal remains the mechanism. Original text: *"What stays open
(BLK-08's mechanism limb): R-139 control 25 refuses a `toleranced` ledger entry declaring TECU
units whose `producing_path` carries no `inverse_route`, until `evaluation-and-comparison`'s
R-103 joint contract is adopted by both halves."*

**Choice A — reopen D-27 (new D-number): build the general inverse route.**
`src/features` transforms would gain `inverse`/`apply`; TECU tolerances become freezable
for any output. Cost: contradicts the implemented state (Q4 = A removed `inverse`/`apply`
from `Transform` by design; `touches_target=False` everywhere), reopens a settled reading
without a new argument from the data, and adds a leakage-adjacent surface NFR-LEAK-01
exists to shrink.

**Choice B — affirm the withholding; adopt R-103's joint contract in D-27's identity
form.** The primary path's outputs are ALREADY raw TECU (D-27 evidence row 1: "Primary
remains Raw TECU"), so their honest `inverse_route` is the IDENTITY route, citable as
`identity (D-27: primary target untransformed)`; `ABL-DIFF` remains the only real inverse,
scoped to `src/evaluation`'s ablation scoring with error propagation recorded (TE §7.2).
R-139 control 25 keeps refusing a TECU tolerance with NO declared route; it accepts the
declared identity route once the joint contract adopts this reading at both units' gates.

**RECOMMENDATION: Choice B.** It matches the implemented state exactly (no inverse code
exists anywhere; `Transform` deliberately carries none), honours D-27's reasoning instead
of overturning it, unblocks every primary-path TECU tolerance without new leakage surface,
and leaves `ABL-DIFF`'s real inverse where TE §7.2 puts it. What the owner would sign: the
R-103 joint-contract adoption (both halves) stating the identity-route reading — a
contract adoption at the two units' gates, with or without a new D-number as the owner
prefers. **Nothing here performs it.**

---

## 3. Q5 / `tests/test_external_drivers.py` (11 standing failures) — decision request

**No explicit ruling exists** (`evidence/DECISIONS.md`, `governance/`, and the questions
files searched 2026-09-10); `CR-2026-09-07` §6.2 routed it to `external-products`' owner
and it has not returned. The exact question: *how should `test_external_drivers.py`'s nine
non-fixture subprocess invocations of `scripts/04_build_external_products.py` coexist with
the Q5 = A receipts gate?* Options, updated for board Rec 2 (which changed the space):

- **(a) Pass `--fixture-manifest` in the smoke invocations** — CR §6.2's first option, now
  **FORECLOSED** for the audit tests: Rec 2 binds 04's fixture exemption to the scope's
  window, and 04's declared window is the full calendar year, so a fixture-flagged full
  audit refuses by design.
- **(a2) Plant synthetic frozen manifests + receipts in the smoke workspace** so the gate's
  REAL happy path admits the run. Highest fidelity (exercises the gate as designed); the
  costliest (each smoke test builds the full receipt apparatus; needs pyyaml).
- **(b) Assert the new first refusal** for the full-scale invocations (the receipts gate's
  message) and keep the driver/audit refusal texts covered at function level, where most
  already are. Cheapest; loses subprocess-level coverage of the specific refusal texts.
- **(c) Narrow Q5** (a new visible exemption class for declared smoke workspaces) — a
  governance change to a receipted answer; weakens the gate's universality.

**RECOMMENDATION: (b)**, with (a2) as the follow-up once fixtures actually run: it
preserves the gate's strength, keeps every refusal covered somewhere, costs one test-module
edit, and requires no governance change. **Not implemented — the 11 failures stand until
the owner rules.** On this clone they fail earlier (pyyaml preflight) either way.
