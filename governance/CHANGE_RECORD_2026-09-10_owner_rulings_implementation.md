# Change Record — 2026-09-10 — Implementation of the owner's rulings on the 2026-09-10 decision requests

**Change ID:** `CR-2026-09-10-OWNER-RULINGS`
**Authority:** the project decision owner's ruling of **2026-09-10** on
`governance/FREEZE_DECISION_REQUEST_2026-09-10.md` (Q5, cell_rule,
practical_relevance_threshold, permitted_producers, the TensorFlow pin, D-27/BLK-08).
**Repository state:** written from `HEAD = 8097e77`. **No commit is made by this pass.**
**Register discipline:** no agent writes `evidence/DECISIONS.md`. Every decision this
ruling needs is DRAFTED below as proposed D-number text for the owner to adopt; a
decision is not real until it has a D-number in the register.

This record is written FIRST, before any code, config or test edit of this pass.

---

## 0. What the owner ruled, and what this pass did with each ruling

| # | Ruling | Implemented here | Owner act still owed |
|---|---|---|---|
| 1 | **Q5 = Choice B** | `tests/test_external_drivers.py`'s subprocess tests now assert the TE §9.2 receipt-gate contract: a full-scale (non-fixture) `04` invocation is **not accepted merely because it produced outputs**, and the gate **fails closed** while no frozen-manifest/receipt chain exists. Refusal-text coverage stays at function level. | none (a test-design ruling) |
| 2 | **cell_rule = freeze the EXISTING convention** | `configs/data.yaml: cell_rule` filled with the existing implemented identifier `floor-half-open-d1`, citing draft **D-A** below. No grid invented, no station moved. | adopt **D-A**; §18.2 **Student + Supervisor countersignature owed** |
| 3 | **practical_relevance_threshold = no invented numeric** | **TBD sentinel PRESERVED.** The frozen object is the RULE (Vision §5.4 + PC-09), now transcribed into `configs/experiment.yaml`'s comment block at the field and drafted as **D-B**. | adopt **D-B** (and, only if the supervisor ever approves a threshold, a separate later decision) |
| 4 | **permitted_producers = freeze the strict leakage-safe policy** | The policy is transcribed at the field, and the **11 dictionary rows whose producing artifact the implemented contract itself fixes** are filled with their code-constant / release identities. The **7 driver-class rows are left unfilled with their reason named** (see §4.3) — filling them would invent a provider artifact-id string. Leakage-safe enforcement tests added. | adopt **D-C**; supply the 7 driver producer ids when the driver release exists |
| 5 | **TensorFlow == 2.21.0** | `requirements.txt` carries the frozen pin; `src/models/lstm.py`'s stale "pin is TBD" prose corrected; the pin-guard negative controls re-pointed at synthetic absent/commented-pin files so the refusal proof is preserved. | adopt **D-D** |
| 6 | **D-27 = Choice B (affirm withholding)** | No duplicate decision. Reaffirmation drafted as **D-E**; BLK-08's mechanism limb recorded everywhere as **"resolution drafted, owner adoption owed"** — never "closed". R-139 control 25 untouched. | adopt **D-E** |
| 7 | **models.selected / embargo_hours / folds / every other unruled TBD** | **Untouched.** Refusals re-probed after the config edits (§7). | the freezes themselves |

---

## 1. Q5 = Choice B — the receipt gate asserted at subprocess level

**What Q5 = A made true (unchanged):** every full-year stage-script invocation calls
`require_receipts_for_snapshot` inside `_stage_entry`, and the exemption is granted only
for a run carrying a validating fixture scope whose declared window lies inside the
scope's cited window (board Rec 2). No frozen manifest and no receipt exist, so **every
full-scale invocation of `scripts/04_build_external_products.py` refuses, by design**.

**What CR-2026-09-07 §6.2 routed, and what the owner has now ruled.** §6.2 offered three
ways out (pass `--fixture-manifest` in the smoke invocations; assert the new refusal;
narrow Q5). Board Rec 2 foreclosed the first for this script — `04`'s declared window is
the full calendar year, so a fixture-flagged full audit refuses against every fixture
scope. The owner ruled **Choice B**: assert the gate at subprocess level, keep the
refusal-text coverage at function level.

