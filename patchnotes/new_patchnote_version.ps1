param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [string]$Date = (Get-Date -Format 'yyyy-MM-dd'),

    [switch]$Force
)

$ErrorActionPreference = 'Stop'

function Normalize-Version {
    param([string]$RawVersion)

    $v = $RawVersion.Trim()
    if (-not $v.StartsWith('v')) {
        $v = "v$v"
    }

    if ($v -notmatch '^v\d+\.\d+\.\d+$') {
        throw "Version invalide '$RawVersion'. Format attendu: vMAJOR.MINOR.PATCH"
    }

    return $v
}

$versionTag = Normalize-Version -RawVersion $Version
$patchnotesDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $patchnotesDir

$patchnoteFileName = "patchnote_$versionTag.md"
$patchnotePath = Join-Path $patchnotesDir $patchnoteFileName

if ((Test-Path $patchnotePath) -and -not $Force) {
    throw "Le fichier existe deja: $patchnotePath (utilise -Force pour ecraser)"
}

$patchnoteContent = @"
# Patchnote Gameplay - $versionTag

- Version: $versionTag
- Date: $Date
- Comparaison: K-Mod Karadoc -> version actuelle du mod.
- Resume cumulatif: [patchnote_full.md](../patchnote_full.md)

## Changements globaux
- A completer.

## Changements par civilisation (ordre alphabetique FR)
- A completer.
"@

Set-Content -Path $patchnotePath -Value $patchnoteContent -Encoding UTF8

$readmePath = Join-Path $patchnotesDir 'README.md'
if (-not (Test-Path $readmePath)) {
    @"
# Historique des Patchnotes

Derniere version: $versionTag ($Date)

## Versions
"@ | Set-Content -Path $readmePath -Encoding UTF8
}

$readmeLines = [System.Collections.Generic.List[string]](Get-Content -Path $readmePath)

$latestIndex = -1
for ($i = 0; $i -lt $readmeLines.Count; $i++) {
    if ($readmeLines[$i] -like 'Derniere version:*') {
        $latestIndex = $i
        break
    }
}

$latestLine = "Derniere version: $versionTag ($Date)"
if ($latestIndex -ge 0) {
    $readmeLines[$latestIndex] = $latestLine
}
else {
    $insertAt = [Math]::Min(2, $readmeLines.Count)
    $readmeLines.Insert($insertAt, $latestLine)
    if ($insertAt + 1 -lt $readmeLines.Count -and $readmeLines[$insertAt + 1] -ne '') {
        $readmeLines.Insert($insertAt + 1, '')
    }
}

$versionsHeader = '## Versions'
$versionsIndex = -1
for ($i = 0; $i -lt $readmeLines.Count; $i++) {
    if ($readmeLines[$i] -eq $versionsHeader) {
        $versionsIndex = $i
        break
    }
}

if ($versionsIndex -lt 0) {
    if ($readmeLines.Count -gt 0 -and $readmeLines[$readmeLines.Count - 1] -ne '') {
        $readmeLines.Add('')
    }
    $readmeLines.Add($versionsHeader)
    $versionsIndex = $readmeLines.Count - 1
}

$newEntry = "- [$versionTag - Patchnote]($patchnoteFileName)"
$alreadyExists = $false
for ($i = 0; $i -lt $readmeLines.Count; $i++) {
    if ($readmeLines[$i] -eq $newEntry) {
        $alreadyExists = $true
        break
    }
}

if (-not $alreadyExists) {
    $readmeLines.Insert($versionsIndex + 1, $newEntry)
}

Set-Content -Path $readmePath -Value $readmeLines -Encoding UTF8

$fullPath = Join-Path $repoRoot 'patchnote_full.md'
if (-not (Test-Path $fullPath)) {
    throw "Fichier introuvable: $fullPath"
}

$fullRaw = Get-Content -Raw -Path $fullPath
$headerMatch = [regex]::Match($fullRaw, '(?ms)^# .*?(?=^## )')
if (-not $headerMatch.Success) {
    throw 'Impossible de mettre a jour les metadonnees de patchnote_full.md (section ## introuvable).'
}

$newFullHeader = @"
# Patchnote Gameplay Complet (cumulatif)

- Derniere version patchnote: $versionTag
- Derniere mise a jour: $Date
- Comparaison: K-Mod Karadoc -> version actuelle du mod.
- Historique versions: [patchnotes/README.md](patchnotes/README.md)

"@

$fullUpdated = $newFullHeader + $fullRaw.Substring($headerMatch.Length)
Set-Content -Path $fullPath -Value $fullUpdated -Encoding UTF8

Write-Host "Patchnote cree: $patchnotePath"
Write-Host "README mis a jour: $readmePath"
Write-Host "Metadonnees mises a jour: $fullPath"
