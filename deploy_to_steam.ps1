param(
    [string]$ModsRoot = "C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword\Beyond the Sword\Mods",
    [string]$ModName = "K-Mod",
    [switch]$UseBuiltDll,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetRoot = Join-Path $ModsRoot $ModName

if (-not (Test-Path $ModsRoot)) {
    throw "Mods root folder not found: $ModsRoot"
}

if (-not $DryRun) {
    New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
} else {
    Write-Host "DRY RUN: target mod folder would be $targetRoot"
}

$runtimeDirs = @(
    "Assets",
    "Info",
    "PublicMaps",
    "Settings"
)

foreach ($dir in $runtimeDirs) {
    $src = Join-Path $repoRoot $dir
    $dst = Join-Path $targetRoot $dir

    if (-not (Test-Path $src)) {
        throw "Missing source directory: $src"
    }

    $args = @(
        $src,
        $dst,
        "/MIR",
        "/R:2",
        "/W:1",
        "/NFL",
        "/NDL",
        "/NP",
        "/NJH",
        "/NJS",
        "/XJ"
    )

    if ($DryRun) {
        $args += "/L"
    }

    & robocopy @args
    $exitCode = $LASTEXITCODE
    if ($exitCode -ge 8) {
        throw "Robocopy failed for '$dir' with exit code $exitCode"
    }
}

$runtimeFiles = @(
    "K-Mod.ini",
    "K-Mod 2.ini",
    "K-Mod 2.ini.bak",
    "changelog.txt",
    "readme.txt"
)

foreach ($file in $runtimeFiles) {
    $src = Join-Path $repoRoot $file
    $dst = Join-Path $targetRoot $file

    if (-not (Test-Path $src)) {
        throw "Missing source file: $src"
    }

    if ($DryRun) {
        Write-Host "DRY RUN: copy $src -> $dst"
    } else {
        Copy-Item -Path $src -Destination $dst -Force
    }
}

if ($UseBuiltDll) {
    $builtDll = Join-Path $repoRoot "CvGameCoreDLL\Release\CvGameCoreDLL.dll"
    $targetDll = Join-Path $targetRoot "Assets\CvGameCoreDLL.dll"

    if (-not (Test-Path $builtDll)) {
        throw "Built DLL not found: $builtDll"
    }

    if ($DryRun) {
        Write-Host "DRY RUN: copy $builtDll -> $targetDll"
    } else {
        Copy-Item -Path $builtDll -Destination $targetDll -Force
    }
}

Write-Host "Deploy complete: $targetRoot"
