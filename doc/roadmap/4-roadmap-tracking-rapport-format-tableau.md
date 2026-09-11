---
plan:
  id: '4'
  name: 4-roadmap-tracking-rapport-format-tableau.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/4-roadmap-tracking-rapport-format-tableau.md
status: active
date: 2026-09-11
description: >
  Corriger le bug de format de listing des plans : le skill génère un format
  clé-valeur (#: / Fichier: / Statut:) au lieu d'un tableau markdown, et ajouter
  une règle transverse imposant le format tableau pour tous les rapports du skill.
priority: medium
complexity: XS
scope:
  modules:
    - SKILL.md
issue:
  id: 4
  url: https://github.com/ehouriez/roadmap-tracking/issues/4
---

# [🐛] Plan #4 - roadmap-tracking : format tableau obligatoire pour tous les rapports

## Objectif

Le skill génère un format `#: N / Fichier: / Statut: / ───` au lieu d'un tableau
markdown lors du listing des plans, malgré l'exemple déjà présent dans `SKILL.md`.
La cause : l'exemple n'est pas une règle contraignante, le modèle l'ignore.

Ajouter une règle `⛔` explicite interdisant les formats non-tableau et renforcer
l'instruction de listing.

## Périmètre

### Inclus
- `SKILL.md` : nouvelle section `⛔ Règle absolue — format des rapports`
- `SKILL.md` : renforcement de la règle de listing (Règle de démarrage)

### Hors scope
- Autres fichiers de référence (`references/`)
- Modification des colonnes ou du contenu des tableaux existants

## Étapes

- [ ] Étape 1 — Ajouter la règle `⛔ Règle absolue — format des rapports` dans `SKILL.md` (XS · standard → Sonnet)
- [ ] Étape 2 — Renforcer l'instruction de listing (Règle de démarrage) avec interdiction explicite du format `clé: valeur` (XS · standard → Sonnet)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test
- [ ] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Emplacement de la règle transverse | Nouvelle section `⛔ Règle absolue — format des rapports` juste avant les autres règles absolues | Cohérence avec les autres règles absolues du skill ; visibilité maximale |
| Formulation de l'interdiction | `⛔ Interdit : format clé: valeur, listes séparées par ───, puces non structurées` | Précis sur les formats observés en production |

## Journal de session

### Session 2026-09-11
- 📋 Prochain : étape 1 — ajouter la règle transverse
