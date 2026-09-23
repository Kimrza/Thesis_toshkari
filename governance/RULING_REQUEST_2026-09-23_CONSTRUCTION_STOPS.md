# Ruling request — 2026-09-23 — two items raised while resuming Construction

**Raised by:** the agent, under the owner's instruction of 2026-09-23: *"Proceed with the
remaining Construction scope… Keep changes within the existing governed scope and stop for
any new decision or cross-unit producer/contract change."*
**Repository state:** `HEAD = d64a0f1`, working tree clean at the time of writing.
**Nothing below is decided here.** No config, no frozen value and no module was changed on
either item; `evidence/DECISIONS.md` was not written.

---

## §1 — STOP: `f107_safe` and `f107_81_trailing` share one `source_series`, so they would receive identical values

### What was found

`build_features` resolves each driver field's values from
`drivers[entry["source_series"]]` — the dictionary's `source_series`, not the field name
(`src/features/build.py:975-1002`, then `driver_values[name]` at `:1000` and the per-field
assignment at `:1038`). Printed from `configs/features.yaml` before asserting it:

```
driver fields:                    kp_safe, ap_safe, hp60_safe, ap60_safe, f107_safe, f107_81_trailing
fields sharing f107_daily_median: f107_safe, f107_81_trailing
source_series usage:              f107_daily_median x2, kp, ap, hp60, ap60
```

Both F10.7 fields declare `source_series: "f107_daily_median"`. One key can hold one frame,
so whatever the loader supplies under that key becomes the value of **both** fields at every
epoch: **`f107_81_trailing` would equal `f107_safe`**, and the 81-day trailing mean — the
quantity Vision §6 and TE §6.2 require, and the one whose *centered* form
`project.md` § Forbidden calls "a defect, not a fallback" — would never be computed.

### Why no loader can fix it

The release loader I was implementing supplies `drivers`. It can supply any frames it likes,
but it cannot make one mapping key return two different frames to two different fields. The
selection happens inside `build_features`, keyed by `source_series`. So this is a **contract**
gap between the frozen feature dictionary and the feature builder, not a wiring gap — which
is why I stopped rather than working around it.

### Why it is not caught today

`f107_81_trailing`'s *availability* limb is fully enforced: `build_availability_matrix`
requires `window.source` to be supplied, and `assert_anchor_recomputed` recomputes the
81-day mean from the daily values and refuses a wrong anchor (D-47's tolerance
`8e-12`, input bound 400 sfu). That limb checks the **availability rows** the producer
supplies. Nothing cross-checks that the **feature column** built from those rows carries the
mean rather than the daily value, because the column's provenance stamp
(`dictionary_row`/`dictionary_field`/`producing_artifact`) is identical either way — both
rows legitimately come from `nrcan_f107_observed_daily_median_2022` (D-63).

### The three ways out

1. **Give `f107_81_trailing` its own `source_series`** — e.g. `f107_81_trailing_mean` — and
   have the loader supply that key with the trailing series it already has to compute for
   the anchor limb. *Consequence:* one line of `configs/features.yaml` changes, and it is a
   field **D-60 froze** (the dictionary: 21 fields over 13 rows, source_series included), so
   it needs your decision; it is a naming change, not a change to any scientific value —
   the row id, the lag rule, the window, the normalization and the producing artifact all
   stay exactly as frozen. *Recommended.*
2. **Teach `build_features` to resolve a windowed field through its `window` block** rather
   than through `source_series`. *Consequence:* no config change, but the builder grows a
   special case for one field, and the rule "a driver field names its `source_series`"
   (`build.py:402`) stops being true of every driver field. A behavioural change to a
   reviewed module in another unit, for a contract that reads correctly today.
3. **Declare the two fields intentionally identical.** Not defensible — it contradicts
   TE §6.2's dictionary row and Vision §6, and would make ABL-HIST48's premise meaningless.
   Recorded only so the option set is complete.

**Recommendation: option 1**, adopted under D-60's existing scope as a transcription
correction (the dictionary keeps its 13 rows and 21 fields; one field's `source_series`
string changes so the two rows can carry different series, which is what the dictionary
already says they are). If you would rather it carry its own D-number, that is equally fine
and changes nothing about the code.

**Until this is ruled, stage 05 cannot be completed correctly**, so the release loader,
`features-and-splits`, `models-and-baselines` and `evaluation-and-comparison` all stay where
they were at `d64a0f1`. Nothing was half-built: no partial loader was committed.

