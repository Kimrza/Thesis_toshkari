# Change record — 2026-09-24 — proposed D-number and gate-record text for three ripe items

**Purpose.** Draft text only. Nothing here is written to `evidence/DECISIONS.md`, no config
is changed, no tag is moved, and no `.gitleaks.toml` is edited. Per `project.md` § Corrections
("ALWAYS offer a proposed D-number text inside the change record for the owner to adopt rather
than writing into evidence/DECISIONS.md"), this drafts the exact text the Student/Supervisor
can paste into the register on approval — approval is theirs to give, the write is theirs to
make. **Repository state:** `HEAD = 92e0f5f`, working tree as left by the prior session.

Three items are drafted, chosen because each has a recommended option already stated and needs
no further investigation to rule — only a decision:

1. §A — Layer‑1 §3: `f107_safe`'s `source_series` split (`RULING_REQUEST_2026-09-23...`, §3)
2. §B — Layer‑2 §1: historical email in git history (`RULING_REQUEST_2026-09-21...`, §1)
3. §C — Layer‑2 §3: authorization occasion for the three December-reading test modules
   (`RULING_REQUEST_2026-09-21...`, §3)

Each section ends with an **Approve / Reject / Modify / Postpone** ask, per this project's
question-recommendation convention.

---

## §A — D-66 (proposed): `f107_safe`'s `source_series` renamed to separate it from the daily-median key the trailing window reads

**Status quo problem.** `feature_dictionary.f107_safe.source_series` and
`availability_lags.f107_81_trailing.window.source` are both the literal string
`"f107_daily_median"`. `build_features` needs per-hour rows under that key for `f107_safe`;
`build_availability_matrix`'s trailing limb needs per-day rows under the same key for the
81-day window. One key cannot serve both row shapes at once (measured 2026-09-23, `§3` of the
2026-09-23 ruling request).

### Proposed D-66 text (for `evidence/DECISIONS.md`, pending owner approval)

> **D-66 — `f107_safe`'s `source_series` renamed to `f107_safe_at_origin` (transcription
> correction under D-60's existing scope)**
>
> | Countersignature | Date | Rationale |
> |---|---|---|
> | *(owner fills)* | *(owner fills)* | Corrects a key collision in the D-60 dictionary: `f107_safe` and `f107_81_trailing` both declared `source_series: "f107_daily_median"`, and the same key is read by two consumers needing incompatible row shapes (per-hour vs. per-day). `configs/features.yaml`'s `feature_dictionary.f107_safe.source_series` changes from `"f107_daily_median"` to `"f107_safe_at_origin"`. **Nothing scientific moves**: the row id, lag rule `[1]` (previous-day observed value), the producing artifact (`nrcan_f107_observed_daily_median_2022`, D-63), and the normalization (`train_only_standardize`, D-60) are all unchanged — only the label distinguishing the per-origin selection from the plain daily series. `f107_daily_median` keeps its plain meaning (D-21: the daily series) and is what `f107_81_trailing.window.source` reads. Symmetrical with D-60's earlier resolution of the sibling collision (`f107_81_trailing`'s own `source_series` → `f107_81_trailing_mean`), same session, same class of fix. **Field and row counts stay at 21 fields over 13 dictionary rows** (D-60's frozen count); this changes one string value in one existing row, not the row inventory. |
>
> **Verification obligation before this is marked executed:** `load_feature_dictionary` still
> accepts 21 fields; `f107_safe` and `f107_daily_median` diverge in every printed config dump;
> `build_features` resolves `f107_safe` from per-hour rows under the new key and
> `f107_81_trailing` continues resolving from `f107_81_trailing_mean` (D-60's prior fix,
> already implemented); a negative control asserts the two keys are never equal to prevent
> this collision recurring under a third field.

### Matching gate-record note (no gate is being signed by this — for the record only)

> This is an implementation-detail correction inside D-60's already-frozen dictionary scope,
> not a new scientific decision. It discharges no gate on its own and requires no
> countersignature beyond what D-60 already carries, per the TE §18.2 precedent D-63 set for
> transcription-only corrections.

**Decision required — Approve / Reject / Modify / Postpone.**

---

## §B — Proposed G-09 gate-record entry: historical personal email, accept-and-disclose

**Status quo problem.** The working tree is clean (verified 2026-09-21, `git ls-files` finds
no live occurrence), but four historical commits touching
`notebooks/madrigal_phase1_coverage_audit.ipynb`, plus thirteen committed manifests carrying
`user_fullname`/`user_affiliation`, still carry a personal identity literal (Rec 39 / DATA-16).
Rewriting history to remove it would invalidate every `code_commit` reference recorded across
the registry, environment locks, and change records project-wide — a strictly worse outcome
than a disclosed, bounded exception.

### Proposed `.gitleaks.toml` allowlist entry (for the owner to add, not added here)

```toml
# Historical, disclosed exception — see G-09 gate record and GOV-2026-08-20-RA-01
# finding DATA-16 / Recommendation 39. Working tree is clean; this covers only the
# four pre-existing commits of notebooks/madrigal_phase1_coverage_audit.ipynb and
# thirteen already-committed manifests carrying user_fullname/user_affiliation.
# Personal identifier only — not a credential, key, or secret.
[allowlist]
  commits = [
    # owner fills: the four commit SHAs from DATA-16's own record
  ]
  paths = [
    "notebooks/madrigal_phase1_coverage_audit.ipynb",
  ]
  regexes = [
    # owner fills: the exact literal or its pattern, scoped as narrowly as possible
  ]
```

### Proposed G-09 gate-record entry text

> **TA-22 (secret scan, tree + history) — discharged as bounded.** The working tree scans
> clean. History (four commits touching the coverage-audit notebook, plus thirteen manifests)
> carries one disclosed, non-credential personal identifier (a name/email), accepted under a
> dated, commit-range-scoped `.gitleaks.toml` allowlist entry rather than removed by history
> rewrite. Rewrite was rejected: it would invalidate every `code_commit` reference recorded in
> the experiment registry, environment locks, and change records project-wide (`project.md` §
> Forbidden; NFR-AUD-01's immutable audit trail), trading a disclosed personal identifier for a
> broken provenance chain across the whole project. No tag moves. Ruled
> *(owner fills: Student + Supervisor, date)*.

**Decision required — Approve / Reject / Modify / Postpone.**

---

## §C — Proposed authorization record: one-time guard-verification run of the three December-reading test modules

**Status quo problem.** `tests/test_release_hashes.py`, `tests/test_acquisition_window.py`,
`tests/test_phase_boundary.py` read bytes under `evidence/locked_test_restricted/`. They are
correctly deselected from the pre-commit hook and every suite run (Recommendation 30's split:
gate-only modules that read restricted bytes don't run on every commit) — but as a consequence
they have **never executed**, so TA-15, the acquisition-window control, and the phase-boundary
control rest on static reading alone, and the `aws_ai_dlc_preflight_report`'s "release hashes"
limb renders absent.

### Proposed authorization text (for the owner to sign and date)

> **Authorization for a locked-root guard-verification occasion.**
> On *(owner fills: date)*, the Student runs, once, locally, under the governed Python 3.11
> pin:
> ```
> python -m pytest -q tests/test_release_hashes.py tests/test_acquisition_window.py tests/test_phase_boundary.py
> ```
> with `purpose = "guard_verification"` and `performance_inspected = false`. The run reads
> December **target bytes only**, through the three modules' existing `open_restricted`
> routing; it computes no metric, no prediction, and no comparison, and inspects no model
> performance. Its access rows append to `evidence/test_run_access_log.jsonl` exactly as every
> other restricted-root read does (Vision §8.3; TE §13.4), and the junit result becomes the
> evidence for TA-15, the acquisition-window control, and the phase-boundary control, closing
> the `aws_ai_dlc_preflight_report`'s currently-absent "release hashes" limb. Disclosed to the
> Supervisor at the next gate. This is independent of §A/§2's persistence-baseline question and
> of G-05: it verifies guards, not a model, and is the same performance-blind class as the
> required pre-G-05 coverage audit.

**Owner:** Student, with Supervisor informed. **Due:** before G-05 (the preflight report
cannot reach a green verdict without this).

**Decision required — Approve / Reject / Modify / Postpone.**

---

## What happens on approval

For each of §A/§B/§C the agent's next action on an **Approve** is mechanical and stated here so
it needs no further round trip:

- **§A**: change the one `source_series` string in `configs/features.yaml`, add the negative
  control, re-run the fixture ladder to confirm stage 05 resolves correctly, paste the D-66
  text above into `evidence/DECISIONS.md` under the owner's own countersignature line.
- **§B**: add the `.gitleaks.toml` allowlist entry with the owner-supplied commit SHAs, paste
  the gate-record text into the G-09 record. No code change.
- **§C**: the Student runs the stated command; the agent verifies the access-log rows appended
  correctly and updates `aws_ai_dlc_preflight_report`'s release-hashes limb from `absent` to
  the junit evidence path. No config or scientific value changes.

**STOP.** No document is updated, no config changed, and no D-number written beyond this
change record until the owner rules on each item above.
