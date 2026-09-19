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
| Producing notebook | `kaggle/kaggle_iri2016_verification.ipynb` at SHA-256 `b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa` (the second-revision notebook; unchanged between the third, stopped run and this fourth, passing run) |
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
  `apf107.dat`'s last covered date is **2024-03-06** — see the note below.
- Smoke test: `iricore.vtec(2024-01-06T12:00:00, lat=40.286, lon=44.086, hbot=90.0,
  htop=2000.0, hstep=0.5, version=16)` → `37.373754526924806` TECU, finite, inside
  `[0, 200]`, **bit-identical on the repeated call**.

**Note — index-file coverage differs from the earlier source inspection.**
`CR-2026-09-19-SCI-DECISIONS` §3 (and D-45 item 2, which cites it) recorded the shipped
`apf107.dat` as ending `2024-06-17` and `ig_rz.dat` as "updated 6/2024"; those values
were read from the `master` branch / 1.9.0 sources and the GitHub release
infrastructure, not from the 1.8.0 wheel. The 1.8.0 wheel actually installed ships an
`apf107.dat` ending `2024-03-06` — different bytes, so a different freeze pin. Both copies
cover calendar 2022. The installed `ig_rz.dat`'s own update month was **not** read by the
notebook (it was hashed only) and is therefore not claimed here. The hashes above are the
candidate D-45 freeze pins **for release 1.8.0 specifically**; D-45 is a countersigned
record and is not edited by this filing — the proposed annotation is in
`governance/CHANGE_RECORD_2026-09-19_scientific_decisions_p3.md` §3.6.

**What it does NOT establish.** No GNSS/VTEC target value was read; no full-year or
multi-station run occurred; no producer artifact, `write_release` call or
`permitted_producers` entry exists; R-59 limb 1 (a passing validation report for the
benchmark) is untouched; G-04 is not passed.
