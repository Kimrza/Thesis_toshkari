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
