# Change Record — the three comparison-set memberships confirmed and transcribed (R-106), and the Q2 = B sibling `AccessRecord` containment fields

**Record ID:** `CR-2026-09-06-R106-COMPARISON-SETS`
**Date:** 2026-09-06 (rulings receipted); record filed 2026-09-06 at the start of the
`evaluation-and-comparison` code-generation pass, BEFORE any module of that unit was written
(plan Step 1; the plan's own ordering rule).
**Ruling:** Project decision owner, at the `evaluation-and-comparison` code-generation plan gate
(Q1 = A, Q2 = B, Q3 = A, Q4 = A, Q5 = A; receipted in
`aidlc/spaces/default/intents/260813-tec-hourly-forecast/construction/evaluation-and-comparison/code-generation/code-generation-questions.md`,
Consolidated Summary Confirmation `Looks correct`, Plan Approval `Approve Plan`).
**Change class:** (1) The owner's confirmation of the three comparison-set memberships that
`functional-design` R-106 declared configuration and **routed to the gate as a §18.2/TC-03e
frozen scientific choice this stage may propose but not make** — confirmed under the recorded
owner-equivalence precedent (D-122's seeds transcription; D-28's ratification), with a proposed
D-number text below for `evidence/DECISIONS.md` that the owner adopts or edits (**no agent
writes the register**). (2) One transcription of that confirmation into a governed config
(`configs/experiment.yaml` gains `comparison_sets`; nothing else in the file is touched).
(3) One owner-instructed in-place edit of a sibling unit's module (`src/data/locked_test.py`,
Q2 = B), recorded here and **flagged for `governance-guards`' record and re-check**.

## What was owed, and by whom

`evaluation-and-comparison` R-106 (functional-design, remediated 2026-08-28 under
`GOV-2026-08-28-FD-01` Recommendation 19) declares each comparison set **named in
`experiment.yaml` with its enumerated member IDs** (TC-03e: membership is a frozen scientific
choice, not code) and proposes three sets, stating: *"the memberships go to the gate as an
explicit confirmation, not a default, and nothing here presents them as frozen."* No
`comparison_sets` block existed in `configs/experiment.yaml` before this pass (verified
2026-09-06), and TE §18.3 bars any implementer from filling it by convenience. Without the
declaration, `build_comparison_mask` can never build a mask (the mask builder refuses on any
mismatch against the declared set), so every mask-dependent path was unbuildable.

## The rulings this record implements

### Q1 = A — the three memberships are CONFIRMED and transcribed, citing this record

Exactly as R-106 / `domain-entities.md` § 1 propose them, grounded source by source:

