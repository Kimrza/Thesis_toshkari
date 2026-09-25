# Offline environment rebuild (Windows win-64)

Reproducible reconstruction of the governed Python 3.11.16 environment
(TE §13.1; TC-06; TA-02) without PyPI access. This documents what
`environment/bootstrap_env.ps1` enforces; the pins themselves live in
`requirements.txt` (the single governed pin surface) and the exact solved
artifact set in `environment/conda-win64.lock` (98 conda-forge artifacts,
each line `URL#sha256`).

## Network reality on the implementation machine (measured 2026-09-26)

| Host | Status |
|---|---|
| pypi.org | **blocked** (timeout) |
| conda.anaconda.org (conda-forge) | reachable |
| repo.anaconda.com | reachable |

The repo's established reconstruction path is therefore conda-forge
(build-instructions.md, addendum 2026-09-24), not pip.

## Artifact store layout

The offline store is any directory (default `%USERPROFILE%\Tools\tec-offline`;
override with `-ArtifactStore`) shaped as:

```
<store>\
  Miniconda3-latest-Windows-x86_64.exe    # sha256 27f1f8ae8c27bc22bbc383b84bf08c63a20a6e190f3975f3502625b1045330b2
  channel\
    win-64\<artifact>.conda               # conda packages from conda-win64.lock
    noarch\<artifact>.conda               # conda packages from conda-win64.lock
  wheels\
    *.whl                                 # pip wheels from wheels-win64.lock (see "pip-wheel layer")
  wheels-staging\
    *.whl                                 # verified wheels whose dependency closure is not yet complete;
                                          # never read by the installer (the strict lock check would
                                          # otherwise refuse them as unlocked strays)
```

Two artifact kinds, two locks: `.conda` files are the base environment,
enforced by `environment/conda-win64.lock`; `.whl` files are the pip layer on
top, enforced by `environment/wheels-win64.lock`. They never mix directories.

Every `.conda` file must hash-match its lock line; the bootstrap refuses on any
missing or mismatched artifact. The store is a cache of verified upstream
bytes, **never** a copy of installed site-packages.

The store currently on this machine was populated 2026-09-26 by copying the 98
lock-referenced artifacts out of the (volatile) `Temp\30\tec\mc3\pkgs` conda
cache, verifying each SHA-256 against the lock before copy: 98/98 verified,
0 missing, 0 mismatched.

## Rebuild command

```powershell
# offline, from the verified store (default mode):
powershell -ExecutionPolicy Bypass -File environment\bootstrap_env.ps1

# online fallback (conda-forge reachable; still hash-enforced by the lock):
powershell -ExecutionPolicy Bypass -File environment\bootstrap_env.ps1 -Online
```

Default target prefix: `%LOCALAPPDATA%\tec-envs\tec311` — **outside the
repository by requirement**: the suite's tree-walking containment scanners
(`tests/test_iri_denial.py`, phase-boundary siblings) exclude `.venv` by name
but AST-parse everything else under the repo root, so an in-repo conda env
stalls the suite (measured 2026-09-26: >30 min inside scipy site-packages).
The script refuses an in-repo prefix. The script
installs Miniconda user-scoped into the store if no conda exists, verifies the
installer hash first, creates the env with `conda create --file <lock> --offline`
(URLs rewritten to `file:///` into the store), then verifies: Python 3.11.16
exactly, 64-bit, all pinned imports resolve **inside the prefix** (never the
shared `Tools\Python311` directory — no `.pth`, no `PYTHONPATH`), and emits the
TE §13.1 environment-lock evidence under `artifacts\exec_evidence\`.

## Populating the store on a connected machine

If the store is lost, regenerate it anywhere with unrestricted egress:

```powershell
# 1. Miniconda installer
Invoke-WebRequest https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile Miniconda3-latest-Windows-x86_64.exe
Get-FileHash .\Miniconda3-latest-Windows-x86_64.exe -Algorithm SHA256
# NOTE: "latest" moves. Either verify against the sha256 pinned at the top of
# bootstrap_env.ps1, or download that exact release from
# https://repo.anaconda.com/miniconda/ and update the pinned hash in the script
# as a reviewed change.

