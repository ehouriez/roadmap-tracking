---
plan:
  id: '6'
  name: 6-roadmap-tracking-tests-mode-accessibilite.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/6-roadmap-tracking-tests-mode-accessibilite.md
status: done
date: 2026-09-11
description: >
  Reformuler la proposition Phase 7 du choix manual/autonomous pour ancrer la
  décision sur le vrai critère : l'environnement de test est-il directement
  accessible à l'agent depuis cet IDE.
priority: medium
complexity: XS
scope:
  modules:
    - SKILL.md
    - references/autonomous-tests.md
issue:
  id: 6
  url: https://github.com/ehouriez/roadmap-tracking/issues/6
---

# [🐛] Plan #6 - roadmap-tracking : proposition du mode de tests axée sur l'accessibilité de l'environnement

## Objectif

La proposition Phase 7 du choix `manual`/`autonomous` présente les deux modes de
façon abstraite. L'utilisateur ne perçoit pas le critère de décision réel :
**l'environnement de test est-il accessible à l'agent ?**

Recentrer la question et les libellés sur ce critère.

## Périmètre

### Inclus
- `SKILL.md` : reformulation de la question + des 2 libellés (Phase 7, proposition du mode de tests).
- `references/autonomous-tests.md` : alignement de la ligne descriptive du mécanisme sur le nouveau cadrage.

### Hors scope
- Logique de persistance dans `.skill-config.yml`.
- Schéma de configuration dans `references/environment.md`.
- Config `tests.verifier` (inline/subagent).

## Wording retenu

**Question** : « L'environnement de test de ce projet est-il directement accessible depuis cet IDE ? »

- **Non → tests en mode `Manuel`** : je te propose les procédures de test, tu les
  exécutes et me transmets les résultats. (`manual`)
- **Oui → tests en mode `Autonome`** : un agent vérificateur indépendant (si
  disponible) exécute et vérifie les tests après chaque étape. (`autonomous`)

## Étapes

- [x] Étape 1 — Reformuler la question + les 2 libellés dans `SKILL.md` (Phase 7) + message de reset post-persistance (XS · standard → Sonnet)
- [x] Étape 2 — Aligner la ligne descriptive de `references/autonomous-tests.md` sur le nouveau cadrage (XS · standard → Sonnet)
- [x] 🧪 Tests — Rédiger et exécuter la procédure de test
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Nom du projet dans la question | Formulation générique (« ce projet ») | Évite un placeholder à résoudre et tout risque d'erreur de nom |
| Portée du wording | Question + libellés reformulés | Le critère d'accessibilité doit apparaître dès la question, pas seulement dans les descriptions |
| Mention du vérificateur autonome | « agent vérificateur indépendant (si disponible) » | Ne pas surpromettre : en `tests.verifier: inline`, pas de sous-agent réel |

## Journal de session

### Session 2026-09-11
- ✅ Étape 1 : question + libellés reformulés dans `SKILL.md` + message de reset post-persistance ajouté
- ✅ Étape 2 : `references/autonomous-tests.md` aligné sur le nouveau cadrage
- ✅ Tests : vérification grep — tous les checks passent
- ✅ Validation : plan clôturé, version bumpée à `2.2.0`