### What the loader will do once it is ruled (for your information, not for approval)

Supply `drivers` with both key kinds, because the two consumers key it differently:
`build_availability_matrix` by **feature** (`kp_safe` … `f107_81_trailing`, rows carrying
`forecast_origin`, `observation_timestamp`, `publication_timestamp`, `release_status`, plus
`anchor_day`/`mean_value` for the trailing field), and `build_features` by **`source_series`**
(`kp`, `ap`, `hp60`, `ap60`, `f107_daily_median`, plus whatever §1 resolves for the trailing
mean). Every frame comes from the four releases stage 04 now publishes, through
`spaceweather.select_lagged_series` (which applies each safe lag **once**, D-43/D-44) and
`spaceweather.trailing_mean` (never centered). `dst` needs no driver frame at all: it is in
no dictionary row, being diagnostic-only (TC-11) — verified, not assumed.

**Decision required — Approve / Reject / Modify / Postpone.**

---

## §2 — Proposal: how a fixture release should be named so it cannot be mistaken for a product

### The question, as you put it

A fixture release currently sits under the same citation a governed product would, yet the
directory name has to be fixed so consumers can find it.

### What is actually true today, measured

Three release kinds now exist under `artifacts/releases/`:

| Kind | Directory | Fixed name? | Who resolves it |
|---|---|---|---|
| acquisition (stage 00) | `plumbing_7day_<UTC stamp>/` | no — fixture id **and** run stamp | scanned by `rglob`, consumed by content |
| target (stage 02) | `phase1_hourly_target/` | **yes** | `05`, `06`, `07`, each by literal path |
| drivers (stage 04) | `<D-63 identity>/` | **yes** | the permitted-producer list, by identity |

So the fixed name is not a convenience: for the target it is three consumers' hardcoded
path, and for the drivers it **is** the D-63 identity that `build_features` matches
`producing_artifact` against. Renaming either per run breaks the thing that makes the
provenance check work.

Since 2026-09-23 every release manifest carries `evidence_class`
(`fixture_plumbing` | `governed_run`), `fixture_scope_id` and its `window`, so the
distinction exists **in the artifact**. What it does not yet have is a mechanism that
*stops* the confusion rather than merely documenting it.

### The proposal: separate the ROOT, not the name

Keep every release's directory name exactly as it is — the consumers and the identity check
are untouched — and make a fixture run write its releases under a **different release
root**:

```
artifacts/releases/                      <- governed runs only
artifacts/walking_skeleton/<fixture_id>/releases/   <- fixture runs
        phase1_hourly_target/
        gfz_kp_ap_nowcast_2022/
        ...
```

resolved once, at stage entry, from `snapshot.resolved_roots["release_root"]` plus the
fixture scope — exactly the way `CR-2026-09-13-04-FIXTURE-WINDOW` already quarantines the
stage-04 **audit** artifact to the walking-skeleton root and for the same stated reason
(TC-03f: fixture output is plumbing evidence, never governed evidence).

**Why this is the right shape here**

* **The name stays fixed, so nothing that resolves it changes.** `05/06/07` still read
  `<release_root>/phase1_hourly_target/release_manifest.json`; the D-63 identities are still
  their own directory names. Only the root differs, and the root is already a resolved
  value rather than a literal.
* **The confusion becomes impossible rather than detectable.** A seven-day fixture release
  cannot occupy the governed citation at all, so no reader — and no later full-year run —
  ever meets one where the other belongs. Today a fixture run *does* occupy it, and a
  subsequent governed run would hit the "different content" refusal I built for R-13, which
  is the right refusal for the wrong reason: it would be reporting a collision that should
  never have been possible.
* **It matches a precedent this project already set and you already approved.** The stage-04
  audit artifact is quarantined exactly this way; this extends the same rule from the audit
  artifact to the releases beside it.
* **It costs nothing in provenance.** The manifests keep `evidence_class`, `fixture_scope_id`
  and `window`; the root becomes a second, structural statement of the same fact, and the
  two cannot disagree because the root is derived from the same scope.

**What it costs.** One resolution helper used by stages 00, 02 and 04, and a matching
resolution in `05/06/07` when they read (they must look under the fixture root on a fixture
run — they already receive `--fixture-manifest`, so the scope is in hand). Stage 00's
existing `plumbing_7day_<stamp>/` directories would move under the fixture root too, which
is a tidy-up rather than a requirement.

