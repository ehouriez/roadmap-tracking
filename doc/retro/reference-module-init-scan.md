# Référence — module-init-scan

> Voir aussi : [Explication module-init-scan](explanation-module-init-scan.md)

`modules/init-scan.md` — Chargé au tour 1 de toute session. Contient la garde d'entrée non-sautable, la règle de démarrage, les blocs A.0–A.1, la réconciliation au démarrage, le budget CONTEXT.md, la détection de drift d'ID/issue, et les Phases 1–1.5.

---

## Convention de chemin des scripts

| Variable | Valeur | Résolution |
|---|---|---|
| `${SKILL_DIR}` | Répertoire du skill injecté par le harness | Première ligne du résultat de `Skill(...)` |
| `${PY}` | Interpréteur Python résolu une fois | `python3 → python → py` via `import sys` |

`--roadmap-dir doc/roadmap` = toujours relatif au CWD du projet.

Raison de `import sys` : contourne le stub Microsoft Store `python3.exe` (détectable par `command -v` mais inutilisable).

---

## Bloc A.0 — Configuration collaborative

Lit `./doc/roadmap/.skill-config.yml` :

| État | Action |
|---|---|
| Clé `roadmap-tracking.collaborative` absente | AskUserQuestion → écrit `collaborative`, `mode: auto`, `last-calibration: <aujourd'hui>` |
| Présente | Lit sans redemander |

Après A.0 : si `help.welcomed` absent/`false` → affiche note de bienvenue → écrit `help.welcomed: true`.

---

## Bloc A.1 — Garde universelle d'index

S'exécute avant tout branchement listing/reprise, quel que soit le prompt.

| État de `.index.json` | Action |
|---|---|
| Présent | Continue silencieusement |
| Absent | AskUserQuestion → génère via `${PY} ${SKILL_DIR}/scripts/build_roadmap.py --roadmap-dir doc/roadmap --write` |

Si plans mal placés détectés après génération → **`⏸️ STOP OBLIGATOIRE`** → AskUserQuestion normaliser.

---

## Réconciliation au démarrage (bas coût)

Une fois par session, après A.1. Signaux détectables via `stat` uniquement (jamais de parsing individuel des plans) :

| Signal | Détection |
|---|---|
| Index périmé | `mtime(*.md)` > `mtime(.index.json)` |
| `roadmap.md` désynchronisé | `mtime(.index.json)` > `mtime(roadmap.md)` |
| Plan mal placé | Entrée `.index.json` : `status: done` hors `done/`, `status: archived` hors `archived/`, `active`/`blocked` sous `done/`/`archived/` |

Marqueur `.reconcile-declined` : `snooze-until: YYYY-MM-DD` ou `declined`.

