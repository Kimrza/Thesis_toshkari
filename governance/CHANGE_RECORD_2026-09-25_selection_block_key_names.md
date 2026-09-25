# Change Record — `_read_selection_block` reads the owner-transcribed key names

**Date:** 2026-09-25
**Change ID:** CR-2026-09-25-SELECTION-KEYS
**Owning unit:** `models-and-baselines` (`src/models/train.py`, `tests/test_models_smoke.py`), edited
under that unit's frozen receipt on the Student's explicit instruction (`project.md`
`code-generation:c32`).
**Owner instruction (verbatim, 2026-09-25):** "Fix the key-name mismatch ... determine which side
is actually wrong ... Make the minimal fix on whichever side is actually wrong ... Don't touch
anything else in that function."
**Decision numbers relied on:** D-124 (selection rule), D-58 (declared baseline). No new decision
is made here; no scientific value moves.

## The defect

`src/models/train.py: _read_selection_block()` required `models.selection.simplicity_tolerance_fraction`
and `models.selection.declared_baseline`. The real `configs/experiment.yaml` carries neither:

- `models.selection.simplicity_margin: 0.01` — transcribed from D-124 under
  `CR-2026-09-21-RECONCILIATION` §2, which names this key explicitly;
- `models.declared_baseline_per_track: {all_tracks: "persistence"}` — a sibling of `selection`,
  filled by D-58 (register entry `evidence/DECISIONS.md`, Student freeze, supervisor
  countersignature stated 2026-09-21).

So `select_configuration()` raised `IntegrityError` ("`models.selection.simplicity_tolerance_fraction`:
absent or TBD") against the real config. Every selection test used a synthetic snapshot built with
the code's own names, so the real file was never read by a selection test and the mismatch was
invisible.

## Which side was wrong

The code. Its two key names were written by `models-and-baselines` code-generation while all three
fields were still `TBD — freeze gate` (that unit's `code-summary.md`: "`models.declared_baseline_per_track`,
`models.selection`, and `models.selected` all still read `TBD — freeze gate`"). No governed record —
functional design, domain entities, business rules, or change record — ever named
`simplicity_tolerance_fraction` or `selection.declared_baseline`; grepped across the unit's design
artifacts, zero hits. The config names come from the owner's transcription act, which is the
authoritative shape. Changing the config to match the code would have re-transcribed an owner act
by convenience (`project.md` § Forbidden).

## The change (minimal)

1. `_read_selection_block()`: reads `selection.simplicity_margin` (same TBD and non-negative-number
   checks as before) and `models.declared_baseline_per_track.all_tracks` (same TBD check). Nothing
   else in the function changed; the refusal for an absent/TBD `selection` block is byte-identical.
2. `select_configuration()`: the one line reading the tolerance now reads `simplicity_margin`.
   Required by (1); no other change.
3. `tests/test_models_smoke.py`: the one synthetic snapshot that supplied the retired names now
   supplies the transcribed ones.
4. New control `test_selection_reads_the_real_transcribed_config_keys`: reads the REAL
   `configs/experiment.yaml` through `select_configuration()`, and pins that the retired names and
   an absent baseline both refuse by name.

## Verification

- `tests/test_models_smoke.py`, governed env `tec-thesis-311` (Python 3.11.16), `PYTHONHASHSEED=0`:
  **72 tests, 71 passed, 0 failed, 1 skipped** (pre-existing skip: scikit-learn is installed, so
  its absence-refusal path is unreachable).
- **The control bites.** Run against HEAD's `train.py` (copied to a scratch tree), the new test
  fails with `IntegrityError: configs/experiment.yaml: models.selection.simplicity_tolerance_fraction:
  absent or TBD`.
- `ruff check` on both files: the same 4 findings before and after (all in the test module, all
  pre-existing, one line number shifted by the insertion); `train.py` has none.

## Not changed

`configs/experiment.yaml`; `models.selected`; `models.refit.epochs`; any other function. No commit
made by this session; committing is the Student's act.
