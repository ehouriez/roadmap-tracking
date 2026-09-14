---
plan:
  id: '12'
  name: 12-session-clear-gate-suggestion.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/12-session-clear-gate-suggestion.md
status: done
date: 2026-09-14
description: >
  Afficher un bloc informatif /clear à chaque gate ⏸️ de la Phase 5+ pour
  suggérer à l'utilisateur de réinitialiser la session et économiser des tokens.
  Le fichier plan contient déjà tout le contexte nécessaire à la reprise.
priority: medium
complexity: S
intent: null
scope:
  modules:
    - modules/execute.md
    - modules/wrapup.md
issue:
  id: 12
  url: https://github.com/ehouriez/roadmap-tracking/issues/12
---

# [💾] Plan #12 - Session Clear Gate Suggestion

## Objectif

À chaque gate ⏸️ de Phase 5+, le fichier plan est autoportant (status, étapes progressées, section Tests, journal). Afficher un bloc informatif propose à l'utilisateur de faire `/clear` puis de reprendre sur une session neuve, sans perte de contexte — économie de tokens significative sur les plans M/L/XL.

## Périmètre

### Inclus

- Injection du bloc dans `modules/execute.md` aux 4 points d'arrêt : POINT D'ARRÊT 2 (Phase 5), gate Phase 6, tests intermédiaires Phase 7, 🧪 Tests finaux Phase 7
- Injection dans `modules/wrapup.md` après le ⏸️ de reprise
- Logique conditionnelle : ne pas afficher en fast-track avant la gate 🧪 Tests finaux

### Hors scope

- Modifications du `.skill-config.yml` ou des autres modules
- Automatisation du `/clear` (suggestion uniquement, action reste manuelle)

## Étapes

- [x] Étape 1 — Injecter le bloc dans `execute.md` aux 4 points d'arrêt (S · standard → Sonnet)
- [x] Étape 2 — Injecter le bloc dans `wrapup.md` après le ⏸️ de reprise (XS · standard → Sonnet)
- [x] 🧪 Tests — Vérifier que le bloc s'affiche correctement à chaque gate et que le prompt de reprise est cohérent
- [x] ✅ Validation — Valider les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Position du bloc | Après le ⏸️, avant le STOP | Le bloc est informatif, ne bloque pas la gate |
| Condition fast-track | Afficher quand même à la gate 🧪 Tests finaux | Seul gate avec gain réel même pour XS/S |
| Format prompt reprise | Phrase courte + `:` pour tests gates | Autoportant, indique que des résultats doivent suivre |

## Tests

> Section renseignée lors de l'étape 🧪 Tests.

### Procédure de test

```bash
echo "=== Check execute.md — Phase 5 clear block present ==="
grep -n "INTRO_FICHIERS" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/execute.md | head -10

echo "=== Check execute.md — Phase 6 clear block present ==="
grep -n "Afficher également" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/execute.md

echo "=== Check execute.md — tests intermédiaires clear block present ==="
grep -n "résultats des tests intermédiaires" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/execute.md

echo "=== Check execute.md — tests finaux clear block present ==="
grep -n "résultats des tests finaux" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/execute.md

echo "=== Check wrapup.md — resume clear block present ==="
grep -n "INTRO_FICHIERS" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/wrapup.md

echo "=== Count total clear blocks ==="
grep -c "INTRO_FICHIERS" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/execute.md
grep -c "INTRO_FICHIERS" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/wrapup.md

echo "=== Verify variable note present in execute.md ==="
grep -n "Variables du bloc" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/execute.md

echo "=== Verify PLAN_COURANT placeholder in each block ==="
grep -n "PLAN_COURANT" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/execute.md
grep -n "PLAN_COURANT" /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/modules/wrapup.md
```

**Résultats attendus :**
- `grep INTRO_FICHIERS execute.md` : 4 occurrences (Phase 5, Phase 6, tests intermédiaires, tests finaux)
- `grep "Afficher également" execute.md` : 1 occurrence (Phase 6)
- `grep "résultats des tests intermédiaires" execute.md` : 1 occurrence
- `grep "résultats des tests finaux" execute.md` : 1 occurrence
- `grep INTRO_FICHIERS wrapup.md` : 1 occurrence
- Count total : execute.md = 4, wrapup.md = 1 (5 blocs au total)
- `grep "Variables du bloc" execute.md` : 1 occurrence (note explicative présente)
- `grep PLAN_COURANT execute.md` : ≥ 4 occurrences ; `grep PLAN_COURANT wrapup.md` : ≥ 1 occurrence

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-14 | INTRO_FICHIERS execute.md (injections) | 4 injections | 4 injections + 1 note explicative (grep=5) | ✅ PASS |
| 2026-09-14 | "Afficher également" execute.md (Phase 6) | 1 | 1 (ligne 118) | ✅ PASS |
| 2026-09-14 | "résultats des tests intermédiaires" | 1 | 1 (ligne 367) | ✅ PASS |
| 2026-09-14 | "résultats des tests finaux" | 1 | 1 (ligne 445) | ✅ PASS |
| 2026-09-14 | INTRO_FICHIERS wrapup.md | 1 | 1 | ✅ PASS |
| 2026-09-14 | Note "Variables du bloc" execute.md | 1 | 1 (ligne 76) | ✅ PASS |
| 2026-09-14 | PLAN_COURANT execute.md | ≥ 4 | 9 | ✅ PASS |
| 2026-09-14 | PLAN_COURANT wrapup.md | ≥ 1 | 2 | ✅ PASS |
| 2026-09-14 | Bloc Phase 5 à l'intérieur des fences ``` | inside fences | inside fences (lignes 67-73, fence fermée ligne 74) | ✅ PASS |
| 2026-09-14 | PLANS_LIES présent ≥ 3 blocs | ≥ 3 | 6 (5+1) | ✅ PASS |

## Journal de session

### Session 2026-09-14
- ✅ Fait : Issue #12 créée, plan écrit
- 🔄 En cours : —
- 📋 Prochain : —
- 🚧 Blocages : aucun
- ✅ Clôturé : Étapes 1 et 2 implémentées, 10/10 tests PASS (vérificateur autonome), plan status: done
