# environment/install_wheels.ps1 -- pip-wheel layer over the conda base env (TE S13.1).
#
# Purpose: install the two governed pins that have no win-64 conda-forge build --
#   matplotlib==3.9.0 (owner pin, Rec 38) and, if it ever gains a Windows artifact,
#   tensorflow==2.21.0 (D-36) -- from a verified offline wheelhouse ONLY. Every wheel
#   is SHA-256-checked against environment/wheels-win64.lock (generated at download
#   time on a connected machine; see OFFLINE_REBUILD.md) before pip sees it.
# Inputs: <ArtifactStore>\wheels\*.whl and environment/wheels-win64.lock.
# Re-run behaviour: idempotent; pip skips satisfied requirements. Refuses on any
#   missing or hash-mismatched wheel, on lock/wheelhouse absence, and on a failed
#   dependency dry-run. Never reaches a network index (--no-index everywhere).
#
# tensorflow==2.21.0, CORRECTED 2026-09-26: a native Windows wheel DOES exist --
#   tensorflow-2.21.0-cp311-cp311-win_amd64.whl (12,966 files, tag cp311-win_amd64,
#   metadata Version 2.21.0), supplied by the project owner and hash-verified against
#   the owner's stated SHA-256. The earlier "Linux-only" conclusion (inferred from
#   setup.py.tpl + tensorflow-intel history) was wrong. The wheel sits in
#   <store>\wheels-staging\ until its ~22 dependency wheels arrive (OFFLINE_REBUILD.md
#   S 'pip-wheel layer'); it enters the live wheelhouse and this lock together with
#   them. The TE S8.1 BOTH-platform check still requires the Kaggle run regardless.
#
# Primary-wheel hash pins: the two governed pins' wheels are additionally pinned
#   HERE, so a future regeneration of wheels-win64.lock cannot silently swap their
#   bytes (a redownload must reproduce these exact hashes or this script refuses).

[CmdletBinding()]
param(
    [string]$ArtifactStore = "",
    [string]$Prefix = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path $ScriptDir -Parent
if (-not $ArtifactStore) { $ArtifactStore = Join-Path $env:USERPROFILE "Tools\tec-offline" }
if (-not $Prefix) { $Prefix = Join-Path $env:LOCALAPPDATA "tec-envs\tec311" }

$py = Join-Path $Prefix "python.exe"
if (-not (Test-Path $py)) { throw "NO ENV at $Prefix -- run environment\bootstrap_env.ps1 first." }

# Hash pins for the two primary wheels (measured 2026-09-26 from the owner-supplied
# files; matplotlib pin owner-frozen per Rec 38, tensorflow per D-36).
$PrimaryPins = @{
    "matplotlib-3.9.0-cp311-cp311-win_amd64.whl"  = "a5be985db2596d761cdf0c2eaf52396f26e6a64ab46bd8cd810c48972349d1be"
    "tensorflow-2.21.0-cp311-cp311-win_amd64.whl" = "0064a19bdc054a4b7c5e7e21cdf50ce38a114c2bada578b4f5267a37410f6784"
}

$WheelLock = Join-Path $ScriptDir "wheels-win64.lock"
$Wheelhouse = Join-Path $ArtifactStore "wheels"
if (-not (Test-Path $WheelLock)) {
    Write-Host "wheels-win64.lock not present -- the pip-wheel layer has not been prepared yet."
    Write-Host "This is the documented state until a connected machine runs the download step"
    Write-Host "in environment\OFFLINE_REBUILD.md S 'pip-wheel layer'. Nothing to do."
    exit 0
}
if (-not (Test-Path $Wheelhouse)) { throw "LOCK PRESENT but wheelhouse missing: $Wheelhouse" }

# --- 1. Verify every wheel in the lock against the wheelhouse ---------------------------
$entries = @(Get-Content $WheelLock | Where-Object { $_ -match '\.whl#[0-9a-f]{64}$' } | ForEach-Object {
    $name, $sha = $_ -split '#', 2
    [pscustomobject]@{ Name = $name.Trim(); Sha256 = $sha.Trim().ToLower() }
})
if ($entries.Count -eq 0) { throw "LOCK EMPTY: no wheel lines (name.whl#sha256) in $WheelLock" }
$failures = @()
foreach ($e in $entries) {
    $f = Join-Path $Wheelhouse $e.Name
    if (-not (Test-Path $f)) { $failures += "MISSING  $($e.Name)"; continue }
    $h = (Get-FileHash $f -Algorithm SHA256).Hash.ToLower()
    if ($h -ne $e.Sha256) { $failures += "BADHASH  $($e.Name) expected=$($e.Sha256) actual=$h" }
}
# Also refuse wheels in the house that the lock does not know -- pip must never see them.
$known = $entries | ForEach-Object { $_.Name }
Get-ChildItem "$Wheelhouse\*.whl" | Where-Object { $known -notcontains $_.Name } | ForEach-Object {
    $failures += "UNLOCKED $($_.Name) -- present in wheelhouse but absent from the lock"
}
# The lock itself must agree with the primary-wheel pins above.
foreach ($p in $PrimaryPins.Keys) {
    $inLock = $entries | Where-Object { $_.Name -eq $p }
    if ($inLock -and $inLock.Sha256 -ne $PrimaryPins[$p]) {
        $failures += "PINDRIFT $p lock=$($inLock.Sha256) pinned=$($PrimaryPins[$p])"
    }
}
if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Host "  $_" }
    throw "Wheelhouse does not match wheels-win64.lock ($($failures.Count) problem(s)). Refusing."
}
Write-Host "verified: $($entries.Count)/$($entries.Count) wheels match the lock"