### The alternative I am not recommending, and why

**Prefix the directory name** (`fixture__phase1_hourly_target/`). It keeps one root, but it
breaks the fixed name three consumers hardcode and breaks the identity equality the
permitted-producer check depends on, so each consumer would need to learn a naming
convention — which is precisely the "convention a reader has to learn" the D-63 identity
naming was chosen to avoid. It also leaves both kinds in one directory listing, where the
next reader still has to know which prefix means what.

### What I would need from you

This touches the read path of three consuming stages, so it is a cross-unit contract change
and I have not made it. If you approve it, I will implement the root resolution and move the
existing fixture releases, in one pass, with the consumers updated together so no
intermediate state exists where a stage looks in the wrong place.

**Decision required — Approve / Reject / Modify / Postpone.**

---

## §3 — STOP (second, same class as §1): `f107_safe`'s series and the trailing window's `source` are one key, and the two consumers need different ROW SHAPES from it

*Raised 2026-09-23, after §1 and §2 were approved and implemented. Found while writing the
loader §1 unblocked — not by review, but by working out what the two consumers actually
require from each key.*

### What was found

§1 fixed the two F10.7 **fields** sharing one `source_series`. One layer down, the same key
is still doing two jobs — this time for two *consumers* that need incompatible row shapes:

| Consumer | Reads | Needs from `f107_daily_median` |
|---|---|---|
| `build_features` (for `f107_safe`) | `_hourly_series` — requires `interval_start_utc` + `value` per row, refuses a row without them (`build.py:674`) | a value at **every hourly epoch** of the served window (168 rows for the fixture) |
| `build_availability_matrix` (trailing limb) | `_daily_values` — requires `day` + `value` per row (`availability.py:636`) | a value for **every day of the 81-day window** (88 days for the fixture) |

Both resolve the same key: `feature_dictionary.f107_safe.source_series` and
`availability_lags.f107_81_trailing.window.source` are both `"f107_daily_median"` (printed
from the config). One frame cannot be both without lying about one of them:

* **per-day rows** (88 rows, one per covered day) satisfy `_daily_values`, but give
  `f107_safe` a value only at each day's 00:00 — and the frozen carry-forward bound is
  **3 hours** (TC-09), so hours 04:00–23:00 would carry no driver value and every such row
  would be dropped from the feature matrix. Five sixths of the fixture's rows, silently.
* **per-epoch rows** (168 rows) satisfy `f107_safe`, but then `_daily_values` sees only the
  ~7 distinct eligible days, and `trailing_mean` refuses — correctly — that a
  81-day window has 7 constituents (TC-20: a missing window day is never filled).

### Why I stopped rather than choosing

Either fix edits a field D-60/D-47 froze, exactly as §1 did, and the choice of *which*
field to rename is a contract decision rather than an implementation detail. I have not
touched either.

### The two ways out

1. **Give `f107_safe` its own `source_series`** — e.g. `f107_safe_at_origin` — leaving
   `f107_daily_median` to mean what its name says and what D-21 defines: the daily series,
   which is exactly what `window.source` needs. *Recommended:* the daily median is the
   thing D-21 froze and the thing the trailing window recomputes from, so the plain name
   should keep the plain meaning; the per-origin selection is the derived object and should
   carry the qualified name. Symmetrical with §1, where the derived (trailing) object took
   the qualified name and the source kept the plain one.
2. **Repoint `window.source`** to a new daily key — e.g. `f107_daily_median_by_day` —
   leaving `f107_safe` on the plain name. Same one-line cost, but it names the *source* as
   the special case and leaves two keys that both sound like the daily series, which is the
   confusion this pair has already produced twice.

Under either, nothing scientific moves: D-21's median rule, D-25's availability rule,
D-47's tolerance and input bound, the 81-day window, the normalizations and the D-63
producing artifact are all untouched, and the field and row counts stay at 21 and their
current set.

**Recommendation: option 1**, adopted under D-60's existing scope as §1 was, with no new
D-number unless you want one.

### What is already done and works, so you can see where this sits

Both approved items are implemented, executed and committed:

* **§2, the release-root split**: every producer and consumer now resolves through one
  `release_root_for`. A fixture run writes and reads
  `artifacts/walking_skeleton/<fixture_id>/releases/`; a governed run uses
  `artifacts/releases/`. Directory names and D-63 identities are untouched. Verified by
  running the ladder: stage 05's refusal now names the fixture path.
