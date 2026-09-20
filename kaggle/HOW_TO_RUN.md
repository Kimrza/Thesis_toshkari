# How to run `kaggle_iri2016_verification.ipynb` on Kaggle

**This has not been executed on Kaggle by this session.** No Kaggle account, API key,
or network session is available here. Everything below is a set of instructions for
you to run it, plus what the notebook does and does not verify locally.

## What to upload

Just **`kaggle_iri2016_verification.ipynb`** — it is fully self-contained. It writes
and reads only files under `/kaggle/working/`; it never reads from your Windows
filesystem and needs no other project file uploaded alongside it. No credentials are
embedded anywhere in it.

## Kaggle settings to select

1. **New Notebook** → **File → Upload Notebook** → select `kaggle_iri2016_verification.ipynb`.
2. **Settings** (right sidebar):
   - **Accelerator: None / CPU** — this notebook never requests a GPU and does not
     benefit from one.
   - **Internet: ON** — required to `pip install` the pinned packages and, if your
     kernel's Python is not already 3.10, to `apt-get install python3.10`. **This
     toggle was OFF in the second and third runs and is the sole reason they stopped**
     (see the 2026-09-19 sections below); it needs a phone-verified Kaggle account. With
     it OFF every rung fails with `Temporary failure in name resolution`.
   - **Environment:** the default "Latest environment" image is fine — the notebook
     detects its actual Python version itself in Step 1 rather than assuming it, and
     adapts (or stops with a diagnosis) in Step 2.
3. No Kaggle dataset attachment is needed.

## How to run it

