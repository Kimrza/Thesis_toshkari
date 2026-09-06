# Code Generation Plan — `acquisition`

**Unit** `acquisition` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (W-1…W-9; R-30…R-43), `nfr-design/security-design.md` (SD-A-00…SD-A-04), `nfr-design/logical-components.md`, `unit-of-work.md` §3, `requirements.md`. Answers: Q1=A (R-33/BLK-07 amendment accepted; `write_restricted` built), Q2=A (new `src/data/acquisition.py`) — receipted.
**Authority**: G-09 signed (D-31). Foundation + governance-guards passes already landed `configs/`, pins, `experiment_registry.py`, `phase_contract.py`, AST literal scan, Q1=A platform refusal.

## Ground rules binding every step

Same as prior units (3.11 target; in-place edits; no scientific constant in source; no credential values; two-tier errors; docstrings; ruff clean; negative control per hard rule; nothing discharged; smoke ≠ governed evidence; **no git commit**). Plus this unit's own: **no acquisition run may touch calendar 2022-12 while BLK-07 stands** — nothing in this run executes a December read or write; the D-144 notebook stays self-contained (imports nothing from `src/`); credentials reach the provider client via foundation's resolution only; membership from record timestamps only (R-31).

## Recorded input — nfr-design review Minors (human ruling 2026-09-05)

Two record-only Minors ride this unit's terminal READY review: a missing prior-review receipt in the artifact (restored by the review section itself) and one prospective-versus-remedial framing note around the notebook. Neither changes a design decision; no code step derives from them.

## Operational values proposed here (not scientific constants; recorded in the run record per SD-A-01)

- Retry: max **5** attempts per file; exponential backoff base **1 s**, factor **2**, cap **60 s**, full jitter.
- Per-request timeout: **60 s** connect+read.
- All three recorded in the run record and the request manifest per retrieval, so behaviour is reconstructible.

## Steps

- [x] **Step 1 — `src/data/acquisition.py` (new): redaction serializer** [REQ-ENG-13/TA-16 subject, FR-P1-01-10/NFR-SEC-01 supporting; SD-A-02; R-39; W-9; Q2=A]
  One declared serializer every manifest/log/notebook-output value passes through: signed request URLs and auth headers **refused unconditionally** (structural detection); everything else through an entropy/prefix heuristic that **blocks and names what it matched**; `CredentialEgressError` terminates (integrity tier, `aborted` row through the `IntegrityError` catch); allowlist file as a review surface (never grown to silence a failure — documented). Negative controls: token-shaped value refused; signed URL refused even when allowlisted-shaped; legit hash/UUID passes via allowlist.

- [x] **Step 2 — `acquisition.py`: bounded-retry retrieval client** [FR-P1-00-1/TA-31, FR-P1-01-1/TA-32 subjects; SD-A-01; TS-A-01/03; §8.1 provider terms]
  Bounded retry with backoff on transient transport failure (values above), resumption where provider supports it, **completeness check BEFORE hash** (partial file never promoted: target absent or explicitly `incomplete` in the manifest — never a short file that looks whole); re-run recomputes SHA-256 and on difference **records the divergence (both provider filenames incl. version suffixes, both hashes) and refuses to overwrite** (SEC-A-02). Rate bounded per provider terms. Negative controls: truncated stream never yields a manifest row with a hash; divergent re-run refuses overwrite and records both.

- [x] **Step 3 — `acquisition.py`: manifest writers** [FR-P1-01-2…4, FR-P1-01-5/7/8/9/11 subjects; SD-A-04; R-34, R-36, R-37, R-40, R-41, R-42; W-3, W-4]
  `request_manifest.json` + `sha256_manifest.json` writers: full provider filename incl. version suffix, retrieval date, SHA-256 per provider file; version-suffix mismatch recorded at retrieval and **refused at release**; driver rows carry a **release-grade field** (Kyoto Dst grades never mixed within one series; no backfill from future final values); gaps stored as explicit NaN (no interpolation/smoothing/fill at acquisition — injected-gap negative control); derived multi-month release either re-merges or carries a D-number re-pointing provenance (R-42, FULL's notice contract). All output values pass through Step 1's serializer.

- [x] **Step 4 — `write_restricted` in `src/data/locked_test.py`** [FR-P1-01-6/TA-08 subject; SD-A-03; R-33; Q1=A change-control acceptance]
  Sibling of `open_restricted`: **logs durably first (shared `_append_and_flush`), then writes**; boundary derived from the module's own location; refuses ordinary paths; same Q1=A uncharacterised-platform refusal; `AccessRecord.purpose` field extension. Exempt list STAYS at seven (no new literal holder — the writer lives in the module that already names the root). Negative controls: failed log append aborts the write (no mutation without record); ordinary path refused; uncharacterised platform refused. **No test or fixture touches `evidence/locked_test_restricted/` or any December content** — tmp_path roots only, monkeypatched boundary via the module's own supported test seams.

- [x] **Step 5 — `scripts/00_acquire_prepared_vtec.py` (new)** [W-1; §12/§13.2 conventions; producing-script contract]
  `NN_verb_noun` position 00; takes `--config configs/`; `main()` opens with `ensure_process_determinism`; six-step stage entry contract (load_configs, assert_no_tbd, resolve_platform_roots, assert_phase_boundary, credential-name presence); calls `assert_no_raw_fields` before first write (governance-guards' completeness test starts checking it the moment this file exists); orchestrates Steps 1–3; run record via foundation's registry writer; **December excluded by record-date predicate; no restricted path constructed**. Two-tier error posture; `audit_ec1_drivers.py:184`-class gap not reproduced (missing months are machine-readable manifest fields, non-zero data-loss exits only on integrity violations).

- [x] **Step 6 — Pre-commit hook: notebook saved-output refusal** [SD-A-02 limb 2, Q3=A]
  Extend `.githooks/pre-commit`: a staged `.ipynb` carrying non-empty `outputs`/`execution_count` fails closed with a clear message (clear-and-recommit); no auto-stripping. Negative control via hook-logic test (hook body factored into a testable helper or tested via subprocess on a fixture notebook).

- [x] **Step 7 — Tests: `tests/test_acquisition.py` (new) + `test_acquisition_window.py` kept green** — negative controls named in Steps 1–4 + R-31 record-date membership reaffirmed; existing suite untouched and green.

- [x] **Step 8 — Full-suite smoke run + lint** — suite green under 3.11.9 (smoke only); ruff clean on created/modified files.

- [x] **Step 9 — Governance records + stop before commit (student acts)**
  Write `governance/CHANGE_RECORD_2026-09-05_R33_write_restricted.md` (the Q1=A acceptance: interface amendment to `locked_test.py` — `write_restricted`, shared `_append_and_flush`, `AccessRecord.purpose` — citing R-33/BLK-07 and this ruling). Owed list grows: TE §12 naming amendment for `src/data/acquisition.py` (third this Bolt); commit citing D-144, D-15, D-5/D-10.2 as touched. **No governed commit before the records exist.** BLK-07 closure itself remains a 3.1-owned contract decision — this run builds the mechanism, not the closure.

## Out of scope

Any December read/write or FULL re-verification run (BLK-07), the re-acquisition itself (deferred work, DATA-07 obligations recorded), `merge_coverage_year.py` migration (inventory-and-registry's), `audit_ec1_drivers.py` migration (external-products'), notebook rewrite (D-144 approved as-is), the Madrigal-identity NFR-SEC-01 conflict (supervisor's), every acceptance-row discharge (TA-16, TA-31, TA-32, TA-08, TA-15 stay `Pending`; the 7 rowless requirements stay `UNTESTED`).