* **§1, the dictionary**: `f107_81_trailing` carries `source_series: f107_81_trailing_mean`.
  21 fields and the same `dictionary_row` set, derived and printed before and after.
* **A consequence of the frozen contract, implemented and recorded rather than decided**:
  a driver release must CARRY more than it SERVES, because a feature at the first served
  origin reads history before it. Each release now covers its served window extended
  backwards by exactly what `configs/features.yaml` declares — measured on the fixture:
  F10.7 **2022-08-12..11-07 (88 days = the 81-day window + the 7 served days)**, Kp/ap and
  Hp60/ap60 two days, Dst one. The manifests carry `window` (served) and `covered_window`
  (carried) as distinct fields. The numbers come from the frozen 81 and the frozen lags;
  none was chosen here.

**The loader itself is not written.** Stage 05's stub is untouched, so there is no
half-built path anywhere.

**Decision required — Approve / Reject / Modify / Postpone.**

---

## §4 — Disposition question: five pre-ruling fixture releases still sit under the governed root

`artifacts/releases/` currently holds `plumbing_7day_<stamp>/` ×5 plus
`phase1_hourly_target/` and the four driver directories — all published by fixture runs
*before* §2's ruling, all committed. §2 stops any new one appearing there, but does not
move the existing ones.

I deleted them while re-running, then **restored them from git**: removing committed
release artifacts is a destructive act on published evidence and is yours to authorise, not
mine to tidy. Three options: leave them as pre-ruling historical artifacts (a reader sees
duplicates of the current fixture releases, which the manifests' `evidence_class` already
marks as `fixture_plumbing`); `git mv` them under the fixture root, preserving bytes
exactly; or remove them, since the current fixture run reproduces equivalent content.

**No urgency and no correctness consequence** — nothing reads them any more. Recorded so it
is a decision rather than a drift.

**Decision required — Approve / Reject / Modify / Postpone.**

---

## §5 — STOP: a single-station fixture cannot fit `station_lat`, whose frozen normalization is train-only standardize

*Raised 2026-09-23 after §1 and §3 were approved and the loader was built. The ladder now
reaches the feature build and gets all the way through it — this is the first thing it
cannot resolve without you.*

### What happens

`plumbing_7day` is a **one-station** fixture (D-20: BSHM), so `station_lat` is the same
value in every row. D-60 freezes its normalization as `train_only_standardize`, and
`fit_transforms` refuses a constant column by design:

> "has zero variance over the training range; a scale for a constant column cannot be
> chosen by convenience — declare it `normalization: none` in the dictionary or fix the
> input (TE §18.2)"

That refusal is **correct**. A constant column has no scale to fit, and inventing one is
exactly what TE §18.2 forbids. But it means the plumbing fixture cannot build a transformed
bundle for any partition, so the ladder stops here.

### Why this is yours and not mine

Both escapes change something frozen:

* setting `station_lat` to `normalization: none` would change a D-60 value for the
  **governed** run too, where three stations make it genuinely variable — a scientific
  change, and not defensible;
* giving the plumbing fixture more than one station would change **D-20**, which froze the
  single-station choice under Q-31 and TC-03f.

### The options

1. **Fixture-scoped normalization override.** The fixture declares, in its own manifest,
   that `station_lat` is `none` **for this fixture only**, as an apparatus constant (R-122)
   with the reason recorded: a one-station fixture has no station spread to scale by. The
   governed dictionary is untouched. *Recommended* — it keeps the frozen value frozen, puts
   the deviation in the apparatus where the fixture's other apparatus constants already
   live, and is visible in the manifest a reviewer reads.
2. **Give the plumbing fixture a second station.** Makes `station_lat` genuinely variable
   and needs no override, but reopens D-20 and changes what the seven-day smoke test is.
3. **Exclude `station_lat` from the fixture's feature set.** Smaller than (2) but it means
   the fixture stops exercising the station-registry path for that field, which is part of
   what the smoke test exists to exercise.

Under (1) nothing scientific moves: the dictionary, the producing artifact and the governed
behaviour are unchanged, and the scientific fixture (three stations) is unaffected either
way.

### A defect this surfaced, already fixed — worth reading even if you pick (2) or (3)

The refusal above fired for **one** partition and not the other two, which should have been
impossible for a column that is constant in all three. Derived and printed:

