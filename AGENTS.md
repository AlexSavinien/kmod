# AGENTS.md - Compilation et Deploiement K-Mod

Ce document definit le workflow de reference pour recompiler la DLL C++ du mod puis deployer le mod dans Steam.

## Objectif

- Recompiler `CvGameCoreDLL.dll` a partir de `CvGameCoreDLL/*`.
- Deployer le mod dans:
  - `C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword\Beyond the Sword\Mods\K-Mod`

## Prerequis

- `Microsoft Visual C++ Toolkit 2003`
- `Microsoft Platform SDK`
- Dependances Civ4 SDK (Boost/Python/fastdep) disponibles dans:
  - `C:\Dev\Civ4 SDK\CvGameCoreDLL`

Le script `CvGameCoreDLL/build_kmod.cmd` utilise ces chemins par defaut et accepte des overrides via variables d'environnement:
- `TOOLKIT`
- `PSDK`
- `NMAKE_EXE`
- `CIV4_SDK_DEPS`
- `CVTRES_DIR`

## Compilation (workflow standard)

Depuis `C:\Dev\kmod new\CvGameCoreDLL`:

```bat
build_kmod.cmd Release
```

Autres options:

```bat
build_kmod.cmd Debug
build_kmod.cmd Profile
build_kmod.cmd clean
```

Sortie attendue:
- `CvGameCoreDLL\Release\CvGameCoreDLL.dll`

## Deploiement vers Steam

Depuis `C:\Dev\kmod new`:

Dry-run:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy_to_steam.ps1 -DryRun
```

Deploiement reel:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy_to_steam.ps1 -UseBuiltDll
```

Important:
- Utiliser `-UseBuiltDll` apres une compilation pour copier la DLL fraichement compilee dans le dossier Steam.

## Verification rapide

Comparer les hashes de la DLL compilee et deployee:

```powershell
Get-FileHash .\CvGameCoreDLL\Release\CvGameCoreDLL.dll -Algorithm SHA256
Get-FileHash "C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword\Beyond the Sword\Mods\K-Mod\Assets\CvGameCoreDLL.dll" -Algorithm SHA256
```

Les hashes doivent etre identiques.

## Problemes frequents

- `LNK1158: cannot run 'cvtres.exe'`
  - Verifier `CVTRES_DIR` ou la presence de `cvtres.exe` dans le `PATH`.
- Erreurs Boost/Python introuvables
  - Verifier `CIV4_SDK_DEPS` et la presence de `Boost-1.32.0`, `Python24`, `bin\fastdep.exe`.
- Erreurs de quoting/nmake
  - Passer par `build_kmod.cmd` (eviter les appels `nmake` manuels).

