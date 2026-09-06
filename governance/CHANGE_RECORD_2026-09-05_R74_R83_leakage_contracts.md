# Change Record — R-74 and R-83 approved as the governed BLK-04 / BLK-09 contracts

**Record ID:** `CR-2026-09-05-R74-R83-LEAKAGE-CONTRACTS`
**Date:** 2026-09-05 (rulings receipted); record filed 2026-09-06 at the start of the
`features-and-splits` code-generation pass, BEFORE any module of that unit was written.
**Ruling:** Project decision owner, at the `features-and-splits` code-generation plan gate
(Q1 = A, Q2 = A, Q3 = A, Q4 = A, receipted in
`aidlc/spaces/default/intents/260813-tec-hourly-forecast/construction/features-and-splits/code-generation/code-generation-questions.md`).
**Change class:** Change-control acceptance of two functional-design contracts that were
authored at stage 3.1 and never separately approved — the acceptance
`GOV-2026-08-22-REM-01`'s exit ruling (`REM-02`, options 1 + 3) made a precondition of
exiting stage 3.1 for every affected unit. This record is that acceptance for **R-74**
(BLK-04) and **R-83** (BLK-09). It also records the **Q3 = A** accessor decision and the
**Q4 = A** deferral of BLK-08's mechanism limb.

## What was owed, and by whom

`GOV-2026-08-22-REM-01` `REM-02` reworded BLK-03/BLK-04 from entry conditions to **exit
conditions** on stage 3.1: an affected unit may enter `functional-design`, where the contract
is authored, but *"no affected unit may complete or exit 3.1 without its approved contract,
and no implementation may proceed while this blocker stands."* Every stage-3.1 artifact of
`features-and-splits` repeats *"approving this design is not its approval."*
`nfr-design/security-design.md` opens with *"No implementation is authorised while BLK-04
stands."* BLK-09 (added 2026-08-23) and BLK-08 (co-owned with `evaluation-and-comparison`)
carry the same exit-condition status.

The contracts themselves were fully authored at 3.1:

- **R-74** (`functional-design/business-rules.md`), rebuilt 2026-08-26 on ADR-11 and
  remediated 2026-08-28 on `GOV-2026-08-28-FD-01` Recommendations 4, 8 and 25.
- **R-83** (`functional-design/business-rules.md`), added 2026-08-28 on Recommendation 4
  (board option 1).

What was missing was the change-control act: an owner ruling that accepts them as the
governed cross-unit contracts, recorded in `governance/` before any commit.

## The rulings this record implements

### Q1 = A — R-74 is APPROVED as the governed BLK-04 cross-unit contract

The ADR-11 train-only fitting contract, exactly as R-74 states it (four elements):

1. **Allowed partitions.** A transform is fitted only on the named partition's training
   range **exactly** — `[partition.train_start, partition.train_end]`, both bounds fields
   of the `Partition` (R-83). Range **equality**, not containment.