```
48 identical values of 32.778987
  mean == value?            False
  computed variance          2.0194839173657902e-28      (strictly positive)
  passes `variance <= 0.0`?  True        <-- the guard let it through
  scale                      1.4210854715202004e-14
  standardised value         1.0         <-- every row, exactly
```

The guard tested `variance <= 0.0`. For a constant column the computed mean differs from the
value in the last bits, so the variance comes out at 1e-28 rather than 0, the guard **passes**,
and the column is standardised by a scale of 1e-14 — turning every row into exactly `1.0`.
A meaningless number wearing a plausible face, which is worse than a refusal. One partition
happened to cancel exactly and refused; the other two sailed through and wrote bundles.

Fixed in `src/features/transforms.py`: constancy is now tested **directly** (`min == max`,
exact for floats) with the variance test kept after it. The existing control used three
values of `1.0`, whose mean is exact and whose variance is exactly `0.0` — it passed under
either guard and never exercised the escape, which is why this survived. A new control uses
the fixture's own literals (BSHM's latitude, 48 rows), asserts the computed variance really
is positive before asserting the refusal, and tells a future reader to recompute the
literals rather than delete the test if the escape ever closes. A must-not-fire limb pins
that a column with real spread still fits.

**This fix is a defect repair, not a decision, and is already in.** It also makes the
refusal above fire for every partition rather than one, which is why the fixture now stops
cleanly instead of writing two bundles of noise.

**Decision required — Approve / Reject / Modify / Postpone.**

> ## ✅ RULED 2026-09-23 — option 1 approved by the owner, and implemented
>
> **The mechanism.** A fixture scope may carry an `apparatus_normalization` block declaring
> a column `normalization: none` **for that fixture**, with the reason recorded.
> `configs/features.yaml` is untouched — `station_lat` is still `train_only_standardize`,
> exactly as D-60 froze it — and a governed run reaches `build_features` by a path that
> carries no fixture scope, so it can never pick an override up. Declared in
> `tests/fixtures/plumbing_7day/identity_declaration.yaml`, beside the apparatus partitions,
> as R-122 apparatus constants.
>
> **The override is closed to `none`.** It can only ever REMOVE a standardisation the
> dictionary declares, never introduce or alter one — an apparatus file that could set
> `train_only_standardize` would be adding a scientific transform, which is what keeping the
> deviation out of `configs/features.yaml` exists to prevent (TE §18.2).
>
> **It is a claim the code checks, not a licence.** `fit_transforms` verifies that each
> overridden column really is constant over the fitting range and refuses when it is not,
> quoting the declared reason back. Without that limb an override would be a way to silently
> drop a genuine train-only standardisation while wearing an apparatus label — a
> leakage-shaped change (NFR-LEAK-01) that raises nothing and improves the numbers.
> `build_features` checks the other half: an override naming no dictionary field, or naming
> one the dictionary already declares `none`, is refused rather than ignored, so a typo can
> never read as a discharged obligation.
>
> **Measured result.** Stage 05 now **completes** for all three apparatus partitions, writing
> eight bundles plus `fixture_measurements.json`. `station_lat` carries BSHM's true
> `32.778987` in every bundle including the transformed ones — the override removes the
> scale, it does not corrupt the value — while `kp_safe` is still standardised
> (`1.667 → -1.2045`), so the deviation is confined to the one declared column. WS-13's
> value-level parity measured **0.0 TECU** over 8 bundles, which is the number a tolerance
> freeze needs; WS-13 stays Pending, because a measurement is not a passed check.
>
> **Controls added**, in this project's negative-control-per-rule idiom: the override
> honoured for a genuinely constant column (and leaving its neighbour standardised); the
> override **refused** when the column has real spread; `build_features` refusing an unknown
> field and refusing a no-op override; the manifest validator refusing any value but `none`
> and refusing a missing reason; and a pin on the shipped declaration carrying exactly the
> one column approved here. Full suite: no new failures, no new lint findings.

### Where the ladder stands, measured

