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

---

## Repair step added 2026-09-13 — owner ruling at the rejected stage gate

The project owner selected **Request Changes** at the `code-generation` approval gate on
2026-09-13 and ruled the standing receipts-gate item **"pass `--fixture-manifest`"**. That
lifts the reviewer receipt freeze and authorises the step below. This step is plan INPUT
for the repair pass, not a retroactive summary.

- [~] **Step 10 — WITHDRAWN 2026-09-13 as already-discharged. Not executed; nothing was
  edited.** See § "Step 10 withdrawal" below for the owner's ruling and the verified
  grounds. The step as written is preserved unchanged beneath it, because a withdrawn step
  is a record of what was asked, not a blank.

- [ ] ~~**Step 10 — Route the nine non-fixture smoke invocations through a fixture manifest**
  [TE §9.2; `CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` §6.2;
  `tests/test_external_drivers.py`]~~

  `tests/test_external_drivers.py` drives `scripts/04_build_external_products.py` in a
  subprocess via its `_run_script` helper. Derived 2026-09-13: **11** `_run_script(` call
  sites, of which two (`:839`, `:862`) already pass
  `--evidence-root evidence_fixture/...`, leaving **nine** non-fixture invocations. In a
  governed environment (pyyaml present) all nine now refuse at
  `require_receipts_for_snapshot` — no frozen manifest, no receipt — **before** reaching
  the path each test asserts. On this clone they fail earlier still, at `load_configs`
  (pyyaml absent), so the change is not observable here; it is certain elsewhere. §6.2
  routed the choice to this unit's owner, and the owner has now ruled.

  **The ruling: pass `--fixture-manifest` in the smoke invocations.** TE §9.2's receipts
  gate stays intact and is NOT narrowed — the rejected alternatives were rewriting the
  nine to expect the refusal (which would stop exercising the assertions those tests exist
  for) and narrowing Q5 (which would loosen a governance gate to suit a test harness).

  1. Read `src/data/fixture_manifest.py`, `src/data/fixture_gate.py` and
     `scripts/run_walking_skeleton.py` first to learn the real manifest shape and the exact
     `--fixture-manifest` argument contract, and confirm
     `scripts/04_build_external_products.py` accepts the argument.
  2. Route the nine through a fixture manifest that satisfies
     `require_receipts_for_snapshot`. A shared test helper, not nine copy-pasted blocks.
  3. The manifest the tests construct is **test control data, never governed evidence** —
     this module's own header already draws that distinction ("Injected gate-state values
     are CONTROL DATA, not governed evidence"). Say so where it is constructed and keep it
     inside the test's temporary workspace. No manifest is hand-authored into
     `tests/fixtures/`.
  4. `require_receipts_for_snapshot` itself is not weakened, bypassed, monkeypatched away
     or narrowed. If an invocation could only pass by weakening the gate, the executor
     STOPS and reports that invocation rather than doing it.
  5. Negative control: one test proving a non-fixture invocation **without** the manifest
     still refuses at the receipts gate. The gate is proven to still bite.

  **Out of scope for this step**: no `code-summary.md` edit (the orchestrator owns the
  artifact corrections in this pass), no write to `evidence/DECISIONS.md`, no commit, no
  change to `src/data/fixture_gate.py` or any fixture-owned module. No acceptance row is
  claimed discharged.

### Step 10 withdrawal — owner ruling 2026-09-13

**Ruling: Q5 = Choice B stands. Step 10 is withdrawn as already-discharged. Zero files
were modified by it.**

The step was written on the premise that §6.2's receipts-gate choice was still standing.
It was not, and the orchestrator failed to verify that before putting the scope to the
owner — `project.md` requires verifying every item of a proposed fix scope at its named
location before asking for a ruling, and an item verified only against the review that
raised it describes what was true when that review ran. Recorded here as the correction,
not smoothed over.

**What the record actually says**, verified 2026-09-13 at its named location:
`governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md` §0 row 1 records the
owner ruling **Q5 = Choice B** on 2026-09-10 — *"`tests/test_external_drivers.py`'s
subprocess tests now assert the TE §9.2 receipt-gate contract: a full-scale (non-fixture)
`04` invocation is not accepted merely because it produced outputs, and the gate fails
closed while no frozen-manifest/receipt chain exists"* — and §1 records why option 1 was
closed: *"Board Rec 2 foreclosed the first for this script — `04`'s declared window is the
full calendar year, so a fixture-flagged full audit refuses against every fixture scope."*

