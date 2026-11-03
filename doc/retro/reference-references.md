# Référence — références

> Voir aussi : [Explication références](explanation-references.md)

Sept fichiers dans `references/` chargés à la demande selon la phase. Contrats et formats du workflow.

---

## Chargement conditionnel

| Fichier | Quand charger |
|---|---|
| `environment.md` | **Toujours au démarrage** |
| `forms.md` | Phase 2 (cadrage) |
| `templates.md` | Phase 5 + tout changement de statut |
| `roadmap-file.md` | Phase 5 + tout changement de statut |
| `github-issues.md` | Mode `github` uniquement |
| `migration.md` | Mode `github`, migration IDs |
| `autonomous-tests.md` | Phase 7 avec `tests.mode: autonomous` |

---

## environment.md

### Détection IDE

| IDE | Signal de détection |
|---|---|
| Claude Code | System prompt contient `"You are powered by the model named…"` |
| Codex | Marqueurs runtime Codex |
| Fallback | Tout autre environnement |

### Tiers de modèle

| Tier | Alias Anthropic | Alias OpenAI | Comportement |
|---|---|---|---|
| `standard` | sonnet | luna | Travail général |
| `reasoning` | opus | sol | Analyse complexe, architecture |
| `light` | haiku | terra | Toujours un mismatch — jamais recommandé |

**Résolution** : `models.map` (`.skill-config.yml`) en premier, puis defaults case-insensitive.

### Schéma `.skill-config.yml` (complet)

```yaml
ide: auto                       # auto | claude-code | codex
models:
  active: null
  map: []                       # [{name: "sol", tier: "reasoning"}, ...]
issues:
  mode: auto                    # auto | github | local
tests:
  mode: manual                  # manual | autonomous | null
  max_iterations: 3
  verifier: auto                # auto | subagent | inline
grilling:
  enabled: true
  categories:
    phase2: []
    phase4: []
    phase6: []
roadmap-tracking:
  collaborative: false
  mode: auto                    # auto | full | lightweight | off
  last-calibration: null        # YYYY-MM-DD
  help:
    welcomed: false
```

Toutes les clés optionnelles. Absent + Claude Code + `gh` = comportement v1.3.x.

### Formatage des commandes opérateur

Règles pour toute commande shell présentée à l'opérateur :

