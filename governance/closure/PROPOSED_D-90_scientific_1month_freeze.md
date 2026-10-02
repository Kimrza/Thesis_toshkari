# Proposed D-90: `scientific_1month` Q-31 freeze (prepared 2026-10-02)

**Status: PREPARED, NOT PERFORMED.** The candidate has been promoted (installed as
`tests/fixtures/scientific_1month/fixture_manifest.yaml`, `status: candidate`; promotion row
`20261002T153643Z`, authorization D-90; the previous installation is preserved as
`fixture_manifest.superseded_20261002T153643Z.yaml`). The session's permission control then
refused the agent's edit of the governed manifest's `status` field, so the two freeze-edit
steps below are the Student's to perform, or to authorize through a permission rule.

The Student pre-authorized this freeze on 2026-10-01, on D-85's terms, "provided every check
passes" (see `AUTONOMOUS_EXECUTION_PROGRESS.md`, Student rulings item 2).

## Checks that passed

- **Runs.** The four P-S5 designated runs at code `b357ec6`, as recorded in
  `PROGRESS_2026-10-01.md`, under precommitment P-S5 and its designation note:
  - (a) SA2 `...151259Z-0d0342c7` and SA3 `...152403Z-cbb18809` (the outputs run);
  - (c) SC3 `...151800Z-57d1687c` and SC4 `...152642Z-fa0a06b5` (fresh clone `~/g07_clone_s4c`).
- **Plumbing receipts.** Both plumbing_7day (D-88) receipts were re-verified at `b357ec6` and
  passed, in (a) and in (c).
- **Per-leg candidates.** Both legs' candidates validated: (a) `...cbb18809.yaml`, (c) the copy in
  `ps5c_verification/`.
- **Cross-environment candidate.**
  `fixture_manifest.candidate_walking-skeleton-scientific_1month-20261002T152403Z-cbb18809+xenv.yaml`
  has SHA-256 `3a2550eef04df9eced7195842ad6066cbe2eeae76b43f142bb6dbf621091031c`, contains 0
  `TBD`, and passed schema validation. The determinism precondition held in both legs.
- **Measured values.**
  - runtime (a): 650.22-659.92 s; runtime (c): 488.36-498.15 s;
  - `widening_guard_cpu` max: 0.234 s;
  - planted-correlation recovery deviation: 0.0;
  - `y_hat` cross-environment tolerance: 0.0022459 TECU over 12,681 elements.

## The act (D-85 shape)

1. In `tests/fixtures/scientific_1month/fixture_manifest.yaml`, change exactly two fields:
   - `"status": "candidate"` becomes `"status": "frozen"`;
   - `identity.freeze_citation` becomes `{"decision": "D-90"}`.

   Keep the existing serialization: JSON with indent 2 and sorted keys, the same line endings.
   Check that every other byte is unchanged.
2. Write the sibling `fixture_manifest.sha256` with the new file's SHA-256.
3. Append D-90 to `evidence/DECISIONS.md`, in D-88's form, citing that SHA-256 as
   `fixture_manifest_sha256`. D-90 also records the identity change ruled on 2026-10-02:
   FIX-MAR-FOLD-02 is shifted one day, giving 10 scored days.
4. Run F7: `assert_freeze_record_agrees` and `assert_identity_agrees_with_decisions`.
5. Run the post-freeze verification of scientific_1month in (a), and in (c) from a fresh clone.
   Neither run uses `--emit-candidate`. Each writes the scientific receipt.

After step 1, the agent can do steps 2-5 if the permission is granted.
