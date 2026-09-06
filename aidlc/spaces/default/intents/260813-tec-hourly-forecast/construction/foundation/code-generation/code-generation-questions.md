# Code Generation Questions — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`

Construction questions are exceptional, not routine. The three below are the
genuine gaps the design artifacts leave open at implementation time — each is a
§18.3 stop-and-report point or a repository-tooling decision the nfr-design
stage explicitly deferred to the scaffold. Everything else is fixed upstream
(D-29 `dataset_version`, SD-04 enumeration surface per the owner's Q2=A
decision, the two-tier error posture, the 20-column §13.4 schema, Python 3.11
pin per TS-01/TC-03d).

**Recorded input (human ruling, 2026-09-05)**: the Minor findings riding this
unit's terminal READY nfr-design review are recorded input for this run — see
`governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`. For
`foundation` these are three record-only procedural Minors (provenance-banner
redo-count drift, one banner sentence's missing verb, one placeholder review
timestamp); none changes a design decision, and the plan lists them as
record-only.

---

## Question 1
The experiment-registry writer (component C-2, the twenty-column §13.4
append-only registry) has **no module path**: `business-logic-model.md` names
"the experiment-registry writer this unit owns" with no path, and the
2026-09-04 Critical correction establishes it is **not** `src/data/registry.py`
(that module belongs to `inventory-and-registry` and holds the `Station`
dataclass). TE §18.3 forbids an implementer picking an unresolved mechanism by
convenience. Where does C-2 live?

A) New module `src/data/experiment_registry.py`, with the owner's approval of this answer standing as the §18.3 stop-and-report resolution, and a TE §12 naming amendment recorded the same way `src/data/config.py` was (`CR-2026-08-22-TE-AMEND` precedent; D-number cited in the commit)
   > **Impact**: Clear one-module home for the unit's most integrity-critical writer; no collision with `inventory-and-registry`'s `src/data/registry.py`. Requires the owner to record the §12 naming amendment/change record — one more governance artifact before commit.

B) Fold C-2 into `src/data/release.py` beside the release writer
   > **Impact**: No new module, but it merges the two writers whose separation is the design's own boundary criterion (C-2's unit of damage is a row, C-3's a release directory; separate acceptance rows TA-10/TA-21 vs TA-15). Blurs the reviewed component decomposition.

C) Fold C-2 into `src/data/config.py`
   > **Impact**: Violates the reviewed boundary outright — C-1 is resolve-only ("a bad read fails a run; a bad write corrupts the permanent record"). A registry defect would then sit in the module every unit imports at startup.

D) Stop and report: defer C-2 entirely to a later ruling; generate only C-1/C-3 work this run
   > **Impact**: Strictest §18.3 reading. Leaves TA-10/TA-21's subject unwritten in Bolt 1, and the unit completes without its permanent-record writer — a second pass on this unit becomes necessary.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the design already isolates C-2 as its own component with its own acceptance rows; a dedicated module is the only home that preserves that boundary, and the config.py precedent shows exactly how the naming authority is recorded. Risk stated plainly: the §12 amendment record is owed before the commit that creates the module.

[Answer]: A

## Question 2
SD-01's secret scan needs a concrete tool, and nfr-design explicitly left the
selection to the `pyproject.toml` scaffold this run builds ("gitleaks,
trufflehog or equivalent, pinned"). Which scanner does the pre-commit hook and
the gate scan pin?

A) `gitleaks`, version-pinned
   > **Impact**: Single static binary, fast diff-mode for the pre-commit net and full-history mode for TA-22's gate scan; reviewed allowlist file supported. Config lives in the repo; version recorded in the tooling pins.

B) `trufflehog`, version-pinned
   > **Impact**: Stronger verified-credential detection (live checks), heavier runtime and a Python/Go dependency surface; history scans slower. Same two-mode design applies.

C) Defer selection; ship the hook as a stub that fails open
   > **Impact**: SD-01's preventive net does not exist in Bolt 1 and TA-22's evidence path stays unimplementable; the deny-list `.gitignore` remains the only guard. Pushes a named open item into a later Bolt.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — gitleaks matches SD-01's two-mode design with the least dependency surface, and a pinned single binary is the easiest thing to record in the environment lock. Known cost: periodic false positives on test fixtures, handled by the reviewed allowlist, never by disabling the hook.

[Answer]: A

## Question 3
`requirements.txt` and `pyproject.toml` are created this run. The TensorFlow
pin is **`TBD — freeze gate`** (TS-02), and no agent may fill a freeze-gate
value by convenience. How do the pins handle TensorFlow?

A) Exclude TensorFlow from foundation's pins entirely; the pin enters `requirements.txt` only when frozen at its gate, before `models-and-baselines` builds
   > **Impact**: Keeps the freeze-gate rule intact and foundation's Bolt 1 needs no TF. The governed environment stays incomplete for model work until the freeze — which is already the gated order.

B) Include TensorFlow unpinned (`tensorflow` with no version)
   > **Impact**: Makes the environment lock's `requirements.txt` hash cover an unpinned resolver choice — the lock would stabilise an under-specified environment, exactly what SD-06 warns against.

C) Include a TensorFlow version chosen now
   > **Impact**: An agent filling a `TBD — freeze gate` value by convenience — forbidden outright (TE §1.2/§18.2; project Forbidden list).

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the only option that neither fills a frozen-pending value nor under-specifies the lock. Risk stated: a later freeze changes `requirements.txt`, so the environment-lock hash changes at that boundary; that is the designed behaviour, not a defect.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — C-2, the twenty-column §13.4 experiment-registry writer, gets its own new module `src/data/experiment_registry.py`; this approval stands as the §18.3 stop-and-report resolution, with the TE §12 naming amendment recorded per the `config.py` precedent before the commit that creates it.
- Q2 = A — the secret scanner is `gitleaks`, version-pinned: diff mode in the pre-commit hook (preventive net, not evidence), full history/config/log/artifact mode for TA-22's gate evidence; false positives handled by a reviewed allowlist, never by disabling the hook.
- Q3 = A — TensorFlow is excluded from `pyproject.toml`/`requirements.txt`; its pin enters only when frozen at its gate, before `models-and-baselines` builds.
- Recorded input (2026-09-05 ruling): foundation's three record-only nfr-design Minors are listed in the plan as record-only; no design decision changes.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `foundation` is at
`construction/foundation/code-generation/code-generation-plan.md` — 12 steps:
scaffold + pins + gitleaks (1), four governed configs (2), C-1 resolve +
environment lock (3–4), C-2 experiment-registry writer at
`src/data/experiment_registry.py` + tests (5–6), C-3 release writer + TA-15
tests (7–8), TA-22 gate-scan wrapper (9), test config + smoke run (10), docs
(11), governance stop before commit (12).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
