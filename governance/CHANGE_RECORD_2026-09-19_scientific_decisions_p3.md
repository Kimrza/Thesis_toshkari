# Change Record — 2026-09-19 (part 3) — Countersignature closure; D-43/D-44/D-47 configuration enforcement (reader + real consumer wiring); Kaggle IRI-2016 verification notebook

**Change ID:** `CR-2026-09-19-SCI-DECISIONS-P3`
**Authority:** the project decision owner's instruction of 2026-09-19 ("Continue from
the latest handoff. The next task is to complete configuration validation and prepare
a reproducible Kaggle execution of IRI-2016", items 1–7), continuing
`CR-2026-09-19-SCI-DECISIONS-P2`, and the owner's supplementary instruction ("for the
first blocker: supervisor has approved and countersigned"). **Boundary respected:** no
producer artifact, `write_release`, `permitted_producers` entry, dataset registration,
model training, commit or push. **G-04 is NOT passed by this record.**

---

## 1 — Countersignature closure

The project owner / student stated, later the same day as the prior pass's report:
**"supervisor has approved and countersigned"** (item 1's instruction, "for the first
blocker"). Recorded exactly as that statement — the recording date is 2026-09-19; no
earlier date, no signature, and no direct supervisor communication is invented anywhere.
`governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`'s status line and all four item
rows now read **"items 1–4 are countersigned by the supervisor"** / **"Countersigned
2026-09-19"**, matching exactly the mechanism `COUNTERSIGNATURE_REQUEST_2026-08-16.md`
established (a letter whose status line the student updates on the supervisor's
countersignature, recorded on the student's report). `evidence/DECISIONS.md`'s D-42,
D-43, D-45, D-46 review-table rows and body annotations were updated the same way, with
the interim "reported, not verified" wording preserved for the audit trail inside each
annotation rather than deleted. **This closes each item's TE §18.2/§18.3 requirement as
of 2026-09-19; it does not, by itself, pass G-04**, which needs every P0 decision
resolved plus the executable §18.3 preflight.

Three stale trailing clauses left over from the prior pass ("No config transcribed",
"Dependent patch prepared, not applied", "config transcription pending") were already
corrected in the previous change record; no further staleness was found in this pass
beyond the countersignature status itself.

---

## 2 — Configuration validation and enforcement (D-43/D-44/D-47)

### 2.1 What was found

The six-entry `availability_lags` transcription (prior pass) carried
`lag_reference_instant`, `selection_rule`, and `window.recomputation_input_bound_sfu`
through `read_availability_lags` **without any validation** — no required-field check,
no closed-set check, no numeric-bounds check — and, critically, **the matrix-build path
(`build_availability_matrix`) never read `recomputation_input_bound_sfu` at all**: the
D-47 domain certificate (`assert_recomputation_domain`) existed and was tested in
isolation, but nothing in the production call chain ever passed it an `input_bound`.
Passing the reader is not the same as a consumer applying the setting — exactly the gap
named in the authorizing instruction.

### 2.2 What was implemented

| Contract item | Enforcement added | Where |
|---|---|---|
| Required fields / supported values / bounds | `lag_reference_instant` and `selection_rule` are now REQUIRED on every scalar-lag (GFZ-style) row, each validated against a CLOSED set (`LAG_REFERENCE_INSTANT_KINDS = {"interval_end_utc"}`; `SELECTION_RULE_KINDS`, imported from `spaceweather.SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG` — one source of truth, never retyped); `window.recomputation_input_bound_sfu` is now REQUIRED alongside `recomputation_tolerance`, validated as a positive number | `src/features/availability.py: read_availability_lags`, `_validate_window_fields` |
| Rejection of malformed/incompatible combinations | absent → `FeatureAvailabilityError` naming the field; unrecognised value → named and refused; non-positive/non-numeric bound → refused | same |
| F10.7-only scope for `previous_day_median_midnight_utc` | unchanged (D-25, pre-existing `AVAILABILITY_RULE_SCOPE`); **newly added**: `lag_reference_instant`/`selection_rule` are now FORBIDDEN on a rule-governed row (they have no meaning on a calendar-day rule — D-25 fixes its own reference instant) | `read_availability_lags`, rule branch |
| Rule + trailing-81-day-window composition | unchanged (A2, pre-existing) | `AVAILABILITY_RULES_WITH_WINDOW` |
| Interval-end lag semantics for GFZ | `assert_lagged_selection` gains `expected_reference_instant`: a config-vs-implementation drift guard — the selector only ever implements `interval_end_utc` (hardcoded, D-43), so any other declared value is refused rather than silently miscomputed | `src/external/spaceweather.py` |
| 3-hour missing-update allowance, approved boundary | unchanged from the prior pass's implementation (`resolve_f107_at_origin`, D-46) — already correctly enforced and tested; this pass adds no new logic here, only reader-level validation of the two upstream fields it composes with (`lag_reference_instant`/`selection_rule` are unrelated to F10.7's own composition field) | — |
| Numerical tolerance and applicability conditions | **the real gap closed**: `build_availability_matrix` now reads `window["recomputation_input_bound_sfu"]` and passes it as `assert_anchor_recomputed`'s `input_bound=` on every real call — the D-47 domain certificate now actually runs in production, not only when a test calls `assert_anchor_recomputed` directly | `src/features/availability.py: build_availability_matrix` |

**End-to-end consumer wiring (the specific instruction: "verify that downstream
consumers actually apply these settings").** `AvailabilityRow` gained two additive
fields, `lag_reference_instant` and `selection_rule`, populated by
`build_availability_matrix` from the validated config entry. `build_features`
(`src/features/build.py`) now looks up the matrix row for each driver feature and passes
its `selection_rule`/`lag_reference_instant` into `_assert_driver_alignment`, which
cross-checks them against the driver's ACTUAL `attrs["selection"]` at build time: a
config that declares one selection mechanism while the producer implements another is
refused (`AlignmentError`, naming both values); a `lag_reference_instant` the selector
cannot honour is refused by `assert_lagged_selection`'s drift guard. This closes the
loop config → reader (validated) → matrix (carried) → `build_features` (applied and
cross-checked against the real driver), not merely reader → carried → nothing.

### 2.3 No genuine contradiction found

Every additive field the prior pass transcribed into the real `configs/features.yaml`
already satisfied the new stricter reader (checked directly:
`test_prepared_six_entry_availability_lags_load_without_error` passes unmodified). No
scientific decision or configuration value was changed; only validation and consumer
wiring were added.

### 2.4 Tests (focused, positive and negative, plus integration)

Four new test functions in `tests/test_feature_availability.py` (module now 85 test
functions, up from 81):

- `test_reader_enforces_d43_d44_reference_instant_and_selection_rule` — positive control
  (the base fixture passes); required-absent for both fields; unrecognised value for
  both fields; forbidden-present on a rule row for both fields.
- `test_reader_enforces_d47_recomputation_input_bound` — positive control; required-
  absent; four invalid values (negative, zero, string, bool); required on BOTH the
  scalar-lag-plus-window shape and the rule-plus-window shape (A2).
- `test_build_availability_matrix_actually_applies_the_configured_input_bound` — the
  integration test closing the exact gap in §2.1: the same window and constituents pass
  through the real `build_availability_matrix` call at the configured 400 sfu bound and
  fail through the SAME call when only the configured bound is lowered to 5 sfu — proving
  the value governing the outcome comes from configuration, not a hardcoded default.
- `test_config_declared_selection_mechanics_are_cross_checked_against_the_driver` — the
  end-to-end integration test: a matching config/driver pair passes through
  `build_features`; a `selection_rule` mismatch is refused naming both values; a
  `lag_reference_instant` the code cannot honour is refused by the drift guard.

Existing test fixtures (`_lags()` in `tests/test_feature_availability.py`, plus one
inline dict in `test_interval_end_observation_timestamps_make_the_lag_a_post_completion_margin`)
were updated to carry the now-required `lag_reference_instant`/`selection_rule` fields —
26 pre-existing tests initially failed against the stricter reader and are now green
with no test weakened, no assertion removed, no skip added.

**Verification (governed pin, conda `tec-thesis-311`, CPython 3.11.16):**
`tests/test_feature_availability.py`: 85 passed, 0 failed. `tests/test_external_drivers.py`,
`tests/test_iri_denial.py`, `tests/test_locked_test_guard.py`: unaffected, all green.
`ruff check`/`ruff format`: clean on `src/features/availability.py`,
`src/features/build.py`, `src/external/spaceweather.py`; `tests/test_feature_availability.py`
at 4 pre-existing findings (matches the pre-pass baseline exactly, none newly
introduced). **Full governed suite: 1278 passed / 4 skipped / 0 failed**, exit 0 (1282
collected; +4 net over the prior pass's 1278/1274, matching the 4 new test functions
added). `compileall`: clean.

`configs/features.yaml`'s comments describing the additive fields as "carried through
without yet asserting" were corrected to describe the now-implemented enforcement, and
its countersignature-status comments were updated per §1.

---

## 3 — Kaggle IRI-2016 verification notebook

**File:** `kaggle/kaggle_iri2016_verification.ipynb` (17 cells: 7 markdown, 10 code).
**Companion:** `kaggle/HOW_TO_RUN.md` (upload/settings/run/return instructions, and an
explicit list of what was and was not verified locally).

### 3.1 Version selection (not master, not assumed)

Re-verified against PyPI's JSON API, exhaustively, per release: `iricore` 1.8.1 through
1.9.0 publish a macOS-arm64 wheel **only** — no Linux wheel exists at any version newer
than **1.8.0**, which is the newest release with a published Linux wheel
(`iricore-1.8.0-cp310-cp310-manylinux_2_35_x86_64.whl`, CPython 3.10 specifically). This
is the version the notebook installs — a verified fact about the actual PyPI release
archive, not the `master` branch and not an assumption that the two are equivalent.

### 3.2 Design

- **Runtime detection first** (`platform.platform()`, `sys.version_info`) — nothing
  assumes Kaggle's Python matches the governed local 3.11.16 pin.
- **Environment strategy**: if the kernel's own Python is 3.10, an isolated `venv` is
  created from it directly (purely to protect the pinned `numpy==1.26.4` and friends
  from Kaggle's own site-packages); otherwise the notebook looks for an existing
  `python3.10` binary, then attempts `apt-get install python3.10 python3.10-venv`. **If
  neither succeeds, the notebook stops with a precise diagnosis** (the exact `apt-get`
  output is captured and included in the diagnosis) rather than falling back to a
  mismatched wheel or an unpinned/from-source install — no compiler-toolchain fallback
  is attempted, matching the instruction not to repeat the local native-build path.
- **Hash-pinned install**: `pip install --no-deps --require-hashes` against a
  requirements file carrying each package's real, PyPI-published SHA-256 (fetched this
  session, embedded verbatim): `numpy==1.26.4`, `fortranformat==2.0.3`,
  `pymap3d==3.2.0` (iricore's own declared runtime dependencies, pinned within its
  declared bounds), `iricore==1.8.0`.
- **One reusable inner verification script**, written to disk once and executed via
  `subprocess` with whichever Python was chosen (kernel or venv) — so the verification
  logic itself does not fork between the two environment-strategy branches. It:
  1. imports `iricore`, records `importlib.metadata.version`, `__version__`, and the
     resolved module file path (provenance);
  2. reads `iricore.config.DEFAULT_IRI_VERSION` and reconciles it against the earlier
     source inspection (expected 20/IRI-2020 — a drift is reported, not hidden);
  3. locates and SHA-256-hashes the shipped `apf107.dat`/`ig_rz.dat` **before** any call;
  4. parses `apf107.dat`'s own last covered date (never assumed) and picks a smoke-test
     timestamp 60 days back from it, walked away from December if the result would land
     there — a real, non-December, safely-in-coverage date computed from the actual
     installed file;
  5. states the approved integration settings explicitly: `htop=2000` km (the ONLY
     value TE/Vision freeze, Vision §6.11), `version=16` (explicit — the installed
     default is 20 and is never relied on), ARUC's D-1 frozen coordinate (40.286°N,
     44.086°E — station metadata only, no GNSS/VTEC target data read), `hbot=90`/
     `hstep=0.5` km disclosed as the wrapper's own defaults, **not** project-frozen
     values — nothing is invented as if it were an approved setting;
  6. calls `iricore.vtec(...)` **twice with identical inputs** (repeatability), checks
     both outputs are finite and inside iricore's own internal plausibility bound
     (0–200 TECU, the same bound the package's own code warns against);
  7. re-hashes the index files **after** the calls and asserts the hashes are unchanged
     — the guard against a silent `indices_uptodate`-triggered refresh;
  8. prints exactly one JSON object; on any failure, prints a JSON object naming the
     exact stage (`import_iricore`, `smoke_test_call_1`, etc.) and the exception,
     exit code 1 — never a bare traceback, never a silent partial result.
- **Output unit** verified from source: `iricore.tec._integrate_ne` sums `Ne × step_km`,
  converts km→m (`×1e3`) then to TECU (`×1e-16`) — the wrapper already returns TECU, no
  extra project-side conversion is needed or applied.
- **Bundle**: `verification_report.json` + the exact `requirements-iri.txt` used + the
  exact `iri_inner_verify.py` executed, zipped to
  `/kaggle/working/iri_verification_bundle.zip`. Explicitly labelled throughout as a
  **diagnostic verification bundle, not a producer release or a registered benchmark
  artifact**.
- **Scope boundary enforced by construction**: the notebook reads no GNSS/VTEC file, no
  Madrigal/ICTP path, nothing under `evidence/`; it makes exactly one point call per
  repeatability check (two calls total) at one station coordinate and one timestamp —
  never a multi-day, multi-station, or full-year loop.

### 3.3 Local validation performed (this session; no Kaggle access)

- `kaggle_iri2016_verification.ipynb` parses as valid nbformat 4 JSON; every one of its
  10 code cells parses as syntactically valid Python (`ast.parse`, verified
  programmatically).
- The embedded inner script (`iri_inner_verify.py`, ~180 lines) parses as valid Python
  **independently** of the outer cell that embeds it as a string literal, and contains
  no `'''` sequence that would break that embedding.
- The inner script's `apf107.dat`-coverage-parsing and safe-date-selection logic was run
  against a REAL `apf107.dat` (downloaded this session from the `iricore` project's own
  GitHub `master` branch, byte-identical in format to the shipped index file) and
  correctly extracted the file's last covered date (`2024-06-17`) and picked
  `2024-04-18` as the smoke-test date — 60 days back, non-December, well inside
  coverage.
- The `iricore.vtec()` call signature (`hbot=`, `htop=`, `hstep=`, `version=` as keyword
  names; a scalar `lat`/`lon` returning a length-1 array) was cross-checked against
  `iricore`'s own upstream test suite (`tests/test_tec.py`), not assumed from the
  wrapper's docstring alone.
- The notebook's orchestration helpers (`run()`'s subprocess capture, `write_bundle()`'s
  JSON + ZIP writing) were extracted and exercised standalone; both work correctly.
- The inner script's FAILURE path was executed end-to-end on this local machine (where
  `iricore` genuinely cannot be installed — §2 of the prior change record) and confirmed
  to print a well-formed JSON object with `ok: false`, `failed_stage:
  "import_iricore"`, a clean exception message, and exit code 1 — exactly the contract
  the outer notebook cells rely on.

