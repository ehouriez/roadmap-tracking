---
name: roadmap-tracking
description: >
  Use to frame, plan, track and trace any development, configuration or
  architecture request through plan files (./doc/roadmap/{issue}-slug.md,
  named after the linked GitHub issue), a consolidated roadmap.md and linked
  GitHub issues. Drives a strict
  7-phase workflow — silent analysis, interactive scoping, plan proposal,
  validation, plan/issue/roadmap creation, validation, then step-by-step
  implementation — with hard stop points between planning and coding.
  Invoke at the start of any dev/config/architecture session, on reference
  to an existing plan or issue, or on demand.
license: MIT
metadata:
  author: Emmanuel Houriez
  version: "3.0.0"
  domain: workflow
  triggers: >
    plan, cadrage, roadmap, issue GitHub, suivi de tâche, planification,
    traçage de demande, démarre, implémente, commence, exécute, lance,
    étape, étapes, continue, reprends, enchaîne, déploie, code, développe,
    implémentation, #[0-9]+, go, fais tout, fais le
  role: process
  scope: planning-and-implementation
  output-format: markdown
---

# Roadmap Tracking

Cadre, suit et trace les demandes de développement, configuration ou
architecture via des **fichiers plan**, un **roadmap.md** consolidé et des
**issues GitHub** liées.

> Toutes les interactions sont en **français**. Tout le contenu écrit dans le
> code est en **anglais** (variables, commentaires, docstrings, messages). Les
> commits suivent la convention **Conventional Commits** (`feat:`, `fix:`,
> `docs:`, `refactor:`, `chore:`…), un commit = un changement logique.

## Prerequisites

This skill is self-contained: all required rules and environment mappings are
embedded in `references/environment.md`. No external files needed.

Every shell command presented for manual execution **must** follow the
**Operator Commands Formatting** rules defined in
`references/environment.md § Operator Commands Formatting`.

## Fichiers de référence

Charge-les **à la demande**, seulement quand la phase l'exige :

| Fichier | Quand le lire |
|---|---|
| `references/environment.md` | **Toujours au démarrage** — mapping IDE, tiers, défauts, schéma config, formatage commandes |
| `references/forms.md` | Phase 2 — construire le formulaire de cadrage interactif |
| `references/templates.md` | Phase 5 — nommage `NNN-kebab`, front matter YAML, template de plan |
| `references/roadmap-file.md` | Phase 5 et à chaque changement de statut — structure et tri de `roadmap.md` |
| `references/github-issues.md` | **Mode `github` uniquement** — dès qu'une issue doit être créée ou mise à jour |
| `references/migration.md` | **Mode `github` uniquement** — migrer d'anciens plans `NNN-*` vers l'ID = numéro d'issue |
| `references/autonomous-tests.md` | Phase 7 avec `tests.mode: autonomous` — boucle vérif/exéc, reporting, garde-fou |

## Applicabilité

Ce workflow s'applique au **travail de développement, configuration ou
architecture** sur le projet courant.

> **En cas de doute, applique le workflow.**

Il **ne s'applique PAS** pour :
- Les questions de culture générale / explications techniques ne touchant **aucun fichier du projet** (aucun read, write, create, delete).
- Les urgences explicites (`URGENT`, `FIX IMMÉDIAT`, `PROD DOWN`) — le fix immédiat est autorisé, mais une étape post-fix de traçabilité est obligatoire (voir ci-dessous).
- **Demandes d'aide sur le skill lui-même** : `aide`, `aide workflow`, `aide config`, `aide planification`,
  `aide plans`, `aide tests`, `aide git`, `aide intégrations`, `aide roadmap`, `help`
  → Afficher l'aide demandée et **STOP**.
  Aucune règle de démarrage. Aucun listing de plans. Aucune vérification de `doc/roadmap/`.
  Fonctionne même si le projet n'a jamais eu le skill.

> **Urgences — traçabilité post-fix obligatoire** : dès la correction appliquée,
> créer ou mettre à jour le fichier plan correspondant pour consigner ce qui a
> été fait, pourquoi, et quel impact. L'urgence exempte de la planification
> amont, pas de la traçabilité aval.

> **`doc/roadmap/` absent** : si le skill est invoqué sur un projet sans
> répertoire `doc/roadmap/`, il ne refuse pas — il propose de le créer (voir
> « Règle de démarrage » dans `modules/init-scan.md`). Si l'utilisateur refuse, le workflow ne
> s'applique pas pour cette demande ; si une demande ultérieure dans la même
> session implique une modification de fichier du projet, le skill re-propose
> la création une seule fois (voir « Règle de démarrage » dans `modules/init-scan.md`).

