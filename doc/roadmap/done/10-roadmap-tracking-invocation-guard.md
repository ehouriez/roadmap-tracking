---
plan:
  id: '10'
  name: 10-roadmap-tracking-invocation-guard.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/10-roadmap-tracking-invocation-guard.md
status: done
date: 2026-09-12
enriched: 2026-09-12
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

- [x] Étape 1 — Ajouter la règle dans « Interdit avant ce checkpoint » : accès aux fichiers du skill avant invocation interdit (XS · standard → Sonnet)
- [x] Étape 2 — Ajouter l'entrée dans le tableau bypass tacite : accès direct aux fichiers du skill sans invocation (XS · standard → Sonnet)
- [x] Étape 3 — Ajouter la détection obligatoire de `issues.mode` en Phase 5 avant les deux branches github/local : rendre le choix du mode explicite, jamais implicite (XS · standard → Sonnet)
- [x] 🧪 Tests — Relire les trois sections modifiées, vérifier cohérence avec les règles voisines
- [x] ✅ Validation — Vérifier que les ajouts couvrent les deux patterns de bypass observés en session

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Où placer la règle d'invocation | « Interdit avant ce checkpoint » + tableau bypass tacite | Double couverture : règle prescriptive (interdit) + description du pattern (bypass) |
| Où placer la détection `issues.mode` | Prérequis explicite en Phase 5, avant les deux branches | Le choix du mode doit être un résultat de détection, pas une valeur par défaut silencieuse |

## Tests

> Section renseignée aux étapes de tests.

### Procédure de test

Relecture des trois sections modifiées dans `SKILL.md` par un Vérificateur sub-agent indépendant :
1. Cohérence de la 5ème règle dans « Interdit avant ce checkpoint » avec les 4 règles existantes
2. Cohérence de la nouvelle entrée bypass tacite avec les entrées adjacentes (pas de doublon avec « Demande portant sur le skill lui-même »)
3. Cohérence du bloc de détection `issues.mode` en Phase 5 avec `references/environment.md § Skill Configuration Schema` et les deux branches `github`/`local`
4. Absence de contradictions avec d'autres règles du fichier

**Résultats attendus :** PASS sur les 4 points — aucun doublon, aucune contradiction, alignement avec environment.md.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-12 | Point 1 — 5ème règle interdit checkpoint | Pas de doublon ni contradiction | Périmètre non couvert par les 4 règles existantes, cohérent | ✅ PASS |
| 2026-09-12 | Point 2 — Entrée bypass tacite | Distinct de la ligne adjacente | Angles complémentaires (scope vs mécanisme) | ✅ PASS |
| 2026-09-12 | Point 3 — Bloc détection Phase 5 | Aligné avec environment.md | Correspondance exacte, surcharge .skill-config.yml cohérente | ✅ PASS |
| 2026-09-12 | Point 4 — Contradictions autres règles | Aucune contradiction | Aucune contradiction détectée | ✅ PASS |

## Journal de session

### Session 2026-09-12
- ✅ Fait : règle ajoutée dans « Interdit avant ce checkpoint » (accès fichiers skill sans invocation)
- ✅ Fait : entrée ajoutée dans le tableau bypass tacite (lecture directe des fichiers skill)
- ✅ Fait : bloc de détection `issues.mode` ajouté en Phase 5 avant les deux branches
- ✅ Tests : Vérificateur PASS sur les 4 points de cohérence
- ✅ Validé et clôturé
