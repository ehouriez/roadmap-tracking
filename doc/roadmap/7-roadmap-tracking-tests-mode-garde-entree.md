---
plan:
  id: '7'
  name: 7-roadmap-tracking-tests-mode-garde-entree.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/7-roadmap-tracking-tests-mode-garde-entree.md
status: active
date: 2026-09-11
description: >
  Rendre la résolution de tests.mode (proposition manual/autonomous quand non
  fixé) non-sautable en l'ajoutant à la checklist pré-action de la garde
  d'entrée, avant l'item étape 0, et en l'intégrant à la table anti-court-circuit.
priority: medium
complexity: XS
scope:
  modules:
    - SKILL.md
issue:
  id: 7
  url: https://github.com/ehouriez/roadmap-tracking/issues/7
---

# [🐛] Plan #7 - roadmap-tracking : résolution tests.mode non-sautable dans la garde d'entrée

## Objectif

La résolution de `tests.mode` (proposition manual/autonomous quand la clé est
non fixée dans `.skill-config.yml`) n'est imposée que dans le corps de Phase 7,
pas dans la checklist pré-action de la garde d'entrée. Elle est donc
contournable — reproduit : entrée directe dans l'étape 0 sans jamais poser la
question d'accessibilité de l'environnement de test. Le plan #5 avait ajouté le
déclencheur ; ce plan le rend **non-sautable**, au même niveau que l'étape 0.

## Périmètre

### Inclus
- `SKILL.md` : nouvel item dédié « `tests.mode` résolu ? » dans la checklist
  pré-action (avant l'item étape 0, qui se décale).
- `SKILL.md` : mise à jour de la table anti-court-circuit pour intégrer la
  résolution `tests.mode` dans la séquence.

### Hors scope
- Corps de Phase 7 (déjà correct — la proposition y est décrite).
- `references/` et toute autre logique de tests.

## Étapes

- [ ] Étape 1 — Insérer le nouvel item « `tests.mode` résolu ? » comme item 4 de la checklist pré-action ; l'étape 0 devient item 5 (XS · standard → Sonnet)
- [ ] Étape 2 — Mettre à jour les lignes de la table anti-court-circuit pour intégrer la résolution `tests.mode` dans la séquence (XS · standard → Sonnet)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test
- [ ] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Structure de l'ajout | Nouvel item dédié avant l'item 4 (l'étape 0 devient item 5) | Séparation nette : la résolution tests.mode et la sélection des tests intermédiaires sont deux gardes distinctes |
| Portée | Checklist + table anti-court-circuit | Cohérence complète : la séquence d'entrée Phase 7 doit être reflétée partout où elle est décrite |

## Journal de session

### Session 2026-09-11
- 📋 Prochain : étape 1 — insérer l'item tests.mode dans la checklist pré-action
