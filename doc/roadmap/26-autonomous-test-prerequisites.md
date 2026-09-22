---
plan:
  id: '26'
  name: 26-autonomous-test-prerequisites.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/26-autonomous-test-prerequisites.md
status: active
date: 2026-09-22
description: >
  Imposer une section "Prérequis pour les tests" avant toute procédure de test dans les plans,
  avec des commandes 100 % exécutables par copier-coller (zero-lookup), modes manual et autonomous.
priority: medium
complexity: M
intent: null
scope:
  modules:
    - references/templates.md
    - modules/execute.md
issue:
  id: 26
  url: https://github.com/ehouriez/roadmap-tracking/issues/26
---

# [🧪] Plan #26 - Autonomous Test Prerequisites

## Objectif

Imposer dans tous les plans roadmap-tracking (modes `manual` et `autonomous`) une section
`### Prérequis pour les tests` positionnée immédiatement avant `### Procédure de test`,
garantissant que toutes les commandes de test sont exécutables par copier-coller sans
recherche manuelle de valeur (zero-lookup).

## Périmètre

### Inclus
- `references/templates.md` — ajout de la section `### Prérequis pour les tests` dans le template `## Tests`
- `modules/execute.md` — ajout d'une règle ⛔ imposant la création/MAJ de cette section à chaque écriture d'une procédure de test

### Hors scope
- Modification de plans existants déjà créés
- Ajout d'une garde bloquante (vérification enforcement) — règle documentée uniquement

## Étapes

- [ ] Étape 1 — Mettre à jour `references/templates.md` : ajouter `### Prérequis pour les tests` avant `### Procédure de test` (S · standard → Sonnet)
- [ ] Étape 2 — Mettre à jour `modules/execute.md` : ajouter la règle ⛔ zero-lookup (S · standard → Sonnet)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test
- [ ] ✅ Validation — Vérifier les résultats des tests et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Emplacement de la règle | Template + module execute | Template = structure visible à la création ; execute = enforcement lors de l'écriture effective |
| Type d'enforcement | Règle documentée (pas de garde bloquante) | Demande explicite de l'utilisateur |
| Portée | Modes manual ET autonomous | Utile dans les deux cas : manual = opérateur exécute, autonomous = agent ou opérateur peut exécuter |

## Tests

### Prérequis pour les tests

```bash
echo "=== Set Working Directory ==="
cd /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking

echo "=== Verify Templates File Exists ==="
ls references/templates.md

echo "=== Verify Execute Module Exists ==="
ls modules/execute.md
```

### Procédure de test

```bash
echo "=== Check Prerequisites Section in Template ==="
grep -n "Prérequis pour les tests" references/templates.md

echo "=== Check Prerequisites Before Procedure in Template ==="
grep -n "Prérequis\|Procédure de test" references/templates.md

echo "=== Check Zero-Lookup Rule in Execute Module ==="
grep -n "zero-lookup\|Prérequis pour les tests" modules/execute.md

echo "=== Check Rule Marker in Execute Module ==="
grep -n "⛔" modules/execute.md | grep -i "test\|prérequis\|procédure"
```

**Résultats attendus :**
- `references/templates.md` contient `### Prérequis pour les tests` positionné avant `### Procédure de test`
- `modules/execute.md` contient une règle ⛔ mentionnant zero-lookup et la section prérequis

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|

## Journal de session

### Session 2026-09-22
- 🔄 En cours : implémentation étapes 1 et 2
- 📋 Prochain : tests et validation