**Not claimed and not performed: actual execution on Kaggle.** No Kaggle account,
session, or network access exists in this environment. Whether `iricore==1.8.0`
actually installs on Kaggle's current base image (glibc compatibility with
`manylinux_2_35`), whether the smoke test call succeeds, and whether the repeatability
and index-hash-stability checks pass there are **all open until the student runs the
notebook and returns `iri_verification_bundle.zip`.**

---

## 3.4 — First Kaggle run (student-reported) and the resulting notebook revision

The student ran the notebook on Kaggle and returned the traceback: Step 3's
`bash -lc /usr/bin/python3.10 -m venv /kaggle/working/iri_venv` exited 1. **What that
run established** (the first real Kaggle facts this project holds): the kernel's own
Python is not 3.10; `/usr/bin/python3.10` exists on the image; it lacks the Debian
`python3.10-venv` package, so the stdlib `venv` cannot seed pip (`ensurepip` absent).
**Defect in the first version:** `python3.10-venv` was only installed on the branch
where `python3.10` itself was absent — a pre-installed interpreter bypassed it.
**Revision:** the isolated environment is now created with `virtualenv` (pip-installed
into the kernel's Python; self-contained pip/setuptools seeds, nothing needed from the
target interpreter but its binary), with `apt-get install python3.10-venv` + stdlib
`venv` as a single fallback; every attempt's command/exit code/stdout/stderr is recorded
in `report["installation"]["isolated_env_creation"]` before any stop; the stale venv
directory from a failed run is removed first. The revised mechanism was exercised
locally with the governed interpreter (pip install virtualenv → `-m virtualenv -p
<interpreter>` → the new environment's pip responds; seeds reported as
`pip=bundle, setuptools=bundle`). Notebook rebuilt and re-validated (17 cells, 10 code
cells, all parse). `kaggle/HOW_TO_RUN.md` carries the same account. Steps 4–6 remain
un-executed on Kaggle and are not claimed.

