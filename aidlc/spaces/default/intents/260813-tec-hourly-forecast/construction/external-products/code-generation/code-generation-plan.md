# Code Generation Plan — `external-products`

**Unit** `external-products` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (W-1…W-9; R-54…R-61; carried Finding 9), `nfr-design/security-design.md` (SD-E-00…SD-E-07), `nfr-design/logical-components.md`, `unit-of-work.md` §6, `requirements.md`. Answers: Q1=A (BenchmarkError + ComparatorError declared; DriverError stays out) — receipted.
**Authority**: G-09 signed (D-31). `src/external/{spaceweather,iri,gim}.py` + `scripts/04_build_external_products.py` all §12/unit-of-work-named — no naming amendment. `tests/test_iri_denial.py` is §12-mandated.

## Ground rules binding every step

Same as prior units (3.11 target; in-place edits; no scientific constant in source; no credential values; two-tier errors; docstrings; ruff clean; negative control per hard rule; nothing discharged; smoke ≠ governed; **no git commit**). Plus this unit's own: **no IRI benchmark and no GIM comparator is generated** (R-59 validation not run; Q-15 UNSET — both refusals are the deliverable); no `iri_*` value, IRI-derived residual, or IRI-computed value reaches any training/inference surface; `tests/*` is NOT allowlisted for IRI/GIM imports (the blanket-row discrepancy stays gate-routed); F10.7 mean is trailing, never centered; no backfill from future final values; Dst grades never mixed; time-indexed drivers only; membership by record timestamps.

## Recorded input — nfr-design review Minors (human ruling 2026-09-05)

This unit's terminal READY (iteration 2) followed seven reviewer passes and two owner-directed redos; its record-only Minors (banner divergence-count undercount; the disclosed evidentiary-not-cryptographic framing of the provenance flip) are listed here and quoted at the stage gate. No code step derives from them.

## Steps

- [x] **Step 1 — Exceptions in `src/data/config.py` (in place)** [Q1=A + nfr-design Q2=A; SD-E-02]
  Declare `ImportBoundaryError`, `FeatureAvailabilityError`, `BenchmarkError`, `ComparatorError` — IntegrityError subclasses, `__all__`, any-future clause. `ImportBoundaryError`'s expectation names the full reachability CHAIN, not the endpoint. **`DriverError` NOT declared** (contested; declaration waits on the domain-entities reconciliation — recorded in module docstring).

- [x] **Step 2 — `src/external/spaceweather.py` (new)** [FR-P1-04-3/WS-11 subject, FR-P1-04-4, FR-P1-04-17/TA-36 subject, REQ-ENG-9; SD-E-06; W-5/W-8]
  Driver-series builders: availability lags (Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 previous-day observed + **trailing** 81-day mean ending at the safe-lagged day — proven as a shifted-input property test); carry-forward ≤ 3 h then row excluded (injected four-hour-gap control); one value per epoch identical across cells (a per-cell join shape is refused); Kyoto Dst single recorded release grade per series, diagnostic-only flag; no backfill from future final values; four provenance fields per series on the manifest (`release_status`, `retrieval_date`, full product identity incl. version suffix, `sha256`) with the bounded reanalysed-value consistency check (declared-status-only for F10.7/Dst — never reported as closed); F10.7 outage window never imputed; `carry_forward_composition` TBD in `features.yaml` → `FeatureAvailabilityError` and stop (D-21/G-04); alignment failures raise the existing `AlignmentError`.

- [x] **Step 3 — `src/external/iri.py` (new)** [FR-P1-04-15, FR-P1-04-9 partial; SD-E-04; R-59; W-6]
  Benchmark gate: generation **refuses without a passing pre-declared validation report** (`BenchmarkError` naming report + missing pass); tolerance's recorded timestamp must **precede** the comparison (ordering evidence class); report content asserted **field by field** (pinned package/version, model switches, topside, 2000 km ceiling, units, drivers with no-future-centering confirmation, 5–10 official-interface samples, predeclared tolerance); on failure the implementation is never silently switched (R-59); benchmark drivers' availability obligations stated against the frozen matrix (D-25 carried AS STANDING — the §15.2 amendment is NOT treated as granted). `iricore` import deferred inside the gated path (package absent here; generation blocked regardless). **No benchmark is generated.**