2. **Fitting failure.** `fit_transforms(bundle, *, partition)` raises **`LeakageError`**
   when `bundle.spec.role != "train"`; when `bundle.transform_id is not None` (already
   transformed); or when the bundle's scored range is not exactly the partition's
   training range — in **either** direction, over-wide or strict subset. It raises
   **`PartitionError`** when `bundle.spec.partition_id != partition.partition_id`
   (a declared-identity disagreement, Recommendation 8's discriminating rule).
3. **Ownership of the fitted state.** `Transform` carries `transform_id` and
   `partition_id`; the identity is persisted with the data as `FeatureBundle.transform_id`
   and travels to `Prediction.partition_id`/`transform_id`.
4. **Applying failure.** `apply_transforms` does not exist. Transforms are applied only
   inside `build_features`, which raises `LeakageError` when
   `transform.partition_id != spec.partition_id`, with **exactly one** enumerated
   exception — `REFIT` → `DEC` under `spec.role == "score"` (the G-06 apply). The same
   pair under `role="train"` raises. Every other mismatched ordered pair of the six ids
   raises, asserted by enumeration (36 ordered pairs, 30 mismatched, 1 exempt, so 29 + 1
   = **30 raising conditions**). An untransformed bundle (`transform_id is None`) is never
   consumable: `fit_predict`, `06` and `07` raise on it.

**Also accepted with it:** the `PartitionError` reassignment of `fit_transforms`' id limb
(`component-methods.md:642-648` types it `LeakageError`; R-74 element 2 and
`domain-entities.md` § 10 type it `PartitionError`). R-83's § Amendments owed bundles this
reassignment with the `train_start` field as **one** consolidated amendment; this record is
that amendment's change-control trail.

### Q2 = A — R-83 is APPROVED: `Partition` states BOTH bounds

`Partition` gains **`train_start: date`** alongside `train_end`. Both bounds are read from
**`configs/data.yaml`** by `build_partitions(snapshot)` — never inferred from a January-1
convention, never hard-coded in `src/data/splits.py` (TC-03e), and **never derived from the
earliest row present** (which would make the range-equality check a tautology). The
negative control is the **strict-subset** fit: F4 (`2022-01-01`…`2022-10-31`) fitted on
`2022-02-01`…`2022-10-31` → `LeakageError`.

**What this record does NOT decide about R-83.** The calendar **values** — every
`train_start`, `train_end` and `validation_month` of R-80's six-row table, and
`DEC.train_end = 2022-11-30` — enter `configs/data.yaml` only at their freeze, under their
D-number, by their owner. They are TE §7.1-fixed text already; what is unfilled is the
config transcription. Until it lands, `build_partitions` **refuses**, naming
`data.partitions` as absent or `TBD — freeze gate` — a refusal, not a default.

### Q3 = A — the permitted-producer accessor is a SEPARATE LOADER

`load_permitted_producers(configs_dir)` reads `configs/features.yaml`'s
`permitted_producers` block. The approved, frozen `ConfigSnapshot` is **not amended** and
carries no new field. The `permitted_producers` block's **shape** is added to
`configs/features.yaml` with the literal `TBD — freeze gate` sentinel; the **list itself
stays unauthored** — it is assigned to nobody, and whether any entry encodes a scientific
choice (TC-03e) is decided when it is authored. While it is unset or incomplete,
`build_features` raises `LeakageError` naming WHICH §6.2 rows lack an entry and **no feature
matrix is produced**.

### Q4 = A — BLK-08's mechanism limb stays DEFERRED (D-27)

`Transform` is built with its fitted state and `transform_id` addressing. **No inverse
loading path (`load_inverse` / `Inverse`) is built and no `src/evaluation` → `src/features`
import edge is added** — D-27 states *"No import-boundary change is authorised by this
decision."* BLK-08's premise limb is closed for the primary path (the primary transform does
not touch the target; model output is raw TECU and needs no inverse); its mechanism limb
stays open, narrowed to `ABL-DIFF`. The R-84 (`load_inverse`/`Inverse`) versus R-103 half A
(`load_transform`/`Transform`) naming divergence is untouched here and is
`evaluation-and-comparison`'s gate item.

## Blocker-register consequences — ROUTED TO THE GATE, NOT APPLIED

The blocker register lives in `inception/units-generation/unit-of-work.md`, an approved
Inception artifact. `governance/CHANGE_RECORD_PROCEDURE.md` permits annotate-in-place only
with owner approval for the specific item, so the status updates below are **recorded here
and put to the owner at the code-generation gate**, not written into the register by this
pass:

| Blocker | Consequence of this record | Register action owed |
|---|---|---|
| **BLK-04** | Contract (R-74) approved. NFR-LEAK-01's **evidence** stays owed to the Supervisor at G-04/G-05; approval governs the mechanism, not the evidence | Annotate: contract approved 2026-09-05 (Q1 = A); status remains open on the evidence limb |
| **BLK-09** | Contract (R-83) approved; the field exists; the values enter at their freeze | Annotate: contract approved 2026-09-05 (Q2 = A) |
| **BLK-08** | Deferred per D-27 (Q4 = A); nothing changes | Annotate: defer confirmed 2026-09-05; mechanism limb narrowed to `ABL-DIFF`, open for both owners |

## Propagation sweep (`CHANGE_RECORD_PROCEDURE.md`)

