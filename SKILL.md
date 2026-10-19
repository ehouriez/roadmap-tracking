---
name: roadmap-tracking
description: >
  Frame, plan, track and trace dev/config/architecture requests via plan files
  (./doc/roadmap/{issue}-slug.md), roadmap.md and GitHub issues. Strict 7-phase
  workflow with hard stop points between planning and coding.
license: MIT
metadata:
  author: Emmanuel Houriez
  version: "4.0.1"
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

Le contexte persistant inter-sessions (décisions en cours, pièges, dépendances
entre features, consignes durables) est **segmenté** pour borner le coût fixe
d'amorçage — un `CONTEXT.md` non borné est un gouffre à tokens re-payé à chaque
session (voir rapport d'audit §4.3) :

| Fichier | Rôle | Chargement |
|---|---|---|
| `./doc/roadmap/CONTEXT.md` | **Noyau** — RÈGLES ABSOLUES uniquement (pièges structurants, invariants, consignes transverses). Budget dur : **≤ 200 lignes / ≤ 15 Ko**. | **Toujours** au démarrage (si existe et non vide). |
| `./doc/roadmap/context/*.md` | **Notes thématiques** (`context/pieges.md`, `context/deploiement.md`…) | **À la demande** — uniquement quand la tâche courante touche le thème. |

### Comportement au chargement (noyau `CONTEXT.md`)

| Condition | Action |
|---|---|
| `CONTEXT.md` **existe et non vide** | Lire et injecter comme **contexte actif de la session**. Autorité = message utilisateur. |
| `CONTEXT.md` **absent ou vide** | Continuer silencieusement — aucune erreur, aucun avertissement, aucune proposition de création. |
| `CONTEXT.md` **dépasse le budget** (> 200 l. / 15 Ko) | Le lire quand même (ne jamais tronquer un noyau existant), mais **signaler le dépassement** et proposer de basculer le surplus vers `context/*.md`. |

### Chargement des notes thématiques (`context/`)

- Ne **jamais** charger `context/*.md` en bloc au démarrage (ce serait recréer le coût fixe qu'on supprime).
- Charger un fichier thématique **uniquement** quand son thème est pertinent pour la demande en cours (ex. tâche de déploiement → lire `context/deploiement.md`).
- `context/` absent → continuer silencieusement.

### Capitalisation automatique encadrée

Le skill peut consigner un apprentissage durable pour qu'il survive au reset de
session. **Toujours encadré** — jamais d'écriture silencieuse :

1. **Capture gatée** — à la détection d'un élément capitalisable, proposer via `AskUserQuestion` : **Oui** (consigner) / **Non** (ignorer) / **Instructions** (l'utilisateur dicte quoi et où consigner). Ne jamais écrire sans ce feu vert.
2. **Catégorisation obligatoire** — chaque entrée porte un préfixe de catégorie **et** une référence au plan d'origine. Format : `⚠️ [#27] <contenu>`.

   | Préfixe | Catégorie |
   |---|---|
   | ⚠️ | Piège / régression évitée |
   | 🔗 | Dépendance entre features/plans |
   | 📌 | Contrainte durable |
   | 💡 | Insight / décision structurante |

3. **Garde-fou de budget (routage)** — avant d'écrire dans le noyau `CONTEXT.md`, vérifier le budget. Si l'ajout fait **dépasser 200 lignes / 15 Ko**, **refuser l'ajout au noyau** et proposer de l'écrire dans le fichier thématique approprié (`context/<thème>.md`, créé si absent). Le noyau reste réservé aux RÈGLES ABSOLUES.
4. **Purge à la clôture** — à la clôture d'un plan, proposer de purger les entrées CONTEXT devenues obsolètes (ex. un piège résolu par le plan clos). Proposition OUI/NON, jamais de suppression silencieuse. Voir `modules/wrapup.md § Clôture d'un plan validé`.

### Ordre d'exécution

L'hydratation du noyau se fait **après le chargement de `modules/init-scan.md`** (qui garantit l'existence de `doc/roadmap/`) et **avant** toute action de workflow ; les notes thématiques sont lues plus tard, à la demande :

```
Skill chargé
  │
  ├─ 1. 📖 Lire references/environment.md
  ├─ 2. 📦 Charger modules/init-scan.md (garde d'entrée — vérifie doc/roadmap/)
  ├─ 3. 📥 Lire ./doc/roadmap/CONTEXT.md (noyau, si existe et non vide) → injecter
  └─ 4. 📂 context/*.md : chargé à la demande selon la pertinence de la tâche (jamais au démarrage)
```

### Accès en écriture

`CONTEXT.md` (noyau) et `context/*.md` (thématiques) sont en **LECTURE-ÉCRITURE**
toute la session, afin que chaque session (y compris après reset) dispose d'une
vue d'ensemble et évite régressions et effets de bord. Le chargement initial est
une lecture ; **toute écriture suit la capitalisation encadrée ci-dessus**
(capture gatée, catégorisation obligatoire, garde-fou de budget).

## Fichiers de référence

Charge-les **à la demande**, seulement quand la phase l'exige :

| Fichier | Quand le lire |
|---|---|
| `references/environment.md` | **Toujours au démarrage** — mapping IDE, tiers, défauts, schéma config, formatage commandes |
| `references/forms.md` | Phase 2 — matière des questions et catégories de grilling |
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
