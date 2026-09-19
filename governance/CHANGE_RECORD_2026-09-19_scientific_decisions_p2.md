# Change Record — 2026-09-19 (part 2) — Supervisor approval recorded (reported); IRI-role patch applied; pip/iricore installation diagnosis; six-entry configuration transcribed; stale code summaries updated

**Change ID:** `CR-2026-09-19-SCI-DECISIONS-P2`
**Authority:** the project decision owner's instruction of 2026-09-19 ("Continue with the
following authorization. I confirm that my supervisor has approved the scientific
decisions covered by the latest handoff, including D-42, D-43, D-45, and D-46", items
1–6), continuing `CR-2026-09-19-SCI-DECISIONS`. **Boundary respected:** no producer
artifact, `write_release`, `permitted_producers` entry, dataset registration, model
training, commit or push. **G-04 is NOT passed by this record.** No supervisor signature
artifact is claimed to exist; the reported approval is recorded as exactly that.

---

## 1 — Supervisor approval: recorded as reported by the student

**What was said, verbatim, 2026-09-19:** *"I confirm that my supervisor has approved the
scientific decisions covered by the latest handoff, including D-42, D-43, D-45, and
D-46."*

**Recorded exactly as that** — a report by the recorded decision owner that the approval
occurred — in `evidence/DECISIONS.md`, as a dated annotation on each of D-42, D-43, D-45,
D-46 and in the review-table status column, changing each item's status from "REQUIRED
and OPEN, student [acceptance/decision/selection] only" to **"Reported approved by the
student 2026-09-19; countersignature artifact PENDING."** No signature, no direct
supervisor communication, and no date earlier than 2026-09-19 is invented anywhere in
these annotations.

**The prescribed form of evidence still outstanding**, identified rather than requested
again from the student: a supervisor-signed or otherwise directly-recorded
countersignature artifact, matching the project's own established mechanism
(`governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md` items 1–2,
`governance/COUNTERSIGNATURE_REQUEST_2026-08-21.md`) — a letter the supervisor
countersigns, recorded on the student's report, exactly as TE §18.2's Student +
Supervisor items have been closed before. Drafted this pass:
**`governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`**, covering all four items with
what is asked, why, and the evidence already produced for each. Until it (or an
equivalent directly-recorded supervisor communication) exists, each of D-42/D-43/D-45/D-46
stays **reported, not verified**, and none of them, singly or together, satisfies TE
§18.2/§18.3 or passes G-04.

**D-45's IRI-role patch, applied.** Per the instruction's explicit authorisation
("Apply the prepared IRI-role patch after verifying that it matches the approved
retrospective-reference decision"), the patch was checked line-by-line against D-45 item
4's text (the R-59 limb-3 replacement: `index_inputs_retrospective_centered` recorded
disclosure, refusal of a still-`True` `no_future_centering_confirmed`, three new pinned
fields) — it matches exactly — and applied (`git apply governance/proposed/
P-3_iri_report_confirmations.patch`; the patch file itself is left in place as the
historical proposal record). `src/external/iri.py`'s stale docstring/comment describing
the old two-confirmation check and the "(PROPOSED, applies only once...)" wording were
corrected to state the applied, reported-not-countersigned status accurately.
`tests/test_iri_denial.py` (22 tests) green after the patch; the module still refuses
benchmark generation at R-59 limb 1 regardless (no passing validation report exists), so
applying this patch changes no runtime behaviour reachable today — it only fixes what a
FUTURE passing report must contain.

---

## 2 — The demonstrated pip failure, established from evidence

### 2.1 Exact reproduction