Stages **00, 01, 02, 04** complete; **05 builds the feature matrix**. Before it stops at
`station_lat` it has already produced, for `FIX-NOV-FOLD-01`, a **48 × 46** matrix carrying
all 21 dictionary fields with per-column provenance resolved against the permitted-producer
list — `kp_safe`/`ap_safe` → `gfz_kp_ap_nowcast_2022`, `hp60_safe`/`ap60_safe` →
`gfz_hp60ap60_v2_2022`, `f107_safe`/`f107_81_trailing` →
`nrcan_f107_observed_daily_median_2022`, the `vtec_*` rows → `phase1_hourly_target`, time
rows → `record_timestamp`, station rows → `station_registry` — plus the 24-step sequence
tensor, **zero** carry-forward exclusions and **zero** driver rows excluded. The availability
matrix, the lag assertions and the 81-day anchor recomputation all passed on real released
data.

Three things were needed along the way and are recorded as implementation rather than
decision, each because its value was uniquely determined by something already frozen:

* **`source_column: "vtec_tecu"`** on the four `vtec_lag_*` fields and `vtec_seq_24`.
  `build_features` requires it (`:957`, `:959`) and `load_feature_dictionary` validates it
  only for support fields, so its absence was invisible until a matrix was built. D-17
  defines exactly one VTEC column, so the value was not chosen.
* **`_take_rows` now carries the frame's `attrs`**. The embargo-trimmed score frame came
  back stripped of `producing_artifact` and `build_features` refused it — correctly, since
  SD-E-03 flips the default so absent provenance fails. Subsetting rows changes which rows,
  never who produced them.
* **A measuring counterpart for WS-13's value-level parity limb.** The tolerance is measured
  from the fixtures and frozen, never invented (TE §15.1), so `assert_window_parity` refuses
  while it is unset — leaving a measuring run unable to produce the number the freeze needs.
  `measure_window_parity` runs the shape and ordering limbs and **reports** the largest
  observed difference instead of comparing it; stage 05 folds it into the fixture
  measurements. Measuring and asserting are two functions on purpose, and **WS-13 stays
  Pending**: a measurement is not a passed check.

**One apparatus adjustment inside the shape you approved:** `FIX-NOV-FOLD-02`'s validation
day moved from 2022-11-06 to 2022-11-05. At 11-06 the fold scored 2022-11-07 alone, whose
24-step window history is exactly the day the 24-hour embargo removes, so the assembled
score frame came back empty and R-74 refused it. The one-day shift is forced by the frozen
window length and embargo; the fold stays expanding and no scientific value moves.

---

## §6 — Disposition: four committed feature bundles carry the pre-fix `station_lat = 1.0` noise

*Raised 2026-09-23 on re-running the ladder after the §1/§3 approval. Recorded, not acted
on: these are committed artifacts, and the standing instruction of 2026-09-23 is not to
delete or alter committed artifacts without a separate ruling.*

### What is on disk, measured

`artifacts/walking_skeleton/plumbing_7day/features/` holds **24 tracked files**, last
committed in `5aaf655` (2026-09-23 19:24), written at 19:20 — *before* the constancy-guard
repair described in §5 landed at 19:24. Read back just now:

```
FIX-NOV-FOLD-01__score__T-FIX-NOV-FOLD-01      station_lat=[1.]          n=48
FIX-NOV-FOLD-01__train__T-FIX-NOV-FOLD-01      station_lat=[1.]          n=48
FIX-NOV-FOLD-01__train__untransformed          station_lat=[32.778987]   n=48
FIX-NOV-FOLD-02__score__T-FIX-NOV-FOLD-02      station_lat=[1.]          n=24
FIX-NOV-FOLD-02__train__T-FIX-NOV-FOLD-02      station_lat=[1.]          n=72
FIX-NOV-FOLD-02__train__untransformed          station_lat=[32.778987]   n=72
```

The four **transformed** bundles carry `station_lat` standardised to exactly `1.0` — the
meaningless value §5 derives, produced by dividing a constant column by a scale of
`1.4e-14`. The two **untransformed** bundles carry BSHM's true latitude and are unaffected.

These are exactly the "two bundles of noise" §5 says the repair prevents. The repair
prevents new ones; it does not reach the ones already written and committed.

