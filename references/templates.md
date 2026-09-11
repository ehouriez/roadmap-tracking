# Nommage, front matter et template de plan (Phase 5)

## Stockage et nommage

Les fichiers de plan sont créés dans `./doc/roadmap/` du projet courant.

Le **préfixe numérique** vient de deux sources selon le mode `issues` :

| Mode | Source de l'ID | Exemple |
|---|---|---|
| `github` | Numéro de l'issue GitHub rattachée | `27-image-versioning.md` |
| `local` | Compteur local = max(préfixes existants) + 1 | `5-new-feature.md` |

- Nom après le préfixe : **kebab-case**, concis et descriptif.
- **Mode `github`** ⚠️ : l'issue doit exister avant le fichier plan (son numéro est l'ID). Si l'issue n'est pas encore créée, voir le fallback ci-dessous.
- **Mode `local`** : pas de collision distribuée possible (git arbitre au merge).

```
./doc/roadmap/
├── 5-new-feature.md              ← ID local (mode local)
├── 8-setup-initial.md
├── 12-auth-module.md
└── 27-image-versioning-policy.md ← ID = numéro d'issue GitHub (mode github)
```

### Fallback : plan sans issue (mode `github` temporaire)

Si tu dois esquisser un plan avant de créer l'issue, nomme-le
`draft-nom-du-plan.md`. Dès que l'issue est créée, **renomme** le fichier en
`{ISSUE}-nom-du-plan.md` (via `git mv`) et mets à jour `plan.id`, `plan.name`,
`plan.link` et le titre H1.

## Titre du plan

H1 avec le `#{ISSUE}` (ici le `#` est du texte lisible, pas un problème de
lien), et un emoji cohérent :

- `8-setup-initial.md` → `# [🔧] Plan #8 - Setup Initial`
- `27-image-versioning-policy.md` → `# [🖼️] Plan #27 - Image Versioning Policy`

> Le `#` n'apparaît **jamais** dans le nom de fichier ni dans les cibles de
> liens — uniquement dans le texte affiché.

## Front matter YAML (obligatoire)

| Attribut | Obligatoire | Description |
|---|---|---|
| `plan.id` | ✅ | Identifiant du plan — numéro d'issue GitHub *(mode `github`)* ou compteur local *(mode `local`)*. String sans padding (ex. `'27'`). |
| `plan.name` | ✅ | Nom du fichier (ex. `27-saas-v2.md`) |
| `plan.link` | ✅ | URL GitHub du fichier *(mode `github`)* ou chemin relatif `doc/roadmap/{id}-slug.md` *(mode `local`)* |
| `plan.source` | ❌ | `local` si créé en mode local (absent = mode github, rétrocompat) |
| `status` | ✅ | `active`, `done`, `archived` ou `blocked` |
| `date` | ✅ | Date de création (`YYYY-MM-DD`) |
| `enriched` | ❌ | Dernière modif significative (`YYYY-MM-DD`) |
| `description` | ✅ | Phrase succincte (1-2 lignes) |
| `priority` | ✅ | `low`, `medium`, `high`, `critical` |
| `complexity` | ✅ | `XS`, `S`, `M`, `L`, `XL` |
| `scope.modules` | ❌ | Dossiers/fichiers principaux impactés |
| `scope.patterns` | ❌ | Glob patterns concernés |
| `issue.id` | ✅ | Numéro d'issue GitHub ou `null` *(mode `local` → toujours `null`)* |
| `issue.url` | ✅ | URL de l'issue ou `null` *(mode `local` → toujours `null`)* |

### Exemple

**Mode `github`** :

```yaml
---
plan:
  id: '30'
  name: 30-saas-v2.md
  link: https://github.com/owner/repo/blob/main/doc/roadmap/30-saas-v2.md
status: active
date: 2026-06-14
enriched: 2026-08-18
description: >
  Transformer la plateforme vers un SaaS orienté catalogue de services.
priority: high
complexity: L
scope:
  modules:
    - src/connectors/
    - src/api/gateway.ts
  patterns:
    - "**/*.ts"
issue:
  id: 30
  url: https://github.com/owner/repo/issues/30
---
```

**Mode `local`** :

```yaml
---
plan:
  id: '5'
  name: 5-new-feature.md
  link: doc/roadmap/5-new-feature.md
  source: local
status: active
date: 2026-06-14
description: >
  Ajouter la fonctionnalité X.
priority: medium
complexity: M
issue:
  id: null
  url: null
---
```

> **Mode `github`** : `plan.id` = `issue.id`. Dériver l'`owner/repo` via
> `gh repo view --json nameWithOwner -q .nameWithOwner` ou
> `git remote get-url origin`. Convertir les dates relatives en dates absolues.
>
> **Mode `local`** : `plan.link` est un chemin relatif, pas une URL.
> `issue.id` et `issue.url` sont toujours `null`.

## Template de contenu

```markdown
---
(front matter YAML)
---

# [🔧] Plan #{ISSUE} - Nom du Plan

## Objectif

Pourquoi ce plan existe (1-3 phrases).

## Périmètre

### Inclus
- Module / fichier / fonctionnalité concernée

### Hors scope
- Ce qui ne sera PAS traité

## Étapes

- [ ] Étape 1 — Description succincte (XS · standard → Sonnet)
- [ ] Étape 2 — Description succincte (L · reasoning → Opus)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test (avant-dernière étape, obligatoire)
- [ ] ✅ Validation — Vérifier les résultats des tests et clôturer (dernière étape, obligatoire)

> Chaque étape d'implémentation porte un tag `(taille · tier → modèle)` en
> fin de ligne — taille selon la grille de sizing, tier selon la matrice
> complexité → tier, modèle résolu au moment de la création depuis le mapping
> de `references/environment.md` (voir la section « Évaluation de complexité »
> du SKILL). Ce tag est **persisté ici** pour que la reprise d'un plan puisse
> le réafficher. Les étapes `🧪 Tests` et `✅ Validation` n'en portent jamais.

> Les deux dernières étapes (`🧪 Tests` et `✅ Validation`) sont **obligatoires,
> non supprimables et non fusionnables** avec une étape d'implémentation. Elles
> restent **toujours les deux dernières**, quel que soit le nombre d'étapes
> d'implémentation. Voir la Phase 7 du SKILL.

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|

## Journal de session

### Session YYYY-MM-DD
- ✅ Fait : ...
- 🔄 En cours : ...
- 📋 Prochain : ...
- 🚧 Blocages : ...
```

> **Décisions techniques** et **Journal de session** peuvent être vides à la
> création et se remplissent au fil des sessions.
