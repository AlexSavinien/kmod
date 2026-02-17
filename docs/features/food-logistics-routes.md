# Feature Notes - Food Logistics Routes

Date: 2026-02-17

## Scope
- Routes logistiques intra-joueur, ville source -> ville cible, ressource nourriture.
- Flux configurable en nourriture/tour.
- Famine volontaire possible en source.
- Suspension auto si rupture du reseau commercial.
- Persistence save/load.

## Fichiers cle modifies
- `CvGameCoreDLL/CvPlayer.h`
- `CvGameCoreDLL/CvPlayer.cpp`
- `CvGameCoreDLL/CvCity.cpp`
- `CvGameCoreDLL/CvMessageData.cpp`
- `CvGameCoreDLL/CyPlayer.h`
- `CvGameCoreDLL/CyPlayer.cpp`
- `CvGameCoreDLL/CyPlayerInterface1.cpp`
- `CvGameCoreDLL/CvDLLWidgetData.cpp`
- `Assets/Python/EntryPoints/CvScreensInterface.py`
- `Assets/Python/Screens/CvMainInterface.py`
- `Assets/Python/Screens/CvLogisticsRoutesScreen.py`

## Cote DLL
- Nouveau canal logistique (routes + flux + etat actif/suspendu).
- APIs exposees Python:
  - creation/maj flux,
  - lecture import/export/net par ville,
  - lecture flux route active/configuree.
- Integration dans calcul nourriture nette/croissance (`CvCity`).
- Message reseau modded pour set du flux (`MOD_NET_MESSAGE_SET_FOOD_ROUTE_FLOW = 7100`).

## Cote UI
- Nouveau menu dedie `CvLogisticsRoutesScreen`.
- Tableau villes cibles avec colonnes info + actions:
  - `-`, `+`, `Flux (nourriture/tour)`, `Etat`.
- Boutons style ville (`BUTTON_STYLE_CITY_MINUS/PLUS`).
- Feedback immediat apres clic via redraw + override local en attente.
- Boutons grises hors reseau.

## Ajustements UX importants
- Layout inspire Domestic Advisor, sans modifier Domestic Advisor.
- Correction de decalage vertical des boutons (offset header du tableau).
- Statut route affiche de facon coherente juste apres clic.
- Detail routes retire du texte inline nourriture et deplace dans hover barre nourriture (liste).

## Hover nourriture (city screen)
- `CvDLLWidgetData::parsePopulationHelp` affiche:
  - nourriture stockee/seuil,
  - nourriture brute (nourriture/tour),
  - consommation (nourriture/tour),
  - import/export/net routes (nourriture/tour),
  - solde net (nourriture/tour),
  - croissance/famine en tour(s).

## Build / deploy
1. `cd CvGameCoreDLL`
2. `build_kmod.cmd Release`
3. `powershell -ExecutionPolicy Bypass -File .\deploy_to_steam.ps1 -UseBuiltDll`
4. Verifier hash DLL compilee vs deployee.

## Checklist test rapide
1. Ouvrir ecran routes depuis une ville avec grenier.
2. Clic `+/-` met a jour le flux de la bonne ligne.
3. Source peut tomber en famine si export > net.
4. Affichage croissance cohherent carte + panneaux ville.
5. Rupture reseau => route suspendue, reprise quand reconnectee.
6. Save/load conserve les flux.
