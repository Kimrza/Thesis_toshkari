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

## 3.7 — D-45 annotation (owner-authorized), index-file coverage and comparison, notebook revision 3

**Authority for this section.** The project decision owner's instruction of 2026-09-19:
"I approve a dated D-45 annotation identifying the actual verified runtime and its bundled
index files, subject to the evidence checks below" (items 1–5). Recorded as the student's
authorization; **no supervisor signature is claimed or fabricated**. Boundaries as in the
header: no full-year benchmark, locked-target access, training, producer release,
`write_release`, `permitted_producers`, commit or push; G-04 not passed.

### 3.7.1 The annotation — status

Written under D-45 in `evidence/DECISIONS.md` on 2026-09-19 as an **annotation block
appended after item 4**; every original line of D-45 is preserved; the register's D-45
summary row gained a bracketed pointer. This is the annotate-in-place disposition
`governance/CHANGE_RECORD_PROCEDURE.md` allows on owner approval for the specific item,
which the instruction above is. Approval status: **owner-authorized annotation, recorded;
D-45's own supervisor status unchanged** (student-reported approval and countersignature,
2026-09-19, as the entry records). Material-change assessment (annotation item 6): none —
the release and pin values are the concrete form of D-45 item 1, and the 2022 inputs are
equal to the copies the original text described (§3.7.3), so TE §18.2 requires no
additional approval; the two hashes go to the Vision §6.11 driver-input freeze gate
(G-03/G-05) with the rest of D-45, as already planned.

### 3.7.2 The verified runtime and index files (from the bundle and the wheel bytes)

Runtime: `iricore==1.8.0`, wheel `iricore-1.8.0-cp310-cp310-manylinux_2_35_x86_64.whl`,
SHA-256 `f452b22316891d87ee766dba266de6a07e4e6008ab515ffed902ea8b5446a874` (PyPI upload
2024-04-02); CPython 3.10.12 `virtualenv` on the Kaggle image (kernel 3.12.13, glibc 2.35);
`numpy==1.26.4`, `fortranformat==2.0.3`, `pymap3d==3.2.0` at the pinned hashes;
`version=16` explicit against an installed default of 20. To read metadata the Kaggle run
had not read, the same wheel was downloaded from PyPI here, hash-verified, and its
`iricore/data/index/` members extracted: **they hash exactly to the Kaggle-reported values**
(`apf107.dat` `cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674`,
`ig_rz.dat` `fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486`), so every
statement below is about the installed bytes. Both files are filed under
`evidence/iri2016_kaggle_verification_2026-09-19/index_files/installed_iricore-1.8.0_wheel/`.

| File | Update metadata and coverage (installed 1.8.0) |
|---|---|
| `apf107.dat` | 1,329,460 bytes; 24,172 rows, contiguous daily, **1958-01-01 → 2024-03-06**; the unused 13th integer column is −11 on every row; format `(3I3,9I3,I3,3F5.1)` as the wheel's own `irifun.for:readapf107` reads it |
| `ig_rz.dat` | 9,815 bytes; header `3,7,2024` = update date **2024-03-07** in the file's month-day-year convention (the 2024-06 copy's `6,18,2024` cannot be day-month-year); declared range 1958-01 → 2024-10; 804 IG12 + 804 Rz12 values = one edge value before and after the range, exactly `3-imst+(iyend-iyst)*12+imend` as `read_ig_rz` computes and `tcon` indexes (value 1 = 1957-12, value 804 = 2024-11) |

**Support required for every 2022 target time**, derived from the compiled sources the
wheel ships (`irifun.for`), not from the wrapper's comments: `APF` takes 3-hourly ap back
to UT−39 h (`aap(is-2, …)`), `APF_ONLY` the target row plus the previous day's F10.7
(`AF107(IS-1,1)`), `tcon` the target month plus the previous (day < 15) or next (day ≥ 15)
month. Hence direct reads: `apf107.dat` rows **2021-12-30 → 2022-12-31** (367 rows) and
`ig_rz.dat` months **2021-12 → 2023-01** (14 months). Behind those rows the file carries
centered means whose windows must also lie inside the file for the values to be
full-window: F10.7_81 needs **2021-11-22 → 2023-02-09**, F10.7_365 needs **2021-07-03 →
2023-07-01**, and the 12-month IG12/Rz12 mean for 2023-01 rests on observed months through
**2023-07**. Result on the installed files: all 367 rows present, none with a negative
missing sentinel; both centered windows inside the file; all 365 rows of 2022 have
F10.7_81 / F10.7_365 that recompute from the same file's daily column within 0.049 / 0.050
(F5.1 rounding) — full-window values; all 14 months present and non-negative; update date
2024-03-07 ≥ 2023-07. The files do not label values observed versus predicted, so
"final" is asserted only as "the window the update date covers".

