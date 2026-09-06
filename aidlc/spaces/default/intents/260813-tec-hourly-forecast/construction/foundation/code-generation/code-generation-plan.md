# Code Generation Plan — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (W-5, W-6, W-8; R-05…R-20), `nfr-design/security-design.md` (SD-01…SD-06), `nfr-design/logical-components.md` (C-1…C-3), `unit-of-work.md` §1, `requirements.md`. Answers: Q1=A, Q2=A, Q3=A (receipted).
**Authority to create modules**: G-09 signed (D-31) — signature opens the gate; its unmet preconditions are disclosed there and nothing in this plan claims them met.

## Ground rules binding every step

- Code goes to the workspace root; `src/data/config.py`, `src/data/release.py` exist — **modify in place**, never duplicate.
- Target **Python 3.11 exactly** (TS-01/TC-03d). The local 3.14.7 interpreter runs tests as smoke evidence only — never governed evidence.
- No scientific constant in source; configs only (TC-03e). No credential value read, logged, or persisted (SD-02). No path into `evidence/locked_test_restricted/` (SD-05). No machine path in a governed config (ADR-07).
- Two-tier error posture: integrity violations exit non-zero naming file + violated expectation; completeness shortfalls become machine-readable manifest fields.
- Every module/script docstring states purpose, inputs, re-run behaviour. `ruff` lint + format.
- Every hard rule ships with a **negative control** test proving the violation is caught (team practice).
- No `TBD — freeze gate` value is filled by convenience: TF pin excluded (Q3=A); unfrozen config fields carry the literal `TBD — freeze gate` sentinel for `assert_no_tbd` to catch.

## Recorded input — nfr-design review Minors (human ruling 2026-09-05)

Foundation's terminal READY review carries three **record-only** Minors: (1) provenance-banner redo-count drift between the two nfr-design artifacts, (2) one banner sentence's missing verb, (3) a placeholder review timestamp in a standing prior entry. None changes a design decision; no code step derives from them. Listed per `governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`; the review artifacts are standing records and are not edited.

## Steps

- [x] **Step 1 — Repository scaffold + tooling pins** [REQ-ENG-1, REQ-ENG-2, REQ-ENG-3, TC-06, TA-01, TA-02; SD-01; Q2=A, Q3=A]
  Create the §12 tree (six `src/` packages with `__init__.py`, `scripts/`, `notebooks/`, `tests/`, `tests/fixtures/`, `artifacts/`, `configs/`), `pyproject.toml` (project metadata, `requires-python == 3.11.*`, ruff lint+format config, pytest config), `requirements.txt` (pinned; **no TensorFlow**), `README.md`. Pin `gitleaks` version; add reviewed allowlist file (`.gitleaks.toml`) and pre-commit hook running gitleaks in diff mode + the critical test set (team practice Q7=D). Verify `.gitignore` credential deny-list (already present pre-first-commit precondition).

- [x] **Step 2 — Four governed configs** [TC-03e, §12, TA-23 subject; ADR-07; D-122]
  `configs/data.yaml`, `features.yaml`, `experiment.yaml`, `seeds.yaml`. Frozen values enter only from `evidence/DECISIONS.md` D-numbers (seeds D-122: dev 42, final {1337, 2024, 7}, bootstrap 20221201 — carried with its "supervisor sign-off pending at G-05" status); every unfrozen scientific value is the literal `TBD — freeze gate`. No machine paths.

- [x] **Step 3 — C-1 Resolve: extend `src/data/config.py` in place** [REQ-ENG-6, REQ-ENG-10, NFR-DET-01, SD-02, SD-06; W-8; R-05, R-06, R-14]
  `load_configs` (+ per-run snapshot + per-file SHA-256 hashes), `assert_no_tbd`, `assert_declared_sources_exist`, `seed_everything`, `ensure_process_determinism` (re-exec before any graph construction, R-05), `resolve_platform_roots` (exactly `kaggle`|`local`, else `PlatformError`; returns label + roots, never a credential value), credential **name** presence check failing early by name, eight-item environment-lock capture (requirements.txt hash + pip freeze; Python/OS/CPU/key libs; code commit; four config hashes; dataset+manifest versions; platform; recorded nondeterministic ops — empty list never claimed as proof, R-06).

