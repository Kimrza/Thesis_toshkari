# CR-2026-10-02-C01-GIM-BRIDGE — the `gim` comparison set's C-01 member is produced and its disclosure is checked per station

**Date:** 2026-10-02. **Author:** the agent, under the Student's mandate for autonomous closure
(Stage 2, scientific_1month). **Decision class:** implementation of an already-approved design.
No scientific value, tolerance, threshold, dataset definition or evaluation policy is changed.

## What failed

scientific_1month rehearsal 4 (undesignated, (a) `tec-thesis-311`, code `749d743`, log
`governance/closure/sci/rehearsal4.log`) aborted in stage 07:

> comparison set gim on partition FIX-MAR-FOLD-01: prediction(s) missing for declared member(s) ['C-01']

Root cause, verified in the repository:

1. **No producer of a C-01 prediction existed.** D-80 freezes the `gim` set as
   `{M-06, C-01}`, and the evaluation design states that "B-01 and C-01 are producible as
   `Prediction`s with `seed = None`". Stage 04 built `gim_comparator.parquet` but only B-01
   had a bridge into the `06` predictions run (`_emit_prediction_payload`). Plumbing never
   met the gap, because Fixture 1 skips the `gim` set evaluation (TE §15.3 reading,
   `07_evaluate_and_report.py`). Fixture 2 must run "the full benchmark join at evaluation
   time" (TE §15.3), so it reached the gap.
2. **The disclosure inputs were never wired.** `07` called `build_metrics_artifact` without
   `gim_overlap_audit` or `gim_comparator_provenance`. The fail-closed overlap disclosure
   (control 26) would therefore have refused the `gim` set even with a C-01 prediction
   present.
3. **The containment hash differs by station.** Stage 04 generates each station's
   comparator against the D-73 audit with the flag set to that station's own receiver
   presence (ARUC False, BSHM and NICO True). Each row's `overlap_audit_sha256` is the hash
   of that per-station record. A single-record containment check against the audit file
   would refuse ARUC.

## What changed

- `src/external/gim.py`:
  - `station_overlap_audit(audit, station)` is the one definition of the per-station record,
    now used by both the generator and the containment check.
  - `predictions_from_comparator_rows(...)` is the pure C-01 adapter, the counterpart of
    `iri.predictions_from_benchmark_rows`:
    - fold partitions only;
    - Option B window scoping (Student/Owner ruling 2026-09-26);
    - stamps required, never defaulted;
    - per-station containment evidence carried in `c01_generation_provenance`;
    - out-of-window rows counted, not silently dropped.
- `scripts/04_build_external_products.py`:
  - The generator calls `gim.station_overlap_audit`. It produces the same dict as the former
    inline code, so the same hashes.
  - `_emit_gim_prediction_payload` re-verifies the release against its own manifest (producing
    artifact and parquet SHA-256) and writes one write-once `C-01.json` per fold partition.
  - The fixture path calls it after building the release (TE §15.3 "C-01 sample generation").
  - The governed path reaches it through `--emit-gim-payload DIR --gim-release-dir PATH`.
  - Stamps: `phase_id` and `target_definition_id` come from `resolve_target_identity`, the
    same source the release manifest records. `source_id` is the release's
    producing-artifact identity `gim_comparator_C-01_2022`, which is provenance and not
    comparison identity (`src/evaluation/masks.py`). No new configuration value was
    introduced.
- `src/evaluation/masks.py`: `prediction_from_payload` keeps `c01_generation_provenance` on
  the frame's attributes.
- `src/evaluation/metrics.py`: `_gim_disclosure_block` checks containment per station when the
  provenance is per station.
  - Each station's recorded audit id, hash and flag must equal what
    `gim.station_overlap_audit` yields from the registered audit.
  - The disclosure states the network-level flag and every station's own flag.
  - The single-record path is unchanged.
- `scripts/07_evaluate_and_report.py`: for the `gim` set it reads the registered D-73 audit
  (`--gim-overlap-audit`, default the same file 04 generates against) and the C-01 provenance,
  and passes both to `build_metrics_artifact`.
- `tests/test_c01_prediction_adapter.py` (new) covers:
  - the envelope and the round trip through `prediction_from_payload`;
  - window scoping and row accounting;
  - refusal of REFIT and DEC;
  - integrity refusals;
  - per-station flags;
  - a negative control: a comparator generated against another audit, or a station whose
    flag differs, fails the disclosure.

## Effect

- **Plumbing:** the `gim` set is still skipped. One new file appears under
  `predictions/<partition>/C-01.json`. `predictions.parquet` is built from 06's own payload
  list, so no compared output is expected to change. Plumbing is re-verified at the new
  commit in both environments, because the change touches `src/` and `scripts/` (P-1 rule).
- **Leakage, uncertainty and claim:** none. C-01 stays an evaluation-time-only comparator; it
  is not a model input and no independence claim is made (D-73's flags are disclosed per
  station).
- **The knowledge graph** (`graphify-out/`) is stale for the touched files; no `graphify`
  CLI is installed on this clone.
