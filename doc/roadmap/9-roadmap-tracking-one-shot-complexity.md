---
plan:
  id: '9'
  name: 9-roadmap-tracking-one-shot-complexity.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/9-roadmap-tracking-one-shot-complexity.md
status: done
date: 2026-09-12
description: >
  Ajouter le champ Complexity dans les blocs Phase 5 et reprise, et une option
  d'implémentation one-shot qui enchaîne toutes les étapes sans tests intermédiaires.
priority: medium
complexity: S
scope:
  modules:
    - SKILL.md
issue:
  id: 9
  url: https://github.com/ehouriez/roadmap-tracking/issues/9
---

# [⚡] Plan #9 - One-shot Implementation Option + Complexity in Breakpoints

## Objectif

Enrichir les points d'arrêt de Phase 5 (création) et de reprise avec (a) l'affichage
de la complexité du plan et (b) une option d'implémentation one-shot qui enchaîne toutes
les étapes d'implémentation sans tests intermédiaires ni ⏸️ entre étapes.

## Périmètre

### Inclus
- `SKILL.md` — 3 blocs modifiés : Phase 5, reprise, Phase 7 step 0

### Hors scope
- `references/` — aucun changement
- Comportement autonomous — inchangé
- Phase 6 — toujours exécutée normalement même en mode one-shot

## Étapes

- [x] Étape 1 — Modifier Phase 5 : ajouter `📊 Complexity :`, option `⚡ one-shot` (option 2), renuméroter (XS · standard → Sonnet)
- [x] Étape 2 — Modifier bloc reprise : ajouter `complexité` au résumé + option `⚡ one-shot` (option 2), renuméroter (XS · standard → Sonnet)
- [x] Étape 3 — Modifier Phase 7 step 0 : note one-shot → step 0 supprimé, enchaîner directement étape 1 (XS · standard → Sonnet)
- [x] 🧪 Tests — Relire les 3 blocs modifiés dans SKILL.md, vérifier cohérence numérotation et sémantique
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Emoji `Complexity :` | `📊` | Signifie mesure/sizing |
| Emoji option one-shot | `⚡` | Vitesse, tout d'un coup |
| Comportement step 0 | Supprimé en one-shot | Implicitement : aucun test intermédiaire |
| Phase 6 | Toujours exécutée | Grilling L/XL ne peut pas être bypassé |
| ⏸️ Tests finaux | Conservé obligatoire | L'utilisateur doit toujours transmettre les résultats |

## Tests

> Section renseignée à l'étape 🧪 Tests.

### Procédure de test

```bash
grep -n "Complexity\|one-shot\|POINT D'ARRÊT 2" SKILL.md
grep -n "complexité.*Sonnet\|one-shot.*enchaîner\|Résumé du plan" SKILL.md
grep -n "Mode one-shot" SKILL.md
sed -n '744,760p' SKILL.md
sed -n '1192,1214p' SKILL.md
sed -n '876,896p' SKILL.md
```

**Résultats attendus :**
- Phase 5 : bullet `📊 Complexity :` présent, options 1→4 correctement numérotées avec ⚡ en 2
- Reprise : `complexité` dans la ligne Statut, ⚡ en option 2, options 3→5 correctes
- Phase 7 step 0 : bloc `Mode one-shot` présent entre `autonomous` et `manual`

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-12 | Phase 5 block | `📊 Complexity :` + ⚡ opt 2 + 4 options | Conforme | ✅ PASS |
| 2026-09-12 | Resume block | `complexité` in Statut + ⚡ opt 2 + 5 options | Conforme | ✅ PASS |
| 2026-09-12 | Phase 7 step 0 | Note `Mode one-shot` insérée | Conforme | ✅ PASS |

## Journal de session

### Session 2026-09-12
- ✅ Fait : plan créé, issue #9 créée
- ✅ Fait : étape 1 — Phase 5 block (`📊 Complexity :` + ⚡ one-shot option 2)
- ✅ Fait : étape 2 — reprise block (`complexité` in Statut + ⚡ one-shot option 2)
- ✅ Fait : étape 3 — Phase 7 step 0 note one-shot
- ✅ Fait : 🧪 Tests — vérification des 3 blocs (PASS)
- ✅ Fait : ✅ Validation — plan clôturé, issue #9 fermée
- ✅ Fix post-clôture : placeholder `{taille} · {tier} → {modèle}` dans la ligne complexité du résumé (valeur hardcodée corrigée)
- 🚧 Blocages : aucun