- [x] **Step 4 — `src/external/gim.py` (new)** [FR-P1-04-9/WS-09 subject, FR-P1-04-18; SD-E-05; W-7]
  Comparator: **refuses while Q-15's interpolation rule is UNSET** (§18.2 Student choice — zero-TBD-preflight shape); hand-check timestamp asserted to precede generation; the map-product-to-map-product limitation AND the spatial-representativeness mismatch emitted **by the reporting path itself**; no-tuning grep-class check over `gim.py` (outside-tuning residual stays open, named); `gim_network_overlap_flag` disclosure keyed to a comparison artifact existing (mandatory whatever the result; audit has not run — no independence claim). **No comparator is generated.**

- [x] **Step 5 — Provenance stamps + SD-E-07 refusal** [SD-E-03 producing half; SEC-E-05]
  Every value `04_build_external_products.py` writes carries a provenance stamp (the flipped default's producing half — evidentiary, never described as cryptographic); byte-identical re-run rule adopted unchanged from acquisition's SEC-A-02 contract (divergence records both identities + both hashes, refuses overwrite), recorded identity includes version/issue designation.

- [x] **Step 6 — `scripts/04_build_external_products.py` (new)** [W-8; §12/§13.2 conventions]
  Position 04; six-step entry (`ensure_process_determinism` first; `assert_no_raw_fields` before first write); orchestrates Steps 2–5; registry rows via foundation's writer; **`audit_ec1_drivers.py` logic migrated in** — the `:184` unconditional `return 0` closed onto the two-tier posture (missing months = machine-readable manifest field naming WHICH months, non-fatal; hash mismatch terminates naming file + expectation; both injections tested, opposite outcomes); original script untouched this run (retirement is a gate item); all outputs through `guard_egress`.

- [x] **Step 7 — `tests/test_iri_denial.py` (new, §12-mandated) — the largest open item closed** [FR-P1-04-1, NFR-IRI-01/WS-10/TA-07 subjects; SD-E-01, SD-E-03]
  The ordered-switch containment check: reports `skipped` (never `passed`) with a **structured skip reason** when either limb is unpopulated (target limb: `iri.py`/`gim.py` existence; risk-surface limb: candidate-importer cardinality); candidate-importer set defined **by complement** of TE §12's two allowlisted paths over `.py` files AND `.ipynb` code cells (ast-parsed); walk includes `__init__.py`, count subtracts it; transitive reachability; provenance limb — **absent provenance fails** (present-and-not-IRI admits). Negative controls: WS-10's injected `iri_*` field caught; an injected direct import caught; an injected transitive import caught; a stripped provenance stamp caught; today's live state pinned (clause-4 `skipped` naming the target limb over the real candidate set).

- [x] **Step 8 — Driver/comparator tests (`tests/test_external_drivers.py` new)** — every Step 2–6 refusal negative-controlled (centered-mean variant caught by the shift property; 4h gap excluded; per-cell join refused; mixed grades refused; backfill refused; TBD composition stops; Q-15 refusal; ordering violations refuse; migrated exit-code both-injection pair).

- [x] **Step 9 — Full-suite smoke + lint** — green under 3.11.9 (smoke only); ruff clean on touched files.

- [x] **Step 10 — Governance records + stop before commit (student acts)**
  DRAFT `governance/CHANGE_RECORD_2026-09-05_R55_external_contracts.md` (one record: boundary-contract blocks for `spaceweather.py`, `iri.py`, `gim.py` — owed per R-55, applied only on owner approval). Gate-routed items restated: `tests/*` blanket row (owner discrepancy), foundation-preflight structured-skip dependency (FR-WS-7), provenance-default enlargement (features-and-splits' half unstated), `DriverError` reconciliation, D-25's ungranted amendment. Commit cites D-25, D-21 as touched context. **No governed commit before the records exist.**

## Out of scope

Generating the IRI benchmark or GIM comparator (blocked by design), deciding Q-15 or `carry_forward_composition` or the iricore configuration (freeze-gate/Student items), the network-overlap audit, `audit_ec1_drivers.py` deletion, features-and-splits' assertion half of the provenance contract, every acceptance-row discharge (WS-09, WS-10, WS-11, TA-07, TA-36 stay `Pending`; the 4 rowless requirements stay `UNTESTED`).
