---
plan:
  id: '23'
  name: 23-phase2-grilling-obligatoire.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/23-phase2-grilling-obligatoire.md
status: done
date: 2026-09-15
description: >
  Rendre la Phase 2 (cadrage interactif) obligatoire pour toutes les complexités (XS→XL),
  avec grilling universel en Phase 2 et suppression du fast-track XS/S-solo et du bypass intent:prototype.
priority: high
complexity: S
intent: null
scope:
  modules:
    - modules/init-scan.md
    - modules/plan.md
    - SKILL.md
issue:
  id: 23
  url: https://github.com/ehouriez/roadmap-tracking/issues/23
---

# [🔧] Plan #23 - Phase 2 Grilling Obligatoire

## Objectif

Rendre la Phase 2 (cadrage interactif / grilling) obligatoire pour toutes les
complexités (XS, S, M, L, XL), en supprimant tout mécanisme de bypass : fast-track
XS/S-solo, bypass `intent: prototype`, et remplacement du formulaire `AskUserQuestion`
par le grilling dans Phase 2.

## Périmètre

### Inclus

- `modules/init-scan.md` : suppression fast-track (matrice Axe A + règle + template)
- `modules/plan.md` : suppression `intent: prototype` bypass + grilling universel Phase 2
- `SKILL.md` : retrait note fast-track dans Résumé compact des phases

### Hors scope

- Phases 4 et 6 : comportement grilling L/XL inchangé
- `modules/execute.md` : aucune modification
- `grilling.enabled` en Phases 4 et 6 : comportement inchangé (toujours actif pour L/XL)

## Étapes

- [x] Étape 1 — `modules/init-scan.md` : matrice Axe A + suppression fast-track (S · standard → Sonnet)
- [x] Étape 2 — `modules/plan.md` : supprimer intent/prototype + grilling universel Phase 2 (S · standard → Sonnet)
- [x] Étape 3 — `modules/plan.md` : trigger grilling universel + note toggle ignoré (XS · standard → Sonnet)
- [x] Étape 4 — `SKILL.md` : retirer note fast-track du Résumé compact (XS · standard → Sonnet)
- [x] 🧪 Tests — Rédiger et exécuter la procédure de test
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| XS/S-solo après suppression fast-track | Mode `lightweight` | Déjà défini, Phase 2 s'y exécute naturellement |
| `grilling.enabled` en Phase 2 | Ignoré (note explicite) | Toggle reste pour Phases 4/6, sans effet Phase 2 |
| `intent: prototype` | Supprimé entièrement de Phase 2 | Phase 2 doit toujours s'exécuter complètement |
| `AskUserQuestion` en Phase 2 | Supprimé | Remplacé par grilling universel |

## Tests

### Procédure de test

```bash
echo "=== Verify Fast-Track Removal In Matrice Axe A ==="
grep -n "Fast-track" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking-roadmap-tracking/modules/init-scan.md

echo "=== Verify Fast-Track Rule Section Removed ==="
grep -n "Règle.*Fast-track\|FAST-TRACK" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking-roadmap-tracking/modules/init-scan.md

echo "=== Verify Intent Prototype Removed From Plan.md ==="
grep -n "intent.*prototype\|prototype.*intent\|Axe B\|désengagement prototypage" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking-roadmap-tracking/modules/plan.md

echo "=== Verify AskUserQuestion Removed From Phase 2 Cadrage ==="
grep -n "AskUserQuestion" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking-roadmap-tracking/modules/plan.md

echo "=== Verify Grilling Universal Trigger In Plan.md ==="
grep -n "toutes les complexités\|XS.*S.*M.*L.*XL\|universel" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking-roadmap-tracking/modules/plan.md

echo "=== Verify Fast-Track Note Removed From SKILL.md ==="
grep -n "Fast-track\|phases 2-6 supprimées" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking-roadmap-tracking/SKILL.md
```

**Résultats attendus :**
- Étape 1 : `grep Fast-track init-scan.md` → 0 résultat (ou uniquement dans historique/commentaires)
- Étape 2 : `grep "FAST-TRACK"` → 0 résultat
- Étape 3 : `grep "intent.*prototype"` plan.md → 0 résultat
- Étape 4 : `grep "AskUserQuestion" plan.md` → 0 résultat (ou uniquement hors Phase 2)
- Étape 5 : `grep "toutes les complexités"` plan.md → au moins 1 résultat
- Étape 6 : `grep "Fast-track" SKILL.md` → 0 résultat

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-15 | `grep "Fast-track" init-scan.md` | 0 résultat | 0 résultat | ✅ PASS |
| 2026-09-15 | `grep "FAST-TRACK" init-scan.md` | 0 résultat | 0 résultat | ✅ PASS |
| 2026-09-15 | `grep "intent.*prototype" plan.md` | 0 résultat | 0 résultat | ✅ PASS |
| 2026-09-15 | `grep "AskUserQuestion" plan.md` | 0 résultat | 0 résultat | ✅ PASS |
| 2026-09-15 | `grep "toutes les complexités" plan.md` | ≥1 résultat | ligne 218 | ✅ PASS |
| 2026-09-15 | `grep "Fast-track" SKILL.md` | 0 résultat | 0 résultat | ✅ PASS |
| 2026-09-15 | `grep "forms.md" SKILL.md` | référence mise à jour | ligne 72 OK | ✅ PASS |

## Journal de session

### Session 2026-09-15
- ✅ Fait : init-scan.md — matrice Axe A (XS/S-solo → lightweight), fast-track template + règle supprimés
- ✅ Fait : plan.md — intent/prototype bypass supprimé, grilling universel Phase 2, trigger + toggle mis à jour
- ✅ Fait : SKILL.md — note fast-track supprimée, reference forms.md mise à jour
- ✅ Fait : 7/7 tests PASS
