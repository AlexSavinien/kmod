# Dev Workflow K-Mod (Memo rapide)

Objectif: reduire le temps de re-contextualisation sur les gros tickets (SDK C++ + UI Python).

## Vue d'ensemble de l'archi
- `CvGameCoreDLL/*`: logique gameplay, save/load, widgets, API Python exposee.
- `Assets/Python/*`: ecrans UI, handlers input, orchestration UI.
- `Assets/xml/*`: donnees de contenu (batiments, textes, etc.).
- Build DLL: `CvGameCoreDLL/build_kmod.cmd`.
- Deploy Steam: `deploy_to_steam.ps1`.

## Workflow standard
1. Coder dans repo local (`C:\Dev\kmod new`).
2. Compiler DLL: `build_kmod.cmd Release` dans `CvGameCoreDLL`.
3. Deploy vers Steam (strict): `powershell -ExecutionPolicy Bypass -File .\deploy_to_steam.ps1 -UseBuiltDll`.
4. Verifier hash DLL source/deployee (le script fait aussi une verification automatique).
5. Tester en jeu.

## Regle stricte de deploy
- Ne pas lancer `deploy_to_steam.ps1` sans `-UseBuiltDll`.
- Toujours faire au minimum un dry-run strict avant un deploy reel:
  - `powershell -ExecutionPolicy Bypass -File .\deploy_to_steam.ps1 -UseBuiltDll -DryRun`
- Objectif: eviter les faux bugs dus a un Python a jour avec une DLL Steam obsolete.

## Commandes utiles
- Recherche code rapide: `rg "pattern" path`.
- Etat git: `git status --short`.
- Diff cible: `git diff -- path/file`.
- Hash DLL:
  - `Get-FileHash .\CvGameCoreDLL\Release\CvGameCoreDLL.dll -Algorithm SHA256`
  - `Get-FileHash "C:\Program Files (x86)\Steam\...\K-Mod\Assets\CvGameCoreDLL.dll" -Algorithm SHA256`

## Ou regarder selon le probleme
- Calcul gameplay (croissance, famine, rendements): `CvGameCoreDLL/CvCity.cpp`, `CvGameCoreDLL/CvPlayer.cpp`.
- Transport de messages UI->DLL: `CvGameCoreDLL/CvMessageData.cpp`.
- Hover/tooltips widgets: `CvGameCoreDLL/CvDLLWidgetData.cpp`.
- Binding Python<->DLL: `CvGameCoreDLL/CyPlayer*.{h,cpp}`.
- Ecrans/flux UI: `Assets/Python/Screens/*.py`, `Assets/Python/EntryPoints/CvScreensInterface.py`.

## Pieges frequents
- Python Civ4 est ancien (eviter syntaxes modernes risquee).
- Regressions d'UI si coords absolues mal alignees (header/rows des tableaux).
- Valeurs UI parfois asynchrones apres `sendModNetMessage`.
- Tri tableau + widgets superposes peuvent desynchroniser l'affichage.
- Jeu ouvert peut locker la DLL pendant deploy.

## Bonnes pratiques ticket long
- Garder un fichier note par feature dans `docs/features/`.
- Centraliser:
  - fichiers touches,
  - decisions de design,
  - checklist de test,
  - commandes build/deploy.
- Committer par bloc coherent (pas de gros commit flou).

## Regles de push (obligatoire)
- Generer un nouveau patchnote versionne:
  - `powershell -ExecutionPolicy Bypass -File .\patchnotes\new_patchnote_version.ps1 -Version vMAJOR.MINOR.PATCH`
- Completer `patchnotes/patchnote_vMAJOR.MINOR.PATCH.md` avec les changements du commit.
- Mettre a jour `patchnote_full.md` pour conserver le resume cumulatif total.
- Mettre a jour `patchnotes/README.md` avec la nouvelle version.
- `patchnote_full.md` doit refleter le delta global vs `karadoc/Civ4-K-Mod`.
- Verifier avant push:
  - `git diff -- patchnotes/patchnote_vMAJOR.MINOR.PATCH.md patchnote_full.md patchnotes/README.md AGENTS.md docs/DEV_WORKFLOW.md`
