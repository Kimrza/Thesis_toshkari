# Code Generation Plan — `governance-guards`

**Unit** `governance-guards` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (W-8/W-8a, W-10, W-11; R-23, R-25, R-27, R-28 et al.), `nfr-design/security-design.md` (SD-G-00…SD-G-06, DISC-1, DISC-2), `unit-of-work.md` §2, `requirements.md`, application-design `component-methods.md` (`phase_contract` signatures). Summary confirmation receipted (no open questions — all decisions design-fixed).
**Authority**: G-09 signed (D-31, preconditions disclosed as unmet there). Foundation's pass (same Bolt) already built `src/data/experiment_registry.py`, `configs/`, `pyproject.toml`, `requirements.txt`.

## Ground rules binding every step

Same as foundation's plan (Python 3.11 target; modify existing files in place; no scientific constant in source; no credential values; two-tier error posture; docstrings with purpose/inputs/re-run behaviour; ruff clean; negative control per hard rule; no `TBD — freeze gate` filled; no acceptance row claimed; smoke runs never governed evidence; **no git commit** — governance stop). Plus this unit's own: the exempt list stays a source constant (SD-G-03, Q2=A — TC-03e does not reach it); no foundation-module edit beyond what the join requires (dependency runs governance-guards → foundation, never reverse).

## Recorded input — nfr-design review Minors (human ruling 2026-09-05)

Two scope-limited verification Minors ride this unit's terminal READY review: the seven-member exempt list was spot-checked rather than re-derived line-by-line, and `_read_guarded`'s defining files sat outside the reviewer's read scope. Addressed here in code: Step 5's test re-derives the exempt set exactly, and the code summary names `_read_guarded`'s homes.

## Steps

- [x] **Step 1 — `src/data/phase_contract.py` (new): run-time phase boundary** [FR-P1-03-2, REQ-ENG-5, FR-P1-06-1/2, NFR-PHASE-01, TA-27 subject; SD-G-05; R-23; component-methods signature]
  `assert_phase_boundary(phase: int, *, loaded_modules: Mapping[str, object]) -> None` — under Phase 1, any of the four `RAW_MODULES` (`src/gnss/rinex`, `calibration`, `target`, `verification`) present in `loaded_modules` raises `PhaseBoundaryError` (derives from `IntegrityError` imported from `src/data/config.py`). Boundary derived from module names, not caller input.

- [x] **Step 2 — `phase_contract.py`: produced-field limb** [SD-G-05; R-23]
  `assert_no_raw_fields(artifact_fields)` refusing DCB/STEC/mapping/satellite/arc field classes before a Phase 1 producing script writes. Completeness check enumerates the eight named producing scripts and asserts each calls it before first write — **gated on script existence** (none exists today; the test asserts over the existing subset and fails when a producing script appears without the call, never passes-by-vacuity silently: it records the empty population explicitly). Neither limb substitutes for the other (R-23) — independence test included.

- [x] **Step 3 — `phase_contract.py`: transition-manifest hash diff** [TE §7.0B, gate G-P3C, TA-27 hash-diff half]
  `diff_protected_hashes(manifest_a, manifest_b)` returning the named set of protected entries whose hashes differ; Phase 2 refusal semantics (any diff → refuse to train) expressed as a pure function + negative-control test. No manifest format invented beyond the design's protected-entry list; unknown/missing entries are integrity failures naming file + expectation.

- [x] **Step 4 — DISC-2 closure: AST literal scan** [SEC-G-04, nfr-requirements Q2=B; SD-G-04; R-27, R-28]
  Upgrade the restricted-root literal scan in `tests/test_locked_test_guard.py` from `"locked_test_restricted" in text` to AST-based with constant folding (string concatenation of literals folded before matching), catching `EVIDENCE_DIR / ("locked_test" + "_restricted")`. Negative control: a fixture snippet with the concatenated form must be caught; unparseable file = failure (R-27, shared helper both scans call). Notebooks' code cells included per the scan's declared width.

- [x] **Step 5 — Exempt-set exact re-derivation test** [SD-G-03; R-28; DISC-1; review-Minor closure]
  Test re-derives `RESTRICTED_LITERAL_EXEMPT_MODULES` membership exactly — the seven on-disk members (chokepoint + `scripts/merge_coverage_year.py` + five test modules) — failing on any addition or removal. DISC-1's six-vs-seven stays a gate item for the prose; the code asserts the true seven.

- [x] **Step 6 — `src/data/locked_test.py`: Q1=A fail-closed durability posture** [FR-P1-05-12/WS-18/TA-18 subject; SD-G-01]
  Verify the built properties (refuse ordinary paths; boundary from module location; failed log write aborts read; fsync; guard-stamped `logged_at_utc`) — no behavioural change to them. Implement, if absent, the refusal on a platform whose durability semantics are uncharacterised (characterised set is a module constant, empty ⇒ `kaggle` refused until W-6 step 8's measurement; `local` posture exactly as the design's scheduling note fixes it). Negative control: uncharacterised platform → `LockedTestError`, no read, no log row consumed.