| Choix | Action |
|---|---|
| Réconcilier | `build_roadmap.py --write` / `normalize_status.py --write` (dry-run d'abord) |
| Reporter | Écrit `snooze-until: <date>` dans `.reconcile-declined` |
| Refuser | Écrit `declined` dans `.reconcile-declined` |

---

## Budget CONTEXT.md

Mesure `wc -l` / `wc -c` uniquement (jamais relecture du contenu).

| Seuil | Valeur |
|---|---|
| Lignes | > 200 |
| Octets | > 15 360 |

Si dépassé : AskUserQuestion → `${PY} ${SKILL_DIR}/scripts/split_context.py --roadmap-dir doc/roadmap --write`.

Marqueur `.context-split-declined` (même pattern que `.reconcile-declined`).

---

## Lecture bornée de roadmap.md

Ne jamais lire `roadmap.md` en intégralité. Formes autorisées uniquement :

| Forme | Usage |
|---|---|
| `head -50` | Plans critical/high actifs, en-tête |
| `tail -30` | Clôtures récentes |
| `grep` | Comptage par statut/priorité |

---

## Source du listing : .index.json

`.index.json` = source canonique pour tout listing/filtrage.

| État | Action |
|---|---|
| Index présent | Lire `.index.json` → dériver le tableau listing |
| Index absent | Fallback lecture bornée de `roadmap.md` + proposition de génération |

Entrée par plan : `{id, status, priority, complexity, title, deps, path}`.  
Plans `status: done` exclus du listing actif (visibles dans `done/INDEX.md`).

---

## Détection de drift ID/issue (mode `github` uniquement)

Compare `plan.id` à `issue.id` pour chaque plan. Si drift détecté :

1. Lit `.migration-declined`.
2. Propose migration via AskUserQuestion.
3. `${PY} ${SKILL_DIR}/scripts/migrate_plan_ids.py --dry-run` → validation → `--patch-issues`.
4. Exécute `doctor.py` après migration.

Désactivé en mode `local`.

---

## Système d'aide

Déclencheurs (ne déclenchent pas le workflow, fonctionnent même sans `doc/roadmap/`) :

| Déclencheur | Contenu |
|---|---|
| `aide` | Aide complète |
| `aide workflow` | Phases 1→7, reprise, urgences, signaux de mode |
| `aide config` | `.skill-config.yml` complet, tous les champs |
| `aide planification` | Sizing, gate modèle, grilling, désengagement |
| `aide plans` | Front matter, listing, incohérences, clôture |
| `aide tests` | Tests intermédiaires, finaux, mode autonomous |
| `aide git` | Commits, migration, issues |
| `aide intégrations` | Skill impeccable, mapping IDE |
| `aide doctor` | `doctor.py` : commande, catégories de findings |
| `aide stats` | Statistiques portfolio depuis `.index.json` |
| `aide migration` | Adoption sur projet existant, quickstart 5 min |
| `help` | Alias de `aide` |

Générée à la volée depuis SKILL.md et references (pas de fichier séparé).

---

## Phase 1 — Analyse silencieuse

Mode : `🧠 MODE PLAN`. Aucune écriture, aucune commande.

Évalue : objectif principal, périmètre, zones d'ombre, dépendances, complexité globale et par étape (XS/S/M/L/XL).

Alimente : gate modèle (Phase 1.5), tags d'étape (Phase 3), champ `complexity` du front matter (Phase 5).

---

## Phase 1.5 — Gate modèle

| Cas | Condition | Action |
|---|---|---|
| Cas 1 | Tier du modèle actif ≥ tier requis par la complexité | Continuer silencieusement (aucun affichage) |
| Cas 2 | Mismatch | Bloc `⚠️` + `⏸️` bypass stop |

Si modèle non détectable : gate silencieusement sautée.

Gate réévoluée à chaque changement de modèle en session. Section canonique hébergée dans `modules/plan.md`.

---

## Garde d'entrée — checklist pré-action

6 vérifications obligatoires dans l'ordre avant toute implémentation :

1. Signal de mode affiché ?
2. A.1 exécutée ?
3. Plan identifié (reprise) ou listing affiché (nouveau) ?
4. Point d'arrêt `⏸️` respecté ?
5. `tests.mode` résolu ?
6. Phase 7 étape 0 exécutée (mode `manual`) ?

---

## Règle anti-court-circuit

| L'utilisateur dit | Traduction obligatoire |
|---|---|
| `Reprends le plan #NNN` | A.1 d'abord → résumé → `⏸️` → choix |
| `Démarre toutes les étapes de #109` | A.1 → reprise → résumé → `⏸️` → `tests.mode` → étape 0 → implémenter |
| `Go` / `Fais tout` | ≠ autorisation de bypass. Dérouler le workflow normalement |
| Prompt structuré comme une spec | Entrée de cadrage, pas bypass. Dérouler Phase 1 normalement |

---

## Enforcement mécanique (hooks)

| Hook | Événement | Comportement |
|---|---|---|
| `UserPromptSubmit` | À chaque tour | Réinjecte la préséance de la garde |
| `PreToolUse (Write\|Edit\|...)` | Premier outil mutant | Refuse une fois, s'auto-désarme, force l'invocation du skill |

Kill-switch : `ROADMAP_TRACKING_AUTOSTART=off`.
