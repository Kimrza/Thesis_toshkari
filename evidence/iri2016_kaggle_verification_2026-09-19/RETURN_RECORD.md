# Returned Kaggle verification bundle — IRI-2016 / `iricore==1.8.0` — 2026-09-19

**What this directory is.** The diagnostic verification bundle produced by
`kaggle/kaggle_iri2016_verification.ipynb` on Kaggle and returned by the project owner /
student (Kimia Rezaei) on 2026-09-19, filed verbatim. It is a **diagnostic
installation/runtime report** under `CR-2026-09-19-SCI-DECISIONS-P3` §3 — **not** a
producer release, **not** a registered benchmark artifact, **not** a G-04 pass
(`verification_report.json["boundaries"]` records all four boundary flags as `false`).

**Provenance.**

| Item | Value |
|---|---|
| Returned file | `iri_verification_bundle.zip`, downloaded from the Kaggle notebook output pane; SHA-256 `3a0723a1ff70c213ed3cb7139cbfc02e4495d04888a00136c3e5a6c9afa6d508` |
| Members | `verification_report.json`, `iri_inner_verify.py`, `requirements-iri.txt` — extracted copies here are byte-identical to the zip members (checked by SHA-256 at filing; see `sha256_manifest.json`) |
| Producing notebook | **revision 2**, SHA-256 `b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa`, preserved byte-exactly in this directory as `kaggle_iri2016_verification.ipynb` (regenerated from its own builder and hash-verified; unchanged between the third, stopped run and this fourth, passing run). The live file `kaggle/kaggle_iri2016_verification.ipynb` is now **revision 3** (SHA-256 `0e4d4478f256c37737038388b52e2a29960909657ee4fa4672774974911d2a34`), which has **not** run on Kaggle and produced none of this evidence. |
| Kaggle session | CPU, **Internet ON**; report `generated_at_utc` `2026-09-19T17:35:33Z` |
| Filed by | this session, 2026-09-19, from the owner's `Downloads/` copy; nothing in the three member files was edited |

**What the bundle establishes** (every value below is read from
`verification_report.json`, not restated from memory):

- Kaggle kernel: Python `3.12.13`, `/usr/bin/python3`, `Linux-6.12.90+-x86_64-with-glibc2.35`.
- Isolated environment: `virtualenv` against the image's `/usr/bin/python3.10`
  (Python `3.10.12`), seeded `pip==26.2.1`, `setuptools==84.0.0`; all three rung-1
  attempts exit 0, no timeouts; rungs 2–3 never needed.
- `pip install --no-deps --require-hashes` exit 0; the four wheels resolved were
  `numpy-1.26.4-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`,
  `fortranformat-2.0.3-py3-none-any.whl`, `pymap3d-3.2.0-py3-none-any.whl`,
  `iricore-1.8.0-cp310-cp310-manylinux_2_35_x86_64.whl`; `pip freeze` lists exactly those
  four at those versions. Kaggle's glibc `2.35` sits exactly at the `manylinux_2_35`
  floor the `iricore` wheel requires.
- Inner verification exit 0, `_stage: done`, `ok: true`; `iricore` dist version `1.8.0`
  (no `__version__` attribute); installed `DEFAULT_IRI_VERSION == 20`, matching the
  pre-Kaggle source inspection, so passing `version=16` explicitly remains necessary.
- Shipped index files as installed from the **1.8.0 wheel**
  (`.../site-packages/iricore/data/index/`):
  `apf107.dat` SHA-256 `cdf4d5dffe6d05eaae9ed90532cddea4c3cf2fdad255d837e660018cae60e674`,
  `ig_rz.dat` SHA-256 `fbbed3049483ac445070cc63841b7d14aa2929894eb725bdf946889840a41486`;
  both **unchanged** after the smoke-test calls (no silent refresh).
  `apf107.dat`'s last covered date is **2024-03-06** (the run parsed that; `ig_rz.dat`'s
  update date was read afterwards from the same bytes — see the index-files section).
- Smoke test: `iricore.vtec(2024-01-06T12:00:00, lat=40.286, lon=44.086, hbot=90.0,
  htop=2000.0, hstep=0.5, version=16)` → `37.373754526924806` TECU, finite, inside
  `[0, 200]`, **bit-identical on the repeated call**.

**Index files — metadata, coverage, and comparison with the earlier source inspection
(completed 2026-09-19 after the return; `index_comparison_report.json`, `index_files/`,
`iri_index_checks.py` in this directory).** The installed 1.8.0 wheel was re-downloaded
from PyPI (hash `f452b223…` verified) and its two index files hash exactly to the values the
Kaggle run reported, so the bytes below are the installed bytes. `apf107.dat`: 24,172
contiguous daily rows 1958-01-01 → 2024-03-06. `ig_rz.dat`: header `3,7,2024` = update
date 2024-03-07 (month-day-year, the file's convention), range 1958-01 → 2024-10, 804
values each of IG12 and Rz12. For every 2022 target time the rows and months the compiled
IRI-2016 reads (`APF` to UT−39 h, `APF_ONLY` previous day, `tcon` previous/next month) are
present and non-negative, and the centered 81-/365-day and 12-month windows behind them
lie inside the file (2022 rows' centered columns recompute from the daily column within
0.05). The copies `CR-2026-09-19-SCI-DECISIONS` §3 inspected (GitHub `master` at commit
`92c6d8c727b0300d8bd61e7e8e91dd97514256a7` and the PyPI 1.9.0 sdist, byte-identical index
files: `apf107.dat` `4de3bfa2…` ending 2024-06-17, `ig_rz.dat` `e688620c…` updated
2024-06-18) differ from the installed ones **only** from 2023-09-08 (`apf107.dat`, 176 of
24,172 common rows) and 2023-09 → 2024-11 (`ig_rz.dat`, 15 of 804 months) — outside every
window a 2022 target time touches. The installed files are the D-45 freeze pins for
release 1.8.0 (annotation recorded under D-45 on the owner's authorization, 2026-09-19).

**What it does NOT establish.** No GNSS/VTEC target value was read; no full-year or
multi-station run occurred; no producer artifact, `write_release` call or
`permitted_producers` entry exists; R-59 limb 1 (a passing validation report for the
benchmark) is untouched; G-04 is not passed.

**Directory contents.** `iri_verification_bundle.zip` and its three members (the return);
`kaggle_iri2016_verification.ipynb` (revision 2, the producer, hash above);
`index_files/installed_iricore-1.8.0_wheel/` and
`index_files/historical_master-92c6d8c7_and_1.9.0-sdist/` (the two `apf107.dat` /
`ig_rz.dat` pairs compared); `iri_index_checks.py` (the parser/comparison code, also
embedded verbatim in notebook revision 3); `index_comparison_report.json` (its output);
`validation/` (the scripts that produced revision 3 and validated it, as run, with a README); `sha256_manifest.json` + `sha256_manifest_meta.json`; this file.