## Modules de workflow (chargement conditionnel)

Le corps du workflow est découpé en modules chargés **au moment pertinent** via
l'outil de lecture de fichier. Ne charge **jamais** plus d'un module à la fois
sauf en Phase 1 (init-scan + plan).

| Module | Fichier | Quand le charger |
|---|---|---|
| Initialisation & scan | `modules/init-scan.md` | **Tour 1** — démarrage, aide, reprise |
| Planification | `modules/plan.md` | **Phases 1–4** — cadrage, sizing, proposition |
| Exécution | `modules/execute.md` | **Phases 5–7** — création plan, implémentation, tests |
| Clôture & reprise | `modules/wrapup.md` | **Reprise d'un plan** ou **clôture** |

### ⛔ Bootstrap — obligation de charger init-scan au tour 1

```
⛔ Le tout premier acte de toute session touchant le workflow (nouveau plan,
   reprise, prompt d'action directe) est de CHARGER `modules/init-scan.md` et
   d'y exécuter la garde d'entrée (checkpoint universel) — non sautable.
   Tant que ce module n'est pas chargé et sa checklist satisfaite, il est
   INTERDIT de lire du code source applicatif, d'écrire/modifier un fichier, de
   lancer une commande de développement, ou de produire du code.
   Aucune formulation impérative (« démarre », « implémente », « go », « fais
   tout ») n'autorise à sauter ce chargement — voir la règle anti-court-circuit
   dans `modules/init-scan.md`.
```

## Résumé compact des phases

Le workflow complet compte **7 phases strictement séquentielles**, chaque point
d'arrêt `⏸️` étant bloquant. Détail dans les modules.

