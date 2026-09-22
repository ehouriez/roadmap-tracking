---
plan:
  id: '25'
  name: 25-done-subfolder-plan-management.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/25-done-subfolder-plan-management.md
status: active
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

- [ ] Étape 1 — Mettre à jour `modules/init-scan.md` — exclure `done/` du listing, règle de consultation contexte (S · standard → Sonnet)
- [ ] Étape 2 — Mettre à jour `modules/wrapup.md` — clôture : `git mv` vers `done/` + MAJ lien `roadmap.md` (S · standard → Sonnet)
- [ ] Étape 3 — Mettre à jour `references/roadmap-file.md` — format de lien `done/NNN-slug.md` pour les entrées "Fait" (XS · standard → Sonnet)
- [ ] Étape 4 — Migrer les 23 plans existants (#1–#23) — `mkdir done/` + `git mv` + MAJ liens dans `roadmap.md` (M · standard → Sonnet)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test
- [ ] ✅ Validation — Vérifier les résultats des tests et clôturer

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
(à remplir à l'étape 🧪 Tests)
```

**Résultats attendus :** (à remplir)

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|

## Journal de session

### Session 2026-09-22
- ✅ Fait : Plan créé, issue #25 ouverte
- 🔄 En cours : —
- 📋 Prochain : Étape 1 — modules/init-scan.md
- 🚧 Blocages : —