| `set_id` | Members (enumerated, ordered) | Model | Benchmarks | Grounding |
|---|---|---|---|---|
| `primary` | `M-01`, `M-02`, `M-03`, `M-06`, `B-01` | `M-06` | `B-01`, `M-01`, `M-02`, `M-03` | Vision §2.4 tiers 1–2 (LSTM-vs-IRI plus the three mandatory difficulty controls co-reported); PC-03/PC-04 |
| `gim` | `M-06`, `C-01` | `M-06` | `C-01` | Vision §2.4 / §6.10 (CODE final GIM, evaluation-time-only comparator; separate set so a differently-caveated comparator never shrinks the primary scored set — R-106's own rationale) |
| `tier3` | `M-04`, `M-05`, `M-06` | `M-06` | `M-04`, `M-05` | Vision §2.4 tier 3 (LSTM versus ridge and versus direct RF); §8.4's model table (M-04 ridge, M-05 direct RF, M-06 LSTM); §8.9's matched-learned-model clause (the flattened matrix supplied to M-04 and M-05 is the flattened form of the identical causal window supplied to M-06); `GOV-2026-08-28-FD-01` Recommendation 19's owner ruling adding the third set |
|

Member counts, derived by enumeration above and printed before asserted: **5 / 2 / 3.**
Separate sets, separate masks, **never merged silently** (R-106; NFR-FAIR-01; TC-16). The
code asserts membership content **from config, never from source**, and the test module
re-reads the counts 5 / 2 / 3 from `configs/experiment.yaml` rather than asserting literal
member lists.

D-24 item 17's protected-baselines enumeration ({M-01, M-02, M-03, B-01, C-01}) does **not**
name M-04/M-05; the tier-3 set is grounded on §2.4 and §8.9 rather than on D-24, exactly as
R-106 records.

**What this confirmation is, and is not.** It is the R-106 membership confirmation the design
routed to the gate, made by the project decision owner at that gate under the recorded
authority equivalence — the same act pattern as D-122's seeds and D-121's grids
(`CR-2026-09-06-BLK03-CONFIRMATORY-CONTRACT` Q5 = A). Honestly stated: **no supervisor
signature artifact exists and none is claimed.** The §18.2 assignment of this choice is
Student + Supervisor; the proposed D-number below records that limitation on its face, exactly
as D-28 recorded its own.

### Q2 = B — the sibling `AccessRecord` gains SD-C-02's two containment fields, on the owner's explicit instruction

`nfr-design/security-design.md` § SD-C-02 proves mask-freeze-before-access by **containment**:
the locked-test access record carries `mask_bundle_ids` (the frozen bundle's `mask_id`s found
at access time) and `mask_registry_hash` (the SHA-256 of the frozen bundle's **write-once
manifest** at that moment). Those fields live on `governance-guards`' `AccessRecord` in
`src/data/locked_test.py` — a sibling unit's module. The owner's Q2 = B ruling instructs the
edit now, in place, rather than deferring to the sibling's next touch:

- `AccessRecord` gains `mask_bundle_ids: tuple[str, ...] | None = None` and
  `mask_registry_hash: str | None = None` — **additive, optional; existing rows and callers
  unbroken** (the `__post_init__` required-field check is untouched).
- `open_restricted` populates both when a frozen-bundle manifest is supplied and exists at
  access time (reads the manifest, hashes its bytes, lists its `mask_id`s); with no manifest
  the fields stay `None` — and this unit's `require_locked_receipt` **refuses** a `DEC` metric
  on `None`, which is the fail-closed half (SD-C-02: the access path fails closed, not the
  audit after the fact).
- The module docstring records the edit and this record.
- **Flagged for `governance-guards`' record and re-check**: the edit is an in-place change to
  a module whose unit was reviewed READY, made outside its own stage on the owner's explicit
  Q2 = B instruction (the legitimating condition the question named). `governance-guards` owes
  its own review of the two fields at its next touch.

### Q4 = A — the SD-C-02 read-then-write race is closed by write-once semantics, no new machinery

The frozen bundle's manifest is written **once per freeze** via the project's
`.tmp` → fsync → atomic-rename idiom (the same idiom as `write_prediction_hash_receipt`,
SD-M-04), and **any second write refuses**. A mid-registration read therefore sees either the
old complete manifest or the new complete manifest, never a partial one. The residual case —
a registration landing between the access path's registry read and its record write — is
**benign by containment**: the record simply evidences the earlier freeze, and post-hoc
verification (re-hash the manifest, compare, check `mask_id` ∈ `mask_bundle_ids`) still
decides ordering on any clocks. This analysis is recorded in `src/evaluation/masks.py`'s
docstring where 3.6 and G-05 will read it. This resolves nfr-design review Minor (a) riding
READY per the 2026-09-05 ruling.

## Proposed decision text for the owner to adopt (NOT a decision)

> **This section is a DRAFT for the owner's consideration. It has no authority. It becomes a
> decision only when the project decision owner writes it — adopted, edited, or replaced —
> into `evidence/DECISIONS.md` under the next free D-number (D-33, if still unallocated),
> dated on or after 2026-09-06. The developer does not write it there.**

```
## D-<n> — The three comparison-set memberships are FROZEN as configuration (R-106)

**Decision date:** <date ≥ 2026-09-06>. **Decided by:** the project decision owner under the
recorded authority equivalence, at the `evaluation-and-comparison` code-generation gate
(Q1 = A). **Authority:** Vision §2.4 (tiers 1–3), §8.4 (model table), §8.9 (matched-window
and matched-learned-model clauses); NFR-FAIR-01 / TC-16 (one comparison-wide mask per set);
TE §18.2/TC-03e (membership is a frozen scientific choice living in configuration);
GOV-2026-08-28-FD-01 Recommendation 19 (the third set).
**Raised by:** evaluation-and-comparison functional-design R-106, which proposed the three
sets and routed the confirmation to the gate.

**Decision.** Exactly three comparison sets are declared in `configs/experiment.yaml` under
`comparison_sets`, each with its own comparison-wide mask, never merged:

- primary — members {M-01, M-02, M-03, M-06, B-01}; model M-06; benchmarks
  [B-01, M-01, M-02, M-03] (5 members);
- gim — members {M-06, C-01}; model M-06; benchmarks [C-01] (2 members);
- tier3 — members {M-04, M-05, M-06}; model M-06; benchmarks [M-04, M-05] (3 members).

The mask builder checks passed predictions against the declared set EXACTLY (missing, extra,
duplicate, or any two sets merged — all refuse). A secondary comparator's availability can
never shrink the primary scored set, which is why gim and tier3 are separate sets.

**Limitation, recorded on the decision's face.** The §18.2 assignment of comparison-set
membership is Student + Supervisor. No supervisor signature artifact exists for this
confirmation; the ratification is the owner's under the recorded equivalence, exactly as
D-28 recorded for the scored window. The supervisor's countersignature remains owed at the
G-05 freeze, where the mask registry and the declared sets it was built from are hashed
into the frozen bundle.

**What is NOT decided.** No mask is built, no metric computed, no gate opened; G-05 and
G-06 remain Blocked; the memberships decide no model, threshold, seed, or scored window.
```

**If the owner declines**, the `comparison_sets` block transcribed by this pass loses its
confirmation basis and is removed on the owner's word; the mask builder then refuses
fail-closed naming the missing declaration (the Q1 = B posture), and every mask-dependent test
asserts refusals only.

## Honest limits — nothing below is changed by this record

- **G-05 and G-06 remain `Blocked`.** No DEC read, no DEC metric, no mask freeze occurs in
  this pass; the DEC path is built and stops at `materialise_locked_partition`'s G-05
  signature guard and `open_restricted`'s door.
- **FR-P1-05-7 stays `Pending`** (row approved under D-32 on 2026-08-28, never run — NOT
  passed); **FR-P1-05-17 stays `UNTESTED`** (no acceptance row; the freeze-precedes-access
  ordering is the G-05 record's to produce). **WS-16, TA-11, TA-18 stay `Pending`.** Nothing
  in this pass discharges any acceptance row.
- **D-27 is UNREOPENED** (verified 2026-09-06: `evidence/DECISIONS.md` ends at D-32). The
  R-103 `src/evaluation` → `src/features` import edge stays unauthorised; **no such import,
  direct or transitive, exists in `src/evaluation`** after this pass, and `ABL-DIFF` keeps
  refusing naming D-27 exactly as `src/models/train.py` built it.
- **No supervisor signature artifact exists or is claimed** for the membership confirmation;
  the proposed D-number records that limitation.
- **BLK-08's mechanism limb stays open** (the gate's adoption ruling and the edge's
  authorisation both remain outside this unit); BLK-03/BLK-04/BLK-09's evidence limbs are
  untouched.
- The R-85…R-89 rule-numbering gap remains **observed, not explained** (a standing gate item).
- `statistical-inference`'s R-113 precondition 2 correction (`PartitionError` on a
  `partition_id` mismatch) remains **its owner's**, raised at the gate, not made here.
