# Change record — 2026-09-24 — D-28 option (b): bounded 1-December read (design spec, BLOCKED on implementation)

**Authority:** Student ruling — option (b) approved: revert the 29-day amendment, implement
`RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md` §2 Option A instead.
**Status: DESIGN DRAFTED, IMPLEMENTATION STOPPED.** The revert (D-28 back to 30 days) is done
— see `evidence/DECISIONS.md`. The bounded-read mechanism itself is **not built**, for the
reason in the STOP section below, which was discovered while implementing it, not assumed in
advance.

---

## What was done

`evidence/DECISIONS.md` D-28 reverted to its original 30-day text, with the 29-day amendment
kept as dated, struck-through history rather than deleted (this project's standing convention).
`governance/RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md` §2 and
`governance/REC_13_60_STATUS_2026-09-24.md` Rec 15 updated to point here.

## STOP — implementation blocked by the same class of freeze as Layer-1 §7

Locating where the mechanism would live:

```
$ grep -n "def open_restricted" src/data/locked_test.py
436:def open_restricted(...)

$ grep -n "^PURPOSES" -A 8 src/data/locked_test.py
PURPOSES: Final[frozenset[str]] = frozenset({
    "coverage_audit", "regime_audit", "locked_evaluation", "acquisition_read", "acquisition_write",
})
```

The originally-specified Option A (`RULING_REQUEST_2026-09-21...` §2) requires an
`AccessRecord` with `purpose = "persistence_history"` — **not currently in the closed
`PURPOSES` set**, which `AccessRecord.__post_init__` enforces by raising on any value outside
it. Adding this value means editing `src/data/locked_test.py`.

```
$ grep -rl "src/data/locked_test.py" aidlc/.../construction/*/code-generation/code-summary.md
... governance-guards/code-generation/code-summary.md  <- owning unit, confirmed by content
... (six other units cite it, none own it)

$ grep -n "^\*\*Verdict:\*\*" .../governance-guards/code-generation/code-summary.md
215: READY
291: NOT-READY
340: NOT-READY
568: READY
689: READY   <- terminal, most recent
```

`src/data/locked_test.py` is owned by the **`governance-guards`** unit — the exact same unit
whose terminal `READY` receipt (line 689) already blocks the Layer-1 §7 chokepoint-scanner
fix, per the AI-DLC stage-receipt write-freeze mechanism confirmed present in
`.claude/tools/aidlc-audit.ts`/`aidlc-state.ts` in an earlier session. Adding a new `PURPOSES`
value, a new lookup function, and the `open_restricted` call site all sit inside this frozen
file. Per this task's own general rule ("If anything in Part 1's implementation turns out to
require touching a frozen/locked module... STOP and report rather than proceeding"), **no
edit was made to `src/data/locked_test.py`.**

**Nothing in `scripts/06_train_and_predict.py` or `src/models/persistence.py` was touched
either** — wiring either of those to a lookup mechanism that doesn't yet exist, or that reads
from an unauthorized purpose value, would just move the same problem, not solve it.

## Design specification (for the record, and for whoever unfreezes `governance-guards`)

The mechanism, as it would be built once `governance-guards` is redone or the freeze is
otherwise lifted:

1. **New `PURPOSES` entry**: `"persistence_history"`, added to `src/data/locked_test.py`'s
   closed set.
2. **New function**, e.g. `read_persistence_history_lookup(snapshot, *, g05_signature, loader,
   registry)` in `src/data/locked_test.py`, mirroring `materialise_locked_partition`'s own
   `g05_signature` verification (`verify_g05_signature`, `src/data/splits.py:692`) — refuses
   with no signature, refuses on a non-verifying signature. Routes the read through
   `open_restricted` with `purpose="persistence_history"`, `performance_inspected=False`,
   `locked_test_accessed=True`, logging the access exactly as every other restricted-root read
   does (Vision §8.3; TE §13.4).
3. **Returns 1-December rows only** — `(station, timestamp)` → value, timestamps restricted to
   `2022-12-01T00:00:00Z .. 2022-12-01T23:00:00Z` inclusive, never anything from 2 December
   onward (that's what `materialise_locked_partition`'s own embargo-trimmed frame already
   supplies, untouched by this mechanism).
4. **Caller-side gating in `scripts/06_train_and_predict.py`**: in `_locked_predictions`
   (`:737`), when `model_id in ("M-01", "M-02")`, merge the 1-Dec lookup dict into the
   `series` `target_series()` builds — via a NEW keyword-only parameter on `fit_predict`/
   `persistence.fit_predict_rows`, never by mutating `locked_target` itself (the SCORED
   frame, which stays exactly what D-28/D-59 define — 2–31 December). Any model other than
   M-01/M-02 requesting the lookup is refused.
5. **The 5 conditions, and how each is mechanically enforced by the design above:**
   - *(i) no 1-Dec row is ever scored* — structurally guaranteed: `persistence_rows`
     (`src/models/persistence.py:113`) iterates `bundle_index(score_bundle)`, whose index is
     built from the embargo-trimmed frame (2–31 Dec only); the 1-Dec lookup values are only
     ever read via `series.get((station, stamp - offset))` — as a value looked up *from*, never
     as a `stamp` that could itself be scored. No code change to `persistence.py`'s indexing
     logic is needed or proposed.
   - *(ii) only M-01/M-02* — enforced by the new keyword-only parameter's caller-side gate in
     step 4, plus a refusal in the new function itself if invoked for any other `model_id`.
   - *(iii) routed through `open_restricted`, logged* — step 2, by construction (the same
     chokepoint used everywhere else).
   - *(iv) gated to post-G-05* — step 2's `g05_signature` verification, reusing the existing
     `verify_g05_signature` mechanism `materialise_locked_partition` already uses; before G-05
     the function refuses exactly as `materialise_locked_partition` does today.
   - *(v) frozen under its own D-number before use* — the function additionally checks a new
     `configs/experiment.yaml` authorization flag (e.g.
     `persistence_history_lookup.authorized: true` with a `decision` field citing the D-number),
     read the same fail-closed way `resolve_budget_rule` reads `uncertainty_budget` — absent or
     `TBD` means refuse, never a silent default.
6. **Tests, once buildable**: pre-G-05 refusal; wrong-`model_id` refusal; wrong-`purpose`
   refusal (any caller bypassing the new function and hand-building an `AccessRecord` with
   `purpose="persistence_history"` some other way must still fail the closed-set check);
   1-Dec value never appears in any scored bundle's row index; access-log row appended with
   full provenance; pre-authorization (config flag absent/TBD) refusal.

## Proposed D-number text (draft only, for the owner to adopt once buildable)

> **D-6? Bounded 1-December persistence-history lookup for M-01/M-02 (Option A, `RULING_REQUEST_2026-09-21...` §2)**
>
> | Countersignature | Date | Rationale |
> |---|---|---|
> | *(owner fills — Supervisor, per the original routing: "Owner: Supervisor. Due: before G-05")* | *(owner fills)* | Authorizes a narrowly-scoped, logged, performance-blind read of 2022-12-01 target values, strictly as backward-looking lookup history for M-01 (`y(t-1h)`) and M-02 (`y(t-24h)`), recovering the full D-28/D-59 30-day scored set (2–31 December) without amending either decision. Subject to all 5 conditions in `governance/CHANGE_RECORD_2026-09-24_d28_option_a_bounded_read.md`'s design specification: no 1-Dec row is ever scored; only M-01/M-02 may use it; routed through `open_restricted` with `purpose="persistence_history"`, logged; active only post-G-05; and this D-number itself, cited in `configs/experiment.yaml`, is the final gate — absent it, the mechanism refuses. **Does not touch, amend, or contradict D-28 or D-59** — both stand exactly as originally frozen; this is an additive lookup path for two specific, unfitted difficulty controls, not a change to the locked-test scored-set definition. **Not yet implementable**: the mechanism's home, `src/data/locked_test.py`, is owned by the `governance-guards` unit, which carries a terminal `READY` AI-DLC stage-receipt (write-frozen) — building this requires either an AI-DLC stage redo for that unit or an explicit unfreeze, neither of which is in scope for a documentation/config session. |

**Decision required — Approve / Reject / Modify / Postpone** on the design as specified, plus
a separate decision on whether/when to route the `governance-guards` unfreeze needed to
actually build it (see `governance/PENDING_FOLLOWUPS.md` item 1, the parallel chokepoint-
scanner blocker — these two items should likely be unfrozen together, in one stage redo,
rather than twice).
