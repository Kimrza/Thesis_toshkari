# Change record — `CR-2026-09-20-FIXTURE-CANDIDATE-PATH`

**Date:** 2026-09-20 · **Author:** implementation session, under the project decision owner's
explicit authorization of the same date · **Status:** implemented, statically and by execution

---

## 1. The authorization, as given

> "I approve generating candidate manifests at a separate output path while preserving
> existing manifests and evidence. Make `--emit-candidate` capable of measuring the fixture
> and writing a new candidate without requiring an already-complete reference manifest. It
> must still enforce all other applicable prerequisites. Comparison mode must continue
> rejecting incomplete reference manifests. Prevent overwriting existing candidates or frozen
> evidence. Validate the candidate before any explicit promotion to the reference manifest;
> preserve the superseded file and provenance."

This record is the narrowly scoped contract amendment that authorization calls for. It changes
**where a measuring run writes** and **how a candidate reaches the reference path**. It changes
no scientific value, no fixture window, no acceptance criterion, and no freeze act.

## 2. The defect

`GOV-2026-09-20-CG-01`'s remediation of Recommendation 37 authored both fixture manifests as
**structural skeletons** — every measured quantity written as the literal `TBD — freeze gate`,
zero values invented. That was correct in itself and it deadlocked the fixture lifecycle,
because the two halves then refused each other:

```
# comparison run
run_walking_skeleton: preflight refusal: … fixture_manifest.yaml:
row_count_ranges.hourly_target: measured field carries no measuring_run_id …

# measuring run
run_walking_skeleton: aborted: … fixture_manifest.yaml:
a manifest already exists; it is preserved, never overwritten (R-134 obligation 3)
```

Neither refusal was wrong. The collision was: `write_candidate_manifest` enforced R-134
obligation 3 with a bare `path.exists()` check on the **reference** path, and that check cannot
tell a frozen, measured manifest — what the obligation exists to protect — from a
sentinel-only skeleton waiting to be replaced. Dispositions §5 item 8 was unperformable.

## 3. What changed

**`src/data/fixture_manifest.py`**

| Added | Contract |
|---|---|
| `candidate_path_for(workspace, fixture_id, run_id)` | `tests/fixtures/<id>/fixture_manifest.candidate_<run_id>.yaml` — one path per measuring run. Run ids are made filename-safe; an id with no usable character is refused, never collapsed onto a shared name. |
| `promote_candidate_manifest(candidate, manifest, *, promoted_by, authorization, now=None)` | The separate installation act. |
| `CANDIDATE_NAME_TEMPLATE`, `SUPERSEDED_NAME_TEMPLATE`, `PROMOTION_RECORD_NAME` | The three filename contracts. |

`validate_manifest_mapping` additionally **refuses any `TBD — freeze gate` value anywhere in a
manifest mapping**. This was found by the new tests, not carried from the finding: the existing
validator refused a measured field carrying *no* `measuring_run_id`, but a field carrying a run
id **and the sentinel as its value** loaded clean, so an unmeasured bound could have reached a
comparison run's runtime-range assertion. That hole is now closed for every caller.

**`scripts/run_walking_skeleton.py`**

* The blanket `.exists()` refusal on the reference path is removed from the measuring branch.
  The obligation is now met by construction: the candidate goes to its own per-run path, and
  `write_candidate_manifest` still refuses an existing file **there**.
* New `--promote-candidate <path> --promoted-by <who> --authorization <record>`. It runs no
  fixture, reads no config, and refuses to combine with `--emit-candidate`, so measuring and
  installing stay two separately authorised acts.

## 4. What did NOT change, deliberately

* **Comparison mode is untouched.** It still reads only `fixture_manifest.yaml`, still refuses a
  manifest that is not loadable, and now also refuses one carrying a sentinel.
* **Promotion never freezes.** The installed file keeps `status: candidate`. Writing `frozen`
  is R-134 obligation 2, the owner's Q-31 act, and no code path performs it.
* **Nothing is overwritten.** A second write at the same candidate path refuses; an existing
  reference manifest is renamed to `fixture_manifest.superseded_<utc>.yaml` before installation,
  and its `fixture_manifest.sha256` sibling travels with it so a freeze record never ends up
  describing a different file; a promotion whose preservation target already exists refuses
  rather than destroying the earlier preservation.
* **Provenance is recorded**, one append-only row per promotion in
  `fixture_manifest.promotions.jsonl`: the source candidate, its SHA-256, the file superseded,
  the actor, and the authorization.

## 5. Controls

Nine tests in `tests/test_clean_run.py`, all synthetic — no fixture was run, no measured value
invented, nothing under the real `tests/fixtures/` touched:

| Test | Limb |
|---|---|
| `test_candidate_path_is_per_run_and_is_not_the_reference_manifest` | the paths differ, per run |
| `test_candidate_run_id_is_made_filename_safe_and_an_empty_one_is_refused` | id sanitising; empty/unusable refused |
| `test_a_measuring_run_writes_its_candidate_while_a_skeleton_holds_the_reference_path` | **the deadlock control** — succeeds with a skeleton in place, and the skeleton is byte-unchanged |
| `test_a_second_write_at_the_same_candidate_path_is_still_refused` | R-134 ob. 3 preserved where it means something |
| `test_promotion_installs_the_candidate_preserves_the_old_manifest_and_records_it` | install + preserve + ledger + status stays `candidate` |
| `test_promotion_refuses_a_candidate_carrying_an_unmeasured_field` | negative control: a skeleton cannot be promoted either |
| `test_promotion_refuses_a_frozen_source_and_a_missing_one` | negative control: frozen never re-installed; nothing never promoted |
| `test_promotion_refuses_rather_than_overwriting_an_earlier_preservation` | negative control: preservation collision |
| `test_comparison_mode_still_refuses_an_incomplete_reference_manifest` | **the half that must not move** |

## 6. Effect, measured

The measuring run now proceeds past the manifest and into the stage sequence. With
`configs/data.yaml: target.identity` transcribed (`CR-2026-09-20-CONFIG-BLOCKS` §3),
`scripts/01_inventory_and_registry.py` **completed inside the fixture sequence**, and the
sequence stopped at the next genuine precondition, `configs/data.yaml: qc_operations`, which is
a supervisor freeze this session did not perform.

No fixture has been measured. Both real manifests remain the unchanged Recommendation 37
skeletons, and both Q-31 freeze acts remain the owner's.