- The `project.md` § Mandated GIM-disclosure wording correction remains **owed at the §13
  learnings ritual** (human-gated); no memory file is edited by this pass.
- **No commit is made by this pass.** The governed commit is the student's act and cites
  **D-27, D-28, D-31, D-32** as touched context, plus the new D-number if adopted. **No
  governed commit before this record and the adopted/declined D-number ruling exist.**

## Propagation sweep (`CHANGE_RECORD_PROCEDURE.md`)

This record changes one governed-artifact content (`configs/experiment.yaml`: the absent
`comparison_sets` block is added; **no existing key is touched** — `folds`, `embargo_hours`,
`estimand`, `bootstrap`, `practical_relevance_threshold`, `grids`, `models`, `ablations` all
keep their current values) and one sibling module (`src/data/locked_test.py`: two additive
optional fields + population logic). No count, ID range or cardinality asserted elsewhere is
changed: rules stay 10 (R-103…R-112), negative controls stay 31 ((2) vacated), entities stay
8, amendments owed stay 7 across 5 units, the member counts 5 / 2 / 3 are NEW facts introduced
by this record, previously asserted only as the R-106 proposal. Sites that state the
memberships as "proposed, not frozen" (`functional-design/*.md`, `nfr-design/*.md` of this
unit) are **not edited** — completed-stage artifacts under receipts; their statements were
true when written and are superseded as to status by this record, exactly the disposition
`CR-2026-09-06-BLK03-CONFIRMATORY-CONTRACT` applied to the BLK-03 banners.