**As implemented** (`tests/test_external_drivers.py`): one shared helper,
`_assert_gate_fails_closed(result, *, also_accepts=())`, states the contract in one place
— a full-scale run **must** exit non-zero, and its stderr must name one of the governed
refusals in force (the TE §9.2 receipt gate; or, on a clone without `pyyaml`, the
governed-config preflight that refuses even earlier). Each formerly exit-0 expectation
becomes an explicit "not accepted merely because outputs exist" assertion; each formerly
exit-1 expectation keeps its own refusal text as an accepted marker. **No fake manifests
or receipts are constructed anywhere** — a synthetic receipt chain would be exactly the
fabricated evidence the rules forbid.

**Honest limit recorded:** on this clone the first governed refusal is the `pyyaml`
preflight, so these tests prove *fail-closed* here and prove *which* gate fires only in a
`pyyaml`-bearing environment. That is stated in the helper's docstring rather than hidden.

---

## 2. DRAFT D-A — `cell_rule`: the existing coordinate-to-cell convention, frozen verbatim

> **Proposed text for `evidence/DECISIONS.md` — NOT adopted; the owner adopts or edits.**
>
> ## D-A — The coordinate-to-cell rule is frozen as the existing convention (freeze)
>
> **Decision date:** *(owner to fill)*. **Decided by:** the project decision owner.
> **§18.2 assigns the coordinate-to-cell rule to Student + Supervisor — a supervisor
> countersignature is OWED before this decision is complete.**
> **Authority:** the owner's ruling of 2026-09-10 ("freeze the EXISTING convention; do not
> invent a new grid, do not move stations"); Vision §6.1A/§6.1B (the rule "must be frozen
> and recorded, not guessed"); `team.md` § Code Style Q11 = B (freeze the current inline
> constants as a D-number BEFORE the migration moves them, so the migration cannot
> silently change a scientific value).
>
> **Decision.** The coordinate-to-cell rule is the convention already implemented and in
> use, transcribed here verbatim and unchanged:
>
> > 1° × 1° cell identified by its **lower-left (floor) corner**, half-open in both axes:
> > `cell = [floor(lat), floor(lat)+1) × [floor(lon), floor(lon)+1)`
>
> Its governed identifier is **`floor-half-open-d1`** — the identifier already declared in
> `src/data/registry.py` (`CELL_RULE_ID`), which `assert_registry_resolved` requires
> `configs/data.yaml: cell_rule` to equal and refuses any other value for. The source of
> the convention is `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 4 ("DEFAULT
> convention adopted here"), whose text is reproduced above without alteration.
>
> **What this decision does NOT do.** It does not move a station, change a cell, choose a
> grid resolution, or discharge the notebook's own standing caveat that the convention be
> **CONFIRMED against the real bin edges Madrigal returns** before it is relied on
> scientifically; that confirmation remains owed and is recorded as a limitation of this
> freeze, not as satisfied by it. It does not resolve `stations` (still
> `TBD — freeze gate`, its coordinates still PROVISIONAL pending IGS site-log validation).
>
> **Consequence.** `configs/data.yaml: cell_rule` carries `floor-half-open-d1`. The
> registry still refuses overall while `stations` and `igrf_version` are unresolved — this
> decision closes one limb of that refusal, not the refusal.

**Implemented now:** `configs/data.yaml: cell_rule: "floor-half-open-d1"` with a comment
citing this draft and the countersignature obligation.

---

## 3. DRAFT D-B — `practical_relevance_threshold`: the rule is the frozen object, not a number

> **Proposed text for `evidence/DECISIONS.md` — NOT adopted.**
>
> ## D-B — Practical relevance is reported descriptively; no threshold is set (reading)
>
> **Decision date:** *(owner to fill)*. **Decided by:** the project decision owner.
> **Authority:** the owner's ruling of 2026-09-10 ("no invented numeric"); **Vision §5.4**;
> **PC-09** (`constraint-register.md`, `binding: hard`).
>
> **Decision.** No practical-relevance threshold is set. What is frozen is the PROTOCOL,
> transcribed from Vision §5.4 and PC-09 without addition:
>
> 1. Ten percent RMSE reduction is a **named reference magnitude, not a pass/fail rule**
>    and not a hypothesis.
> 2. **Practical relevance is reported descriptively unless the supervisor explicitly
>    approves a threshold** (PC-09, `binding: hard`).
> 3. An approved reference or threshold **shall not correspond to an RMSE difference
>    smaller than the target uncertainty budget** of Vision §6.9; if it does, practical
>    relevance is reported descriptively only.
> 4. **No threshold may be introduced, changed, or reinterpreted after December is
>    opened** (Vision §5.4; PC-09; `project.md` § Forbidden).
> 5. Significance and usefulness stay distinct: the confirmatory claim is the paired loss
>    differential with its 95 % interval (Vision §2.3/§5.5); a practical-relevance
>    statement is descriptive commentary beside it, never a second test.
>
> **Consequence.** `configs/experiment.yaml: practical_relevance_threshold` **keeps the
> `TBD — freeze gate` sentinel**, and that sentinel is now the correct, decided state: it
> records "no threshold approved", not "not yet considered". Any future numeric requires an
> explicit supervisor approval and its own D-number, and is barred after December opens.

**Implemented now:** sentinel preserved; the five-point protocol transcribed into the
comment block immediately above the field in `configs/experiment.yaml`, citing this draft.
**Nothing numeric was written anywhere.**

---

## 4. DRAFT D-C — `permitted_producers`: the leakage-safe policy, and the rows the contract fixes

### 4.1 The policy (owner's words of 2026-09-10, transcribed)

A feature may be produced for a dictionary row only if it is **available at the forecast
origin**; carries **no future target TEC**; requires **no locked-December access**;
**respects its declared safe lag**; introduces **no future information through
preprocessing** (train-only fitting where any fitting occurs); is **deterministic where
determinism is required**; and is **compatible with the 1-hour-ahead forecast**. Feature
philosophy: local historical VTEC, temporal features, and legitimately-available
solar/geomagnetic drivers — **no IRI-derived anything**, and **no future leakage**.

Every clause above is already binding project text (Vision §6's feature contract; TE §6.2's
dictionary with its lag and normalization columns; **D-10.3** availability lags; TC-09's
carry-forward bound; NFR-IRI-01/TE §12's IRI denial; NFR-LEAK-01's train-only rule;
TE §6.2's `ssn` REMOVED row; FR-P1-04-10's longitude-only-via-`lst_*` rule). This decision
transcribes; it does not create.

### 4.2 The rows filled (11), each with the authority that fixes its producer

| Dictionary row | Permitted producer | Why this producer, and where it is already fixed |
|---|---|---|
| `vtec_lag` | `phase1_hourly_target` | The released D-17 Phase 1 hourly target, read by manifest by `05`/`06`/`07`; lagged VTEC is target-derived INPUT (TE §6.2 `vtec_lag_*`) |
| `vtec_seq_24` | `phase1_hourly_target` | Same release; the 24-step sequence view of the same target history |
| `target_support` | `phase1_hourly_target` | The support field travels on the target release (R-78 governs whether it is ADMITTED, unchanged here) |
| `utc_hour_sin` | `record_timestamp` | `TIMESTAMP_PRODUCER` in `src/features/build.py` — a pure function of the record's own `interval_start_utc` |
| `utc_hour_cos` | `record_timestamp` | same |
| `doy_sin` | `record_timestamp` | same |
| `doy_cos` | `record_timestamp` | same |
| `lst_sin` | `station_registry` | `STATION_REGISTRY_PRODUCER`; local solar time `(UTC + lon/15) mod 24` — the ONLY route longitude may take (FR-P1-04-10) |
| `lst_cos` | `station_registry` | same |
| `station_onehot` | `station_registry` | `STATION_REGISTRY_PRODUCER`; gated by `assert_registry_resolved` |
| `station_lat` | `station_registry` | same |

All eleven satisfy every policy clause by construction: each is available at the forecast
origin (a timestamp function, a station constant, or target history strictly BEFORE the
origin through the ONE window definition), none carries future target TEC, none touches
December, none is IRI-derived, and any scaling is train-only per fold.

### 4.3 The rows NOT filled (7), and exactly why — reported, not silently dropped

`kp_safe`, `ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe`, `f107_81_trailing`, `dst`.

**None of them is rejected on policy grounds.** All seven are legitimate under the policy
(the first six are exactly the forecast-safe driver set; `dst` is admitted to the
dictionary as **diagnostic/hindcast-only** and is already barred from modelling input by
`DIAGNOSTIC_ONLY_SERIES`). They are unfilled for one reason: **a permitted-producer entry
is a producing-ARTIFACT identity, and the driver artifacts do not exist yet.** The
identity a driver frame will stamp as `producing_artifact` is its provider product
identity, recorded in the driver manifest by the acquisition/driver release. D-10.1 fixes
the **providers** (Kp/ap3 → GFZ Potsdam; Dst → Kyoto WDC; F10.7 → Canada's Solar Radio
Monitoring Program, OBSERVED flux) and TE §6.2 fixes Hp60/ap60 as **"GFZ or approved
source"** — a provider, not an artifact id, and in the Hp60 case not even a single
provider. Writing a literal string today would invent an artifact identity, and a wrong
guess would later refuse a legitimately produced feature. **Deferred, with the entry owed
when the driver release exists.**

**Fail-closed behaviour is unchanged:** `load_permitted_producers` still refuses any run
requesting a driver row, naming exactly those rows, and no feature matrix is produced.

> **Proposed text for `evidence/DECISIONS.md` — NOT adopted.**
>
> ## D-C — The permitted-producer policy and the eleven contract-fixed rows (freeze)
>
> **Decision date:** *(owner to fill)*. **Decided by:** the project decision owner.
> **Authority:** the owner's ruling of 2026-09-10; Vision §6; TE §6.2; **D-10.3**; TC-09;
> NFR-IRI-01; NFR-LEAK-01; FR-P1-04-10; SD-F-01 (Q1 = A).
>
> **Decision.** (a) The leakage-safe policy of §4.1 above governs every permitted-producer
> entry. (b) The eleven rows of §4.2 take the producers listed there, each being the
> identity the implemented feature contract already fixes. (c) The seven driver-class rows
> of §4.3 remain unassigned until the driver release exists; assigning them is a later
> transcription of the driver manifest's recorded provider product identity, not a new
> scientific choice. (d) Nothing here admits a support field: R-78's approval-ID and
> timestamp conditions are unchanged.

**Implemented now:** the eleven entries and the policy text in `configs/features.yaml`,
plus leakage-safe enforcement tests (§9).

---

## 5. DRAFT D-D — The TensorFlow pin

> **Proposed text for `evidence/DECISIONS.md` — NOT adopted.**
>
> ## D-D — The TensorFlow pin is `tensorflow==2.21.0` (freeze)
>
> **Decision date:** *(owner to fill)*. **Decided by:** the project decision owner, by the
> ruling of 2026-09-10 (the owner selected 2.21.0).
> **Authority:** TE §8.1 (the pinned environment); TE §8.3 (TensorFlow/Keras is the ONE
> neural stack; PyTorch prohibited); TC-01 (CPU is a complete execution path — the pin is
> the CPU wheel, never a GPU build); TS-M-01 (M-06's pin guard).
>
> **Decision.** `requirements.txt` carries `tensorflow==2.21.0`. `src/models/lstm.py` was
> implemented against the tf.keras **2.21.0 candidate API**, so the frozen pin and the
> implemented serialization/determinism contract agree by construction.
>
> **What is NOT established by this decision, and is owed before any governed M-06 run.**
> The installability and API-compatibility check **has not been executed**: PyPI is
> unreachable from the implementation environment (verified again 2026-09-10), so
> `pip install tensorflow==2.21.0` has never run here, no TensorFlow import has ever
> succeeded, and **TE §8.1's own condition — that the pin be verified on BOTH governed
> platforms (Kaggle and local) — is unmet**. The **Kaggle compatibility check is owed**.
> Freezing the pin makes the guard pass; it does not make the environment exist.

**Implemented now:** the pin line in `requirements.txt` citing this draft; the stale
"pin is TBD" prose in `src/models/lstm.py` corrected; the pin-guard negative controls
re-pointed at synthetic files so "the guard refuses an absent or commented pin" stays
proved. **BLOCKED — NOT EXECUTED:** install, import, API-compat and Kaggle checks.

---

## 6. DRAFT D-E — D-27 reaffirmed; BLK-08's mechanism limb resolved on paper

> **Proposed text for `evidence/DECISIONS.md` — NOT adopted. This is a REAFFIRMATION;
> D-27 stands and is not superseded, replaced or duplicated.**
>
> ## D-E — D-27 is affirmed; BLK-08's mechanism limb resolves in D-27's identity form
>
> **Decision date:** *(owner to fill)*. **Decided by:** the project decision owner, by the
> ruling of 2026-09-10 (Choice B: affirm the withholding).
> **Authority:** **D-27** (2026-08-24); TE §7.2 (`ABL-DIFF`'s inverse obligation); TE §12's
> import boundary; `RULING_2026-09-05` (the reopening protocol, not invoked).
>
> **Decision.** D-27's withholding of a general inverse route is **affirmed permanently**
> as the project's mechanism. BLK-08's mechanism limb resolves as follows:
>
> 1. **The refusal IS the mechanism.** R-139 control 25 — a `toleranced` ledger entry
>    declaring TECU units for an output whose producing path declares no `inverse_route`
>    is not freezable — stays exactly as implemented, at full strength.
> 2. **R-103's joint contract is adopted in D-27's identity form.** The primary path's
>    output is already raw TECU (D-27: "Primary remains Raw TECU"), so its citable
>    `inverse_route` is the **identity route**, cited as
>    `identity (D-27: primary target untransformed)`.
> 3. **`ABL-DIFF` keeps the only real inverse**, scoped to its own ablation scoring, with
>    error propagation recorded (TE §7.2). No `src/evaluation` → `src/features` route is
>    created and no import-boundary change is authorised.
>
> **Status of BLK-08 after adoption:** the mechanism limb closes. **Until adoption it is
> recorded everywhere as "resolution drafted, owner adoption owed" — never "closed".**

**Implemented now:** the representation update only (§8). No code change: R-139 control 25
and its test are untouched.

---

## 7. Untouched TBDs, re-probed after the config edits

`models.selected`, `folds`, `embargo_hours`, `stations`, `igrf_version`, `feature_set_id`,
`feature_dictionary`, `availability_lags`, `normalization`, the ten ablation
`run_id`/`registered_at` fields, `december_day_range`, `tuning.declared_baseline_per_track`,
`tuning.selection` — **all left exactly as found**. Their refusals were re-probed after
this pass's config edits and all still fire (results in the accompanying report).

## 8. BLK-08 representation updates

Every representation that tracks BLK-08's mechanism limb now reads **"resolution drafted
(D-E draft, CR-2026-09-10), owner adoption owed"**. Nothing reads "closed", and the
blocker is not removed from any ledger.

## 9. Tests added or changed by this pass

- `tests/test_external_drivers.py` — the Q5 = B subprocess gate contract (§1).
- `tests/test_feature_availability.py` — leakage-safe enforcement over the now-filled
  `permitted_producers`: the eleven filled rows are exactly the contract-fixed set with
  the contract-fixed producers; the seven driver rows still refuse by name; a producer not
  on a row's permitted list is refused per (row, producer) pair; `ssn` (REMOVED) and any
  `iri_*`/raw-longitude row cannot be introduced through the block.
- `tests/test_models_smoke.py` — the pin-guard controls re-pointed (§5): the refusal is
  still proved (absent pin, commented pin — synthetic files), and the real
  `requirements.txt` is now asserted to carry the frozen `tensorflow==2.21.0`.

**No test was weakened, skipped or deleted to produce green.** Where a test's expectation
changed, it changed because the owner's ruling changed the governed truth it asserts, and
the negative control it carried was re-pointed rather than removed.