| Phase | Rôle (1 ligne) | Module |
|---|---|---|
| 1 | Analyse silencieuse + complexité + auto-calibrage (Axe A) | `init-scan.md` |
| 1.5 | Gate de recommandation de modèle | `init-scan.md` |
| 2 | Cadrage interactif / grilling + intention (Axe B) | `plan.md` |
| 3 | Proposition du plan (rien n'est écrit) | `plan.md` |
| 4 | Validation de la proposition (⏸️) | `plan.md` |
| 5 | Act limité — création plan/issue/roadmap (⏸️) | `execute.md` |
| 6 | Validation avant implémentation (⏸️) | `execute.md` |
| 7 | Implémentation étape par étape + 🧪 Tests + ✅ Validation | `execute.md` |

**Reprise** d'un plan existant et **clôture** : voir `modules/wrapup.md`.

## ⛔ Règle absolue — format des rapports

```
⛔ Tout rapport listant des plans, étapes, résultats ou entrées structurées
   (listing des plans, résumés, tableaux de décisions, résultats de tests)
   DOIT être rendu sous forme de tableau markdown (`| … | … |`).

⛔ Interdit : format `clé: valeur` sur plusieurs lignes, listes séparées par
   des filets (`───`, `═══`), puces non structurées en remplacement d'un
   tableau. Les exemples de tableau du skill sont des GABARITS CONTRAIGNANTS,
   pas des suggestions.
```

❌ Exemple exact du format INTERDIT — ne jamais produire ceci :

```
#: 1
Fichier: 27-nom.md
Statut: 🟢 Active
Résumé: Description du plan
Priorité: HAUTE
────────────────────────────────────────
#: 2
Fichier: 28-autre.md
Statut: 🔴 Bloqué
```

✅ Seul format valide : `| # | Fichier | Statut | Résumé | Issue GitHub |` (tableau markdown).

## ⛔ Règle absolue — séparation création / implémentation

La **création d'un plan** et l'**implémentation de son contenu** sont TOUJOURS
deux étapes distinctes séparées par une validation utilisateur explicite.

Ne JAMAIS :
- Créer un plan ET commencer à implémenter dans le même passage.
- Créer une issue ET écrire du code applicatif dans le même passage.
- Interpréter « oui » / « go » / « valide » sur la proposition de plan comme une
  autorisation d'implémenter.
- Lancer création du plan, de l'issue ET implémentation « en parallèle ».

Chaque phase se termine par une **question explicite** et un **ARRÊT COMPLET**
en attente de réponse.

## ⛔ Règle absolue — tests obligatoires avant clôture

```
⛔ Un plan ne peut JAMAIS être marqué `status: done` si les étapes 🧪 Tests
   et ✅ Validation n'ont pas été explicitement complétées et cochées.
   Aucune exception.
```

## ⛔ Règle absolue — traçabilité des tests dans le fichier plan

```
⛔ Quel que soit le mode (`manual` OU `autonomous`), la procédure de test, les
   résultats attendus ET les résultats réellement joués et vérifiés sont
   TOUJOURS créés ou mis à jour dans la section `## Tests` du fichier plan
   (voir references/templates.md). Vaut pour les tests intermédiaires comme
   pour les tests finaux 🧪 Tests. Afficher les résultats uniquement dans le
   chat (verdict Vérificateur inclus) ne suffit PAS : le fichier plan est la
   source de vérité traçable, et l'étape ✅ Validation s'appuie dessus.

   Ordre d'exécution OBLIGATOIRE : l'outil Edit/Write sur le fichier plan est
   appelé EN PREMIER ; le chat ne contient ensuite qu'une référence
   (`→ voir section ## Tests de NNN-slug.md`). Reproduire la procédure
   intégralement dans le chat — même dans la même réponse que l'écriture dans
   le plan — est INTERDIT. Le chat pointe vers le plan, jamais l'inverse.
```

## ⛔ Règle absolue — pas de ⏸️ sans 📦

```
⛔ Un point d'arrêt `⏸️` après une procédure de tests (intermédiaires ou
   finaux) ne peut JAMAIS apparaître sans être précédé d'un bloc
   `📦 Commit proposé` (ou d'un `📦 Aucun commit nécessaire` explicite).
   Si le bloc commit est absent, le STOP est invalide — revenir en arrière
   et l'ajouter avant de s'arrêter.
```

## Correction proactive des incohérences de plan

À chaque interaction impliquant un fichier plan (démarrage, reprise, fin
d'étape, mise à jour de statut), **analyser silencieusement** les écarts
présents dans le fichier plan courant **et** dans tout fichier plan lié par une
relation de dépendance (dépend de / est requis par, bloque / est bloqué par,
et toute autre relation inter-plans présente dans les front matters).

### Périmètre des corrections

Appliquer les corrections sur **toute information manquante, obsolète ou
incohérente** détectable sans jugement de valeur — exemples non exhaustifs :

- Champ `status` incohérent avec la progression réelle des étapes cochées.
- Dépendance déclarée dans un sens mais absente dans le plan lié (relation non
  réciproque).
- `updated_at` non rafraîchi après une modification.
- Étape cochée mais `status` toujours `active` (devrait être `in-progress` ou
  `done`).
- Référence à un fichier plan renommé ou déplacé.
- Champ `complexity` ou `priority` présent mais incohérent avec le contenu du
  plan.

### Règle d'exécution

```
✅ Détecter → Corriger immédiatement → Notifier.
❌ Ne JAMAIS demander « voulez-vous que je mette à jour… ? »
```

1. **Correction immédiate** : appliquer les modifications via les outils
   `Edit`/`Write` sans demander de permission.
2. **Notification post-action** : après chaque série de corrections, afficher
   un tableau récapitulatif :

   | Fichier modifié | Champ concerné | Avant | Après | Raison |
   |---|---|---|---|---|
   | `NNN-slug.md` | `status` | `active` | `in-progress` | Étape 2 cochée |
   | `MMM-other.md` | `blocks` | absent | `[NNN]` | Relation réciproque manquante |

3. **Pas de notification si aucun écart** : si le plan est déjà cohérent, ne
   rien afficher — passer directement à la suite du workflow.

> **Limite de périmètre.** Cette correction s'applique aux **métadonnées
> structurelles** (front matter, relations inter-plans, progression d'étapes).
> Elle n'inclut **jamais** de modification du contenu métier du plan (objectif,
> description, étapes, procédures de test) — ces champs sont sous contrôle de
> l'utilisateur et ne sont modifiés qu'à sa demande explicite.

## Signaux de mode

Indique **toujours** le mode courant dans tes réponses :

- `🧠 MODE PLAN` — je réfléchis, rien n'est exécuté.
- `🔍 MODE CADRAGE` — je pose des questions, rien n'est exécuté.
- `🔨 MODE ACT (PLAN)` — je crée le plan, l'issue et roadmap.md. Pas de code.
- `🔨 MODE ACT (IMPLÉMENTATION)` — j'implémente l'étape N du plan.
- `⏸️ POINT D'ARRÊT` — en attente de validation.