## 3.5 — Second Kaggle run (student-reported) and the second notebook revision

Returned traceback: `TimeoutExpired` from Step 3's `apt-get install python3.10-venv`
after 300 s, raised inside `run()` from `/usr/lib/python3.12/subprocess.py`. **Facts
established:** kernel Python is 3.12; the `virtualenv -p /usr/bin/python3.10` rung did
not produce a working environment (cause unrecorded — see defect); apt hangs/exceeds
300 s on that image. **Defects in the notebook:** (a) `run()` did not catch
`subprocess.TimeoutExpired`, so the notebook crashed rather than stopping; (b) the
report was written only on a stop, so the crash lost every captured log. **Revision:**
`run()` records timeouts as outcomes with partial output; `write_bundle()` after every
attempt; a new middle rung using `uv==0.12.17` to install `cpython-3.10.21`
(python-build-standalone, immutable) and `uv venv --seed`; apt demoted to a bounded,
non-interactive last rung; rung 1 probes the image interpreter before using it. Exact
pinned uv commands exercised locally end to end (3.10.21 installed, seeded venv pip
responds). Notebook rebuilt and re-validated (17 cells, all code cells parse). Steps 4–6
remain unexecuted on Kaggle and are not claimed.

## 3.6 — Third Kaggle run (stopped: Internet OFF) and fourth Kaggle run (PASS) — student-reported, bundle returned

