# Référence — scripts-python

> Voir aussi : [Explication scripts-python](explanation-scripts-python.md)

Cinq scripts Python 3 autonomes dans `scripts/`. Bibliothèque commune : `migrate_plan_ids.py`.

---

## Vue d'ensemble

| Script | Rôle | Modifie des fichiers |
|---|---|---|
| `build_roadmap.py` | Génère `.index.json`, `roadmap.md`, `done/INDEX.md` | Oui (avec `--write`) |
| `doctor.py` | Audite l'intégrité — lecture seule | **Non** |
| `normalize_status.py` | Normalise statuts + déplace plans | Oui (avec `--write`) |
| `split_context.py` | Découpe `CONTEXT.md` en fichiers thématiques | Oui (avec `--write`) |
| `migrate_plan_ids.py` | Renomme `NNN→issue-id`, patche issues GitHub | Oui (avec `--patch-issues`) |

**Défaut commun** : `--dry-run` (aucune modification). `--write` ou `--patch-issues` doit être explicite.

**`--self-check` commun** : lance des tests en mémoire sans écriture disque, exit 0/1.

---

## build_roadmap.py

```bash
python3 build_roadmap.py --roadmap-dir DIR [--dry-run|--write|--check|--self-check] [--mode github|local]
```

Scanne `doc/roadmap/` (racine + `done/`) via `plan_files()`. Source de données : front matter uniquement.

**Sorties** :

| Artefact | Description |
|---|---|
| `.index.json` | Liste compacte `{id, status, priority, complexity, title, deps, path}` par plan |
| `roadmap.md` | Backlog actif (status `active` / `blocked`), trié priority↓ puis id↑ |
| `done/INDEX.md` | Table compacte des plans clôturés |

**Modes** :

| Flag | Comportement |
|---|---|
| `--dry-run` | Affiche ce qui serait écrit, rien ne change (défaut) |
| `--write` | Écrit les 3 artefacts |
| `--check` | Exit 1 si `.index.json` diverge du disque (CI staleness detection) |
| `--self-check` | Assertions en mémoire, exit 0/1 |

Nom de projet dérivé depuis l'H1 de `roadmap.md` existant (stabilité entre régénérations).

---

## doctor.py

```bash
python3 doctor.py --roadmap-dir DIR [--dry-run] [--self-check]
```

5 vérifications (lecture seule) :

| Catégorie | Ce que ça détecte |
|---|---|
| `status_enum` | Valeurs hors enum (`in-progress`, `cancelled`, inconnues) |
| `status_location` | Plan `done` hors `done/` ; plan `archived` hors `archived/` |
| `dep_integrity` | `depends_on` référençant un plan introuvable |
| `done_links` | Liens dans `done/INDEX.md` pointant vers des fichiers absents |
| `index_freshness` | `.index.json` plus vieux qu'un plan ou `roadmap.md` modifié |

Rapport en tableau markdown. Exit 1 si au moins un finding.

Ne modifie, déplace ou supprime aucun fichier.

---

## normalize_status.py

```bash
python3 normalize_status.py --roadmap-dir DIR [--dry-run|--write] [--self-check]
```

Deux transformations idempotentes :

1. **Réécriture de statuts** : `in-progress→active`, `cancelled→archived`
2. **Déplacement physique** : `status: done` → `done/` ; `status: archived` → `archived/`

Utilise `git mv` pour préserver l'historique git.

---

## split_context.py

```bash
python3 split_context.py --roadmap-dir DIR [--dry-run|--write] [--self-check]
```

Lit `CONTEXT.md`, identifie les sections `##` dont le titre ne correspond pas à `r[eè]gles\s+absolues` (regex ASCII-folded). Déplace vers `doc/roadmap/context/<slug>.md`.

**Garde-fou collision** : exit 1 avant toute écriture si un fichier cible existe déjà.

---

## migrate_plan_ids.py

```bash
python3 migrate_plan_ids.py --roadmap-dir DIR [--dry-run] [--patch-issues]
    [--map OLD=ISSUE,...] [--map-file FILE] [--mode github|local]
```

Renomme les plans `NNN-slug.md` → `{issue-id}-slug.md` en mode `github`.

**Opérations** :
- `git mv` du fichier
- Réécriture de `plan.id`, `plan.name`, `plan.link`, titre H1
- Mise à jour des références dans `roadmap.md`
- `--patch-issues` : corrige le corps des issues GitHub via `gh`

**Résolution de l'issue ID** : front matter `issue.id` → `--map`/`--map-file` → plan laissé intact (`⚠️ non migré`).

En mode `local` : liste les plans et signale les champs manquants, sans migration.

---

## Bibliothèque partagée (migrate_plan_ids.py)

Fonctions exportées et importées par les 4 autres scripts :

| Fonction | Rôle |
|---|---|
| `read_front_matter(path)` | Parse le bloc YAML `---` d'un fichier plan |
| `get_top_value(fm, key)` | Lit une valeur de premier niveau du front matter |
| `get_nested_value(fm, section, key)` | Lit une valeur imbriquée |
| `plan_files(roadmap_dir)` | Retourne tous les fichiers `.md` (racine + `done/`) |
| `load_issue_mode(roadmap_dir)` | Lit `issues.mode` depuis `.skill-config.yml` |
| `MigrationError` | Exception pour erreurs de migration |

---

## Dépendances entre scripts

```
migrate_plan_ids.py   ← parser central
    ↑
    ├── build_roadmap.py   (importe: plan_files, read_front_matter, get_nested_value, get_top_value, MigrationError)
    ├── doctor.py          (importe: CANONICAL_STATUSES, INDEX_FILENAME, STATUS_MAPPING, build_index + parser helpers)
    └── normalize_status.py (importe depuis build_roadmap + migrate_plan_ids)
```

---

## Cas limites notables

| Situation | Comportement |
|---|---|
| Fichier plan sans front matter parseable | Silencieusement ignoré par `load_plan()` ; `doctor.py` le signale |
| Fichier cible déjà existant (`split_context.py`) | Exit 1 avant écriture (collision guard) |
| Mode `local` dans `migrate_plan_ids.py` | Rapport de conformité, aucune migration |
| `plan.id` zéro-paddé (ex. `'010'`) | Normalisé vers `'10'` pour la réécriture |
| `build_roadmap.py --check` | Exit 0 si cohérent, exit 1 si drift (CI) |