This record amends a **status**, not a count or an enumeration: BLK-04's and BLK-09's
contracts move from *authored, unapproved* to *approved*. The superseded literal is the
phrase **"approving this design is not its approval"** (and its variants *"is not the
amendment's approval"*, *"is not that approval"*) as applied to R-74 and R-83.

Sites found (grep over the active intent's `construction/features-and-splits/` artifacts and
the sibling units that cite the contracts, 2026-09-06), with disposition:

| Site | Disposition |
|---|---|
| `construction/features-and-splits/functional-design/business-rules.md` (R-74 status box; R-83 § Status; § Assumptions BLK-04/BLK-09 bullets) | **Not edited** — completed-stage artifact under a frozen receipt; the statement was true when written. Superseded by this record as to status. Gate item: one annotate-in-place decision. |
| `construction/features-and-splits/functional-design/domain-entities.md` (§ 4 BLK-09 box; § 6; § Assumptions) | Same disposition. |
| `construction/features-and-splits/functional-design/business-logic-model.md` (W-3; W-5; W-10) | Same disposition. |
| `construction/features-and-splits/nfr-design/security-design.md` (banner: *"No implementation is authorised while BLK-04 stands"*; SD-F-03; SD-F-04) | Same disposition. |
| `construction/features-and-splits/nfr-design/logical-components.md` (banner; F-4 "Blocked") | Same disposition. |
| `construction/models-and-baselines/`, `evaluation-and-comparison/`, `statistical-inference/`, `regimes-diagnostics-reporting/`, `fixtures-and-reproducibility/` — "BLK-04 ↓ / BLK-09 ↓ inherited, open" | **Not edited** — terminal-READY under frozen receipts. Their inherited-open statements remain accurate on the evidence limb; the contract-approval fact is carried by this record. |
| `inception/units-generation/unit-of-work.md` blocker register (BLK-04 at `:333`, BLK-08 at `:842`, BLK-09 at `:857`/`:867`) | **Not edited** — approved Inception artifact; annotate-in-place routed to the gate (table above). |
| `aidlc/spaces/default/memory/*.md` | Swept; no site names BLK-04/BLK-09's approval status. Memory layers are never edited by a sweep. |

The **counts this record does not change**, stated so a later sweep does not re-derive them
against it: `build_partitions` returns **6**, the split manifest enumerates **5**, the
identity check has **30** raising conditions, § Amendments owed stays **7 across 5 units**
(this record is the change-control trail for the `features-and-splits` row of that table,
not an eighth amendment).

## What this record does NOT do

- It does **not** fill any `TBD — freeze gate` field, decide any scientific value, or
  transcribe R-80's calendar values into `configs/data.yaml`.
- It does **not** discharge any acceptance row: WS-10, WS-11, WS-12, WS-13, WS-18, TA-07,
  TA-08, TA-11, TA-18, TA-33, TA-34, TA-35, TA-36 all stay `Pending`; FR-P1-04-10 stays
  rowless.
- It does **not** author the permitted-producer list, decide its TC-03e classification, or
  assign it an owner — that assignment is a gate item.
- It does **not** close BLK-04's evidence limb (Supervisor, G-04/G-05), BLK-08's mechanism
  limb, or change any gate status. G-05, G-06, G-P1A, G-P2, G-P3A, G-P3C and G-07 are
  unaffected.
- It does **not** edit `component-methods.md`; this record IS the change-control trail the
  next revision of that contract cites for the `train_start` field and the
  `PartitionError` reassignment.
- **No December execution and no December content** were touched in building or testing
  the modules this record authorises. `materialise_locked_partition` refuses without a
  verifying G-05 signature, and no test supplies one against real December content.

## Evidence (created by the pass this record precedes)

- `src/data/splits.py` — `Partition` with both bounds; `build_partitions` reading
  `configs/data.yaml` and refusing while the block is absent or `TBD`;
  `materialise_locked_partition`'s signature guard.
- `src/features/transforms.py` — `fit_transforms` with R-74's raises in R-83's both-bounds
  form; `Transform` with `transform_id` + `partition_id` and no inverse surface (Q4 = A).
- `src/features/build.py` — the identity check with its one enumerated exception; the
  separate `load_permitted_producers` loader (Q3 = A) and the fail-closed refusal.
- `tests/test_train_only_transforms.py`, `tests/test_split_embargo.py` — the M10
  synthetic fixture over synthetic partition dates: the 30-condition enumeration, the
  strict-subset control, the `PartitionError`/`LeakageError` discrimination.
- Suite results are **smoke evidence only, never governed evidence** (the interpreter and
  environment limits are recorded in the code-generation summary).

## Owed list, carried by this record (recorded, not discharged)

- **The permitted-producer LIST** — assigned to nobody. Needs an owner and a TC-03e
  classification before `build_features` can produce anything.
- **R-80's calendar values into `configs/data.yaml`** — their owner's transcription at the
  split-boundary freeze, citing D-8/FR-P1-04-5 and D-28.
- **The fixture-manifest floating-point tolerance** (TE §15.2) — WS-13's value-level
  parity limb stops naming it until it is measured and frozen.
- **The evaluation-ROLE reading** of Vision §8.1's exactly-one-partition rule — carried to
  the gate, not adopted.
- **The governed commit** for this pass cites **D-27**, **D-28** and **D-10.3** as touched
  context. **No governed commit before this record exists** — it exists first, and the
  commit is the student's act, not the agent's.