**Third run — stopped, diagnosis complete.** With the second-revision notebook, Step 3
stopped cleanly with the full per-rung diagnosis on disk (the §3.5 fixes held: no crash,
every attempt recorded). Every rung failed for one reason: **no network**. `pip install
virtualenv` and `pip install uv==0.12.17` both failed with `Temporary failure in name
resolution` against `/simple/…`; `apt-get` timed out at 240 s; the stdlib `venv` rung
failed on the already-known missing `ensurepip`. The image's `python3.10` probe itself
succeeded (`3.10.12`, stdlib `/usr/lib/python3.10`). **Root cause: the Kaggle session's
Internet toggle was OFF**, which `kaggle/HOW_TO_RUN.md` lists as required. By inference
the same toggle explains the second run's unrecorded `virtualenv` failure (§3.5): that
rung's first step is a `pip install`, and the identical rung succeeded unchanged once
Internet was ON. The first run's stop (§3.4, `ensurepip`) was a genuine notebook defect
and is unrelated to the toggle.

**Fourth run — PASS.** The student re-ran the **same notebook file** (SHA-256
`b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa`; no edit between the
third and fourth runs) with Internet ON and returned `iri_verification_bundle.zip`
(SHA-256 `3a0723a1ff70c213ed3cb7139cbfc02e4495d04888a00136c3e5a6c9afa6d508`). It is filed
verbatim, with its three extracted members verified byte-identical to the zip, at
`evidence/iri2016_kaggle_verification_2026-09-19/` (`sha256_manifest.json`,
`sha256_manifest_meta.json`, `RETURN_RECORD.md`). Every value below is read from that
`verification_report.json`.