# --- 2. Dependency-conflict dry-run, then install, then pip check -----------------------
# Constraints from requirements.txt keep the resolver inside the governed pins
# (numpy 1.26.4 etc. stay untouched; conda owns them).
$req = Join-Path $RepoRoot "requirements.txt"
$targets = @("matplotlib==3.9.0")
if ($known -match '^tensorflow-2\.21\.0-') { $targets += "tensorflow==2.21.0" }
Write-Host "targets: $($targets -join ', ')"
& $py -m pip install --dry-run --no-index --find-links $Wheelhouse -c $req @targets
if ($LASTEXITCODE -ne 0) { throw "dependency dry-run FAILED -- resolve the conflict before installing" }
& $py -m pip install --no-index --find-links $Wheelhouse -c $req @targets
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }
& $py -m pip check
if ($LASTEXITCODE -ne 0) { throw "pip check reports broken dependencies after install" }

# --- 3. Verify imports resolve inside the prefix ----------------------------------------
& $py -c @"
import os, sys, matplotlib
p = os.path.realpath(matplotlib.__file__)
assert p.startswith(os.path.realpath(sys.prefix)), f'matplotlib resolves OUTSIDE the env: {p}'
assert matplotlib.__version__ == '3.9.0', matplotlib.__version__
print('matplotlib', matplotlib.__version__, 'OK at', p)
"@
if ($LASTEXITCODE -ne 0) { throw "matplotlib verification failed" }
if ($targets -contains "tensorflow==2.21.0") {
    & $py -c @"
import os, sys, tensorflow, ml_dtypes, numpy
p = os.path.realpath(tensorflow.__file__)
assert p.startswith(os.path.realpath(sys.prefix)), f'tensorflow resolves OUTSIDE the env: {p}'
assert tensorflow.__version__ == '2.21.0', tensorflow.__version__
assert ml_dtypes.__version__ == '0.5.3', ml_dtypes.__version__
assert numpy.__version__ == '1.26.4', 'governed numpy pin violated: ' + numpy.__version__
print('tensorflow', tensorflow.__version__, 'OK at', p)
print('ml_dtypes', ml_dtypes.__version__, '/ numpy', numpy.__version__, 'OK')
"@
    if ($LASTEXITCODE -ne 0) { throw "tensorflow verification failed" }
}

# --- 4. Evidence (TE S13.1): record the layered state -----------------------------------
$evDir = Join-Path $RepoRoot "artifacts\exec_evidence"
New-Item -ItemType Directory -Force $evDir | Out-Null
$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
& $py -m pip freeze | Out-File -Encoding utf8 (Join-Path $evDir "pip_freeze_$stamp.txt")
@(
    "pip-wheel layer installed by environment/install_wheels.ps1",
    "utc: $stamp",
    "prefix: $Prefix",
    "wheels-win64.lock sha256: $((Get-FileHash $WheelLock -Algorithm SHA256).Hash.ToLower())",
    "targets: $($targets -join ', ')",
    "tensorflow==2.21.0: $(if ($targets -contains 'tensorflow==2.21.0') {'installed from wheelhouse'} else {'ABSENT -- no native Windows artifact exists (tensorflow-intel ended at 2.18.0); owed to Kaggle'})"
) | Out-File -Encoding utf8 (Join-Path $evDir "wheel_layer_$stamp.txt")
Write-Host ""
Write-Host "DONE. Evidence: artifacts\exec_evidence\wheel_layer_$stamp.txt"
