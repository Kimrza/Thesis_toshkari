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

## Performed 2026-10-02 (cloud session): step 1 and step 2

- Step 1 is done. The manifest edit was applied to the `3a2550ee...031c` file: `status` is now `frozen`, `identity.freeze_citation` is now `{"decision": "D-90"}`, the CRLF / indent-2 / sorted-keys serialization is kept, and a parsed comparison shows no other field changed. The new SHA-256 is `355774957e023b86f98b34668ff373e045d3159924e965188cf9926d275e752e`.
- Step 2 is done. The sibling `fixture_manifest.sha256` has been written.
- Step 3 is NOT done. Appending D-90 to `evidence/DECISIONS.md` was refused by the session permission control, and project rule `code-generation:c31` makes the register the Student's. The proposed entry is below for the Student to append verbatim (CRLF, as the file uses).
- Steps 4 and 5 are pending. F7 `assert_freeze_record_agrees` will refuse until step 3 lands, by design. Step 5 needs (a) `tec-thesis-311` and (c) `g07-clean-run`, the laptop environments.

### Proposed D-90 entry

```markdown
## D-90 — `scientific_1month` fixture manifest: Q-31 freeze

**Decision date:** 2026-10-02. **Decided by:** the Student, the Q-31 owner (TE §18.2). On
2026-10-01 the Student pre-authorized this freeze "on the same terms as D-85, provided every
check passes" (`governance/closure/AUTONOMOUS_EXECUTION_PROGRESS.md`, Student rulings
2026-10-01, item 2). On 2026-10-02 the Student instructed the agent to perform the prepared act
(`governance/closure/PROPOSED_D-90_scientific_1month_freeze.md`). The agent performed the
two-field edit (`725b2bb`). **Supervisor approval:** none recorded for this freeze
specifically. Q-31 is Student-owned (team.md § Walking Skeleton).

**Source.** The manifest was composed from exactly the four P-S5 designated runs at code
`b357ec6`, under precommitment P-S5 (`governance/closure/PROGRESS_2026-10-01.md`):
- (a) `tec-thesis-311`: `walking-skeleton-scientific_1month-20261002T151259Z-0d0342c7` and
  `walking-skeleton-scientific_1month-20261002T152403Z-cbb18809` (the outputs run);
- (c) `g07-clean-run`, in a fresh clone: `walking-skeleton-scientific_1month-20261002T151800Z-57d1687c`
  and `walking-skeleton-scientific_1month-20261002T152642Z-fa0a06b5`.

Both plumbing_7day (D-88) receipts were re-verified at `b357ec6` and passed, in (a) and in (c).

**Promotion.** The cross-environment candidate was
`fixture_manifest.candidate_walking-skeleton-scientific_1month-20261002T152403Z-cbb18809+xenv.yaml`,
with candidate SHA-256 `3a2550eef04df9eced7195842ad6066cbe2eeae76b43f142bb6dbf621091031c`. It was
promoted at `promoted_at_utc` `20261002T153643Z`. The previous installation is preserved as
`fixture_manifest.superseded_20261002T153643Z.yaml`. Exactly two fields were then changed:
`status` is now `frozen`, and `identity.freeze_citation` is now `{"decision": "D-90"}`. The
serialization is unchanged: JSON with indent 2, sorted keys, and CRLF line endings. A parsed
comparison confirms that no other field differs.

**Identity change (Student ruling, 2026-10-02).** FIX-MAR-FOLD-02 is shifted by one day. It
trains on 03-01..03-20, with validation from 03-21, giving 10 scored days (240 h: ten 24 h
blocks, five 48 h blocks). Reason: the earlier scored range [03-23, 04-01) is 216 h, which the
predeclared 48 h sensitivity (TE §13.6) cannot tile, and R-115 refuses partial blocks
(Rehearsal 5). The protocol is unchanged. Code `f619d69`.

**Measured values.**
- Runtime in `tec-thesis-311`: 650.22 to 659.92 s.
- Runtime in `g07-clean-run`: 488.36 to 498.15 s.
- Storage, pooled: 10,332,588 to 11,464,573 bytes.
- `widening_guard_cpu` max: 0.234 s.
- Planted-correlation recovery deviation: 0.0.
- `y_hat` cross-environment tolerance: 0.0022459 TECU over 12,681 elements.

The determinism precondition held in both legs. The manifest contains 0 `TBD`.

**Condition carried forward (as D-88).** These runtime ranges were measured under the
Performance power profile. A run under another profile is expected to fall outside them, and
that is an environmental runtime failure, recorded as such.

**Evidence class.** Fixture evidence on March 2022 only. D-14's limitation clauses apply: March
is an equinox month, is not representative of December, and no fixture result may be read as
evidence about December behaviour. The DATA-07 caveat in the manifest identity applies.

fixture_manifest_sha256: `355774957e023b86f98b34668ff373e045d3159924e965188cf9926d275e752e`

**Effect on leakage / uncertainty / comparability / claim.**
- Leakage: none.
- Uncertainty: none.
- Comparability: FIX-MAR-FOLD-02's scored window changes, as stated above.
- Claim: none.
```
