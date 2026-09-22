---
plan:
  id: '25'
  name: 25-done-subfolder-plan-management.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/done/25-done-subfolder-plan-management.md
status: done
date: 2026-09-22
description: >
  Stocker les plans status:done dans doc/roadmap/done/, exclure ce sous-répertoire
  du listing init-scan, ajouter une règle de consultation contexte, et migrer les
  23 plans existants.
priority: medium
complexity: M
intent: null
scope:
  modules:
    - modules/init-scan.md
    - modules/wrapup.md
    - references/roadmap-file.md
    - doc/roadmap/
issue:
  id: 25
  url: https://github.com/ehouriez/roadmap-tracking/issues/25
---

# [📁] Plan #25 - Done Subfolder Plan Management

## Objectif

Les plans `status: done` résident dans `doc/roadmap/done/` (distinct de `_archives/`).
Le listing init-scan les exclut pour n'afficher que le reste à faire, mais le skill
peut les lire pour récupérer du contexte pertinent lors des sessions.

## Périmètre

### Inclus
- `modules/init-scan.md` — exclure `done/` du listing, règle de consultation contexte
- `modules/wrapup.md` — étape de déplacement `git mv` vers `done/` à la clôture
- `references/roadmap-file.md` — format de lien `done/NNN-slug.md` pour les entrées "Fait"
- Migration des 23 plans existants (#1–#23) vers `doc/roadmap/done/`
- Mise à jour des liens dans `roadmap.md`

### Hors scope
- `_archives/` (plans archivés ⚪ — concept distinct, non modifié)
- Contenu des fichiers de plans individuels migrés

## Étapes

- [x] Étape 1 — Mettre à jour `modules/init-scan.md` — exclure `done/` du listing, règle de consultation contexte (S · standard → Sonnet)
- [x] Étape 2 — Mettre à jour `modules/wrapup.md` — clôture : `git mv` vers `done/` + MAJ lien `roadmap.md` (S · standard → Sonnet)
- [x] Étape 3 — Mettre à jour `references/roadmap-file.md` — format de lien `done/NNN-slug.md` pour les entrées "Fait" (XS · standard → Sonnet)
- [x] Étape 4 — Migrer les 23 plans existants (#1–#23) — `mkdir done/` + `git mv` + MAJ liens dans `roadmap.md` (M · standard → Sonnet)
- [x] 🧪 Tests — Rédiger et exécuter la procédure de test
- [x] ✅ Validation — Vérifier les résultats des tests et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Séparation `done/` vs `_archives/` | Deux sous-répertoires distincts | `done` = validé en fin de workflow ; `archived` = statut rare, suppression logique du backlog |
| Déclencheur du déplacement | À la clôture (step 1 de la checklist wrapup) | Moment naturel : `status: done` est posé à cet instant |
| Règle de consultation contexte | Règle explicite dans `init-scan.md` | Évite l'ambiguïté entre "exclure du listing" et "interdire la lecture" |
| Migration des existants | `git mv` (pas de copie) | Préserve l'historique git |

## Tests

> Section renseignée à l'étape 🧪 Tests.

### Procédure de test

```bash
echo "=== Verify done/ directory exists ==="
ls doc/roadmap/done/ | wc -l

echo "=== Verify all 23 plans are in done/ ==="
ls doc/roadmap/done/*.md | wc -l

echo "=== Verify active plans are NOT in done/ ==="
ls doc/roadmap/done/ | grep -E "^(24|25)-"

echo "=== Verify roadmap.md Fait links point to done/ ==="
grep -c "](done/" doc/roadmap/roadmap.md

echo "=== Verify active plan links in roadmap.md are NOT prefixed done/ ==="
grep "Plan :" doc/roadmap/roadmap.md | grep -v "done/"

echo "=== Verify init-scan.md excludes done/ from listing ==="
grep "done/" modules/init-scan.md | head -5

echo "=== Verify init-scan.md has context rule for done/ ==="
grep "peut et doit" modules/init-scan.md

echo "=== Verify wrapup.md has git mv step ==="
grep "git mv" modules/wrapup.md

echo "=== Verify roadmap-file.md has done/ section ==="
grep "Sous-répertoire" references/roadmap-file.md

echo "=== Verify roadmap-file.md structure example uses done/ ==="
grep "done/" references/roadmap-file.md
```

**Résultats attendus :**
- `done/` : 23 fichiers
- Aucun fichier `24-*` ou `25-*` dans `done/`
- 23 liens `](done/` dans `roadmap.md`
- Les liens `Plan :` de `roadmap.md` ne contiennent pas `done/`
- `init-scan.md` mentionne `done/` dans la règle de listing et contient "peut et doit"
- `wrapup.md` contient `git mv`
- `references/roadmap-file.md` a une section "Sous-répertoire" et mentionne `done/` dans l'exemple

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-22 | done/ count | 23 fichiers | 23 | ✅ |
| 2026-09-22 | Plans #24/#25 absents de done/ | NONE | NONE | ✅ |
| 2026-09-22 | Liens Fait → done/ dans roadmap.md | 23 | 23 | ✅ |
| 2026-09-22 | Liens actifs sans done/ | #24, #25 | #24, #25 | ✅ |
| 2026-09-22 | init-scan.md exclut done/ du listing | hors done/ dans règle | présent | ✅ |
| 2026-09-22 | init-scan.md règle contexte | "peut et doit" | présent | ✅ |
| 2026-09-22 | wrapup.md git mv step | git mv présent | présent | ✅ |
| 2026-09-22 | roadmap-file.md section done/ | section présente | présente | ✅ |
| 2026-09-22 | roadmap-file.md exemple lien done/ | done/ dans exemple | présent | ✅ |
| 2026-09-22 | roadmap-file.md quand mettre à jour | clôture mentionnée | présente | ✅ |

## Journal de session

### Session 2026-09-22
- ✅ Fait : Plan créé, issue #25 ouverte, 4 étapes implémentées (init-scan, wrapup, roadmap-file, migration 23 plans), 10/10 tests PASS, plan clôturé
- 🔄 En cours : —
- 📋 Prochain : —
- 🚧 Blocages : —