**Two executable-path facts the earlier inspection did not record.** (a) In 1.8.0 the
Python reader `read_iri_data.readapf107` is dead code (`# IRI_DATA = readapf107()`,
"TODO: Fix data reading from Python"); the compiled library reads both files itself. That
Python reader carries a column bug — its 81-day slot is overwritten by the 365-day values —
which would matter only if a later release activated it; one more reason the pin is on this
exact wheel. (b) `read_ig_rz` multiplies Rz12 by **0.7** for every month from 2014-01 when
the header date is after 2016-09 (new sunspot-number series), so the Rz12 IRI-2016 uses in
2022 is 0.7 × the file value (2022-06: file 81.1, used 56.77); IG12 is used as stored.
Neither changes a decision; both are now in the D-45 annotation.

### 3.7.3 Comparison with the historically inspected files — differences by kind

The copies `CR-2026-09-19-SCI-DECISIONS` §3 inspected were recovered with identifiable
provenance from the 2026-09-19 session's retained archives: the GitHub `master` snapshot
(tarball pax comment = commit `92c6d8c727b0300d8bd61e7e8e91dd97514256a7`, archive SHA-256
`03d8973b6b08c7ef16cb2ea1556509ff2ae9eba3e868fa500bc45f87b69c8e28`) and the PyPI sdist
`iricore-1.9.0.tar.gz` (SHA-256 `6f1503716f5f8ba3e48038a4cade9310d396ee2dce299ac841824a054b595e35`,
matches PyPI's published digest). Their index files are byte-identical to each other
(`apf107.dat` `4de3bfa2d3b488e61477cf7bfb9ec1d9ca891b265694752b20e7b320f9657e82`,
`ig_rz.dat` `e688620c6ac25dec6cf31ebd4afe091a6a083c4e1d50f22c68d096474944e1a8`) and are filed
under `index_files/historical_master-92c6d8c7_and_1.9.0-sdist/`. Today's `master` was not
substituted for them. Comparison (`index_comparison_report.json`, produced by
`iri_index_checks.py`):

| Kind of difference | `apf107.dat` | `ig_rz.dat` |
|---|---|---|
| Length / update date | 24,172 vs 24,275 rows; last row 2024-03-06 vs 2024-06-17 | header 2024-03-07 vs 2024-06-18; same declared range 1958-01 → 2024-10; same 804 values each |
| Values on common dates/months | 24,172 common; **176 differ, earliest 2023-09-08** | 804 common; **15 months differ, 2023-09 → 2024-11** |
| Values inside any 2022 support window | **0** in 2021-07-02 → 2023-07-01 | **0** in 2021-12 → 2023-01 |

So the earlier description ("ends 2024-06-17", "updated 6/2024") was of newer files whose
extra rows and revised tail lie entirely after 2023-09; **every value the 2022 benchmark
reads is identical in both**. The four spot values the earlier inspection quoted (239.0,
144.5, 257.0, 133.1) are unchanged in the installed file. No performance effect is claimed
— none could arise from equal inputs. Nothing was refreshed or replaced; `iricore.update()`
was not run.

### 3.7.4 Evidence preservation and notebook revision 3

**Preserved.** The returned bundle stays as filed (§3.6). The producing notebook, revision 2,
is now also filed byte-exactly beside it (`evidence/…/kaggle_iri2016_verification.ipynb`,
SHA-256 `b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa`) — regenerated
from its own builder and hash-verified, because the working copy in `kaggle/` was found
modified at 21:49 local on 2026-09-19 by something outside this session (cells 1–7 gained
editor `id` fields; **zero source differences**; the file was untracked, so no git copy
existed). The manifest now covers 12 files.

**Revision 3** — `kaggle/kaggle_iri2016_verification.ipynb`, SHA-256
**`0e4d4478f256c37737038388b52e2a29960909657ee4fa4672774974911d2a34`**, 19 cells (11 code),
built from the preserved revision 2 by a builder that asserts revision 2's hash first.
**It has not run on Kaggle and none of the 2026-09-19 evidence is attributable to it**; its
first cell says so. Changes, none of which touch the pins, the smoke test or the ladder:
1. **Step 1b network preflight** before any install: DNS → TCP → TLS → HTTPS for
   `pypi.org/simple/iricore/` (must answer 200) and `files.pythonhosted.org`, each stage
   under a 10 s timeout, bundle written, then a stop naming the failed host, stage,
   closed-set class and exception. The stop text lists the Kaggle Internet setting as a
   *possible* cause of a DNS failure that the probe "cannot tell apart" from a DNS outage
   or a restricted network — never as established.
2. **`failure_class`** on every failed command from `run()` (`dns_failure`, `tls_failure`,
   `connection_failure`, `hash_mismatch`, `platform_tag_mismatch`, `resolution_failure`,
   `missing_module`, `timeout`, `unknown`), tested on the literal run-3 stderr; the rung
   summary and the pip-install stop message name it.
3. **Inner script**: `iri_index_checks.py` embedded verbatim; after hashing, both files are
   parsed as the Fortran reads them and `index_files.apf107.{summary,support_2022}` /
   `index_files.ig_rz.{summary,support_2022}` are recorded (update date, range, counts,
   the required rows/months/windows and whether each holds); the revision-2 last-date
   regex is cross-checked against the parser; Step 5 asserts both `support_2022.ok`.
4. The bundle is still written after every attempt and on every stop.

**Validation performed (focused; no full suite, no Kaggle run).** Notebook is nbformat 4;
all 11 code cells and the 20,071-character inner script parse. Module checks
(`test_modules.py`): real preflight passes all four stages on both hosts from this machine;
synthetic DNS failure (`nonexistent-host.invalid`) → `dns_failure`; TCP refused on a closed
local port → `tcp_connect_failure`; a local plain-HTTP listener answering a TLS ClientHello
→ `tls_failure` with the TCP stage recorded ok; a 404 index path → `http_error` with TLS ok;
10 classifier cases including run 3's exact stderr; parsers reproduce every figure in
§3.7.2–3.7.3 and 5 synthetic index failures (truncated file, negative sentinel, early
update date, missing 2023-01, malformed line) are caught. Notebook checks (`test_rev3.py`):
(A) inner script with `iricore` absent → `ok:false`, `failed_stage: import_iricore`, exit 1;
(B) inner script end to end against a stub `iricore` carrying the real 1.8.0 index bytes →
`ok:true`, hashes, dates, 2022 support and repeatability fields exactly as expected;
(C) outer helper and preflight cells exec'd with the bundle directory redirected: `run()`
classifies a synthetic DNS stderr and a timeout, the preflight stop path writes
`verification_report.json` (`notebook_revision: 3`, `stopped_reason`, the per-stage
record) and the zip, then raises; (D) the Step 5 cell passes on (B) and fails with the
`ig_rz.dat` message on a doctored copy. **Not established locally:** that revision 3
executes on Kaggle's image; the only things a rerun would add are that regression check
and the same metadata fields recorded by the Kaggle run itself, which §3.7.2 already holds
from identical bytes. A rerun is therefore **not required for any claim in this record**;
it is recommended before revision 3 is relied on to produce any future evidence.

**Repository state, re-verified at writing time (`git log`, `git status`).** An owner commit
**`60cdabd`** (2026-09-19 21:48:35 +0330) was made while this section's work was in
progress. It holds: the §3.6 evidence filing (bundle, three members, first manifest,
`RETURN_RECORD.md`), the D-45 annotation in `evidence/DECISIONS.md`, `kaggle/HOW_TO_RUN.md`
with the third/fourth-run section, this record through §3.6, the code-summary amendment (3),
and `kaggle/kaggle_iri2016_verification.ipynb` as **revision 2** — blob
`ba499531…`, which is `b8399c98…` with CRLF normalized to LF by `core.autocrlf=true`
(restoring CRLF reproduces `b8399c98…` byte for byte). One minute later (21:49:45) an
editor re-save added `id` fields to that working copy (§3.7.4 above); revision 3 then
replaced it. **Uncommitted at writing time:** revision 3, this §3.7, the revision-3
`HOW_TO_RUN.md` section, code-summary amendment (4), and the evidence additions
(preserved revision 2, `index_files/`, `iri_index_checks.py`, `index_comparison_report.json`,
`validation/`, the 17-file manifest). No commit was made by this session; the
commit-or-follow-up disposition is the owner's.

### 3.7.5 Not done, by design

No 2022 IRI value was computed; no target time evaluated; R-59 limb 1 (a passing validation
report) untouched; no producer artifact; no `permitted_producers` entry; no commit.
Installation and smoke testing are verified; **scientific validation of the full 2022
benchmark is not**, and nothing here says otherwise.

## 3.8 — Final preparation pass: the B-01 production path (owner instruction 2026-09-19, "one consolidated final preparation pass")

**Authority and boundary.** The owner's instruction authorising implementation and permitted
diagnostic verification to complete preparation; no full-year execution, locked-target access,
producer release, `write_release`, registration, training, commit or push. The reported
supervisor approval of D-45 stands as the entry records it; nothing here re-asks it.

### 3.8.1 R-59 mapped to evidence — what is met, what is genuinely unmet

| R-59 / release requirement | Status | Evidence or gap |
|---|---|---|
| Limb 1 — a passing report exists | **Unmet (student input)** | Report builder implemented (`--build-validation-report`); it needs the 5–10 samples with **official IRI-2016 interface values** (`kaggle/b01_validation_samples.TEMPLATE.json`) — a reading only the student can take |
| Limb 2 — tolerance predeclared, timestamp before comparison | **Unmet (student freeze)** | `experiment.yaml: benchmark_b01.validation_report.tolerance_tecu` / `tolerance_declared_at_utc` are `TBD — freeze gate`; the builder refuses while TBD and refuses a timestamp not preceding the comparison (tested) |
| Limb 3 — seven areas field by field | **Met by construction** | `build_validation_report` emits all seven in this unit's schema; `assert_validation_report` (unchanged) asserts them; ceiling 2000, `version=16`, no overrides, `index_inputs_retrospective_centered: True`, full index hashes |
| Limb 4 — benchmark drivers in the availability matrix | **Met** | `benchmark_driver_rows` emits the three IRI index rows in the EV-12 shape, graded hindcast-only (D-45 item 4); consumed by the gate and written into the provenance |
| D-45 item 1 — index files pinned by full SHA-256, never updated after the pin | **Met** | One authoritative record: `experiment.yaml: benchmark_b01.index_file_pins`; `verify_runtime` before the session, `assert_index_unchanged` after; refusal named per file (tested with altered bytes, wrong release, changed default) |
| Station coordinates (D-1) in configuration | **Unmet (student freeze)** | `data.yaml: stations` and `igrf_version` are `TBD — freeze gate`; the registry refuses and so does generation (tested). D-1 holds the values; transcription + IGS site-log validation is inventory-and-registry's recorded obligation |
| TE 9.2 / TC-03g — both fixtures pass in the Kaggle session before a full-year job | **Unmet (execution prerequisite)** | The stage script's receipt gate is kept on every `--generate-benchmark`; the production notebook checks the receipts and skips step 6 with the reason when absent |
| TC-04 — the 26,000-call workload timed | Met when run | `workload_seconds` and `calls_per_second` in `b01_provenance.json` |
| B-01 labelled generated, not trained | Met | `experiment.yaml: benchmark_b01.label`; provenance `label` |
| TC-03d — governed interpreter 3.11 | **Deviation, recorded** | The only Linux `iricore` wheel is cp310; the session runs under 3.10.12 and the environment lock records it (D-45 annotation item 1; `benchmark_b01.runtime.python`). An owner ruling accepting this for B-01 sessions — or authorising a from-source 3.11 build — is the one environment decision still open |

No new gate, threshold or approval layer was added; the TE 9.2 gate was **scoped** (below), not
bypassed.

### 3.8.2 What was built (all within the existing contracts)

- **`configs/experiment.yaml: benchmark_b01`** — the execution contract transcribed from D-45 as
  annotated: `iri_version 16`, `htop 2000` (frozen) with `hbot 90` / `hstep 0.5` disclosed as
  wrapper defaults, no `oarr` overrides, output field/units, index semantics, the wheel and
  companion pins, the two full index-file hashes, the 2022 hourly grid rule, the three TEC-05
  stamps, and the validation-report contract (tolerance TBD — the student's).
- **`src/external/iri.py`** (+562 / −9 lines after `ruff format`, measured against `60cdabd`; existing functions unchanged): `read_benchmark_contract`,
  `verify_runtime`, `assert_index_unchanged`, `build_target_grid`, `evaluate_points`
  (per-point failure recorded on the row, never fatal — two-tier posture), `benchmark_driver_rows`,
  `build_validation_report` (refuses December samples), `run_gated_generation` (pins → all four
  limbs → report-vs-installed hash cross-check → grid → workload → pins again → stamped rows +
  provenance). `generate_benchmark` keeps its refusal contract; injection mode never generates.
- **`scripts/04_build_external_products.py`**: `--verify-runtime`, `--build-validation-report
  <samples.json>`, `--generate-benchmark --validation-report <report.json> [--months …]`; outputs
  under `artifacts/external/b01/` with a SHA-256 manifest; registry rows as for every run. The
  TE 9.2 receipt gate now applies to full-year jobs (every `--generate-benchmark`, partial or not,
  and the driver audit) and is recorded as "not required" for the two bounded checks
  (`--verify-runtime` hashes two files; `--build-validation-report` makes 5–10 calls and no
  product) — the rule's own text, "before any full-year job".
- **`kaggle/kaggle_iri2016_benchmark.ipynb`** (21 cells, SHA-256 `99815fb6…`, not yet run on
  Kaggle) + **`kaggle/build_b01_package.py`** → `kaggle/dist/tec_b01_package.zip` (58 files: `src/`,
  the stage script, the four configs, `requirements.txt`, `tests/fixtures/`, the samples template
  and, when present, the filled samples; a manifest with per-file SHA-256 and the source commit;
  `evidence/locked_test_restricted/` refused by rule). The notebook reuses the verified
  environment cells of the verification notebook verbatim, hash-verifies the package, then runs
  steps 4–6 through the stage script inside the 3.10 venv, copying every output and the registry
  rows into `b01_bundle.zip`.

### 3.8.3 Validation performed

14 new tests in `tests/test_external_drivers.py` (function level through the stage module, plus
one subprocess-level `--verify-runtime` completing with exit 0 on the real configs; a stub
`iricore` carrying the **real pinned index bytes**): pins verified and written; altered
`apf107.dat` / `ig_rz.dat`, wrong release, changed default each refused by name; the report
passes and carries the seven areas with the D-45 call shape (`version=16`, `htop=2000`, naive UT
handed to iricore); a failed report is written and blocks; TBD tolerance and a late declaration
refused; a December sample refused; a one-month partial generation end to end (3 × 28 × 24 rows,
stamps, cell ids 40/44, 32/35, 35/33, UTC alignment, provenance, manifest, hindcast-only driver
rows); a failed report and a report validated against different index bytes refused at
generation; unresolved stations refused; per-point failures recorded (3 error rows) not fatal;
the config block asserted as the annotated D-45 contract. The package was unpacked into an
empty directory and `--verify-runtime` run from it alone (exit 0, registry rows written).
Full suite in the governed environment (`pytest tests -q`, junit-counted): **1330 tests, 0 failures, 0 errors, 4 skipped** (the four pre-existing environment skips). Ruff clean
on every touched file.

**One guard fired and was honoured.** The locked-month custody guard (R-26,
`tests/test_locked_test_guard.py`) flagged `index_comparison_report.json` and
`validation/test_modules.py` for carrying `2022-12` literals (required-month enumerations and a
synthetic date). Fixed at the source, not in the guard: `iri_index_checks.py` now states the
required rows/months as ranges with exclusive bounds and counts; the report was regenerated;
the two new markdown files were added to the test's inventory of prose outside automated
inspection. **Revision 3 of the verification notebook was rebuilt** with the corrected module:
its hash is now `0e4d4478f256c37737038388b52e2a29960909657ee4fa4672774974911d2a34` (previously
`ec089ff6…`; still not run on Kaggle; swept in every record).

## 3.9 — Remaining preparation (owner instruction 2026-09-19, seven items): interpreter exception, registry transcription, reference samples, tolerance proposal, custody finding, real-Kaggle workflow

### 3.9.1 Python exception — recorded as **D-49**

Owner approval quoted in D-49 (`evidence/DECISIONS.md`); scope = the isolated Kaggle B-01
environment only (CPython 3.10.12 `virtualenv`, pinned `iricore==1.8.0` and companions with
their hashes, IGRF-13 compiled in); training, fixtures and every other stage stay on 3.11
(TC-03d unchanged). Mirrored in `experiment.yaml: benchmark_b01.runtime.interpreter_exception`.
**Fixture interaction, preserved:** `fixture_gate.verify_receipt` accepts a receipt only when
its recorded environment identity equals the caller's lock, so a 3.10 full-year run cannot
consume receipts from 3.11 fixture runs. D-49 item 4 records the two admissible resolutions
(extend the exception to the fixture runs; or build `iricore` for 3.11 from the sdist,
`e5c4a71e…`) and chooses neither. Independently, **no frozen fixture manifest exists yet**
(BLK-02: `tests/fixtures/*` hold identity declarations only), so no receipt can exist in any
environment until the measuring runs and the freeze happen.

### 3.9.2 Transcribed values and their authorities

| Field | Value | Authority |
|---|---|---|
| ARUC / BSHM / NICO lat, lon | 40.286/44.086; 32.778987/35.022987; 35.140989/33.396450 | D-1 (approved), now **validated** against the official IGS site logs (`aruc00arm_20260317.log` `858aa54b…`, `bshm00isr_20260422.log` `d0dae804…`, `nico00cyp_20251027.log` `2740b73a…`): 40.285722/44.085583, 32.778986/35.022986, 35.140989/33.396450 — max Δ 0.0004° (ARUC rounding); cells unchanged; never averaged |
| DOMES | 12312M002, 20705M001, 14302M001 | site logs §1 |
| Ellipsoidal height | 1222.0, 225.1, 190.1 m | site logs §2 |
| Receiver / antenna / firmware intervals covering 2022 | SEPT POLARX5 5.4.0 (ARUC, BSHM); LEICA GR50 4.51/7.710 (NICO); antennas ASH701945C_M SCIS, TRM59800.00 SCIS, LEIAR25.R4 LEIT | site logs §3–4; no change inside 2022 |
| Sampling interval | 30 s | IGS 2022 daily files `<STATION>_R_2022001…_01D_30S_MO.crx.gz` (BKG listing, retrieved 2026-09-19) |
| `igrf_version` | **IGRF-13** | the only IGRF consumer in the Phase 1 executable path is the compiled IRI-2016 in the pinned wheel: `igrf.for` 2020.01, `FELDCOF` wired to `dgrf2015` + `igrf2020` + `igrf2020s` (2022 uses the IGRF-13 2020.0 coefficients, g₁⁰ = −29404.8 nT); coefficient files hashed in D-49 |
| Benchmark location convention | station coordinates, never cell centres | D-45; Vision §6.6 |

Sources filed under `evidence/station_registry_sources_2026-09-19/` (manifested). D-1 carries
a dated annotation; `load_registry` now resolves all three stations with the D-1 cells.
**Genuine gap, stated:** `observable_codes` (Vision §6.2) — in no governing record and not in
a site log; read from a 2022 RINEX header (Phase 2 material). `assert_registry_resolved`
(features path) keeps refusing on that field alone; the B-01 path (`load_registry`) does not
need it.

### 3.9.3 Official reference samples — selection fixed, retrieval refused, manual sheet delivered

The eight cases were **selected before any retrieval** (2026-09-19T20:28:42Z,
`evidence/iri2016_official_reference_2026-09-19/sample_selection.json`): quietest and most
disturbed non-December days of the audited definitive Kp record, three sites, day/night,
two seasons; cases are never replaced. The official interface (CCMC Instant Run IRI-2016;
its API and option catalogue were discovered from the page's own JavaScript and are recorded
in `interface_notes.json`) answered **HTTP 429 to every run request** after two schema probes,
then reset connections; `official_runs.json` holds the attempt log. **No official value was
retrieved; none was fabricated; the adapter was not used to produce any.** Delivered instead:
`kaggle/b01_official_reference_collection_sheet.md` — exact URL, every form setting mapped
to the IRI-2016 standard `jf` switch the adapter uses (the form's default hmF2 model, AMTB, is
**not** the IRI-2016 standard and must be changed to Shubin-COSMIC; `tecLower` must be set to
90), the eight cases, and the output fields to copy (TEC, TOP, header lines with the server's
F10.7/Rz12/IG12, output URL, precision). `b01_validation_samples.TEMPLATE.json` is prefilled
with the eight cases; the report builder now carries the extra provenance fields.

### 3.9.4 Tolerance — proposed, not declared

`governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md`: **1.0 TECU absolute per case**,
derived from display precision (≤ 0.05), the two quadratures (`iri_tec` segment steps vs the
adapter's 0.5 km sum, ≤ ~1 % ≈ 0.5 TECU), the 90-vs-100 km lower segment (≤ 0.02), and zero
for version/switches/ceiling by construction; index inputs are checked from the output
header, not absorbed. D-47's 8e-12 sfu is not reused. No discrepancy was computed or
inspected; `experiment.yaml` keeps `TBD — freeze gate` until the owner's approval instant,
which is then recorded as the declaration time (never backdated).

### 3.9.5 December-custody finding and disposition

**Finding.** §3.8.3's fix reserialised my own new evidence file to avoid the literal scanner.
Against D-48 that is the wrong reflex (item 3: "no evidence file is relocated or
reserialised"; item 1: the detector is literal/structural and cannot see an exclusive-bound
interval). **Assessment of the content, not the serialisation:** the first version carried
December-2022 IG12/Rz12 **values** (driver indices) and was correctly flagged; the current
version carries **no December datum** — only interval bounds (`[2021-12-30, 2023-01-01)` =
367 rows; months `2021-12 … 2023-01` = 14), counts and residuals, each asserted by
`validation/test_modules.py`. It is therefore compliant on content, and the file now says so
in a `custody_statement` that also records the **exposure** D-48 item 4 requires: every
apf107.dat row and ig_rz.dat month, December's included, was read for version comparison
(driver indices only, no target), informing no method, threshold or model decision.
**Scanner gap, reported through the existing rule:** D-48 item 1 already separates scanner
coverage from compliance; an interval-bound representation is outside the detector's reach
and is documented here rather than papered over. No further renaming or reformatting was
done. The first version's hash was not retained (overwritten before the manifest was
refreshed) — recorded as a gap in this trail.

### 3.9.6 Real-Kaggle workflow — one notebook, unchanged identity, new revision

`kaggle/kaggle_iri2016_benchmark.ipynb` (23 cells, SHA-256
`c8a1ef048674f5382982acbcc476f9cb0da0c6b3267c6af90be42f2db898d37b`): steps 4–7 run the real
installed `iricore` through the real adapter via the stage script inside the 3.10 venv;
**Step 6** creates a governed 3.11 environment with pinned `uv`, installs `requirements.txt`,
and runs `run_walking_skeleton.py` for both fixtures **only when frozen manifests are
packaged** — receipts are whatever the orchestrator writes, nothing is marked passed;
**Step 7** full-year generation is **disabled by default** (`RUN_FULL_YEAR = False`) and,
when enabled, still refuses without identity-matching receipts. The local stub checks are
labelled structural tests in the notebook's first cell. Package: `kaggle/build_b01_package.py`
now collects `src/`, all stage scripts, `configs/`, `requirements.txt`, `pyproject.toml`,
`tests/` (the fixtures' M10 contract needs them), the November 2022 acquisition evidence and
the two driver audits (custody classes 1–5 content), `evidence/DECISIONS.md` (the skeleton
asserts identity against it); `evidence/locked_test_restricted/` refused by rule. The manifest
carries a **`tree_sha256`** over every packaged file — the working-tree identifier
independent of HEAD: **`865b33ecd91e91471c625ead8874a97a97fae37c6bbb14a122adafbd2257fa09`**,
zip `1b7af8ec09ae164d9c96075f0446a5c743f4be2992e29126064120482b416e44`, built at commit
`60cdabd+dirty`.

### 3.9.7 Validation and repository state

Full suite in the governed environment after the transcription and config changes:
**1346 tests, 0 failures, 0 errors, 4 pre-existing skips** (the manifest-parametrised release
tests grew by the three new/updated evidence manifests). One of my own tests was corrected to
re-create the pre-transcription refusal state explicitly. HEAD is still `60cdabd`; every
change in §3.7–3.9 is uncommitted working tree (`tree_sha256` above identifies it). No
commit or push by this session.

## 4 — Closure table

| Item | Status |
|---|---|
| 1. Countersignature | **Closed 2026-09-19** — recorded as the student's stated report, matching the established letter mechanism; not a fabricated signature |
| 2. Config validation/enforcement | **Complete**: reader-level required/closed-set/bounds checks for `lag_reference_instant`, `selection_rule`, `recomputation_input_bound_sfu`; real consumer wiring (`build_availability_matrix` → `assert_anchor_recomputed`; `build_features` → `assert_lagged_selection` drift guard); 4 new focused tests + 1 integration test class; no contradiction found; no scientific value changed |
| 3. Kaggle notebook | **Executed on Kaggle 2026-09-19 — PASS (fourth run).** Runs 1–3 stopped in Step 3 (run 1: stdlib `venv` without ensurepip, a notebook defect, fixed; runs 2–3: Kaggle Internet toggle OFF, diagnosed by run 3's complete per-rung log). Run 4, same notebook, Internet ON: `iricore==1.8.0` installed hash-verified into a Python 3.10.12 `virtualenv`, smoke test 37.3737545… TECU bit-identical on repeat, index files unchanged, reconciliation passed. Bundle filed at `evidence/iri2016_kaggle_verification_2026-09-19/`. One reconciliation finding (installed `apf107.dat` ends 2024-03-06, not the 2024-06-17 read from `master`) routed to the owner as a proposed D-45 annotation — see §3.3–3.6 **Then (§3.7):** D-45 annotated on owner authorization (release, wheel, Python, explicit `version=16`, full index-file hashes, smoke-test limits); coverage and 2022 support verified on the installed bytes; historical copies recovered with provenance and compared — 2022 inputs identical; revision 2 preserved beside the bundle; revision 3 (`0e4d4478…`, not run on Kaggle) adds the network preflight, failure classes and `ig_rz.dat` metadata. |
| 4. Verification bundle design | **Delivered** (report + logs + hashes + provenance + smoke test + repeatability, explicitly diagnostic-only) |
| 5. Honest validation | **Done** — structure/syntax/logic locally checked; Kaggle execution explicitly marked pending |
| 6. Code summaries / change record | **Updated** (this record; code-summary addenda below) |
| 7. Boundaries | No producer artifact, `write_release`, `permitted_producers`, training, commit, or push. G-04 not declared passed |

**Concrete remaining blockers:**
1. ~~The student must actually run `kaggle_iri2016_verification.ipynb` on Kaggle and
   return `iri_verification_bundle.zip`~~ — **closed 2026-09-19** (§3.6): run 4 returned
   the bundle; installation, smoke-test correctness and repeatability are verified on
   Kaggle's real environment. ~~Open in its place: the owner's ruling on the proposed D-45
   annotation and the two diagnostic notebook revisions~~ — **both closed 2026-09-19**
   (§3.7): annotation authorized and recorded; revision 3 built and locally validated.
   Closed since (§3.9): stations + `igrf_version` transcribed; 3.10 exception recorded
   (D-49). Still open: the owner's approval of the 1.0 TECU tolerance (declaration time =
   approval time); the eight official reference values (manual sheet; interface refused
   automation); frozen fixture manifests and in-session receipts (BLK-02 — the walking-
   skeleton freeze precedes any full-year job); the fixture/B-01 environment-identity
   resolution (D-49 item 4); `observable_codes` (features path only). The verification notebook revision 3 no longer needs a separate run:
   its checks are incorporated in the production notebook's first execution.
2. `iricore` remains uninstallable in the local governed Windows environment (unchanged
   from the prior pass; Kaggle is the intended path, not a substitute local fix).
3. Producer artifacts, `permitted_producers` registration, and G-04 itself remain
   untouched, as instructed.
