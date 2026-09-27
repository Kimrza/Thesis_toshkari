# Security Test Instructions

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent ·
**Security perspective:** aidlc-devsecops-agent
**Date:** 2026-09-24 · **Repository commit at authoring:** `41fd109`

Security in this project means four concrete things, each with an executable
check: **secrets stay out of the tree** (NFR-SEC-01, TE §10), **the locked
December test set stays inaccessible and every access is recorded**
(locked-test guard, §18.3 critical item 10), **prohibited data flows are
denied by tests** (IRI denial, import boundary), and **release artifacts
cannot be silently mutated** (TA-15). Sources: the units'
`code-generation-plan.md` / `code-summary.md` records (this stage's consumed
inputs), TE §10/§10.1, `team.md` § Deployment.

## Secret scanning and credential hygiene

| Mechanism | Where | How to run |
|---|---|---|
| gitleaks 8.18.4 (pinned as a comment in `requirements.txt` — a Go binary, not a pip package) | `scripts/gate_secret_scan.py`; `.githooks/pre-commit` (SD-01, Q2=A) | `python scripts/gate_secret_scan.py` |
| Credential deny-list | `.gitignore` lines 63–81 (`.env`, `.env.*`, `*.key`, `*.pem`, `*.p12`, `*.pfx`, `kaggle.json`, `.netrc`, `credentials*`, `.aws/credentials`, `id_rsa*`, …) | verified present at HEAD (team.md § Corrections, 2026-09-21) |
| Pre-commit hook | `.githooks/pre-commit` (file) + `core.hooksPath=.githooks` (activation) | file present at HEAD; `core.hooksPath` was UNSET on this clone until 2026-09-24, when it was activated under the Student's Rec 3 option-2 ruling (`GOV-2026-09-24-BT-01`) and re-verified: `git config --get core.hooksPath` → `.githooks`. The earlier "verified 2026-09-24 (Rec 35)" row here was false on this clone when written — prior commits ran ungated. |

Rules: credentials flow only through platform secret stores or environment
configuration excluded from version control; none may appear in a notebook,
source file, configuration snapshot, log, or registry note (TE §10;
NFR-SEC-01; construction-phase guardrail).

**Known open item, disclosed not hidden:** a personal email literal remains
in **git history** (one commit of the coverage notebook — Rec 39, measured
2026-09-24). A deny-list cannot reach history; the disposition is the
owner's, tracked in the governance thread.

## Locked-test custody (the sharpest security boundary here)

The locked December 2022 test set is the asset. Its guard is executable, not
procedural:

```bash
python -m pytest tests/test_locked_test_guard.py tests/test_phase_boundary.py \
  tests/test_merge_script_restricted_reads.py -q
```

- WS-18: the guard blocks December execution before G-05 and records access.
- Every read of `evidence/locked_test_restricted/` lands in the access log;
  test-mode accesses reconcile against an orphan whitelist.
- The pre-commit hook explicitly deselects the three restricted-root modules
  (Rec 30, **option 1** — deselect restricted readers from the commit set,
  retain them in the gate suite; citation corrected 2026-09-24 under Rec 12
  of `GOV-2026-09-24-BT-01`), so a commit does not silently touch December.
- **Owner-ruling status (corrected 2026-09-27, `GOV-2026-09-27-BT-02` R9/R2):**
  the locked-root **git-exposure** question was RULED 2026-09-24 — ACCEPTABLE,
  conditioned (`governance/CHANGE_RECORD_2026-09-24_locked_root_git_exposure_ruling.md`)
  — and the workflow is not hypothetical: it IS pushed and executing (49+ runs;
  the "if pushed" wording above is the `41fd109` state). Until 2026-09-27 every
  push materialised the locked month on GitHub runners AND ran the
  restricted-reader modules there, with access rows destroyed with the runner.
  As of 2026-09-27 those modules are deselected from `verify.yml`; checkout
  still materialises the tracked root. **What survives open:** Rec 47's
  Student + Supervisor authorization change record, the materialisation
  disposition, and the CI-runner access-record persistence residual — all
  consolidated in `governance/CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md`.

### Addendum 2026-09-24 — the SIXTH access purpose: `persistence_history` (D-68)

Added under Rec 7 of `GOV-2026-09-24-BT-01` (ruled option 1): the custody
section above predates D-68 and described a five-purpose world. Since
2026-09-24 a sixth, **live-wired**, post-G-05 December read purpose exists,
and an operator of this boundary must know it:

- **Purpose value**: `persistence_history` — the sixth member of
  `src/data/locked_test.py`'s `PURPOSES`. Sole emitter:
  `read_persistence_history_lookup` (same module).
- **What it reads**: 2022-12-01 target history ONLY (`PERSISTENCE_HISTORY_DAY`;
  rows outside that day are dropped from the output — an output bound), so
  M-01/M-02 persistence baselines can score the full disclosed 30-day set.