- [x] **Step 4 — C-1 tests: `tests/test_determinism.py` (new, CR-2026-08-22-TE-AMEND authority) + config/resolve tests** [WS-17/TA-13 subjects]
  Negative controls: `assert_no_tbd` fires on a planted `TBD — freeze gate`; `PlatformError` on unknown platform; governed-config hash mismatch terminates naming file + expectation; lock capture is 8/8 complete.

- [x] **Step 5 — C-2 Registry writer: new `src/data/experiment_registry.py`** [FR-P1-05-13, NFR-AUD-01, TA-10/TA-21 subjects; SD-03; W-5, W-6; R-07, R-08, R-10, R-18, R-19, R-20; Q1=A]
  Twenty-column §13.4 schema asserted at write (R-18); append-only atomic writes that never read run history (R-08); closed status vocabulary — unknown status is a failure (R-07); `exploratory` derived in the writer, never caller-passed (R-20); `AccessRecord`/`RegistryEvent` orphan detection both ways on `run_id`, orphans reported never backfilled (R-19; the five pre-guard December orphans + Rec-31 unresolved access stay orphans); durability stamp "unverified on this platform" where semantics uncharacterised (Q3=B design); on integrity failure terminate naming file + expectation even when reporting fails (R-10).

- [x] **Step 6 — C-2 tests** [TA-10/TA-21 subjects]
  Negative controls: unknown status refused; write-time schema violation refused; no code path can locate/rewrite a prior row; orphan detected and reported, backfill impossible; durability stamp present on uncharacterised platform; failed/aborted runs remain visible with status + reason.

- [x] **Step 7 — C-3 Release writer: extend `src/data/release.py` in place** [SEC-F-06, TA-15; SD-04; R-11, R-13; D-29]
  §13.3 manifest (ten rows over fourteen fields: version, source manifest, SHA-256 hashes, schema, row counts, exclusions, fold/mask identifiers…), `dataset_version` = first 12 hex chars of `content_hash` (D-29) with verify-on-write uniqueness over the **single authoritative release root** (enumerating each release's recorded `content_hash`); **refuse when the root is unreachable** — never treat unreachable as empty; overwrite refusal (R-13); label never claimed never-reused (open encoding obligation stands).

- [x] **Step 8 — C-3 tests: extend `tests/test_release_hashes.py` in place** [TA-15 — currently NOT covered; this step is what makes it covered-by-test]
  Assert all §13.3 manifest fields present; negative controls: overwrite refused; unreachable release root refuses (not empty-population pass); hash collision at verify-on-write refused; mutation of a written release detected.

- [x] **Step 9 — TA-22 gate-scan wrapper** [REQ-ENG-6, FR-P1-01-10, NFR-SEC-01 subject; SD-01]
  Thin script/config so the history-inclusive gitleaks run emits SD-01's evidence contract: tool name + pinned version, commit range, scan scope (history/configs/logs/artifacts), result. Running it at a gate stays a human/governed act — nothing here claims TA-22 discharged.

- [x] **Step 10 — Test configuration + full-suite smoke run** [pytest config in `pyproject.toml`]
  Existing 6 test modules + new/extended ones all pass under the available interpreter; result recorded as smoke evidence only (3.14.7 ≠ governed 3.11 pin — stated in code-summary).

- [x] **Step 11 — Documentation** — docstrings per mandate, README (§12 layout, two platforms, CPU-only path, how to run suite), inline docs.

- [x] **Step 12 — Governance stop before commit (student acts, agent stops-and-reports)** [TE §18.3; team.md linking rule]
  Present for the owner to record: (a) TE §12 naming amendment for `src/data/experiment_registry.py` (config.py precedent), (b) D-number for SD-04's enumeration-surface decision (owed per security-design), (c) commit message citing D-29, D-122 and the amendment record. No governed commit before these exist.

## Out of scope for this unit

Stage scripts (`scripts/NN_*.py` belong to their owning units), `src/data/registry.py`/`reuse_registry.py` (`inventory-and-registry`), locked-test guard changes (`governance-guards`), fixture manifests (`fixtures-and-reproducibility`), any scientific computation. No acceptance row is claimed discharged: TA rows move only on governed evidence, and the governed 3.11 environment does not exist here.
