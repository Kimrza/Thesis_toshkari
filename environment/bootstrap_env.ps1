# environment/bootstrap_env.ps1 -- reproducible environment bootstrap (TE S13.1; TC-06; TA-02).
#
# Purpose: rebuild the governed Python environment from the hash-locked explicit
#   spec `environment/conda-win64.lock`, installing ONLY from a verified local
#   artifact store (offline) or, with -Online, from conda-forge. Every artifact's
#   SHA-256 is enforced against the lock before installation; a mismatch stops
#   the run naming the file and the violated expectation (project.md S Mandated).
# Inputs: environment/conda-win64.lock (this repo); an artifact store directory
#   holding the .conda files under channel\win-64 and channel\noarch, plus
#   optionally the Miniconda installer (see environment/OFFLINE_REBUILD.md).
# Re-run behaviour: idempotent up to -Prefix; refuses to overwrite an existing
#   prefix unless -Force. Creates no .pth links, sets no PYTHONPATH, and never
#   touches the shared C:\Users\<user>\Tools\Python311 installation.
#
# Known governed deviations (build-instructions.md addendum 2026-09-24):
#   matplotlib==3.9.0 has no win-64 conda-forge build (do NOT substitute 3.9.2);
#   tensorflow==2.21.0 has no Windows conda build. Both are absent from this
#   lock; the suite is written to run in both states. The environment-lock
#   evidence emitted at the end records these absences explicitly.