| Fact | Value from the returned report |
|---|---|
| Kaggle kernel | Python `3.12.13` at `/usr/bin/python3`; `Linux-6.12.90+-x86_64-with-glibc2.35` |
| Isolated environment | rung 1 — `virtualenv` against `/usr/bin/python3.10` (`3.10.12`); seeded `pip==26.2.1`, `setuptools==84.0.0`; three attempts, all exit 0, none timed out; rungs 2–3 not reached |
| Install | `pip install --no-deps --require-hashes` exit 0: `numpy-1.26.4-cp310-…-manylinux2014_x86_64.whl`, `fortranformat-2.0.3-py3-none-any.whl`, `pymap3d-3.2.0-py3-none-any.whl`, `iricore-1.8.0-cp310-cp310-manylinux_2_35_x86_64.whl`; `pip freeze` = exactly those four. **glibc `2.35` is exactly the `manylinux_2_35` floor** the `iricore` wheel demands — the §3.3 "not checked" item is now checked, and at the boundary |
| Provenance | `iricore` dist `1.8.0`, no `__version__` attribute; installed `DEFAULT_IRI_VERSION == 20` — matches the §3 source inspection, so the explicit `version=16` stays necessary |
| Index files (1.8.0 wheel) | `apf107.dat` `cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674`; `ig_rz.dat` `fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486`; **unchanged after the calls**; `apf107.dat` last covered date **2024-03-06** |
| Smoke test | `vtec(2024-01-06T12:00Z, 40.286, 44.086, hbot=90, htop=2000, hstep=0.5, version=16)` = `37.373754526924806` TECU; finite; in `[0, 200]`; **bit-identical on repeat** |
| Outer checks | inner script exit 0, `_stage: done`; Step 5 reconciliation assertions all passed (`reconciliation_passed: true`); `ok: true`; all four boundary flags `false` |