- [x] **Step 7 — SD-G-02 join: orphan reconciliation wiring** [SEC-G-02, NFR-AUD-01 (TA-10/TA-21, rows owned elsewhere)]
  Integration test wiring `AccessRecord` (locked_test) ↔ `RegistryEvent` (foundation's `src/data/experiment_registry.py`, which owns the both-way reconciliation as a pure read): both-direction orphan detection runs; known pre-guard orphans (five December accesses + Rec-31 unresolved) supplied as `known_orphans`, reported never backfilled; byte-identity of both logs after reconciliation.

- [x] **Step 8 — `src/data/reuse_registry.py` (new) + `tests/test_reuse_registry.py` (new)** [FR-P1-06-3/4, NFR-LIC-01, TA-28 subject, gate G-P2; SD-G-06; §10.1]
  Register with the full §10.1 field set (reuse_id, repository URL, immutable commit/tag, upstream file+line/function, retrieval date, licence + SPDX ID, copied-vs-adapted, destination file, scientific purpose, modifications, tests, original citation, notice location, reviewer, approval date); registered-**before**-use enforced (a use without a complete row is a failure); append-safe; reimplementation-as-default posture in the docstring; AGPLv3 dependency stated, not resolved. Negative controls: incomplete row refused; use-before-registration caught.

- [x] **Step 9 — Documentation tests + docstrings** [Q7 rider]
  Documentation test asserting `tests/test_phase_boundary.py`'s subordinate-status docstring stays present (static scan = early-warning limb, does not discharge FR-P1-03-2). Docstrings on all new modules per mandate; code summary names `_read_guarded`'s defining files.

- [x] **Step 10 — Full-suite smoke run + lint** — whole suite green under bootstrapped 3.11.9 (smoke only), ruff clean on created/modified files.

- [x] **Step 11 — Governance stop before commit (student acts)** — add to foundation's owed list: TE §12 naming check for `src/data/phase_contract.py` (amendment if not already named, config.py precedent); commit citing D-15/D-18/D-31 as touched. No governed commit.

## Out of scope

The eight Phase 1 producing scripts (owned by their units), `src/data/registry.py` (inventory-and-registry), fixture manifests, any scientific computation, running the gate scan, and every acceptance-row discharge (WS-18, TA-18, TA-25, TA-27, TA-28 all stay `Pending`).

---

## Repair step added 2026-09-13 — owner ruling at the rejected stage gate

The project owner selected **Request Changes** at the `code-generation` approval gate on
2026-09-13 and ruled **Option 4** on the D-17 field-contract contradiction. That lifts the
reviewer receipt freeze and authorises the step below. This step is plan INPUT for the
repair pass, not a retroactive summary.

- [x] **Step 11 — D-17 field-contract reconciliation in this unit's two test modules**
  [D-17; R-66/R-67; `tests/test_phase_boundary.py`, `tests/test_phase_contract.py`]

  **Established by investigation 2026-09-13; not to be re-litigated in this step.**
  `evidence/DECISIONS.md` D-17's frozen table enumerates exactly **sixteen** target-row
  fields. `processor_qc_flags` is **not** a target-row column — it is a key inside the
  data-quality block (R-71 / NFR-DQ-01, W-3), built at `src/data/prepared.py:1304` as
  `{"aggregation_flags": [...], "not_applicable_classes": [...]}`. The authoritative
  in-code contract is `src/data/prepared.py:195` `D17_FIELDS` (16), already pinned by
  `tests/test_prepared_target_schema.py:196-202`, which asserts `processor_qc_flags` is
  not among them. The producer's header is
  `_TARGET_CSV_HEADER = (*D17_FIELDS, LINEAGE_CAVEAT_FIELD)` (`prepared.py:1324`) and the
  row guard at `prepared.py:791` permits `LINEAGE_CAVEAT_FIELD` (`"lineage_caveat"`) as
  the one field beyond the sixteen. The seventeen entered in commit `b844a4d`
  (2026-08-21) — the same commit that first wrote D-17's sixteen-row table — so it is a
  transcription slip against TE §6.1's data dictionary, not a competing decision, and no
  D-number is required to correct it.

  `tests/test_phase_boundary.py:95` `D17_TARGET_FIELDS` carries seventeen and is consumed
  as a **set equality in both directions** at `:253-256`, so it is stale twice: `missing`
  would flag `processor_qc_flags`, and `extra` would flag `lineage_caveat`. Fixing only
  the first would swap which assertion fires on the first real artifact.

  1. Remove `"processor_qc_flags"` from `D17_TARGET_FIELDS`, leaving sixteen. Correct its
     header comment — "Column names a Phase 1 target artifact may carry" misdescribes an
     exact contract — to match D-17 and `prepared.py:788` ("exactly sixteen fields — not
     fifteen, not seventeen"), stating that `processor_qc_flags` is a data-quality-block
     key (W-3), not a row field.
  2. In `test_target_artifact_conforms_to_d17_when_it_exists`, permit the declared caveat
     column in the `extra` computation, mirroring `prepared.py:791` exactly. The `missing`
     check is not weakened. Update the docstring to state D-17's sixteen plus the declared
     lineage-caveat column.
  3. `tests/test_phase_contract.py:61-63` — correct "the seventeen allowed columns" and
     align `D17_ALLOWED_FIELDS` to sixteen. That constant is only ever passed to
     `assert_no_raw_fields` as a happy-path control (`:147`, `:177`), so it carries no
     runtime contract effect; the comment states what it is actually for.
  4. Drift guard: assert `set(D17_TARGET_FIELDS) == set(prepared.D17_FIELDS)` so the
     test-side and producer-side constants cannot silently diverge again. If reaching
     `src/data/prepared.py` from that module would breach an import boundary or add a
     dependency the file does not already carry, the executor says so and follows the path
     that module already uses to reach source — never a new import invented silently.

  Every constant length touched is derived and printed, before and after.

  **Out of scope for this step**: no `code-summary.md` edit (the orchestrator owns the
  artifact corrections in this pass), no write to `evidence/DECISIONS.md`, no commit, no
  change to `src/data/prepared.py`. No acceptance row is claimed discharged.
