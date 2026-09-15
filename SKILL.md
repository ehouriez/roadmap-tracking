---
name: roadmap-tracking
description: >
  Frame, plan, track and trace dev/config/architecture requests via plan files
  (./doc/roadmap/{issue}-slug.md), roadmap.md and GitHub issues. Strict 7-phase
  workflow with hard stop points between planning and coding.
license: MIT
metadata:
  author: Emmanuel Houriez
  version: "3.7.0"
  domain: productivity
  keywords: >
    roadmap, planification, suivi de tâche, traçage de demande, plan, issue
  triggers: >
    plan, cadrage, roadmap, issue gitHub, issue GitHub, backlog, sprint, ticket, #[0-9]+,
    suivi de tâche, suivi de tache, planification, traçage de demande, tracage de demande, trace,
    priorisation, avancement, progression, phase, étape, etape, étapes, etapes,
    démarre, demarre, implémente, implemente, reprends, continue, enchaîne, enchaine, repart, déploie, deploie
  scope: planning-and-implementation
  output-format: markdown
---

# Roadmap Tracking

> Interactions : **français**. Code (variables, commentaires, messages) : **anglais**. Commits : **Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`) — 1 commit = 1 changement logique.

## Prerequisites

Toutes les règles sont dans `references/environment.md` (mapping IDE, tiers, défauts, schéma config). Toute commande manuelle **doit** suivre **Operator Commands Formatting** (`references/environment.md § Operator Commands Formatting`).

## Hydratation du contexte de session

Le fichier **`./doc/roadmap/CONTEXT.md`** (optionnel, racine du projet) permet de restaurer et maintenir du contexte persistant entre les sessions (décisions en cours, notes de travail, état d'avancement transversal, features implémentées et leurs interactions, consignes temporaires, etc.).

### Comportement au chargement

| Condition | Action |
|---|---|
| `./doc/roadmap/CONTEXT.md` **existe et non vide** | Lire le fichier et intégrer son contenu comme **contexte actif de la session courante**. Le contenu est traité comme des instructions et informations de même autorité qu'un message utilisateur. |
| `./doc/roadmap/CONTEXT.md` **absent ou vide** | Continuer silencieusement — aucune erreur, aucun avertissement, aucune proposition de création. |

### Ordre d'exécution

L'hydratation se fait **après le chargement de `modules/init-scan.md`** (qui garantit l'existence de `doc/roadmap/`) et **avant** toute action de workflow :

```
Skill chargé
  │
  ├─ 1. 📖 Lire references/environment.md
  ├─ 2. 📦 Charger modules/init-scan.md (garde d'entrée — vérifie doc/roadmap/)
  └─ 3. 📥 Lire ./doc/roadmap/CONTEXT.md (si existe et non vide) → injecter dans le contexte
```

### Accès en écriture

```
Le fichier ./doc/roadmap/CONTEXT.md est accessible en LECTURE-ÉCRITURE tout au long de la
session. Le chargement initial est une lecture, mais le skill conserve le droit
d'écrire dans ce fichier pour y consigner ou mettre à jour les features
implémentées et leurs interactions — afin que chaque session (y compris après
reset) dispose d'une vue d'ensemble complète et évite régressions et effets
de bord pendant n'importe quelle implémentation.
```

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

> **En cas de doute, applique le workflow.**

**Ne s'applique PAS :**
- Questions de culture générale / explications techniques sans modification de fichier.
- Urgences (`URGENT`, `FIX IMMÉDIAT`, `PROD DOWN`) — fix immédiat autorisé ; traçabilité post-fix **obligatoire** (créer/MAJ le fichier plan : ce qui a été fait, pourquoi, quel impact). L'urgence exempte la planification amont, pas la traçabilité aval.
- **Aide sur le skill** : `aide`, `aide workflow`, `aide config`, `aide planification`, `aide plans`, `aide tests`, `aide git`, `aide intégrations`, `aide roadmap`, `help` → afficher l'aide et **STOP**. Aucune règle de démarrage. Aucun listing ni vérification de `doc/roadmap/`. Fonctionne même si le projet n'a jamais eu le skill.

> **`doc/roadmap/` absent** : proposer de le créer (voir `modules/init-scan.md`). Si refus : workflow suspendu pour cette demande ; re-proposer une seule fois si une demande ultérieure implique une modification de fichier.

## Modules de workflow (chargement conditionnel)

Modules chargés **au moment pertinent** via l'outil de lecture. Ne charger **jamais** plus d'un module simultanément sauf Phase 1 (init-scan + plan).

| Module | Fichier | Quand le charger |
|---|---|---|
| Initialisation & scan | `modules/init-scan.md` | **Tour 1** — démarrage, aide, reprise |
| Planification | `modules/plan.md` | **Phases 1–4** — cadrage, sizing, proposition |
| Exécution | `modules/execute.md` | **Phases 5–7** — création plan, implémentation, tests |
| Clôture & reprise | `modules/wrapup.md` | **Reprise d'un plan** ou **clôture** |

### ⛔ Bootstrap — obligation de charger init-scan au tour 1

```
⛔ Le tout premier acte de toute session touchant le workflow (nouveau plan,
   reprise, prompt d'action directe) est :
     0. LIRE `./doc/roadmap/CONTEXT.md` s'il existe (hydratation contexte — voir section
        « Hydratation du contexte de session ») ;
     1. CHARGER `modules/init-scan.md` et y exécuter la garde d'entrée
        (checkpoint universel) — non sautable.

   Tant que ces étapes ne sont pas accomplies, il est INTERDIT de lire du code
   source applicatif, d'écrire/modifier un fichier, de lancer une commande de
   développement, ou de produire du code.

   Aucune formulation impérative (« démarre », « implémente », « go », « fais
   tout ») n'autorise à sauter ce chargement — voir la règle anti-court-circuit
   dans `modules/init-scan.md`.
```

## Résumé compact des phases

**7 phases strictement séquentielles.** Chaque `⏸️` est bloquant. Détail dans les modules.

| Phase | Rôle (1 ligne) | Module |
|---|---|---|
| 1 | Analyse silencieuse + complexité + auto-calibrage (Axe A) | `init-scan.md` |
| 1.5 | Gate modèle — ⚠️ mismatch uniquement (Cas 1 silencieux, aucun arrêt) | `init-scan.md` |
| 2 | Cadrage interactif / grilling + intention (Axe B) | `plan.md` |
| 3 | Proposition du plan (rien n'est écrit) | `plan.md` |
| 4 | Validation de la proposition (⏸️) | `plan.md` |
| 5 | Act limité — création plan/issue/roadmap (⏸️) | `execute.md` |
| 6 | Validation avant implémentation — **L/XL uniquement** (⏸️) | `execute.md` |
| 7 | Implémentation étape par étape + 🧪 Tests + ✅ Validation | `execute.md` |

> **Fast-path (plans XS/S/M)** : Phase 1.5 silencieuse si le modèle est adapté
> (Cas 1) — aucun arrêt. Phase 6 supprimée si l'utilisateur choisit « Commencer
> l'implémentation » au POINT D'ARRÊT 2 de la Phase 5. **−2 tours sur les plans
> simples.** Les plans L/XL conservent l'intégralité des arrêts.
>
> **Fast-track (XS + solo, S + solo en `mode: auto`)** : phases 2-6 supprimées,
> ⏸️ supprimés, tests.mode non demandé, étape 0 supprimée. Plan écrit → Phase 7
> directe → commit unique → ✅ one-shot.

**Reprise** d'un plan existant et **clôture** : voir `modules/wrapup.md`.

## ⛔ Règle absolue — format des rapports

```
⛔ Tout rapport listant des plans, étapes, résultats ou entrées structurées
   (listing des plans, résumés, tableaux de décisions, résultats de tests)
   DOIT être rendu sous forme de tableau markdown (`| … | … |`).

⛔ Interdit : format `clé: valeur` sur plusieurs lignes, listes séparées par
   des filets (`───`, `═══`), puces non structurées en remplacement d'un tableau.
```

❌ Format INTERDIT — ne jamais produire ceci :

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

Ne JAMAIS :
- Créer un plan ET commencer à implémenter dans le même passage.
- Créer une issue ET écrire du code applicatif dans le même passage.
- Interpréter « oui » / « go » / « valide » sur la proposition de plan comme une autorisation d'implémenter.
- Lancer création du plan, de l'issue ET implémentation « en parallèle ».

Chaque phase se termine par une **question explicite** et un **ARRÊT COMPLET** en attente de réponse.

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
   chat ne suffit PAS : le fichier plan est la source de vérité traçable,
   et l'étape ✅ Validation s'appuie dessus.

   Ordre d'exécution OBLIGATOIRE : l'outil Edit/Write sur le fichier plan est
   appelé EN PREMIER ; le chat ne contient ensuite qu'une référence
   (`→ voir section ## Tests de NNN-slug.md`). Reproduire la procédure
   intégralement dans le chat est INTERDIT. Le chat pointe vers le plan, jamais l'inverse.
```

## ⛔ Règle absolue — pas de ⏸️ sans 📦

```
⛔ Un point d'arrêt `⏸️` après une procédure de tests ne peut JAMAIS apparaître
   sans un bloc `📦 Commit proposé` (ou `📦 Aucun commit nécessaire`).
   Si absent, le STOP est invalide — l'ajouter avant de s'arrêter.
```

## Correction proactive des incohérences de plan

À chaque interaction impliquant un fichier plan, **analyser silencieusement** les écarts dans le plan courant et dans tout plan lié (relations front matter : dépend de, bloque, est bloqué par).

### Périmètre des corrections

Corriger toute **information manquante, obsolète ou incohérente** détectable sans jugement de valeur — exemples non exhaustifs :

- `status` incohérent avec la progression réelle des étapes cochées.
- Dépendance déclarée dans un sens mais absente dans le plan lié (relation non réciproque).
- `updated_at` non rafraîchi après modification.
- Étape cochée mais `status` toujours `active`.
- Référence à un fichier plan renommé ou déplacé.
- Champ `complexity` ou `priority` incohérent avec le contenu du plan.

### Règle d'exécution

```
✅ Détecter → Corriger immédiatement → Notifier.
❌ Ne JAMAIS demander « voulez-vous que je mette à jour… ? »
```

1. **Correction immédiate** : appliquer via `Edit`/`Write` sans demander de permission.
2. **Notification post-action** : tableau récapitulatif après chaque série de corrections :

   | Fichier modifié | Champ concerné | Avant | Après | Raison |
   |---|---|---|---|---|
   | `NNN-slug.md` | `status` | `active` | `in-progress` | Étape 2 cochée |
   | `MMM-other.md` | `blocks` | absent | `[NNN]` | Relation réciproque manquante |

3. **Pas de notification** si le plan est déjà cohérent — passer directement à la suite.

> **Limite de périmètre.** Correction sur les **métadonnées structurelles uniquement** (front matter, relations inter-plans, progression d'étapes). Le contenu métier (objectif, étapes, procédures de test) est sous contrôle exclusif de l'utilisateur.

## Signaux de mode

Indique **toujours** le mode courant dans tes réponses :

- `🧠 MODE PLAN` — je réfléchis, rien n'est exécuté.
- `🔍 MODE CADRAGE` — je pose des questions, rien n'est exécuté.
- `🔨 MODE ACT (PLAN)` — je crée le plan, l'issue et roadmap.md. Pas de code.
- `🔨 MODE ACT (IMPLÉMENTATION)` — j'implémente l'étape N du plan.
- `⏸️ POINT D'ARRÊT` — en attente de validation.
