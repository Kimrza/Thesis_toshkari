# Proposal — resolving the missing release producer

**Date:** 2026-09-21 · **Status:** PROPOSED, nothing implemented · **Decision owner:** Student
(the stage contract), with §5's field-population questions Student + Supervisor

---

## 1. The defect, stated precisely

`src/data/release.py: write_release` is a complete, tested, TE §13.3-conformant release
writer. **No production code calls it.**

Verified 2026-09-21 by grep across `scripts/`, `src/`, `notebooks/` and `kaggle/`, printed
before assertion:

* callers of `write_release(`: `tests/test_release_contract.py`, `tests/test_release_hashes.py`
  — **tests only**;
* `scripts/` imports from `src.data.release`: `sha256_of_file` in four scripts, and nothing
  else;
* the Kaggle notebooks state their own boundary explicitly: *"no `write_release`, no
  `permitted_producers` registration"*, and *"the generated rows are the B-01 product
  candidate for the project's release path, **not a release**"*.

Meanwhile **two** stages consume releases:

* `scripts/01_inventory_and_registry.py` — reports `release_manifests_found: 0` and completes;
* `scripts/02_standardize_prepared_target.py` — **refuses**: *"no released provider input
  exists under the release root; the standardization consumes releases by manifest and hash
  (R-44), never bare paths, and none has been produced — refusing rather than fabricating
  input."*

Both refusals are correct. The gap is that the producer was never wired to a stage, so the
Phase 1 sequence cannot advance past stage 01. This is the same shape the board recorded four
times at enforcement boundaries — a correct component with no production call site — here on
a producer rather than a guard.

## 2. What a release has to carry, so the options can be judged

`write_release` enforces TE §13.3 in full: `source_files` with its six per-file items,
`processing` with its seven Phase 1 keys, `row_counts` across its four axes,
`exclusions_qc_summary` with a reason and a count, and `dataset_version` **derived**
(D-29's 12-hex prefix of `content_hash`) and refused if the caller supplies it. R-13 refuses a
directory that already holds a release.

So whichever option is chosen, the producing stage must be able to state the provenance of its
inputs and the QC outcome of its own run. That is what makes the choice a real one.

## 3. Option A — stage 00 releases what it acquired *(recommended)*

`00_acquire_prepared_vtec.py` calls `write_release` for the provider rows it assembled, and
stages 01 and 02 consume it.

**For.** Provenance is strongest where the bytes enter the project: stage 00 is the only stage
that knows the source files, their hashes and their retrieval circumstances, which is exactly
`source_files`' six items. It matches the stage's own name in TE §7.0A. It needs no new stage
and no renumbering.

**Against.** D-52 ruled that stage 00 on a fixture run **READS the scope's verified derived
artifacts; no transport**. A release write is arguably "transport", so this option needs D-52
read as *"no transport of provider bytes"* rather than *"no writes at all"* — or a narrow
amendment saying so. **That reading is the one decision Option A turns on.**

## 4. Option B — stage 01 releases what it inventoried

`01_inventory_and_registry.py` already walks the release root, already computes hashes, and
already holds the source inventory (`artifacts/inventory/source_inventory.json`).

**For.** It touches no D-52 question. The inventory it already builds is most of
`source_files`. It is the stage whose `release_manifests_found: 0` currently names the gap.

**Against.** It makes one stage both producer and consumer of releases, which is the seam
R-44 draws — the inventory is supposed to *verify* releases by manifest and hash, and a stage
that writes the thing it verifies is a weaker check. It also puts release identity downstream
of acquisition, so a re-run of 01 over unchanged inputs must be proven to produce the identical
`dataset_version`, or the release becomes run-dependent.

## 5. Option C — a dedicated release step between 00 and 01

A new `00b_release_prepared_vtec.py` (or a `--release` mode on 00) whose only job is to turn
verified acquisition output into a release.

**For.** Cleanest separation: acquire, release, inventory, standardize. Neither D-52 nor R-44
is strained. The step is small and independently testable.

**Against.** It adds a stage to TE §13.2's numbered clean-run fence, which is a governed
sequence — the fence, `REPRODUCTION.md`, the fixture orchestrator's script list and
`test_clean_run.py`'s three-way comparison would all need the same amendment, and that fence is
compared for drift by test. A real but bounded amendment cost.

## 6. Option D — declare the fixture path release-free

Make stages 01 and 02 accept a **verified derived artifact** on a fixture run, as D-52 already
lets stage 00 do, and require releases only on a full-scale run.

**For.** Smallest change to the production contract; the fixture already has verified derived
artifacts with a `sha256_manifest.json`, and D-52 established exactly this precedent for
stage 00.

**Against.** It weakens R-44 (*"consumes releases by manifest and hash, never bare paths"*) on
precisely the path the walking skeleton is supposed to rehearse. The fixture would then never
exercise the release path, so WS-20's clean-run evidence would cover a sequence that differs
from the real one — which is what a walking skeleton exists to prevent. **I would not
recommend this** unless the fixtures are explicitly accepted as not rehearsing release
handling.

## 7. Recommendation

**Option A**, with D-52 read as prohibiting transport of provider bytes rather than all writes
— or Option C if you would rather amend the fence than the reading of D-52. Both keep R-44
intact on the fixture path, which Option D does not, and both put release identity where the
provenance actually is, which Option B does not.

## 8. What is needed to proceed, either way

1. **Your choice of option** (and, for A, the D-52 reading).
2. Whichever stage writes the release must populate TE §13.3's fields from real run facts —
   `source_files`' six items per file, `processing`' seven Phase 1 keys,
   `exclusions_qc_summary`' reason and count. None of these is a scientific constant, so they
   are implementation, not a freeze; but if any cannot be populated from what the stage
   actually knows, that is a second decision and I will bring it back rather than fill it.
3. No release will be fabricated to get past the refusal, and no existing evidence will be
   modified.