1. Une commande par ligne (jamais de `\` de continuation)
2. Pas de commentaires inline (`# ...`)
3. `echo "=== Description In Capitalized English ==="` avant chaque groupe logique
4. Ligne vide entre les groupes
5. Bloc prêt au copier-coller sans modification

### Verifier sub-agent (mode autonomous)

| IDE | Mécanisme |
|---|---|
| Claude Code | Outil `Agent` — fresh agent uniquement (PAS de fork) |
| Codex | `spawn_agent` |
| Fallback | Self-check inline (même contexte, isolation moindre) |

---

## forms.md

Protocole de cadrage interactif Phase 2.

**Format** :
- Round 1 : `AskUserQuestion`
- Rounds suivants : `❓ **Qn** [Catégorie]` (texte)

**Contraintes Round 1** :
- Max 4 questions par appel, max 4 options par question
- `header` ≤ 12 chars, option recommandée en première position

**Catégories** (guide, non exhaustif) :

| Catégorie | Obligatoire |
|---|---|
| Périmètre | Toujours |
| Objectifs / critères de succès | Toujours |
| Dépendances | Toujours |
| Choix techniques | Toujours |
| Découpage en lots | Obligatoire si complexité ≥ M |
| UX/UI | Si demande UX/UI |
| Suggestions | Optionnel |

**Termination** : frontier vide → résumé structuré → confirmation → Phase 3.

---

## templates.md

### Nommage des fichiers plan

| Mode | Format | Exemple |
|---|---|---|
| `github` | `{issue-number}-kebab-slug.md` | `27-image-versioning.md` |
| `local` | `{max(préfixes ∪ plan.id)+1}-kebab-slug.md` | `5-new-feature.md` |
| Draft | `draft-slug.md` | `draft-auth-module.md` |

Draft renommé via `git mv` dès l'issue créée.

### Front matter — champs obligatoires

| Champ | Type | Valeurs |
|---|---|---|
| `plan.id` | string | Numéro de l'issue ou compteur local |
| `plan.name` | string | Nom kebab-case |
| `plan.link` | string | Chemin relatif `doc/roadmap/...` |
| `status` | enum | `active` \| `done` \| `archived` \| `blocked` |
| `date` | ISO date | `YYYY-MM-DD` |
| `description` | string | |
| `priority` | enum | `critical` \| `high` \| `medium` \| `low` |
| `complexity` | enum | `XS` \| `S` \| `M` \| `L` \| `XL` |
| `issue.id` | string \| null | |
| `issue.url` | string \| null | |

Champs optionnels : `enriched`, `plan.source`, `intent` (`null|prototype|production`), `scope.modules`, `scope.patterns`.

Mapping canonique : `in-progress→active`, `cancelled→archived`.

### Tags d'étape

Format : `(taille · tier → modèle)`. Exemples : `(M · reasoning → opus)`, `(S · standard → sonnet)`.

`🧪 Tests` et `✅ Validation` : jamais de tags, toujours les deux dernières étapes.

### Sections du plan

```
## Objectif
## Périmètre (Inclus / Hors scope)
## Étapes
## Décisions techniques
## Tests (Prérequis / Procédure / Résultats)
## Journal de session
## Diagnostic en cours  ← créé à la 1ère failure, supprimé à la résolution
```

---

## roadmap-file.md

### Statuts canoniques

| Statut | Emoji | Sous-dossier |
|---|---|---|
| `active` | 🟢 | racine `doc/roadmap/` |
| `blocked` | 🔴 | racine `doc/roadmap/` |
| `done` | 🔵 | `done/` |
| `archived` | ⚪ | `archived/` |

Tout statut hors enum : rejeter avant create/update.

**Tri du backlog** : `critical → high → medium → low`, puis ID croissant.

**`archived/`** : distinct de `done/`. `archived/roadmap_done.md` = fichier gelé déprécié.

---

## github-issues.md

**Prérequis** : `command -v gh && gh auth status` avant toute action GitHub.

**Ordre** : issue créée avant le fichier plan (numéro = ID = préfixe du fichier).

**Fallback sans `gh`** : titre/labels/body pour copier-coller, `draft-slug.md` provisoire, attente du numéro.

**Clôture** : commentaire + `gh issue close` quand `status: done`. Jamais d'issue ouverte avec plan done.

---

## migration.md

Mode `github` uniquement.

**Résolution ID** : `issue.id` en front matter → `--map`/`--map-file` → `⚠️ non migré`.

**Toujours** : dry-run d'abord + `git status`/`git diff` avant commit.

`.migration-declined` : dans `.gitignore` (état personnel, non partagé).

Script `migrate_plan_ids.py` : ne réécrit jamais le corps des plans (normalisation = tâche humaine guidée par `templates.md`).

---

## autonomous-tests.md

Mode opt-in uniquement. Activation : `tests.mode: autonomous` dans `.skill-config.yml`.

### Rôles

| Rôle | Responsabilités |
|---|---|
| **Executor** | Implémente, corrige, exécute les tests, rapporte les résultats bruts |
| **Verifier** | Reçoit les résultats uniquement, rend verdict PASS/FAIL, ne touche jamais au code |

### Boucle d'itération

```
RÉPÉTER max_iterations fois (défaut 3) :
  Executor → exécute les tests → résultats bruts
  Verifier → verdict PASS/FAIL
  SI PASS → 📦 Commit proposé + ⏸️ STOP
  SI FAIL → Executor corrige
FIN : diagnostic structuré + décision opérateur
```

**Verifier isolation** : fresh `Agent` (PAS fork) sur Claude Code ; `spawn_agent` sur Codex.

**Persistence obligatoire** : après chaque verdict, procédure + résultats écrits dans `## Tests` du plan.

**`max_iterations`** vs **"2 strikes"** : `max_iterations` = intra-session (une étape) ; "2 strikes" = inter-session (un bloc de test).