**Every item §3.3 listed as "cannot be verified without Kaggle" is now verified** on the
2026-09-19 Kaggle image: the wheel installs (glibc compatible); `vtec()` executes on CPU
and returns a finite, plausible TECU value; the call is repeatable; the shipped index
files are not refreshed by the calls; the kernel is not 3.10 and the `apt-get` fallback
was never needed.

**One material reconciliation finding — index-file coverage.** `CR-2026-09-19-SCI-DECISIONS`
§3's execution-path table states "Shipped `apf107.dat` ends 2024-06-17; `ig_rz.dat`
updated 6/2024", and D-45 item 2 carries "the file being updated 2024-06". Those values
were read from the `master` branch / 1.9.0 sources and the GitHub release
infrastructure (§3.3 validated the date parser against that same 2024-06-17 file). The
**1.8.0 wheel actually installed ships a different `apf107.dat`, ending 2024-03-06** —
different bytes, so the D-45 "pinned by SHA-256 at freeze" pin must be the wheel's file,
whose hash is now known (table above), not the `master` copy's. Both copies cover
calendar 2022, so nothing scientific changes for the study year. The installed
`ig_rz.dat`'s own update month was **not** read by the notebook (hashed only) and is not
claimed. **Not applied to D-45** (a countersigned record; `project.md`
`fd-2026-08-30-never-edit-signed-record`, `code-generation:c31`). Proposed annotation
text for the owner to adopt under D-45, verbatim or amended:

