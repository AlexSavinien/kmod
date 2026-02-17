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
3. Deploy vers Steam: `powershell -ExecutionPolicy Bypass -File .\deploy_to_steam.ps1 -UseBuiltDll`.
4. Verifier hash DLL source/deployee.
5. Tester en jeu.

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
