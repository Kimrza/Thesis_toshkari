# Proposal — `features.yaml`: `feature_set_id`, `feature_dictionary`, `normalization`

**Date:** 2026-09-21 · **Status:** PROPOSED, not written to config · **Decision owner:**
Student (the dictionary is the feature contract), with the two conditional-normalization
choices in §4 arguably Student + Supervisor

Asked for by the project decision owner on 2026-09-21 ("propose feature names"). Nothing here
is adopted; `configs/features.yaml` still carries its three sentinels and every reader still
refuses by name.

---

## 1. How much of this is a choice at all

Less than it looks. The input space is **already closed** in two places that agree:

* TE §6.2's dictionary table — thirteen live rows plus one removed (`ssn_*`) and one
  diagnostic (`dst_*`);
* `src/features/build.py: SECTION_6_2_ROWS` — the same eighteen row identities as a frozen
  constant, with `REMOVED_ROWS = {"ssn"}` refusing the removed one by name.

So the *rows* are transcription. What is genuinely open is narrow: **how the multi-field rows
expand into named fields**, and **the four rows whose Normalization column reads the
conditional "Train-only if scaled"** rather than a definite value.

## 2. Proposed `feature_set_id`

```yaml
feature_set_id: "FS-P1-2022-v1"
```

Reading: Phase 1, calendar 2022, first frozen version. No reader constrains the format; it
travels as an identity stamp on every dataset, mask and comparison, so it needs to be stable,
unique and legible — not meaningful. A change to the dictionary means a **new id**
(`…-v2`), never an edit of this one.

## 3. Proposed `feature_dictionary` — 19 fields over 13 rows

Each entry needs `dictionary_row` and `normalization`; driver rows additionally need
`source_series`, and the expanding rows need the extra key the validator names.

| # | Field | `dictionary_row` | Extra keys | `normalization` | Basis |
|---|---|---|---|---|---|
| 1 | `vtec_lag_1h` | `vtec_lag` | `lag_hours: 1` | `train_only_standardize` | §4a |
| 2 | `vtec_lag_2h` | `vtec_lag` | `lag_hours: 2` | `train_only_standardize` | §4a |
| 3 | `vtec_lag_3h` | `vtec_lag` | `lag_hours: 3` | `train_only_standardize` | §4a |
| 4 | `vtec_lag_24h` | `vtec_lag` | `lag_hours: 24` | `train_only_standardize` | §4a |
| 5 | `vtec_seq_24` | `vtec_seq_24` | `sequence_steps: 24` | `train_only_standardize` | TE §6.2 states it outright |
| 6 | `utc_hour_sin` | `utc_hour_sin` | — | `none` | TE §6.2: "None" |
| 7 | `utc_hour_cos` | `utc_hour_cos` | — | `none` | ” |
| 8 | `doy_sin` | `doy_sin` | — | `none` | ” |
| 9 | `doy_cos` | `doy_cos` | — | `none` | ” |
| 10 | `lst_sin` | `lst_sin` | — | `none` | ” |
| 11 | `lst_cos` | `lst_cos` | — | `none` | ” |
| 12 | `station_onehot_ARUC` | `station_onehot` | `station_id: ARUC` | `none` | TE §6.2: "None" |
| 13 | `station_onehot_BSHM` | `station_onehot` | `station_id: BSHM` | `none` | ” |
| 14 | `station_onehot_NICO` | `station_onehot` | `station_id: NICO` | `none` | ” |
| 15 | `station_lat` | `station_lat` | — | `train_only_standardize` | §4b |
| 16 | `kp_safe` | `kp_safe` | `source_series: kp` | `train_only_standardize` | §4b |
| 17 | `ap_safe` | `ap_safe` | `source_series: ap` | `train_only_standardize` | §4b |
| 18 | `hp60_safe` | `hp60_safe` | `source_series: hp60` | `train_only_standardize` | §4b |
| 19 | `ap60_safe` | `ap60_safe` | `source_series: ap60` | `train_only_standardize` | §4b |
| 20 | `f107_safe` | `f107_safe` | `source_series: f107_daily_median` | `train_only_standardize` | §4b |
| 21 | `f107_81_trailing` | `f107_81_trailing` | `source_series: f107_daily_median` | `train_only_standardize` | §4b |

**Twenty-one fields, not nineteen** — corrected while writing this table: the four `vtec_lag`
fields and three `station_onehot` fields expand two rows into seven, so 13 declared rows yield
21 named fields. Derived by counting the table, not carried from the paragraph above it.

**Deliberately absent, each for a stated reason:**

* `dst` — TE §6.2: *"Diagnostic / hindcast-only. Not a confirmatory feature."* Declaring it
  here would place it in the model input space. It reaches diagnostics by its own path.
* `ssn_*` — TE §6.2: *"Removed. Not used anywhere."* `REMOVED_ROWS` refuses it by name.
* `target_support` (`valid_observation_count`, spread/gap/QC fields) — TE §6.2 makes these
  **diagnostic by default**, and model use *"requires explicit G-04 approval"*. G-04 is not
  passed, so no support field is proposed as a feature. Target-hour quality fields are
  permanently forbidden regardless.
* Raw longitude, in any form — it enters only through `lst_sin`/`lst_cos`.
* Anything `iri`-bearing — the denial mechanism refuses it, and WS-10 proves the refusal.

## 4. The two genuinely open choices inside the table

### §4a — the `vtec_lag` set is `[1, 2, 3, 24]`

TE §6.2 states *"exact lags `[1,2,3,24]`"*, so the lag set is transcription. What the table
above settles is only that all four are **declared**, which is the plain reading.

### §4b — "Train-only if scaled" → `train_only_standardize`

Seven rows (`station_lat`, the five drivers, `f107_81_trailing`) carry the conditional
**"Train-only if scaled"**. The validator admits exactly two tokens, so the conditional has to
resolve to one of them. **`train_only_standardize` is proposed for all seven**, for three
reasons:

1. Ridge and the LSTM are scale-sensitive; the drivers span wildly different magnitudes
   (Kp 0–9 against F10.7 in the tens to hundreds), so leaving them unscaled would let the
   larger-magnitude driver dominate the penalty and the gradient.
2. Random Forest is scale-invariant, so standardizing costs it nothing.
3. `train_only_standardize` is the **safe** direction: it is fitted per fold on training rows
   only (NFR-LEAK-01), and the transform-identity guard already refuses a transform fitted
   over a wider range. Choosing `none` would be the irreversible-looking choice, because it
   silently privileges large-magnitude drivers.

**If you prefer `none` for any of the seven, say which** — it is a one-token change per field,
and nothing else in the proposal depends on it.

## 5. `normalization` (the top-level `features.yaml` field)

```yaml
normalization: "train_only_standardize"
```

The per-field column above is what the builder reads; this top-level field is the **default
and the declared posture**. Setting it to `train_only_standardize` makes the leakage-safe
option the default, so a future field added without an explicit column inherits the safe
behaviour rather than the silent one.

## 6. What adopting this would unblock, and what it would not

It would let `load_feature_dictionary` and `build_features` run, which is the next wall after
the release issue. It would **not** discharge G-04, would not make any support field a
feature, and would not change the target contract.

## 7. One outstanding input this proposal cannot supply

`configs/data.yaml: stations.*.observable_codes` is recorded as **not transcribed** — no
governing record or site log states them, and they are read from a 2022 RINEX header, which is
Phase 2 material. `assert_registry_resolved` still refuses on that one field. Adopting this
dictionary does not clear it.