Command (identical to the session-summary's earlier attempt): `python -m pip download
iricore --no-deps --no-binary :all: -d <dir> --timeout 25 --retries 1 -vvv`, run through
`conda run -n tec-thesis-311` (the governed environment's own interpreter — confirmed
`C:\Users\LOTUS\anaconda3\envs\tec-thesis-311\python.exe`, Python 3.11.16, pip 26.2.1).
Full verbose log captured: `pip_exact_repro.log` (scratchpad, 4764 lines).

### 2.2 Environment checks (all clean — none of these caused the failure)

| Check | Result |
|---|---|
| `pip config list` | empty — no `pip.ini`/`pip.conf` anywhere in standard locations |
| Proxy env vars (`*_proxy`, `PIP_*`) | none set |
| DNS resolution, `pypi.org` / `dualstack.python.map.fastly.net` | resolves via `8.8.8.8`, both IPv4 and IPv6 |
| HTTPS connectivity, `curl` to `pypi.org` | `http_code=200`, TLS handshake completes in 1.26 s |
| Certificate chain | `certifi` bundle (`…\envs\tec-thesis-311\Lib\site-packages\certifi\cacert.pem`) validates a live HTTPS GET of the PyPI simple index for `iricore` |
| System clock vs. PyPI server `Date` header | 2026-09-19 12:40:03 UTC (local) vs. 12:40:05 UTC (server) — 2 s skew |
| PyPI JSON API (`urllib`, no proxy) | reachable, returns full release/file metadata |

**Conclusion: not network, not DNS, not TLS/certificate, not proxy, not clock skew.**

### 2.3 The actual, demonstrated cause

**Root cause 1 — no Windows wheel exists for `iricore` at any released version.**
Enumerated exhaustively via the PyPI JSON API (all 33 releases, 1.0.6 through 1.9.0):
every release publishes `manylinux` (Linux) wheels for its target CPython, one macOS
wheel from 1.8.1 onward, and an sdist — **never** a `win32`/`win_amd64` wheel. `pip`
would therefore always fall back to building from source on this platform, at any
version, with or without `--no-binary`.

**Root cause 2 — no Fortran compiler is present.** `iricore`'s `CMakeLists.txt` (line 4:
`enable_language(Fortran)`) requires one to build its Fortran extension from source.
`gfortran`, `cl`, and `clang` are all absent from `PATH` in this environment (checked via
`command -v`, all four returned nothing).

**Root cause 3 — the package's own maintainer documents this as a known, unresolved
Windows incompatibility**, not a locally-fixable gap: the downloaded sdist's `README.md`
(line 9) states verbatim: *"This package proved to work under Linux only (due to
compilation difficulties in Windows). If you are using Windows - consider installing
WSL."* This is authoritative upstream guidance that a native Windows build is not the
supported path, independent of what local tools are installed.

**The specific "Installing build dependencies: finished with status 'error'" reproduced
this pass** (`pip_exact_repro.log`, lines ~4700–4764) is a **diagnostic-flag artifact**,
not evidence of a different problem: `--no-binary :all:` is a blanket flag that bans
binary wheels for the ENTIRE build-dependency chain, not just `iricore` — including
`cmake`, which normally ships perfectly good `win32`/`win_amd64`/`win_arm64` wheels
(verified: `cmake` 4.4.3's PyPI files list three Windows wheels). Forced to build the
`cmake` PyPI package itself from source, pip's inner subprocess ("Building wheel for
cmake (pyproject.toml)") terminated with **exit code 143 (SIGTERM)** and "No available
output" — consistent with a bounded wall-clock cutoff (this pass's own diagnostic
`timeout 90` wrapper cut the outer `conda run` off at the 90 s mark, immediately after
pip had already printed the full failure traceback for the killed `cmake` subprocess;
the original run last turn used no such wrapper and was itself subject to the harness's
own subprocess/session boundaries). **Removing `--no-binary :all:`** — i.e. a normal
`pip download iricore==1.9.0 --no-deps -d <dir> --timeout 25 --retries 1` — succeeds
immediately (exit 0, sdist fetched in seconds, `iricore-1.9.0.tar.gz`, 3,554,652 bytes;
log: `pip_iricore_verbose.log`), because pip correctly falls back to the sdist without
needing binary build tools just to download it. The failure is therefore attributable
to the diagnostic flag choice, not to a defect in the network path, and root causes 1–3
above are the substantive, version-independent blockers to actually *installing* it.

**Classification (per the requested distinction):** not network/proxy/TLS; not
"unavailable version" in the sense of missing bytes (every version's sdist downloads
fine); **incompatible platform** (no Windows wheel, ever) compounded by **missing build
tools** (no Fortran compiler) — and the incompatibility is upstream-documented, not a
locally-fixable configuration gap.

### 2.4 Dependency-pin check (item 4)

`iricore` 1.9.0's `PKG-INFO`: `Requires-Python: >=3.9,<4.0` (governed 3.11.16 satisfies
this); `Requires-Dist: fortranformat (>=2.0.0,<3.0.0)`, `numpy (>=1.25.0,<2.0.0)`.
**No conflict with the project's existing pins**: `requirements.txt` pins
`numpy==1.26.4`, which satisfies `>=1.25.0,<2.0.0` exactly. `fortranformat` is not
currently pinned and would need adding — but only on a platform where `iricore` actually
installs (see §3).

---

## 3 — Targeted repair: none applicable; no environment change made

No pip configuration, certificate store, proxy, or global Python installation was
touched — none was demonstrated broken (§2.2). **No compiler toolchain was installed**
into the governed conda environment: the package's own maintainer states Windows
compilation is known-difficult and points Windows users to WSL instead (§2.3, root cause
3); installing a MinGW/MSVC-hybrid Fortran+CMake toolchain to fight a maintainer-declared
unsupported configuration would be a substantial, likely-fragile environment change for
uncertain benefit, and is not a "targeted repair of a demonstrated problem" — it would be
attempting to solve a problem the evidence shows is not a local misconfiguration.
Certificate verification was not disabled, `--trusted-host` was not used, no proxy was
removed (none existed), and no credential was touched — all per the explicit
instruction not to do any of these, and none was needed.

---

## 4 — Installation: not possible in this local Windows environment; Kaggle path documented

**Direct installation is not attempted and does not succeed**, for the reasons in §2.3.
This is the "direct download is impossible" case the instruction anticipates. Per its
own guidance:

**Recommended path — Kaggle (already an approved platform, TE §9.1).** Kaggle notebook
kernels run Linux (glibc), matching the `manylinux` wheels `iricore` already publishes.
No build is needed there. Exact commands for a Kaggle notebook cell, once the student
runs one (not executed by this session — no Kaggle access exists here, and none is
claimed):

```bash
python -m pip install --no-deps --require-hashes -r iricore_requirements.txt
```

with `iricore_requirements.txt` (to be hashed and pinned from the actual Kaggle kernel's
Python version at that time, since Kaggle's default interpreter version can differ from
the local 3.11.16 pin):

```
iricore==1.9.0 --hash=sha256:<from `pip download iricore==1.9.0 --no-deps -d . --hash` output>
fortranformat>=2.0.0,<3.0.0
```

(numpy is already present in the Kaggle image and satisfies iricore's `<2.0.0` bound in
the versions Kaggle currently ships; verify at run time before relying on this.) This
produces a **Linux** artifact, usable directly in that Kaggle session — it is not a
Windows wheel and cannot be transferred back to run natively on this local machine.

**If a Windows wheelhouse were required instead** (e.g. to run the IRI benchmark step
locally rather than on Kaggle): no source exists that builds a Windows wheel today —
neither PyPI nor this repository's own environment can produce one, and the maintainer's
own README says the same. A wheelhouse/offline-transfer procedure is therefore not
preparable in good faith for Windows without first resolving root causes 1–3 on some
Windows machine with a working Fortran toolchain (not one of this project's two approved
platforms, TC-03c) — which this session has neither built nor claims to have accessed.
**This is stated as a genuine block, not worked around.**

**GitHub source note (item 4's provenance requirement).** This session inspected
`iricore`'s `master` branch (not an immutable commit — the repository was cloned fresh
via GitHub's tarball endpoint, no commit SHA pinned) for the earlier P-3 semantics
inspection (`CR-2026-09-19-SCI-DECISIONS` §3). This pass additionally downloaded and
inspected the **published 1.9.0 sdist** (`iricore-1.9.0.tar.gz`, PyPI, immutable release
artifact) and confirmed its `pyproject.toml`, `README.md`, and `CMakeLists.txt` are
consistent with what was read from `master` (same `enable_language(Fortran)` line, same
build-system requirements, same README Windows caveat) — **no material difference found**
between the master-branch inspection already recorded in D-45 and the actual 1.9.0
release. D-45's semantics table (F10.7 adjusted/centered, IG12/Rz12 centered, target-day
ap, override coupling) is therefore confirmed to describe the real 1.9.0 release, not
merely an unreleased branch state.

**No compatible fixed release was installed anywhere** — the "you may install a
compatible fixed release in the isolated environment" option is not exercised, because
no release is compatible with this isolated (Windows) environment; exercising it on
Kaggle is a future, out-of-session action for the student.

---

## 5 — IRI execution verification: not performed; blocked by §4, not skipped

Per the instruction, "installation alone does not establish scientific compatibility" —
moot here since installation itself did not occur. No version/provenance/hash record is
claimed for an installed package; no smoke test was run; no index files were touched (the
governed environment holds none — `iricore` was never installed, so nothing was
refreshed). This blocker is independent of the config-transcription and D-45-patch work
below, which do not require a runnable `iricore`.

---

## 6 — Configuration applied

**`configs/features.yaml`**, per D-25/D-42/D-43/D-46/D-47 exactly: `availability_lags`
filled with the six §6.2 driver rows (two GFZ scalar-lag pairs, two F10.7 rule rows, the
D-47 tolerance/domain on `f107_81_trailing`'s window); `carry_forward_bound_hours: 3` and
`carry_forward_composition: "clock_hours"` added (D-46). **Untouched:** `feature_set_id`,
`feature_dictionary`, `normalization`, `permitted_producers` — no feature-dictionary
freeze, no producer entries, consistent with the item 9 release boundary.

**Additive-key reader support, verified** (not newly enforced): `read_availability_lags`
carries `lag_reference_instant`, `selection_rule`, and
`window.recomputation_input_bound_sfu` through unmodified — confirmed by loading the
real file through the reader in a new test,
`tests/test_feature_availability.py::test_prepared_six_entry_availability_lags_load_without_error`
(reads `configs/features.yaml` via a bare YAML parse, asserts the six rows, both scalar
and rule branches, the window fields, and `_read_carry_forward_bound`'s acceptance of the
transcribed `carry_forward_bound_hours`). **A reviewed reader change remains owed**
before these three additive fields are themselves *asserted* by the loader — carrying
them through without erroring is not the same as enforcing them, and none of that
enforcement is added by this record.

**Every entry's `publication_latency_statement` and provenance labels are as prepared**
in `CR-2026-09-19-SCI-DECISIONS` §9, unchanged in substance.

**Focused verification (governed pin):** `tests/test_feature_availability.py` (81),
`tests/test_external_drivers.py` (65), `tests/test_iri_denial.py` (22),
`tests/test_locked_test_guard.py` (60) — **228 tests, 0 failed** across two independent
runs. `ruff check`/`ruff format` clean on every touched module.

**Full suite:** see §6.1 (appended once the governed run completes).

### 6.1 Full-suite result

Governed pin (conda `tec-thesis-311`, CPython 3.11.16, every `requirements.txt` pin), `python -m pytest tests -q`: **1274 passed / 4 skipped / 0 failed / 0 errors**, exit 0 (1278 collected; previous full run this session: 1273 passed / 4 skipped — +1 net this pass: +11 new test functions across `test_feature_availability.py`/`test_external_drivers.py`/`test_locked_test_guard.py`, no test removed, no skip added or removed). The four skips are the same pre-existing environment preconditions as every prior run this session. `compileall` on `src`, `scripts`, `tests`: clean. `git -c core.whitespace=cr-at-eol diff --check`: clean. HEAD `18843aa`; no commit.

---

## 7 — Stale code summaries updated

Per §9's carried item (gf-3): `features-and-splits`, `external-products`,
`governance-guards` code summaries each received a dated "Post-receipt amendment —
2026-09-19" block (features-and-splits' second such block this session), listing the
modules actually changed this pass with measured `git diff --numstat` figures, test
counts, and an explicit "what this amendment does NOT do" line. None of the three units'
original verdicts (`external-products` NOT-READY, `governance-guards` READY,
`features-and-splits` — see its own file) is altered; nothing above the new sections is
rewritten.

---

## 8 — Closure table

| Item | Status |
|---|---|
| 1. Supervisor approval | **Recorded as reported by the student, 2026-09-19.** Countersignature artifact drafted (`COUNTERSIGNATURE_REQUEST_2026-09-19.md`) and outstanding. |
| 1. D-45 IRI-role patch | **Applied**, verified to match D-45; denial tests green; no runtime behaviour change reachable today (benchmark still blocked at limb 1). |
| 2. pip failure diagnosis | **Established from evidence**: network/DNS/TLS/proxy/clock all clean; root cause = no Windows wheel at any release + no local Fortran compiler + maintainer-documented Windows incompatibility. The specific verbose-log failure reproduced was a `--no-binary :all:` diagnostic-flag artifact (forced source build of `cmake`, itself unrelated to iricore), not the substantive blocker. |
| 3. Targeted repair | **None applicable** — nothing network/config-side was broken; no compiler installed (maintainer discourages it). |
| 4. Reproducible install | **Not achieved locally; not achievable locally without a Windows Fortran toolchain the project does not authorise as a platform.** Kaggle path (an already-approved platform) documented with exact commands, not executed (no access, none claimed). No conflicting dependency found (numpy pin compatible); `fortranformat` would need adding on whichever platform installs it. |
| 5. IRI execution verification | **Not performed** — blocked by 4, not skipped or faked. |
| 6. Configuration | **Applied**: six-entry `availability_lags`, `carry_forward_bound_hours`/`carry_forward_composition`. Reader compatibility verified by test. Focused checks: 228 tests, 0 failed. |
| Code summaries | **Updated** (features-and-splits, external-products, governance-guards). |

**Concrete remaining blockers:**
1. Supervisor's actual countersignature on `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md` (or equivalent directly-recorded communication) — closes D-42/D-43/D-45/D-46's TE §18.2/§18.3 requirement.
2. `iricore` cannot be installed or verified in this local Windows environment; IRI benchmark generation and the D-45 dependent-patch's *runtime* effect stay unreachable until the student runs the acquisition/benchmark step on Kaggle (or the platform question is otherwise resolved by the owner).
3. The additive `lag_reference_instant`/`selection_rule`/`recomputation_input_bound_sfu` config fields are carried but not yet enforced by the reader — a reviewed reader change is owed.
4. Producer artifacts, `permitted_producers` registration, and G-04 itself remain untouched by this pass, as instructed.

**G-04 remains OPEN.**
