# Patchnote Gameplay - v1.0.2

- Version: v1.0.2
- Date: 2026-03-10
- Comparaison: K-Mod Karadoc -> version actuelle du mod.
- Resume cumulatif: [patchnote_full.md](../patchnote_full.md)

## Changements globaux
- Refonte du palier "cavalerie lourde" via `UNIT_WAR_ELEPHANT` (role remplace):
  - Force 8, Cout 70, Mouvement 2
  - -25% Attaque de ville et -25% Defense de ville
  - 10% retrait, sans bonus anti-unites montees
  - Prerequis: Equitation + Construction + Feodalisme, Ecurie, Cheval ET Fer
- `UNIT_HORSE_ARCHER` (cavalerie legere): Cout 45, Force 5, Mouvement 2, retrait 40%.
- Prerequis batiment harmonises:
  - Cavalerie lourde et Chevalier demandent une Ecurie.
- Flux d'upgrade harmonise:
  - Chariot (et UUs de chariot) -> Cavalerie lourde -> Chevalier.
- Ressource Ivoire:
  - Les elephants de guerre generiques sont retires du role militaire de base; l'Ivoire reste une ressource economique/humeur, sauf pour les UUs qui gardent un acces `Cheval OU Ivoire`.

## Changements par civilisation (ordre alphabetique FR)

### Arabie
- `Camelarcher`: prerequis Ecurie aligne sur la ligne du Chevalier.

### Carthage
- `Numidian Cavalry`: Force 5, Cout 37, Mouvement 2, retrait 30%.
- Specificites conservees: +50% melee, promotion gratuite Combat I.

### Ethiopie
- `Oromo Warrior`: Force 7, Cout 80, Mouvement 2, retrait 20%.
- Plus de bonus anti-unites montees ni bonus/malus ville.

### Inde
- `Indian Ballista Elephant`: Force 8, Cout 65, Mouvement 1, +50% vs unites montees.
- Ressource requise: `Cheval OU Ivoire`.

### Khmers
- `Khmer Ballista Elephant`: Force 7, Cout 70, Mouvement 1, +75% vs unites montees.
- Garde le ciblage prioritaire des unites montees.
- Ressource requise: `Cheval OU Ivoire`.

### Mongols
- `Keshik`: Force 6, Cout 55, Mouvement 2, retrait 30%.
- Garde `IgnoreTerrainCost` et gagne des degats collateraux.

### Perse
- `Immortal` suit le nouveau flux d'upgrade Chariot -> Cavalerie lourde.