- **Who may call**: `PERSISTENCE_HISTORY_CALLERS = {M-01, M-02}` — any other
  `model_id` refuses by name.
- **When**: post-G-05 only — the same `verify_g05_signature` gate the DEC
  materialiser uses; fail-closed while G-05 is `Blocked` (its current state).
- **Kill switch**: `configs/experiment.yaml: persistence_history_lookup`
  (`authorized: true`, `decision: "D-68"` today). Flipping `authorized` back
  to `false` re-inerts the mechanism; absent/`TBD` on either field refuses.
- **Logging**: every call appends a real `AccessRecord` through
  `open_restricted` — `purpose="persistence_history"`,
  `performance_inspected=False`, `locked_test_accessed=True`, and (since
  Rec 10, same date) the **caller-supplied governed `run_id`**, so a G-06
  reviewer attributes each read by key. A row with this purpose is expected
  post-G-05 for M-01/M-02 runs and anomalous in every other circumstance.
- **Guard tests** (run with the custody set):
  `tests/test_locked_test_guard.py` — `test_ph_condition_i…_v` (one per
  enforced condition), `test_ph_run_id_is_caller_supplied_and_empty_refuses`,
  and `test_ph_the_real_config_reflects_its_actual_authorization_state`;
  wiring: `tests/test_models_smoke.py::test_persistence_history_augments_only_m01_m02_and_only_with_all_three_inputs`.

## Prohibited-flow denial tests (negative controls per rule)

```bash
python -m pytest tests/test_iri_denial.py tests/test_import_boundary.py \
  tests/test_feature_leakage_guards.py tests/test_acquisition_window.py -q
```

- `test_iri_denial.py` — WS-10's operational form: a deliberately injected
  `iri_*` field must be **rejected**. Note the widened control set after the
  `iri2016_t_plus_1_tecu` near-miss (a canonical name the old `iri_`-prefix
  filter missed — stage diary, 2026-09-20; **D-77**, adopted 2026-09-27,
  `evidence/DECISIONS.md`, closes the D-number this entry previously owed).
- `test_iri_denial.py` is ALSO the home of the **TA-07 containment scan**
  (`iri_gim_containment`): `src/external/iri.py` / `gim.py` never imported,
  directly or transitively, from `src/features/` or `src/models/` — the only
  permitted importers are TE §12's two paths — with injected direct/transitive/
  notebook-import negative controls.
- `test_import_boundary.py` — a DIFFERENT boundary, in the opposite direction:
  the December-audit surface (`src/data/*` + `scripts/01`) must not import
  `src.models` / `src.evaluation` (SEC-I-01 limb 2 / SD-I-01). *(Corrected
  2026-09-27, `GOV-2026-09-27-BT-02` R16: this document previously attributed
  the TA-07 iri/gim boundary to `test_import_boundary.py`, which does not test
  it — the module's own docstring names the December-audit boundary and claims
  no NFR-PHASE-01/TA-07 coverage. Two guard homes, two boundaries, stated per
  `nfr-design:c58`.)*
- `test_feature_leakage_guards.py` — availability lags, trailing-only F10.7,
  carry-forward ≤ 3 h, no backfill from future finals.
- `test_acquisition_window.py` — fold membership from record timestamps,
  never directory names (ML-07).

## Release integrity and reuse governance

```bash
python -m pytest tests/test_release_hashes.py tests/test_release_contract.py \
  tests/test_reuse_registry.py -q
```

- TA-15's mutation-protection: a release is write-protected or re-versioned,
  never overwritten (TE §13.3).
- `test_reuse_registry.py` — any reused third-party source has its full
  §10.1 register entry (provenance, immutable tag, licence/SPDX, reviewer,
  approval date) **before the code is used** (NFR-LIC-01, G-P2).

## What is deliberately absent

- No SAST/DAST service and no CI-hosted scanning — no CI service is
  authorised (team.md, Q7=D); the hook and the local gates are the
  mechanism. *(2026-09-27 note, `GOV-2026-09-27-BT-02` R2:
  `.github/workflows/verify.yml` exists and runs on GitHub as a NON-scientific
  verification surface under the Rec 47 bound — never gate evidence, never a
  governed platform. The team.md correction reconciling "No CI service is
  used" with this reality is drafted for the §13 learnings ritual at this
  stage's gate; the ritual is its only sanctioned write path.)*
- No auth/injection web testing — nothing serves requests.
- Supply-chain caution is live practice here: the 2026-09-13 vendored-pytest
  integrity finding (a planted one-line marker and an undeclared `import py`
  in a GitHub-served tarball) was halted, recorded, and never placed on the
  import path — the precedent to follow when PyPI is unreachable is
  conda-forge/repo.anaconda.com provisioning, not ad-hoc vendoring.