# 2. Every artifact in the lock, byte-exact (run from the repo root):
New-Item -ItemType Directory -Force channel\win-64, channel\noarch | Out-Null
Get-Content environment\conda-win64.lock | Where-Object { $_ -match '^https://' } | ForEach-Object {
  $url, $sha = $_ -split '#'
  $sub = ($url -split '/')[-2]; $name = ($url -split '/')[-1]
  Invoke-WebRequest $url -OutFile "channel\$sub\$name"
  $h = (Get-FileHash "channel\$sub\$name" -Algorithm SHA256).Hash.ToLower()
  if ($h -ne $sha) { throw "hash mismatch for $name" }
}
```

Then move `channel\` and the installer into the store directory on the target
machine (USB, file share — bytes only, verified again on arrival by the
bootstrap).

## pip-wheel layer (matplotlib) — prepared on a connected machine

`matplotlib==3.9.0` is an owner-frozen pin (Recommendation 38) with **no win-64
conda-forge build** (the channel jumps 3.8.4 → later; do **not** substitute
3.9.2). It IS available from PyPI for this environment: `requires-python >=3.9`
and the cp311/win_amd64 wheel exist (verified 2026-09-26 against the official
`v3.9.0` tag, `https://github.com/matplotlib/matplotlib/blob/v3.9.0/pyproject.toml`).
Its runtime dependencies (from that tag, verbatim): contourpy>=1.0.1,
cycler>=0.10, fonttools>=4.22.0, kiwisolver>=1.3.1, numpy>=1.23,
packaging>=20.0, pillow>=8, pyparsing>=2.3.1, python-dateutil>=2.7 (the
importlib-resources entry applies to Python <3.10 only).

**Since 2026-09-26 matplotlib is fully installable offline from this store.**
Its six missing dependencies were added as conda-forge packages (contourpy,
cycler, fonttools, kiwisolver, pillow, pyparsing plus their 15 native libs —
`conda-win64.lock` grew 98 → 119, strictly additive, governed pins untouched),
the owner-supplied wheel `matplotlib-3.9.0-cp311-cp311-win_amd64.whl` (SHA-256
`a5be985db2596d761cdf0c2eaf52396f26e6a64ab46bd8cd810c48972349d1be`) sits in
`<store>\wheels\`, and `environment/wheels-win64.lock` carries its measured
hash. `install_wheels.ps1` installs it with `--no-index --no-deps`-equivalent
resolution (all deps pre-satisfied) under `-c requirements.txt` constraints.

**Regenerating the wheelhouse from scratch** (only needed if the store is
lost). On a machine with PyPI access, from a checkout of this repo (pip
verifies every download against the index digests over TLS), ONE command
fetches the complete set — the `-c` constraints force the owner-approved
`ml_dtypes==0.5.3` (see the tensorflow section below), and the two primary
wheels MUST reproduce the pinned hashes embedded in `install_wheels.ps1`:

```powershell
py -3.11 -m pip download matplotlib==3.9.0 tensorflow==2.21.0 -c requirements.txt `
  --only-binary=:all: --platform win_amd64 --python-version 3.11 --implementation cp -d wheels
```

Then regenerate the lock over the complete set:

```powershell
Get-ChildItem wheels\*.whl | ForEach-Object {
  "$($_.Name)#$((Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower())"
} | Out-File -Encoding ascii environment\wheels-win64.lock
```