[CmdletBinding()]
param(
    [string]$ArtifactStore = "",
    [string]$Prefix = "",
    [string]$CondaExe = "",
    [switch]$Online,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path $ScriptDir -Parent
if (-not $ArtifactStore) { $ArtifactStore = Join-Path $env:USERPROFILE "Tools\tec-offline" }
# The prefix must live OUTSIDE the repository: the suite's tree-walking scanners
# (run_containment_scan in tests/test_iri_denial.py and its phase-boundary siblings)
# exclude ".venv" by name but would otherwise AST-parse every .py under an in-repo
# environment -- measured 2026-09-26 as a >30-minute stall on scipy/sklearn site-packages.
if (-not $Prefix) { $Prefix = Join-Path $env:LOCALAPPDATA "tec-envs\tec311" }
if (([System.IO.Path]::GetFullPath($Prefix)).StartsWith([System.IO.Path]::GetFullPath($RepoRoot), [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "PREFIX INSIDE REPO: $Prefix -- the suite's containment scanners walk the repository tree; place the environment outside it."
}
$LockFile = Join-Path $ScriptDir "conda-win64.lock"
$MinicondaSha256 = "27f1f8ae8c27bc22bbc383b84bf08c63a20a6e190f3975f3502625b1045330b2"

if (-not (Test-Path $LockFile)) { throw "LOCK MISSING: $LockFile -- the governed explicit lock is required." }
if ($env:PROCESSOR_ARCHITECTURE -ne "AMD64") { throw "ARCH MISMATCH: lock is win-64 (AMD64); this machine is $env:PROCESSOR_ARCHITECTURE." }

if ((Test-Path $Prefix) -and -not $Force) {
    throw "PREFIX EXISTS: $Prefix -- pass -Force to remove and rebuild, or choose another -Prefix."
}

# --- 1. Locate or install conda ---------------------------------------------------------
if (-not $CondaExe) {
    $candidates = @(
        (Join-Path $ArtifactStore "mc3\Scripts\conda.exe"),
        "$env:USERPROFILE\miniconda3\Scripts\conda.exe",
        "C:\Users\s_sch\AppData\Local\Temp\30\tec\mc3\Scripts\conda.exe"
    )
    foreach ($c in $candidates) { if (Test-Path $c) { $CondaExe = $c; break } }
}
if (-not $CondaExe -or -not (Test-Path $CondaExe)) {
    $installer = Join-Path $ArtifactStore "Miniconda3-latest-Windows-x86_64.exe"
    if (-not (Test-Path $installer)) {
        throw "NO CONDA and NO INSTALLER: place the Miniconda installer at $installer (see OFFLINE_REBUILD.md) or pass -CondaExe."
    }
    $h = (Get-FileHash $installer -Algorithm SHA256).Hash.ToLower()
    if ($h -ne $MinicondaSha256) {
        throw "INSTALLER HASH MISMATCH: $installer`n  expected $MinicondaSha256`n  actual   $h`nDo not proceed with an unverified installer."
    }
    $mc3 = Join-Path $ArtifactStore "mc3"
    Write-Host "Installing Miniconda (user-scoped, no PATH changes) to $mc3 ..."
    Start-Process $installer -ArgumentList "/S","/InstallationType=JustMe","/AddToPath=0","/RegisterPython=0","/D=$mc3" -Wait
    $CondaExe = Join-Path $mc3 "Scripts\conda.exe"
    if (-not (Test-Path $CondaExe)) { throw "Miniconda install did not produce $CondaExe" }
}
Write-Host "conda: $CondaExe ($(& $CondaExe --version))"

# --- 2. Verify artifacts against the lock; build the install spec -----------------------
$entries = Get-Content $LockFile | Where-Object { $_ -match '^https://' } | ForEach-Object {
    $url, $sha = $_ -split '#', 2
    [pscustomobject]@{
        Url    = $url
        Sha256 = $sha.Trim().ToLower()
        Name   = ($url -split '/')[-1]
        Subdir = ($url -split '/')[-2]
    }
}
if ($entries.Count -eq 0) { throw "LOCK EMPTY: no artifact lines in $LockFile" }
Write-Host "lock: $($entries.Count) artifacts"

$specLines = @("@EXPLICIT")
if ($Online) {
    Write-Host "MODE: online -- conda will download from conda-forge and verify each SHA-256 anchor."
    $specLines += Get-Content $LockFile | Where-Object { $_ -match '^https://' }
} else {
    Write-Host "MODE: offline -- installing only from $ArtifactStore\channel"
    $failures = @()
    foreach ($e in $entries) {
        $local = Join-Path $ArtifactStore "channel\$($e.Subdir)\$($e.Name)"
        if (-not (Test-Path $local)) { $failures += "MISSING  $($e.Subdir)\$($e.Name)"; continue }
        $h = (Get-FileHash $local -Algorithm SHA256).Hash.ToLower()
        if ($h -ne $e.Sha256) { $failures += "BADHASH  $($e.Subdir)\$($e.Name) expected=$($e.Sha256) actual=$h"; continue }
        $uri = ([System.Uri]$local).AbsoluteUri   # file:///C:/... form
        $specLines += "$uri#$($e.Sha256)"
    }
    if ($failures.Count -gt 0) {
        Write-Host "ARTIFACT VERIFICATION FAILED for $($failures.Count) of $($entries.Count):"
        $failures | ForEach-Object { Write-Host "  $_" }
        throw "Refusing to build from an incomplete or unverified store. Fix the store (OFFLINE_REBUILD.md) and re-run."
    }
    Write-Host "verified: $($entries.Count)/$($entries.Count) artifacts match the lock"
}
$specFile = Join-Path $env:TEMP ("tec311-explicit-{0}.txt" -f [guid]::NewGuid().ToString("N").Substring(0,8))
$specLines | Out-File -Encoding ascii $specFile

# --- 3. Create the environment ----------------------------------------------------------
if ((Test-Path $Prefix) -and $Force) { Remove-Item -Recurse -Force $Prefix }
# --override-channels: keep conda away from repo.anaconda.com defaults (whose ToS
# gate blocks non-interactive runs); every artifact is pinned by URL+sha256 anyway.
$condaArgs = @("create", "-p", $Prefix, "--file", $specFile, "-y", "--override-channels", "-c", "conda-forge")
if (-not $Online) { $condaArgs += "--offline" }
& $CondaExe @condaArgs
if ($LASTEXITCODE -ne 0) { throw "conda create failed with exit code $LASTEXITCODE" }
Remove-Item $specFile -Force

# --- 4. Verify the reconstruction (build-instructions.md Step 2) ------------------------
$py = Join-Path $Prefix "python.exe"
& $py -V
& $py -c "import platform,struct; assert struct.calcsize('P')*8==64, 'not 64-bit'; print('arch', platform.machine())"
& $py -c "import sys; assert sys.version_info[:3]==(3,11,16), sys.version; print('python pin OK', sys.version.split()[0])"
& $py -c "import numpy, pandas, yaml, sklearn, pyarrow, pytest; print('imports OK')"
& $py -c @"
import numpy, pandas, yaml, sklearn, pyarrow, pytest, os, sys
prefix = os.path.realpath(sys.prefix)
for m in (numpy, pandas, yaml, sklearn, pyarrow, pytest):
    p = os.path.realpath(m.__file__)
    assert p.startswith(prefix), f'{m.__name__} resolves OUTSIDE the env: {p}'
assert not any('Tools' in (e or '') and 'Python311' in (e or '') for e in sys.path), 'shared Tools site-packages leaked into sys.path'
print('module isolation OK -- all imports resolve inside', prefix)
"@
if ($LASTEXITCODE -ne 0) { throw "verification failed" }

# --- 5. Emit the TE S13.1 environment-lock evidence --------------------------------------
$evDir = Join-Path $RepoRoot "artifacts\exec_evidence"
New-Item -ItemType Directory -Force $evDir | Out-Null
$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
$reqSha = (Get-FileHash (Join-Path $RepoRoot "requirements.txt") -Algorithm SHA256).Hash.ToLower()
$lockSha = (Get-FileHash $LockFile -Algorithm SHA256).Hash.ToLower()
& $CondaExe list -p $Prefix | Out-File -Encoding utf8 (Join-Path $evDir "conda_list_$stamp.txt")
@(
    "environment lock (TE S13.1) -- emitted by environment/bootstrap_env.ps1",
    "utc: $stamp",
    "prefix: $Prefix",
    "requirements.txt sha256: $reqSha",
    "environment/conda-win64.lock sha256: $lockSha",
    "mode: $(if ($Online) {'online (conda-forge)'} else {'offline (verified local store)'})",
    "governed deviations, disclosed per addendum 2026-09-24:",
    "  matplotlib==3.9.0 ABSENT (no win-64 conda-forge build; owner pin -- do not substitute)",
    "  tensorflow==2.21.0 ABSENT (no Windows conda build; PyPI unreachable; owed to Kaggle)"
) | Out-File -Encoding utf8 (Join-Path $evDir "environment_lock_$stamp.txt")
# --- 6. pip-wheel layer (matplotlib), if prepared ----------------------------------------
# install_wheels.ps1 exits 0 with a message when environment/wheels-win64.lock does not
# exist yet (the documented pre-download state); it hash-verifies and installs when it does.
& (Join-Path $ScriptDir "install_wheels.ps1") -ArtifactStore $ArtifactStore -Prefix $Prefix
if ($LASTEXITCODE -ne 0) { throw "wheel layer failed (see install_wheels.ps1 output)" }

Write-Host ""
Write-Host "DONE. Environment at $Prefix"
Write-Host "Evidence: artifacts\exec_evidence\environment_lock_$stamp.txt and conda_list_$stamp.txt"
Write-Host "Run the suite: `"$py`" -m pytest tests/ -q"
