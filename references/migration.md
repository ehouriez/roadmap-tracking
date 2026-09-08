# Migration rétroactive : NNN → numéro d'issue

Les plans historiques nommés `NNN-slug.md` (numérotation séquentielle) se
migrent vers `{issue}-slug.md` avec le script
`scripts/migrate_plan_ids.py`. À lancer **dans chaque dépôt concerné**, à la
racine (là où vit `doc/roadmap/`).

## Pré-requis

- L'`issue.id` doit être renseigné dans le front matter de chaque plan à migrer
  (c'est la source de l'identifiant). Un plan sans `issue.id` est **ignoré** et
  signalé.
- `git` disponible (le renommage se fait via `git mv`, l'historique est
  préservé).
- `gh` authentifié **uniquement** si tu utilises `--patch-issues`.

## Utilisation

```bash
# 1. Aperçu, aucune modification
python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --dry-run

# 2. Migration réelle (fichiers + roadmap.md)
python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py

# 3. Migration + correction des références dans les issues GitHub
python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --patch-issues

# Répertoire non standard
python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --roadmap-dir chemin/roadmap
```

## Ce que fait le script

Pour chaque `NNN-slug.md` (ou `draft-slug.md`) ayant un `issue.id` :

1. Renomme le fichier en `{issue}-slug.md` via `git mv`.
2. Réécrit dans le plan : `plan.id`, `plan.name`, `plan.link` et le titre H1
   (`Plan NNN` → `Plan #{issue}`).
3. Dans `roadmap.md` : remplace les liens `NNN-slug.md` et les références
   `` `NNN` `` → `` `#{issue}` ``.
4. Avec `--patch-issues` : corrige les références (`NNN-slug.md`, `Plan NNN`)
   dans le corps de l'issue et ajoute un commentaire de traçage.

## Limites

- Ne migre **pas** les plans sans `issue.id` (rien à quoi rattacher l'ID).
- `--patch-issues` modifie le **corps** des issues : relis le diff proposé par
  `--dry-run` avant de l'utiliser sur des issues partagées.
- Toujours commencer par `--dry-run`, puis vérifier `git status` / `git diff`
  avant de committer.

## Marqueur de report / refus

Le fichier `doc/roadmap/.migration-declined` mémorise le choix de report
(`snooze-until: YYYY-MM-DD`) ou de refus (`declined`) d'un utilisateur. C'est un
**état local et personnel** : l'ajouter à `.gitignore` pour ne pas imposer ce
choix aux autres contributeurs.