> ## ⚠ STATUS CHANGED 2026-09-23 — §6 IS NOW THE BLOCKER
>
> When this section was written the stale bundles cost nothing. With §5 ruled and
> implemented they are what stops the ladder: stage 05 gets all the way through the feature
> build and then refuses at the write —
>
> > `artifacts\walking_skeleton\plumbing_7dayeatures\FIX-NOV-FOLD-01__train__untransformed:
> > bundle directory already exists; a bundle is never overwritten (TE §13.3)`
>
> — which is the correct refusal. Stage 05 was proved to complete by running it into a
> scratch directory outside the repository, so nothing about §5 is unverified; what cannot
> happen without a ruling here is the ladder writing its bundles where 06 and 07 read them.
>
> There is also a second reason this now matters more than tidiness: if the ladder were
> allowed to continue past these directories, **stage 06 would read the pre-fix bundles** —
> the ones whose `station_lat` is `1.0` — and train on them.
>
> I was wrong to describe this section as having "no urgency"; that was true only while §5
> was unruled. Nothing was deleted.

### Why this is a disposition question and not a defect to fix

Nothing here is wrong with the code as it now stands — a re-run cannot reproduce these
files, because the repaired guard refuses before any bundle is written. The question is
only what happens to artifacts already in the history. They are **fixture-path** artifacts
(`artifacts/walking_skeleton/`), never the governed root, and the plumbing fixture is a
smoke test and never scientific evidence (TC-03f), so nothing scientific rests on them.

### The options

1. **Delete the four transformed bundles, keep the two untransformed.** Removes the noise
   while keeping what is still true. *Recommended* — a bundle whose only numeric content is
   an artefact of a repaired defect has no reader it can serve correctly, and leaving it
   where a future run writes its successors invites it being read as one.
2. **Delete all 24 files and let the ladder rewrite them once §5 is ruled.** Cleanest, and
   the fixture path is reproducible by construction, but it discards the untransformed
   matrices that are currently the only on-disk evidence that the §1/§3 fix works.
3. **Leave everything and record the caveat here only.** Consistent with the standing
   instruction and costs nothing today, but the `1.0` columns stay readable by anyone who
   opens the fixture path without reading this file.

**Decision required — Approve / Reject / Modify / Postpone.**

> ## ✅ RULED 2026-09-23 — option 1 approved and executed, and it does NOT clear the block
>
> **Done, exactly as ruled.** The four transformed bundles are deleted — 16 tracked files,
> four per directory (`fixture_stamp.json`, `matrix.parquet`, `spec.json`, `tensor.npy`) —
> and the two untransformed bundles are kept, 8 tracked files. The deletions are unstaged in
> the working tree; nothing was committed, and `git checkout` restores them until you commit.
>
> **CORRECTION, measured rather than reasoned.** Option 1 removes the noise but does **not**
> unblock the ladder, and my status box above implied a ruling here would. Stage 05 was
> re-run against the real bundle path after the deletion and refuses at the same place:
>
> > `…features\FIX-NOV-FOLD-01__train__untransformed: bundle directory already exists; a
> > bundle is never overwritten (TE §13.3)`
>
> The refusal names an **untransformed** bundle — one of the two option 1 keeps. Stage 05
> writes each partition's raw bundle BEFORE its transformed one, so the first write of the
> run hits a kept directory. Nothing was written by that aborted run: the refusal precedes
> every write, and the tree still shows exactly the 16 deletions.
>
> **A fact that changes the balance of the remaining choice.** Option 2's stated cost was
> that deleting all 24 "discards the untransformed matrices that are currently the only
> on-disk evidence that the §1/§3 fix works". That is no longer true on either half:
>
> * the §1/§3 fix is now evidenced by the scratch run recorded in §5, independent of these
>   files; and
> * the two kept bundles are **pre-mechanism artifacts** — their `spec.json` carries no
>   `apparatus_unstandardized` key (verified by reading it), because they were written
>   before the override existed. Every bundle written from now on records it. So they are
>   not simply "still true"; they are stale in their metadata, and a re-run reproduces
>   equivalent untransformed matrices with the record attached.
>
> **What is still owed:** a ruling on the two kept untransformed bundles. Deleting them is
> what clears the block, and is option 2 in substance. Nothing further was deleted.
>
> ---
>
> ## ✅ SUPERSEDED BY OPTION 2, RULED AND EXECUTED 2026-09-23 — the block is cleared
>
> The owner ruled option 2 and directed a stage 05 re-run with no commit. The two remaining
> untransformed bundles were deleted (all 24 tracked files gone, directory empty), and
> **stage 05 then completed, exit 0**, writing:
>
> | Bundle | Rows | `station_lat` | `apparatus_unstandardized` |
> |---|---|---|---|
> | `FIX-NOV-FOLD-01__train__untransformed` | 48 | 32.778987 | `station_lat` |
> | `FIX-NOV-FOLD-01__train__T-…` | 48 | 32.778987 | `station_lat` |
> | `FIX-NOV-FOLD-01__score__T-…` | 48 | 32.778987 | `station_lat` |
> | `FIX-NOV-FOLD-02__train__untransformed` | 72 | 32.778987 | `station_lat` |
> | `FIX-NOV-FOLD-02__train__T-…` | 72 | 32.778987 | `station_lat` |
> | `FIX-NOV-FOLD-02__score__T-…` | 24 | 32.778987 | `station_lat` |
> | `FIX-NOV-REFIT__train__untransformed` | 144 | 32.778987 | `station_lat` |
> | `FIX-NOV-REFIT__train__T-…` | 144 | 32.778987 | `station_lat` |
>
> plus `apparatus_split_manifest.json` (three partitions; embargo exclusions 24 rows on each
> fold) and `fixture_measurements.json` (WS-13 value-level parity **0.0 TECU** over 8
> bundles, `status: measured, not frozen; WS-13 Pending`).
>
> **`FIX-NOV-REFIT` exists for the first time.** The pre-fix run never reached the refit
> partition, so both its bundles are new files rather than replacements.
>
> **What the diff proves, without needing to be argued.** For the two untransformed bundles
> only `spec.json` differs from the committed version — `matrix.parquet` is **byte-identical**
> — so the override changed no data, only the record that it applied. In the transformed
> bundles `matrix.parquet` and `spec.json` differ (the `station_lat = 1.0` artefact is gone,
> replaced by the true 32.778987) while `tensor.npy` and `fixture_stamp.json` are
> byte-identical, `station_lat` being no sequence field. Every bundle's `spec.json` now
> carries `apparatus_unstandardized: {station_lat: …}`, so the deviation is disclosed in the
> artifact a reader opens rather than only in this file.
>
> **Not committed**, per the owner's instruction. The experiment registry took 20 further
> appended rows with nothing removed (NFR-AUD-01).