**Run All** (Kaggle's "Run All" button, or execute cells top to bottom). The notebook
is linear and stops itself (raises a clear exception, after writing whatever partial
report it has) the moment anything it checks does not hold — it does not continue past
a failure with a downgraded or silent result.

Expect it to take a few minutes: creating the isolated virtual environment and
installing the four pinned, hash-verified packages is the slowest step.

## Which output to return

After a successful run, the last cell prints:

```
DONE. Download this file from the Kaggle output pane: /kaggle/working/iri_verification_bundle.zip
```

**Return that one file: `iri_verification_bundle.zip`.** Download it from the Kaggle
notebook's Output pane (Kaggle keeps `/kaggle/working/` contents there after a run) and
attach or paste its contents back. It contains:

- `verification_report.json` — the full machine-readable report (runtime info,
  environment strategy, installation logs and exit codes, package versions and
  provenance, index-file hashes before/after, the smoke-test inputs/outputs, the
  repeatability and reconciliation results).
- `requirements-iri.txt` — the exact hash-pinned requirements file actually installed.
- `iri_inner_verify.py` — the exact verification script actually executed.

If the notebook stops partway (raises `STOPPED: ...`), the same zip is still written
with whatever the report holds up to that point, including the precise diagnosis in
`verification_report.json["stopped_reason"]` — **return that too**; a clean stop with a
diagnosis is a valid, useful result, not a failed run to hide.

## Revision after the first Kaggle run (2026-09-19)

The first run reached Step 3 and stopped at `/usr/bin/python3.10 -m venv
/kaggle/working/iri_venv` (exit 1). That run established two facts about the Kaggle
image the notebook now relies on: the kernel's own Python is **not** 3.10, and a
`python3.10` binary **is** already present at `/usr/bin/python3.10` — but shipped without
the Debian `python3.10-venv` package, so the stdlib `venv` module has no `ensurepip` and
cannot seed pip. The notebook's first version only installed that package when
`python3.10` was absent, which is why the pre-installed interpreter slipped through.

**Fix (this revision):** the isolated environment is now created with `virtualenv`
(installed into the kernel's Python via its working pip; it bundles its own pip and
setuptools wheels and needs nothing from the target interpreter beyond the binary).
Only if that also fails does the notebook `apt-get install python3.10-venv` and retry the
stdlib `venv` once. Every attempt's exact command, exit code, stdout and stderr is
captured in `verification_report.json["installation"]["isolated_env_creation"]` before
any stop, so a repeat failure returns its own diagnosis. The revised mechanism was
exercised locally (pip-install virtualenv → `-m virtualenv -p <interpreter>` → the new
environment's pip answers), which is the same command shape Kaggle will run.

**Re-run:** upload the revised `kaggle_iri2016_verification.ipynb` again and Run All
from the top (the venv directory from the failed run is removed automatically).

## Second revision after the second Kaggle run (2026-09-19)

The second run got further and returned a `TimeoutExpired` traceback from Step 3. What
it established: the Kaggle kernel is **Python 3.12** (`/usr/lib/python3.12/...`); the
`virtualenv -p /usr/bin/python3.10` rung did **not** yield a working environment (why is
unknown — the report was not written, see the defect below); and the fallback `apt-get`
hung past its 300 s timeout. **Two defects in the notebook itself:** `run()` let
`TimeoutExpired` escape (so the notebook crashed instead of stopping), and the report was
only written at a stop — together they lost the diagnosis.

**Fixes (this revision):**
1. `run()` records a timeout as an outcome (`returncode: null, timed_out: true`, partial
   output kept) and never raises.
2. The bundle is written after **every** attempt, so nothing can crash before the
   diagnosis is on disk.
3. A new middle rung: **`uv==0.12.17`-managed `cpython-3.10.21`** — uv downloads a
   complete, immutable python-build-standalone interpreter (no apt, nothing needed from
   the image's own `python3.10`), then `uv venv --seed` gives a pip-seeded Python 3.10
   environment. Exercised locally with these exact pinned commands: interpreter
   installed in ~15 s, seeded venv's pip answers on Python 3.10.21. On Kaggle uv will
   fetch the Linux x86_64 build of the same release.
4. `apt-get` (now `DEBIAN_FRONTEND=noninteractive`, `--no-install-recommends`, 240 s) is
   the last rung only, and is skipped entirely when the image has no `python3.10`.
5. Rung 1 now also probes the image's `python3.10` directly (`sys.version`, stdlib
   path) so a broken minimal interpreter is visible in the report.

**Re-run:** upload the revised notebook, Internet ON, CPU, Run All from the top.
Whatever happens, `/kaggle/working/iri_verification_bundle.zip` will now exist — return
it either way.

## Third run (stopped) and fourth run (PASS) — 2026-09-19

**Third run.** Step 3 stopped cleanly with every rung's exit code and stderr on disk — the
second-revision fixes did their job. The diagnosis was uniform: `pip install virtualenv`
and `pip install uv` both failed with `Temporary failure in name resolution`, and
`apt-get` timed out. **That is what "Internet: OFF" looks like on Kaggle.** The Internet
toggle in the notebook's Settings sidebar (which needs a phone-verified Kaggle account)
was off; nothing in the notebook was at fault. In hindsight the second run's unexplained
`virtualenv` failure was the same toggle — that rung starts with a `pip install`.

**Fourth run.** The **same notebook file** (SHA-256
`b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa`) re-run with Internet
ON completed end to end. Rung 1 (`virtualenv` against the image's `/usr/bin/python3.10`,
Python 3.10.12) succeeded on the first attempt; all four wheels installed under
`--require-hashes`; the smoke test returned 37.3737545… TECU, bit-identical on repeat;
the shipped index files were unchanged after the calls; every reconciliation assertion
passed; `ok: true`. The returned `iri_verification_bundle.zip` (SHA-256
`3a0723a1ff70c213ed3cb7139cbfc02e4495d04888a00136c3e5a6c9afa6d508`) is filed verbatim at
`evidence/iri2016_kaggle_verification_2026-09-19/` and written up in
`governance/CHANGE_RECORD_2026-09-19_scientific_decisions_p3.md` §3.6.

**Consequences for this file.**
- Revision 2 — the producer of that evidence — is preserved byte-exactly at
  `evidence/iri2016_kaggle_verification_2026-09-19/kaggle_iri2016_verification.ipynb`
  (hash above). The file in this folder is now **revision 3** (see the next section),
  which has a different hash and has **not** run on Kaggle.
- Everything under "Cannot be verified without actually running on Kaggle" below is now
  verified for the 2026-09-19 Kaggle image (kernel Python 3.12.13, glibc 2.35 — exactly
  the `manylinux_2_35` floor `iricore`'s wheel requires). The list is left as written for
  the record of what was and was not claimed before the run.

## Revision 3 — 2026-09-19 — built and locally validated, NOT yet run on Kaggle

`kaggle/kaggle_iri2016_verification.ipynb` is now revision 3, SHA-256
`0e4d4478f256c37737038388b52e2a29960909657ee4fa4672774974911d2a34`, 19 cells. It does not
change the pins, the smoke test, or the environment ladder. It adds:

1. **Step 1b — network preflight** before anything is installed: DNS → TCP → TLS → HTTPS to
   `pypi.org` and `files.pythonhosted.org`, 10 s per stage. If a stage fails the notebook
   writes the bundle and stops at once, naming the host, the stage, a failure class and the
   exception. A DNS failure's message lists the Kaggle Internet setting as one *possible*
   cause to check first — the notebook cannot see that setting and does not claim it is off.
2. A **`failure_class`** on every failed command (DNS / TLS / connection / hash mismatch /
   platform tag / resolution / missing module / timeout), so a stop can be read without
   the raw log.
3. In the inner script, **`ig_rz.dat` and `apf107.dat` metadata and 2022-support checks**:
   update date, range, counts, and whether every row, month and centered window IRI-2016
   reads for a 2022 target time is present. Step 5 asserts both checks hold.

Validated locally: every cell and the inner script parse; the preflight, classifier and
index parsers were exercised on real and synthetic failures; the inner script ran end to
end against a stub `iricore` carrying the real 1.8.0 index files. **Not validated: an
actual Kaggle execution of revision 3.** Nothing in `evidence/…2026-09-19/` was produced by
it. Run it (Internet ON, CPU, Run All) before relying on it for any new evidence; the run
should reproduce the revision-2 results and additionally show the `index_files.ig_rz` and
`index_files.apf107` blocks with `support_2022.ok: true`.

## What this session verified locally, and what still needs Kaggle

**Verified locally, without Kaggle, before you got this file:**
- The notebook is valid nbformat 4 JSON; every code cell parses as syntactically valid
  Python (`ast.parse`); the embedded inner script also parses as valid Python
  independently.
- The inner script's index-file date-parsing logic was run against a real, byte-for-byte
  `apf107.dat` (downloaded from the `iricore` project's own GitHub release infrastructure
  this session) and correctly extracts the file's last covered date and picks a safe,
  non-December smoke-test date from it.
- The exact `iricore.vtec()` call signature and its array-return handling were checked
  against `iricore`'s own upstream test suite (`tests/test_tec.py`), confirming
  `hbot=`/`htop=`/`hstep=`/`version=` are the right keyword names and that a scalar
  lat/lon returns a length-1 array.
- The notebook's orchestration helpers (subprocess capture, JSON report writing, ZIP
  bundling) were exercised standalone and work correctly.
- The inner script's failure path was run end-to-end locally (with `iricore` genuinely
  absent, since it cannot be installed on this Windows machine — see
  `governance/CHANGE_RECORD_2026-09-19_scientific_decisions_p2.md` §2) and confirmed to
  print a well-formed JSON failure report with a specific `failed_stage` and exit code 1,
  exactly as the outer notebook cells expect.
- Every package pin's exact PyPI-published SHA-256 was fetched and embedded directly
  (not guessed): `numpy==1.26.4`, `fortranformat==2.0.3`, `pymap3d==3.2.0`,
  `iricore==1.8.0` — the newest `iricore` release that still publishes a Linux
  (`manylinux_2_35_x86_64`) wheel, for CPython 3.10 specifically (1.8.1–1.9.0 publish a
  macOS-arm64 wheel only, checked exhaustively against every release on PyPI).

**Cannot be verified without actually running on Kaggle, and are NOT claimed here:**
- That `iricore==1.8.0`'s wheel actually installs on Kaggle's current base image (the
  `manylinux_2_35` tag needs a reasonably recent glibc; Kaggle's exact glibc version was
  not checked from this session).
- That the installed package's `iri()`/`vtec()` calls actually execute correctly on
  Kaggle's CPU and produce a finite, physically plausible TECU value.
- Repeatability of the actual installed binary, and that its shipped index files are
  not silently refreshed by the calls.
- Whether Kaggle's kernel Python is 3.10 already, or whether the `apt-get install
  python3.10` fallback succeeds (this depends on the specific Kaggle base image in use
  at run time, which changes over time).

None of the above is claimed as verified, installed, or executed until you actually run
the notebook and this session (or you) reads back `verification_report.json`.

## The production workflow — `kaggle_iri2016_benchmark.ipynb` (2026-09-19)

**Build the package** (repository root, governed environment):

    python kaggle/build_b01_package.py

→ `kaggle/dist/tec_b01_package.zip` (prints its SHA-256 and the source commit). Upload the zip
as a **Kaggle dataset** and attach it to a new notebook; upload
`kaggle_iri2016_benchmark.ipynb`; Settings: **Internet ON, Accelerator None**; Run All.

**State on 2026-09-19 (revision `c8a1ef04…`).** Stations and `igrf_version` are transcribed
(done). Still needed before the validation step: the owner's approval of the tolerance
(`governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md`; on approval the value and the
approval instant go into `experiment.yaml`), and the eight official reference values
collected per `kaggle/b01_official_reference_collection_sheet.md` into
`kaggle/b01_validation_samples.json`; then rebuild the package. Step 6 (fixtures, real
receipts, governed 3.11 environment) runs only when frozen fixture manifests are packaged —
none exist yet. Step 7 (full year) is disabled by default (`RUN_FULL_YEAR = False` in Step 0).
The next run therefore performs: network preflight, environment, package verification,
`--verify-runtime`, and — once the two inputs above exist — `--build-validation-report`.

**What to return:** `/kaggle/working/b01_bundle.zip`. Steps 1–5 alone establish the runtime
identity and the R-59 validation report on Kaggle; step 6 adds `b01_iri2016_rows.jsonl`,
`b01_provenance.json` (with the measured workload time) and the registry rows.
