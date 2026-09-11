# Migration rétroactive : NNN → numéro d'issue

> **Mode `github` uniquement.** La migration repose sur le `issue.id` de chaque
> plan. En mode `local` (pas d'issue GitHub), le contrôle `plan.id == issue.id`
> n'a pas de sens — cette procédure ne s'applique pas.

Les plans historiques nommés `NNN-slug.md` (numérotation séquentielle) se
migrent vers `{issue}-slug.md` avec le script
`scripts/migrate_plan_ids.py`. À lancer **dans chaque dépôt concerné**, à la
racine (là où vit `doc/roadmap/`).

## Pré-requis

- Le numéro d'issue de chaque plan est résolu dans cet ordre :
  1. `issue.id` dans le front matter du plan (cas nominal) ;
  2. une **table de correspondance** fournie via `--map` / `--map-file` — seul
     moyen de migrer un plan legacy dont le front matter est absent ou sans
     `issue.id` (le numéro n'est **jamais deviné**).
  Un plan dont le numéro reste introuvable est **laissé intact** et listé dans
  le récapitulatif de fin (voir « Migrer un plan sans `issue.id` »).
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

# Plans sans issue.id : fournir la correspondance ancien-id → numéro d'issue
python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --map 10=42,8=51

# Même chose depuis un fichier (une paire OLD=ISSUE par ligne, '#' = commentaire)
python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --map-file migration-map.txt

# Forcer le mode (par défaut : lu depuis .skill-config.yml, sinon github)
python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --mode local
```

> En mode `local` (projet sans issue GitHub), le script ne migre **rien** et le
> signale : la problématique du numéro d'issue ne se pose pas.

## Ce que fait le script

Pour chaque `NNN-slug.md` (ou `draft-slug.md`) ayant un `issue.id` :

1. Renomme le fichier en `{issue}-slug.md` via `git mv`.
2. Réécrit dans le plan : `plan.id`, `plan.name`, `plan.link` et le titre H1
   (`Plan NNN` → `Plan #{issue}`).
3. Dans `roadmap.md` : remplace les liens `NNN-slug.md` et les références
   `` `NNN` `` → `` `#{issue}` ``.
4. Avec `--patch-issues` : corrige les références (`NNN-slug.md`, `Plan NNN`)
   dans le corps de l'issue et ajoute un commentaire de traçage.

En fin d'exécution, un **récapitulatif** classe chaque plan :

- ✅ **migré** (numéro d'issue venant du front matter ou de `--map`) ;
- ℹ️ **local** (`plan.source: local` ou `issue.id: null`) → jamais migré, ce
  n'est pas une anomalie ;
- ⚠️ **non migré** : plan GitHub sans numéro d'issue récupérable → listé avec la
  raison et un exemple de `--map` prêt à compléter.

## Migrer un plan sans `issue.id` (quoi transmettre à l'agent)

Quand le récapitulatif liste des plans **⚠️ non migrés**, le script ne peut pas
deviner leur numéro d'issue. Il faut le lui donner. Concrètement, à l'agent :

> « Migre le plan **10** vers l'issue **#42** et le plan **8** vers l'issue
> **#51**. »

L'agent traduit ça en une seule commande :

```bash
python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --map 10=42,8=51
```

Règles pour la correspondance :

- La **clé** (`10`) identifie le plan existant : c'est son préfixe de fichier
  (`10` pour `10-…` ou `010-…`) ou son slug pour un fichier sans préfixe.
- La **valeur** (`42`) est le **numéro d'issue GitHub** réel (sans `#`).
- Le numéro n'étant pas dans le fichier, va le chercher côté GitHub (issue
  correspondante) ou dans `roadmap.md` (`[Issue: #NN]` en regard du plan).
- Ce qui n'est **pas** dans la table reste intact — rien n'est renommé au hasard.

> ⚠️ Le script **ne fabrique pas** de front matter : pour un plan qui n'en a
> pas, il renomme le fichier et corrige les références `Plan NNN`, mais ne crée
> pas de bloc YAML. Compléter le front matter (statut, priorité, complexité…)
> reste une étape manuelle, guidée par `references/templates.md`.

## Limites

- Ne migre **pas** les plans sans numéro d'issue résoluble (ni `issue.id`, ni
  entrée `--map`) : ils sont signalés dans le récapitulatif, pas modifiés.
- `--patch-issues` modifie le **corps** des issues : relis le diff proposé par
  `--dry-run` avant de l'utiliser sur des issues partagées.
- Toujours commencer par `--dry-run`, puis vérifier `git status` / `git diff`
  avant de committer.

## Marqueur de report / refus

Le fichier `doc/roadmap/.migration-declined` mémorise le choix de report
(`snooze-until: YYYY-MM-DD`) ou de refus (`declined`) d'un utilisateur. C'est un
**état local et personnel** : l'ajouter à `.gitignore` pour ne pas imposer ce
choix aux autres contributeurs.