Transfer the `wheels\` directory into `<store>\wheels\` on the target machine
(bytes only — they are re-verified there; the previously staged
`<store>\wheels-staging\tensorflow-...whl` becomes redundant and can be
deleted after the installer passes), commit the regenerated
`environment/wheels-win64.lock`, and run:

```powershell
powershell -ExecutionPolicy Bypass -File environment\install_wheels.ps1
```

verifies every wheel's SHA-256 against the lock (and refuses unlocked strays),
dry-runs the resolver with `-c requirements.txt` as constraints, installs with
`--no-index`, runs `pip check`, asserts the import resolves inside the prefix,
and emits evidence. `bootstrap_env.ps1` calls the same script at the end of
every rebuild, so a from-scratch offline rebuild includes the layer once the
lock and wheelhouse exist; before then the step reports itself unprepared and
exits 0.

Browse-verification links (real, on PyPI): the release file list is at
<https://pypi.org/project/matplotlib/3.9.0/#files> — the wheel this procedure
installs is `matplotlib-3.9.0-cp311-cp311-win_amd64.whl`. Per-file SHA-256
values are shown on that page; no hash is copied into this document by hand —
the lock is generated from the downloaded bytes, and pip has already verified
those bytes against PyPI's digests.

## tensorflow==2.21.0 — Windows wheel EXISTS (corrected 2026-09-26)

**Correction.** An earlier revision of this section concluded no native Windows
artifact exists, inferred from `setup.py.tpl` at tag `v2.21.0` (which routes
Windows to `tensorflow-intel`) and from `tensorflow-intel` ending at 2.18.0.
That inference was **wrong**: the project owner supplied
`tensorflow-2.21.0-cp311-cp311-win_amd64.whl` (SHA-256
`0064a19bdc054a4b7c5e7e21cdf50ce38a114c2bada578b4f5267a37410f6784`, 334.6 MB),
downloaded from PyPI (<https://pypi.org/project/tensorflow/2.21.0/#files>).
The file's own metadata confirms it: tag `cp311-cp311-win_amd64`, Version
2.21.0, 12,966 archive members. Provenance note, recorded honestly: PyPI is
unreachable from this machine, so the hash was verified against the owner's
attestation and the wheel's internal structure, not against the PyPI page
directly; any connected machine re-downloading it must reproduce that exact
hash (`install_wheels.ps1` enforces this via its embedded primary pins).

**Installed 2026-09-26.** The dependency closure (30 wheels) was transferred
from a connected machine, verified (archive integrity, tags, per-file SHA-256),
assembled into `<store>\wheels\`, locked in `environment/wheels-win64.lock`
(32 lines: tensorflow + 30 deps + matplotlib, all measured hashes), and
installed offline by `install_wheels.ps1`: dry-run clean, `pip check` clean,
`tensorflow 2.21.0` importing from inside the prefix, CPU-only devices
(exactly the TC-01 posture), functional smoke (matmul + Keras forward pass)
passed. The copy in `<store>\wheels-staging\` is now a redundant duplicate.

**ml_dtypes==0.5.3 — owner-approved engineering pin (2026-09-26), recorded in
`requirements.txt`.** The closure pip's resolver selects by default carries
`ml_dtypes 0.6.0`, which requires `numpy>=2.0.0` and therefore conflicts with
the governed `numpy==1.26.4` (an unconstrained install would have upgraded
numpy to the also-downloaded 2.4.6 wheel). The owner approved pinning
`ml_dtypes==0.5.3` (TF permits `>=0.5.1,<1.0.0`; 0.5.3 needs only
`numpy>=1.23.3` on Python 3.11). The rejected `ml_dtypes-0.6.0` and
`numpy-2.4.6` wheels were deliberately excluded from the wheelhouse and the
lock; the installer's constraint file (`-c requirements.txt`) enforces the pin
on every future run. A future regeneration of the wheelhouse on a connected
machine must download with the repo's `requirements.txt` constraints
(`-c requirements.txt`) so the resolver picks 0.5.3, not 0.6.x.

The TE §8.1 **both-platform** check is unchanged by all of this: a local
Windows install, once it exists, satisfies the local half only; the Kaggle
(Linux) run remains required.

## What is deliberately NOT in Git

Per repo policy (environments and large binaries stay out of version control):
the artifact store (`channel\` and `wheels\`), the Miniconda installer, the
environment prefixes, and `.venv/`. In Git: this file, `bootstrap_env.ps1`,
`install_wheels.ps1`, `conda-win64.lock`, `wheels-win64.lock` (once generated),
`requirements.txt`.
