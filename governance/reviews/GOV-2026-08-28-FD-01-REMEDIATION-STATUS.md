# Remediation status — `GOV-2026-08-28-FD-01`

**Written 2026-08-28 at the point the workflow was parked.** This is a resume note, not a
gate report and not a claim of completion. The stage's standing governance verdict is
**FAIL**; nothing here changes it.

## Owner rulings taken (all recorded, all applied where applied)

| Ruling | Decision |
|---|---|
| Rec 6 — 30-day locked-test scored set | **Ratify now.** Written as **D-28** + `CHANGE_RECORD_2026-08-28_locked_scored_set.md`, with the Vision §8.2 / TE §7.1 `—`-cell conflict disclosed verbatim and carried to G-05 |
| Rec 8 — exception taxonomy | **Promote `PartitionError` to a fifteenth** in `foundation` R-01 |
| Rec 19 — tier-3 comparison | **Add a third declared set `{M-04, M-05, M-06}`** with its own mask |
| Recs 13/14/15 — science items | **Mechanism written, value routed** to Student/Supervisor at G-04/G-05 |
| Rec 7 — BLK-08 | **Narrowed to `ABL-DIFF` on D-27's strength** (see the correction below) |

## Governance layer — COMPLETE

- **D-28** in `evidence/DECISIONS.md` (entry + countersignature-status register row).
- **`CHANGE_RECORD_2026-08-28_locked_scored_set.md`** — Vision §15.2's six fields; the
  mandatory propagation sweep over **236 Markdown files** with every site dispositioned.
  Six sites deliberately **not edited** (2 authority documents, 3 completed-stage
  artifacts, 1 memory layer), each with owner and route recorded.
- **Loose December extract manifested** —
  `evidence/locked_test_restricted/loose_artifacts_sha256_manifest.json`,
  `sha256 3a164af0864b2effde2e527ca190c1b050f5a47179eaffa3ccab770bb366f557`,
  1,666,816 bytes, `g.003` suffix recorded. **Access-log row 11 was written BEFORE the
  read**; row 10 retrospectively records the Validation Auditor seat's own metadata reads.

## A correction to the fix scope, found before any artifact was edited

The board's Recommendation 7 rested on a premise it said it could not verify — whether the
primary transform touches the target. **D-27 froze that premise on 2026-08-24**, four days
before the review and three days before the unit depending on it was authored: the primary
train-only transform touches target-**derived inputs**, not the target, which stays **raw
TECU**. D-27 further states it "no longer requires a general `src/evaluation` → `src/features`
route for the primary path" and that "**no import-boundary change is authorised by this
decision**".

`evidence/DECISIONS.md` sat at precedence rank 3 in all seven seats' briefs and **none read
D-27**; the three units depending on it cited it zero times. The remediation was narrowed on
the owner's ruling before any edit. **Corroborated independently:** `component-dependency.md`
shows `src/evaluation` → `features` as **`—` (absent), not `X` (forbidden)**, and its own
closing note says none should be added "**without the design naming the lookup**" — which is
what the narrowed `load_inverse` resolver does.

## Counts verified at source (against the authority documents, not the review)

| Claim | Derived | Board's figure |
|---|---|---|
| TE §13.4 registry columns | **20** (incl. `prediction_hash`, `locked_test_accessed`) | 20 ✓ |
| TE §15.2 content areas | **12** | 12 ✓ (REQ-ENG-4's "thirteen" is wrong) |
| TE §12 test modules | **21** | 21 ✓ (the 4 beyond `team.md`'s 17 named) |

## Per-unit remediation state

| Unit | Applied | Agent self-verified | Receipt | Review |
|---|---|---|---|---|
| `target-standardization` | ✅ | ✅ | ✅ **recorded, post-receipt writes done** | ⬜ |
| `foundation` | ✅ | ✅ | ⬜ | ⬜ |
| `governance-guards` | ✅ | ✅ | ⬜ | ⬜ |
| `external-products` | ✅ | ✅ | ⬜ | ⬜ |
| `features-and-splits` | ✅ | ❌ agent died verifying | ⬜ | ⬜ |
| `models-and-baselines` | ✅ | ❌ agent died verifying | ⬜ | ⬜ |
| `evaluation-and-comparison` | ⚠️ partial | ❌ died mid-edit | ⬜ | ⬜ |
| `statistical-inference` | ⚠️ partial | ❌ died mid-edit | ⬜ | ⬜ |
| `inventory-and-registry` | ⚠️ partial | ❌ died mid-edit | ⬜ | ⬜ |
| `acquisition` | ✅ | ❌ same agent died | ⬜ | ⬜ |
| `regimes-diagnostics-reporting` | ✅ | ❌ agent died verifying | ⬜ | ⬜ |
| `fixtures-and-reproducibility` | ✅ | ❌ agent died verifying | ⬜ | ⬜ |

**Six of eleven remediation agents terminated on the account's session limit** (resets
04:50 Asia/Dubai). Known-incomplete items: `statistical-inference`'s fifth § Gate items
entry (Rec 26); `evaluation-and-comparison`'s rule-numbering `[assumption]` and
governance-dependency line; `inventory-and-registry`'s `provenance_class` figure rebasing.

**Integrity sweep, all 12 units:** 0 unbalanced code fences · 55 `## Review` sections intact
· 0 new mojibake (8 pre-existing in `external-products`' untouched review text, 1 in
`inventory-and-registry` unchecked). Tracked units: **+7,046 / −654** across 27 files. The
four newest units are **untracked**, so `git diff` cannot show them — verify them by content,
not by diff.

## Corrections the finishing agents found (not in the board's report)

- **`foundation`** — "`PartitionError` reaches 10 of 12 units" is raw-token reach; **design
  reach is 2**. Ruling re-based on the taxonomy disagreement instead. Also found **two entity-
  and two workflow-mapping defects the board never named**, incl. FR-WS-7 pointing at
  `write_release` — worse than absence, because it looks answered.
- **`governance-guards`** — the board's `R-122` should be **`R-123`**; **all three** test
  modules read restricted content, not two; and `fluxtable.txt` (95 December lines) plus
  `ec1-audit-report.json` are December-bearing artifacts **already inside R-27's scan root and
  never enumerated** — a guard built from the old text would have failed on first run.
- **`external-products`** — Rec 46's defect is in **three** artifacts, not two; the conditional
  GIM phrasing is **7** occurrences, not 5 (two wrap across lines).
- **`target-standardization`** — **Q8 = D's literal text already placed the statement on the
  target-writing path**; the conflation entered via that option's impact line. No answer letter
  changes.

## Resume sequence

1. Verify the 7 unverified units; finish the 3 known-incomplete items.
2. Take the 11 outstanding summary confirmations (**receipt first, then a native-tool write to
   each artifact** — the ordering that deadlocked this stage once already).
3. Adversarial review per unit.
4. `report --result awaiting-approval`.
5. **Re-run the full board.** The standing verdict is FAIL and the review contract requires a
   fresh pass before the stage may be accepted; remediation is a separate run from the review
   that recommended it.

## Still owed to the owner

- `dataset_version` encoding — a **D-number decision before 3.5 touches `write_release`**.
- `InverseTransformError` as a sixteenth exception — not ruled.
- `RES-02` is itself stale (says 19 modules; derived is 21) — it lives in a completed-stage
  artifact, so annotate-in-place needs owner approval.
- `team.md`'s four stale facts — the practices-affirmation gate is the only sanctioned route.
- The three exempt test modules' disposition (synthetic fixture roots vs logged real-root
  reads) — today all three read December content with no access row.
- `.dst_summary.json` relocation — owes a D-number and a change record.
