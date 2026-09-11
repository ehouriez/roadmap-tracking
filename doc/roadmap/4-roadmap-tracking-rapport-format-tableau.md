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

- [x] Étape 1 — Ajouter la règle `⛔ Règle absolue — format des rapports` dans `SKILL.md` (XS · standard → Sonnet)
- [ ] Étape 2 — Renforcer l'instruction de listing (Règle de démarrage) avec interdiction explicite du format `clé: valeur` (XS · standard → Sonnet)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test
- [ ] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Emplacement de la règle transverse | Nouvelle section `⛔ Règle absolue — format des rapports` juste avant les autres règles absolues | Cohérence avec les autres règles absolues du skill ; visibilité maximale |
| Formulation de l'interdiction | `⛔ Interdit : format clé: valeur, listes séparées par ───, puces non structurées` | Précis sur les formats observés en production |

## Tests

### Procédure de test

```bash
echo "=== Check New Absolute Rule Section Exists ==="
grep -c "## ⛔ Règle absolue — format des rapports" SKILL.md

echo "=== Check Table Format Is Mandated ==="
grep -c "DOIT être rendu sous forme de tableau markdown" SKILL.md

echo "=== Check Key-Value Format Is Forbidden ==="
grep -c "Interdit : format \`clé: valeur\`" SKILL.md

echo "=== Check Section Precedes Other Absolute Rules ==="
awk '/## ⛔ Règle absolue/{print NR": "$0}' SKILL.md | head -1
```

**Résultats attendus :** section présente (count=1), format tableau imposé (count=1), format `clé: valeur` interdit (count=1), et la 1ʳᵉ règle absolue du fichier est « format des rapports ».

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-11 | Étape 1 — section existe | count=1 | 1 | ✅ PASS |
| 2026-09-11 | Étape 1 — format tableau imposé | count=1 | 1 | ✅ PASS |
| 2026-09-11 | Étape 1 — format `clé: valeur` interdit | count=1 | 1 | ✅ PASS |
| 2026-09-11 | Étape 1 — 1ʳᵉ règle absolue = format rapports | ligne 198 | ligne 198 | ✅ PASS |

## Journal de session

### Session 2026-09-11
- 📋 Prochain : étape 1 — ajouter la règle transverse