---

## §7 — For your awareness: three suite failures, all pre-existing, one inside a §18.3 critical module

*Measured 2026-09-23 on the full suite at `996a5f9`. Raised because one of the three sits in
a module §18.3 names in its critical set, not because anything in this session caused it.*

### What fails

The suite runs to completion (3 skips) with **three** failures:

| Test | Module last touched | Cause |
|---|---|---|
| `test_no_restricted_read_in_this_module_bypasses_the_chokepoint` | `tests/test_phase_boundary.py` — `4cdd549`, 09-20 | the scan flags **its own** `Path(__file__).read_text()` at line 667 |
| `test_no_restricted_read_in_this_module_bypasses_the_chokepoint` | `tests/test_release_hashes.py` — `4cdd549`, 09-20 | same self-referential shape |
| `test_the_test_mode_access_log_also_reconciles_when_it_exists` | `tests/test_locked_test_guard.py` — `cda8869`, 09-22 | `run_id "test_phase_boundary"` is absent from the orphan whitelist |

**None of the three touches anything changed in this session.** The first two read their own
source and scan it with a function defined in the same file; both files predate this work by
three days, so their result is deterministic and independent of it. The third fails because
`tests/test_phase_boundary.py:117` writes `run_id="test_phase_boundary"` into the shared
test-mode access log (75 such rows have accumulated) while
`HISTORICAL_TEST_ORPHANS` in `tests/test_locked_test_guard.py` whitelists exactly two
run_ids — `test_release_hashes` and `test_acquisition_window`. `test_phase_boundary` was
never added, so any suite run in which that module has executed fails this reconciliation.

### Why it is raised rather than fixed

`test_locked_test_guard.py` is the module behind **"locked-test access guard"**, one of the
ten items §18.3 names in its critical set, and that gate's criterion is *"zero unresolved P0
fields and no failing critical test."* A failing test in that module is therefore gate-
relevant even though its cause is test isolation rather than a defect in the guard itself —
the guard's own behavioural tests pass. Stating that distinction is the point: the gate reads
pass/fail, and the honest report is that the module is currently red for a reason that has
nothing to do with December access control.

Fixing it means either adding `test_phase_boundary` to the orphan whitelist with its reason,
or stopping that module writing to the shared log. Both are edits to the locked-test-guard
family under a frozen receipt, and neither is inside what was approved for this session, so
neither was made.

**Decision required — Approve / Reject / Modify / Postpone.**
