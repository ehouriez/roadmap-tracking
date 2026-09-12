---
plan:
  id: '10'
  name: 10-roadmap-tracking-invocation-guard.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/10-roadmap-tracking-invocation-guard.md
status: active
date: 2026-09-12
description: >
  Couvrir explicitement le cas où l'agent accède aux fichiers du skill
  (SKILL.md, references/, scripts/) sans l'avoir chargé via son invocation —
  en ajoutant une règle dans la garde d'entrée et une entrée dans le tableau
  bypass tacite.
priority: high
complexity: S
scope:
  modules:
    - SKILL.md
issue:
  id: 10
  url: https://github.com/ehouriez/roadmap-tracking/issues/10
---

# [🛡️] Plan #10 - Invocation Guard for Skill Files

## Objectif

Empêcher le bypass d'invocation du skill via la lecture directe de ses propres
fichiers (`SKILL.md`, `references/`, `scripts/`). La lecture directe sans
invocation préalable est elle-même le vecteur du bypass : elle court-circuite
le workflow avant même que celui-ci puisse s'imposer.

## Périmètre

### Inclus

- Ajout dans « Interdit avant ce checkpoint » : accès aux fichiers du skill
  avant invocation interdit
- Ajout dans le tableau bypass tacite : entrée spécifique pour ce pattern

### Hors scope

- Modification des fichiers `references/`, de la logique de workflow
- Changement de version

## Étapes

- [ ] Étape 1 — Ajouter la règle dans « Interdit avant ce checkpoint » : accès aux fichiers du skill avant invocation interdit (XS · standard → Sonnet)
- [ ] Étape 2 — Ajouter l'entrée dans le tableau bypass tacite : accès direct aux fichiers du skill sans invocation (XS · standard → Sonnet)
- [ ] Étape 3 — Ajouter la détection obligatoire de `issues.mode` en Phase 5 avant les deux branches github/local : rendre le choix du mode explicite, jamais implicite (XS · standard → Sonnet)
- [ ] 🧪 Tests — Relire les trois sections modifiées, vérifier cohérence avec les règles voisines
- [ ] ✅ Validation — Vérifier que les ajouts couvrent les deux patterns de bypass observés en session

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Où placer la règle dans la garde | « Interdit avant ce checkpoint » + tableau bypass tacite | Double couverture : règle prescriptive (interdit) + description du pattern (bypass) |

## Tests

> Section renseignée aux étapes de tests.

### Procédure de test

```bash
(à remplir à l'étape 🧪 Tests)
```

**Résultats attendus :** — à remplir.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|

## Journal de session

### Session 2026-09-12
- 🔄 En cours : plan créé, implémentation à venir