> *Annotation, 2026-09-19 (Kaggle verification, `CR-2026-09-19-SCI-DECISIONS-P3` §3.6).*
> The release actually installed on Kaggle is `iricore==1.8.0`; its shipped index files
> hash to `apf107.dat` `cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674`
> and `ig_rz.dat` `fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486`
> (`evidence/iri2016_kaggle_verification_2026-09-19/`). Item 2's "2024-06-17 /
> updated 2024-06" describes the `master`/1.9.0 copies inspected earlier, not this
> wheel: the installed `apf107.dat` ends 2024-03-06 (2022 fully covered); the installed
> `ig_rz.dat`'s update month is unread and will be recorded on the next Kaggle run.
> These two hashes are the freeze pins for release 1.8.0.

**Follow-up (not done here).** The notebook is left byte-for-byte as it was when it
produced this bundle (hash above), so the evidence and its producer stay matched. Two
small revisions are owed to the *next* version, both diagnostic: (a) read and record
`ig_rz.dat`'s in-file update month alongside its hash; (b) a network preflight in Step 1
(resolve `pypi.org` before any install) so an Internet-OFF session stops in seconds with
the actual cause instead of after three failed rungs and an `apt-get` timeout — the
defect that cost runs two and three.

**Unchanged boundaries.** No producer artifact, `write_release`, `permitted_producers`
entry, benchmark result, commit or push. R-59 limb 1 is untouched. **G-04 is not passed
by this run**; it establishes only that the D-45-selected execution path installs and runs
on Kaggle as designed.

## 4 — Closure table

| Item | Status |
|---|---|
| 1. Countersignature | **Closed 2026-09-19** — recorded as the student's stated report, matching the established letter mechanism; not a fabricated signature |
| 2. Config validation/enforcement | **Complete**: reader-level required/closed-set/bounds checks for `lag_reference_instant`, `selection_rule`, `recomputation_input_bound_sfu`; real consumer wiring (`build_availability_matrix` → `assert_anchor_recomputed`; `build_features` → `assert_lagged_selection` drift guard); 4 new focused tests + 1 integration test class; no contradiction found; no scientific value changed |
| 3. Kaggle notebook | **Executed on Kaggle 2026-09-19 — PASS (fourth run).** Runs 1–3 stopped in Step 3 (run 1: stdlib `venv` without ensurepip, a notebook defect, fixed; runs 2–3: Kaggle Internet toggle OFF, diagnosed by run 3's complete per-rung log). Run 4, same notebook, Internet ON: `iricore==1.8.0` installed hash-verified into a Python 3.10.12 `virtualenv`, smoke test 37.3737545… TECU bit-identical on repeat, index files unchanged, reconciliation passed. Bundle filed at `evidence/iri2016_kaggle_verification_2026-09-19/`. One reconciliation finding (installed `apf107.dat` ends 2024-03-06, not the 2024-06-17 read from `master`) routed to the owner as a proposed D-45 annotation — see §3.3–3.6 |
| 4. Verification bundle design | **Delivered** (report + logs + hashes + provenance + smoke test + repeatability, explicitly diagnostic-only) |
| 5. Honest validation | **Done** — structure/syntax/logic locally checked; Kaggle execution explicitly marked pending |
| 6. Code summaries / change record | **Updated** (this record; code-summary addenda below) |
| 7. Boundaries | No producer artifact, `write_release`, `permitted_producers`, training, commit, or push. G-04 not declared passed |

**Concrete remaining blockers:**
1. ~~The student must actually run `kaggle_iri2016_verification.ipynb` on Kaggle and
   return `iri_verification_bundle.zip`~~ — **closed 2026-09-19** (§3.6): run 4 returned
   the bundle; installation, smoke-test correctness and repeatability are verified on
   Kaggle's real environment. Open in its place: the owner's ruling on the proposed D-45
   annotation (1.8.0-wheel index-file hashes; `apf107.dat` coverage to 2024-03-06), and
   the two diagnostic notebook revisions owed to the next version.
2. `iricore` remains uninstallable in the local governed Windows environment (unchanged
   from the prior pass; Kaggle is the intended path, not a substitute local fix).
3. Producer artifacts, `permitted_producers` registration, and G-04 itself remain
   untouched, as instructed.