**Verified on disk**: `_assert_gate_fails_closed` occurs **12** times in
`tests/test_external_drivers.py` — one definition (`:789`) and **11** call sites, covering
every invocation. The negative control this step's item 5 asked for therefore already
exists; adding one would duplicate it.

**Count correction, derived and printed.** The step says "nine non-fixture invocations".
`grep -c "_run_script(" tests/test_external_drivers.py` = **12**, less the definition at
`:725` = **11 call sites** (`:839, :862, :877, :889, :985, :999, :1012, :1041, :1065,
:1079, :1101`). The two the step treats as already fixture-scoped pass `--evidence-root`,
which is an **input-path option** (`scripts/04_build_external_products.py:197-202`), not a
fixture scope — all 11 reach `require_receipts_for_snapshot`. The figure is **11, not
nine**.

**Correction, 2026-09-13, after the re-review returned a Major on this paragraph.** An
earlier version of this passage explained the discrepancy as "the nine traces to
CR-2026-09-07 §6.2 counting *test functions* (9 functions, 11 invocations, three functions
calling twice or in multi-line form)". **That derivation was invented and is false.**
Re-derived at `ed5808b` (the file's creation commit, 2026-09-06, predating CR §6.2) and at
HEAD: both show exactly **11 distinct test functions, each calling `_run_script` exactly
once** — no function ever calls it twice. CR-2026-09-07 §6.2's "nine" was simply a miscount
when written, not a functions-versus-invocations artefact. The corrected count of 11 and the
CRITICAL finding below are unaffected; what was wrong was the story told about where the
nine came from. Recorded rather than quietly replaced, because a confidently-stated invented
derivation inside a passage whose whole purpose is careful count derivation is exactly the
failure `project.md`'s count-derivation rule exists to catch — and this time the rule was
broken by the correction itself.

**Why option 1 is not merely superseded but unbuildable here** (independent of the
ruling): supplying `--fixture-manifest` is what *arms* the window check
(`04:306`), `_declared_data_window()` returns a hardcoded full calendar year
(`04:265-274`, from `_AUDIT_YEAR`, with no CLI narrowing), and
`assert_declared_window_within_scope` (`src/data/fixture_gate.py:209-251`) refuses unless
both endpoints sit inside the fixture scope's cited window — which is only ever 7 days or
1 month (`src/data/fixture_manifest.py:152-155`). Passing the flag successfully would
require fabricating a year-long scope citing no D-number and spanning the locked month.
The script's own docstring states the consequence: *"this FULL-YEAR declaration refuses
against any fixture scope — a full-scale invocation cannot ride the exemption on a
validating flag alone."*

### Gate finding, raised 2026-09-13 — CRITICAL, owner ruled "record, rule later"

**`scripts/04_build_external_products.py` cannot pass the walking-skeleton fixture ladder,
so the plumbing fixture's receipt can never be written.** Found while verifying the Step 10
withdrawal; appears recorded nowhere else.

Verified chain: `scripts/run_walking_skeleton.py:184` includes
`("04_build_external_products.py", 1)` in `PHASE1_SEQUENCE`; `build_phase1_commands`
(`:513-533`) appends `FIXTURE_SCOPE_OPTION` (`--fixture-manifest`, `:195`)
**unconditionally** at `:529` to every script in that sequence; `lifecycle_arguments`
returns `[]` for `04`, so nothing narrows its window. The flag therefore arms `04`'s
full-year declaration, which refuses at `assert_declared_window_within_scope`.

CR-2026-09-07 §6.1 gave `04` the `--fixture-manifest` option precisely to break a deadlock
("the plumbing fixture would refuse on the receipts only it can write"); §11.5's later
board-Rec-2 window binding **re-created that deadlock for `04` specifically**. As written,
the ladder cannot complete, so no receipt is ever written — and **WS-20 and TA-17 are
unreachable**, not merely `Pending`.

Three remedies, all owner decisions (TE §18.3 — stop and report, never choose a default):
**(a)** make `04`'s audit genuinely window-parameterised under a fixture scope — a real
change to a governed script's data scope, wanting its own D-number; **(b)** remove `04`
from the fixture ladder — `fixtures-and-reproducibility`'s call, and it changes what TE
§13.2's seven-invocation clean-run contract certifies; **(c)** accept that `04` cannot
participate until (a) happens. Making `_declared_data_window()` merely *report* the
scope's window while the audit still reads all twelve months (`_audit_dst` loops months
1-12; `_audit_f107` filters on `_AUDIT_YEAR`) would be a **false declaration** — worse
than the refusal — and is rejected outright rather than offered.

**The owner ruled on 2026-09-13: record it as a gate finding and rule later.** No code
moves on it in this pass.
