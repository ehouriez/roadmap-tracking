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
  version: "1.2.1"
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

This skill requires strict compliance with the rule defined in:
  `operator-commands-formatting.md`
This file is located in the `rules/` directory of the operator's personal `.claude` folder (the one used by Claude Code for personal rules).

Toute commande manuelle présentée à l'opérateur dans le contexte de ce skill
**doit** respecter cette règle de formatage.

## Fichiers de référence

Charge-les **à la demande**, seulement quand la phase l'exige :

| Fichier | Quand le lire |
|---|---|
| `references/forms.md` | Phase 2 — construire le formulaire de cadrage interactif |
| `references/templates.md` | Phase 5 — nommage `NNN-kebab`, front matter YAML, template de plan |
| `references/roadmap-file.md` | Phase 5 et à chaque changement de statut — structure et tri de `roadmap.md` |
| `references/github-issues.md` | Dès qu'une issue doit être créée ou mise à jour |
| `references/migration.md` | Migrer d'anciens plans `NNN-*` vers l'ID = numéro d'issue (script) |

## Applicabilité

Ce workflow s'applique au **travail de développement, configuration ou
architecture** sur le projet courant.

Il **ne s'applique PAS** pour :
- Les questions de culture générale / explications techniques sans impact projet.
- Les urgences explicites (`URGENT`, `FIX IMMÉDIAT`, `PROD DOWN`).
- Les demandes one-shot sans impact codebase (ex. générer une commande curl).

En cas de doute, applique le workflow.

## Règle de démarrage

Si l'utilisateur ne référence pas un plan existant dans son premier prompt :

1. **Lister les plans existants** (mémoires, contexte projet, et inspection de
   `./doc/roadmap/`) :

```
### 📋 Plans existants

| # | Fichier | Statut | Résumé | Issue GitHub |
|---|---------|--------|--------|--------------|
| 1 | `27-nom.md` | 🟢 Active | Description (front matter ou ligne "Description") | `#27` ou ❌ Non rattachée |
```

2. **Demander** : « Souhaites-tu repartir d'un de ces plans existants (indique
   le numéro) ou créer un nouveau plan pour cette session ? »
3. **Attendre la réponse** avant de traiter le prompt.

## Détection d'ID de plan incohérents

En listant les plans (règle de démarrage), compare pour chacun le **`plan.id`**
au **`issue.id`** de son issue rattachée. Si au moins un plan a un `plan.id`
**différent** de son `issue.id` (ex. plan historique `27-slug.md` rattaché à
l'issue `#44`), propose une migration — **avant** de traiter le prompt.

### Marqueur de report / refus

Le fichier `./doc/roadmap/.migration-declined` mémorise le choix de
l'utilisateur. Avant toute proposition, le lire :

- **Absent** → proposer la migration (voir ci-dessous).
- Contient `snooze-until: YYYY-MM-DD` **dans le futur** → ne rien proposer.
- Contient `snooze-until: YYYY-MM-DD` **échu** (≤ aujourd'hui) → reproposer.
- Contient `declined` → ne rien proposer (sauf demande explicite « migre mes
  plans » ou suppression du fichier par l'utilisateur).

> **Déclencheur explicite « migre mes plans ».** Quel que soit l'état du
> marqueur, si l'utilisateur demande « migre mes plans », lancer directement le
> workflow de migration. Si le dry-run ne trouve **aucun** plan à migrer
> (`0 plan(s) migrated` : tous les `plan.id` sont déjà alignés sur leur
> `issue.id`), l'indiquer — « Tes plans sont déjà alignés, rien à migrer. » — et
> ne rien exécuter d'autre.

### Proposition (marqueur absent ou report échu)

Poser un choix à **3 options** via `AskUserQuestion` :

| Choix | Action |
|---|---|
| **Migrer maintenant** | Exécuter le workflow de migration (dry-run puis patch-issues, ci-dessous). Sur succès, supprimer un éventuel `.migration-declined`. |
| **Reporter (2 / 8 / 30 jours)** | Écrire `snooze-until: <aujourd'hui + N jours>` dans `./doc/roadmap/.migration-declined`. |
| **Refuser** | Écrire `declined` dans `./doc/roadmap/.migration-declined` et indiquer à l'utilisateur : « Tu pourras relancer la migration en disant *migre mes plans* ou en supprimant `doc/roadmap/.migration-declined`. » |

### Workflow de migration (choix « Migrer maintenant »)

1. **Dry-run d'abord.** Explique concrètement ce que l'exécution va faire, puis
   lance l'aperçu (aucune modification) :

   ```bash
   python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --dry-run
   ```

   > Cette exécution **ne modifie rien** : elle liste les renommages
   > `plan.id → issue.id`, les fichiers `git mv`, les réécritures de front
   > matter / titre H1 et les liens de `roadmap.md`. Voir `references/migration.md`.

   Présente la sortie et **demande validation**.

2. **Migration réelle, seulement si l'utilisateur valide ET que le dry-run est
   safe** (aucune erreur, aucun plan sans `issue.id` bloquant). Explique que
   cette exécution renomme réellement les fichiers, réécrit les plans + le
   `roadmap.md`, **et** corrige le corps des issues GitHub (référence de plan +
   commentaire de traçage) :

   ```bash
   python3 ~/.claude/skills/roadmap-tracking/scripts/migrate_plan_ids.py --patch-issues
   ```

   Si le dry-run signale une anomalie, **ne pas** lancer la migration : la
   remonter à l'utilisateur.

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

## ⛔ Règle absolue — pas de ⏸️ sans 📦

```
⛔ Un point d'arrêt `⏸️` après une procédure de tests (intermédiaires ou
   finaux) ne peut JAMAIS apparaître sans être précédé d'un bloc
   `📦 Commit proposé` (ou d'un `📦 Aucun commit nécessaire` explicite).
   Si le bloc commit est absent, le STOP est invalide — revenir en arrière
   et l'ajouter avant de s'arrêter.
```

## Signaux de mode

Indique **toujours** le mode courant dans tes réponses :

- `🧠 MODE PLAN` — je réfléchis, rien n'est exécuté.
- `🔍 MODE CADRAGE` — je pose des questions, rien n'est exécuté.
- `🔨 MODE ACT (PLAN)` — je crée le plan, l'issue et roadmap.md. Pas de code.
- `🔨 MODE ACT (IMPLÉMENTATION)` — j'implémente l'étape N du plan.
- `⏸️ POINT D'ARRÊT` — en attente de validation.

## ⛔ Garde d'entrée — checkpoint universel (OBLIGATOIRE)

Ce checkpoint s'exécute **à chaque invocation du skill**, quel que soit le
contexte (nouveau plan, reprise, prompt d'action directe). Il est **non
sautable** et constitue la **toute première action** du skill.

### Interdit avant ce checkpoint

Tant que la checklist ci-dessous n'est pas satisfaite, il est **interdit** de :
- Lire du code source applicatif (hors fichiers plan/roadmap).
- Écrire ou modifier un fichier.
- Lancer une commande shell liée au développement (build, test, install, etc.).
- Produire du code ou du pseudo-code.

### Checklist pré-action

Vérifier **dans l'ordre** :

1. **Signal de mode affiché ?**
   → Le premier message après invocation du skill doit afficher `🧠 MODE PLAN`
   ou `🔍 MODE CADRAGE`. Jamais `🔨 MODE ACT` en premier message.

2. **Plan identifié ?**
   → Si le prompt référence un plan existant (`#NNN`, nom de fichier, nom
   reconnaissable du plan) : dérouler le workflow **« Reprise d'un plan
   existant »** (résumé, point d'arrêt, choix utilisateur).
   → Sinon : dérouler la **« Règle de démarrage »** (listing des plans,
   question, attente de réponse).

3. **Point d'arrêt respecté ?**
   → La reprise ET la création imposent un point d'arrêt `⏸️` avant toute
   implémentation. Vérifier qu'il a été posé ET que l'utilisateur y a répondu
   explicitement.

4. **Phase 7 étape 0 exécutée ?**
   → Si on entre en implémentation : la question `AskUserQuestion` sur les
   tests intermédiaires a-t-elle été posée ?
   → Si non : la poser **MAINTENANT**, avant la première ligne de code.

### Règle anti-court-circuit

Les formulations d'action directe de l'utilisateur — « Démarre », « Implémente »,
« Lance toutes les étapes », « Go », « Fais le », « Enchaîne tout » — expriment
une **intention**, pas une **autorisation de sauter les checkpoints**.

**Traduction obligatoire :**

| L'utilisateur dit | Ce que ça signifie pour le skill |
|---|---|
| « Démarre toutes les étapes de #109 » | Reprendre #109 → résumé → `⏸️` → Phase 7 étape 0 → implémenter |
| « Implémente l'étape 3 » | Reprendre le plan → `⏸️` → Phase 7 étape 0 (même pour 1 seule étape) → implémenter |
| « Go » / « Fais tout » | ≠ autorisation de bypass. Dérouler le workflow normalement |
| « Continue » / « Reprends » | Reprendre le plan → résumé → `⏸️` → choix utilisateur |

> **Principe : aucune formulation utilisateur, aussi impérative soit-elle,
> n'autorise à sauter un point d'arrêt `⏸️` ou l'étape 0 de la Phase 7.**

---

# Workflow : création d'un nouveau plan

7 phases **strictement séquentielles**. Chaque point d'arrêt est bloquant.

## Phase 1 — Analyse initiale (silencieuse)

> 🧠 MODE PLAN — aucune écriture, aucune commande.

Analyse silencieusement le prompt pour identifier : objectif principal,
périmètre probable, zones d'ombre, complexité pressentie, dépendances avec
d'autres plans, nécessité d'un découpage en lots.

**Ne rien proposer.** Passer à la phase 2.

## Phase 2 — Cadrage interactif

> 🔍 MODE CADRAGE — aucune écriture, aucune commande.

Lève les ambiguïtés via un **formulaire interactif** en utilisant l'outil
`AskUserQuestion` (choix cliquables, pas de saisie « 1a, 2c »). Voir
`references/forms.md` pour la matière des questions, les catégories et les
règles de batching (max 4 questions et 4 options par appel, `multiSelect` pour
les réponses multiples, option « Autre » native).

Termine ta compréhension par un court résumé (2-3 phrases) **avant** le premier
appel `AskUserQuestion`.

**STOP.** Attendre les réponses.

## Phase 3 — Proposition du plan

> 🧠 MODE PLAN — aucune écriture, aucune commande.

En intégrant les réponses de cadrage, propose la structure complète (sans
l'écrire) :

```
### 📝 Plan proposé (🧠 MODE PLAN — rien n'est encore écrit)

**Issue** : Créer `#XX — Titre` ou rattacher à `#YY` (son numéro = ID du plan)
**Fichier** : `{ISSUE}-nom-du-plan.md`
**Priorité** : high | **Complexité** : M

**Objectif** : ...
**Périmètre** : Inclus / Hors scope
**Étapes** :
1. … (implémentation)
2. … (implémentation)
3. 🧪 Tests — Rédiger et exécuter la procédure de test
4. ✅ Validation — Vérifier les résultats et clôturer
**Lots** (si applicable) : Lot 1 (étapes 1-3) … Lot 2 (étapes 4-6) …

---
⏸️ POINT D'ARRÊT 1 — Valides-tu cette proposition ? (oui / modifier / questions / annuler)
```

> Les deux dernières étapes `🧪 Tests` et `✅ Validation` sont **obligatoires** et
> doivent **toujours** figurer dans la proposition, quel que soit le nombre
> d'étapes d'implémentation. Elles sont non supprimables et non fusionnables.

**STOP.** Attendre validation.

## Phase 4 — Validation de la proposition

| Réponse | Action |
|---|---|
| « oui » / « go » / « valide » | Phase 5 — **création du plan/issue/roadmap UNIQUEMENT** |
| « modifier » + corrections | Rester en phase 3, réajuster |
| « questions » | Revenir en phase 2 si nouvelles zones d'ombre |
| « annuler » | Abandonner |

> ⚠️ « oui » = autorisation de CRÉER LE PLAN, pas d'implémenter.

## Compatibilité avec le mode plan de Claude Code

Les phases 1→4 sont en lecture seule et se déroulent normalement en mode plan.
La phase 5 est la première à mutier le dépôt (plan file, issue, roadmap).

- Si le mode plan est actif à la fin de la phase 4 : appeler `ExitPlanMode`
  avec le plan validé comme contenu d'approbation. Le point d'arrêt `⏸️` de la
  phase 4 et l'approbation `ExitPlanMode` ne font alors qu'un seul gate.
- Ne jamais tenter de `Write`/`gh`/`git` tant que le mode plan est actif.

## Phase 5 — Act limité (création du plan)

> 🔨 MODE ACT (PLAN) — écriture LIMITÉE au plan, à l'issue et au roadmap.

**UNIQUEMENT et dans cet ordre** (l'issue d'abord : son numéro est l'ID du plan) :
0. **Prérequis** : s'assurer que `./doc/roadmap/` existe (`mkdir -p ./doc/roadmap`) ; si `./doc/roadmap/roadmap.md` est absent, l'initialiser depuis la structure de `references/roadmap-file.md`.
1. Créer ou rattacher l'issue GitHub, récupérer son **numéro** (voir `references/github-issues.md`).
2. Créer `./doc/roadmap/{ISSUE}-nom-du-plan.md` avec ce numéro comme ID (voir `references/templates.md`).
3. **Mettre à jour l'issue** : maintenant que le nom du fichier est décidé, ajouter dans le corps de l'issue la référence vers le plan sous la forme `Plan: doc/roadmap/{ISSUE}-nom-du-plan.md` (voir `references/github-issues.md`).
4. Mettre à jour `./doc/roadmap/roadmap.md` (voir `references/roadmap-file.md`).

> Si aucune issue ne peut être créée maintenant, utiliser le fallback
> `draft-nom.md` décrit dans `references/templates.md`, à renommer plus tard.

**Interdit ici :** lire/modifier/créer du code source, lancer build/test/install,
réfléchir à l'implémentation, proposer du code.

Puis confirme et pose le point d'arrêt :

```
### ✅ Plan créé (🔨 MODE ACT — exécuté)

- 📄 Fichier créé : `./doc/roadmap/{ISSUE}-nom-du-plan.md`
- 🔗 Issue GitHub : #XX (créée / mise à jour / manuel)
- 📋 roadmap.md : mis à jour

---
⏸️ POINT D'ARRÊT 2 — Le plan est créé. Que souhaites-tu faire ?
1. 🚀 Commencer l'implémentation — je démarre l'étape 1
2. 📝 Modifier le plan
3. 🛑 Arrêter ici
```

**STOP.** Attendre la réponse.

## Phase 6 — Validation avant implémentation

| Réponse | Action |
|---|---|
| « 1 » / « implémenter » / « go » | Phase 7 |
| « 2 » / « modifier » | Revenir au plan |
| « 3 » / « stop » | Fin de session |

> ⚠️ Seule une réponse explicite à ce point d'arrêt autorise l'implémentation.

## Phase 7 — Implémentation

> 🔨 MODE ACT (IMPLÉMENTATION).

### Auto-vérification (avant toute action)

Avant de commencer, vérifier silencieusement que les conditions suivantes sont
réunies. Si **une seule** n'est pas remplie, **STOP** — revenir au workflow
approprié (reprise ou création) avant de continuer.

- [ ] Le skill a été invoqué (pas de code écrit avant invocation).
- [ ] Le résumé du plan a été affiché à l'utilisateur (reprise) ou le plan a
  été créé et confirmé (création).
- [ ] Un point d'arrêt `⏸️` a été posé ET l'utilisateur y a répondu
  explicitement en autorisant l'implémentation.
- [ ] L'étape 0 ci-dessous va être exécutée MAINTENANT (ou a déjà été exécutée
  dans cette session pour ce même ensemble d'étapes).

---

0. **Sélection des tests intermédiaires (avant de commencer la 1ʳᵉ étape).**
   Quand l'opérateur demande l'implémentation d'une ou plusieurs étapes (« Démarre
   l'étape 3 », « Exécute les étapes 1 et 4 », « Enchaîne les étapes 3 à 7 »,
   voire une seule étape) :
   - Lister les **étapes d'implémentation** concernées (exclure `🧪 Tests` et
     `✅ Validation`).
   - Poser via `AskUserQuestion` (`multiSelect: true`, **toutes désélectionnées
     par défaut**) : « Pour quelles étapes souhaites-tu recevoir des tests
     unitaires intermédiaires à exécuter avant de passer à la suite ? » — une
     option par étape, format `Étape X — Nom de l'étape`, plus une **option
     explicite de refus** en dernière position :
     `Aucun test intermédiaire (seuls les tests E2E obligatoires en fin d'implémentation)`.
   - **Comportement de l'option de refus** :
     - Si sélectionnée **seule** → aucun test intermédiaire, enchaînement
       direct des étapes. Les étapes `🧪 Tests` et `✅ Validation` finales
       restent obligatoires.
     - Si sélectionnée **avec d'autres étapes** → incohérence : ignorer
       l'option de refus, traiter les étapes cochées comme sélectionnées,
       et signaler l'incohérence à l'opérateur.
   - **Mémoriser la sélection** pour toute la séquence d'implémentation en cours.
   - Poser la question **même pour une étape unique** : ne rien présumer.
   - **Ne pas commencer l'implémentation tant que l'utilisateur n'a pas répondu
     à cette question.**

1. Afficher l'étape en cours avant de commencer :

```
### 🚀 Implémentation — Étape 1/N
**Étape** : … | **Fichiers concernés** : …
Je commence. Tu peux m'interrompre à tout moment.
```

2. Travailler **étape par étape**, jamais tout d'un coup.
3. À la fin de chaque étape d'implémentation, selon la sélection de l'étape 0 :
   - **Non sélectionnée** → `✅ Étape X terminée.` et enchaîner directement
     l'étape suivante, sans attendre de retour.
   - **Sélectionnée** → dérouler la **procédure de tests unitaires
     intermédiaires** (voir ci-dessous) incluant le **bloc `📦 Commit proposé`**
     obligatoire, **STOP** en attente des résultats, puis
     `✅ Étape X terminée et validée.` une fois les tests passés.
4. Une fois les étapes d'implémentation (1 à N-2) terminées, dérouler
   **obligatoirement** l'étape `🧪 Tests` puis l'étape `✅ Validation` (voir
   ci-dessous). Ces deux étapes ne sont **jamais** optionnelles, que des tests
   intermédiaires aient eu lieu ou non.
5. En fin de session, mettre à jour : journal de session du plan, issue GitHub,
   `roadmap.md` si nécessaire.

> **Clôture d'un plan validé — checklist COMPLÈTE (ne rien omettre).** Dès que
> toutes les étapes sont livrées **et** validées, la clôture consiste à mettre à
> jour **les trois supports** de suivi, dans cet ordre :
>
> 1. **Fichier de plan** : passer le front matter à `status: done`, cocher la
>    dernière étape et consigner la validation dans le journal de session.
> 2. **`roadmap.md`** : déplacer l'entrée de la section « À faire » vers
>    **« Fait »** (statut `done` 🔵).
> 3. **Issue GitHub rattachée** : la **fermer** (`gh issue close <issue.id>`),
>    idéalement précédée d'un commentaire de clôture récapitulant ce qui a été
>    livré et validé (`gh issue comment <issue.id> --body "…"`). Voir
>    `references/github-issues.md`. Si le plan n'a pas d'issue rattachée
>    (`issue.id` absent / fallback `draft-`), sauter cette étape et le signaler.
>
> Ces trois actions vont **ensemble** : `status: done` dans le plan implique une
> entrée en « Fait » **et** une issue fermée. Ne jamais laisser une issue ouverte
> alors que son plan est `done`.
>
> **Ne jamais** déplacer un plan validé vers `_archives/roadmap_done.md` : ce
> fichier est un historique figé qui n'est plus utilisé. L'archivage physique
> dans `_archives/` (statut `archived` ⚪) est une opération distincte et rare
> (voir `references/roadmap-file.md`), pas la clôture normale d'un plan.

## Tests unitaires intermédiaires (optionnels, par étape)

Ne s'appliquent qu'aux étapes **sélectionnées** à l'étape 0 de la Phase 7. À la
fin de l'implémentation d'une étape sélectionnée :

1. **Déterminer les tests unitaires pertinents** ciblés sur le périmètre de
   **cette étape uniquement**.

2. **Rédiger une procédure de tests unitaires détaillée pas à pas** dans le plan,
   dans une section dédiée entre balises de code. Cette procédure :
   - Respecte **intégralement** la règle `operator-commands-formatting.md`
     (voir `## Prerequisites`).
   - Inclut les commandes de vérification des résultats attendus.
   - Précise les **résultats attendus** pour chaque vérification.

3. **Afficher la procédure complète ET le commit proposé dans une même
   réponse**, selon ce template obligatoire — les deux blocs sont
   **indissociables** :

   ```
   ### 🧪 Tests intermédiaires — Étape X/N

   **Procédure :**

   ```bash
   <commandes de test>
   ```

   **Résultats attendus :** <ce que l'opérateur doit observer>

   ---

   ### 📦 Commit proposé — Étape X/N

   **Fichiers modifiés :**
   - `<fichier>` — <résumé d'une ligne>
   - …

   **Message de commit :**
   ```
   <type>(<scope>): <description> (#<issue>, step X)
   ```

   ---

   ⏸️ Commit, push si nécessaire, puis exécute la procédure de tests
   dans l'environnement cible et transmets-moi les résultats complets.
   J'attends tes retours avant de passer à l'étape suivante.
   ```

4. **STOP.** Ne pas passer à l'étape suivante tant que les résultats ne sont pas
   reçus.

5. **Si les tests échouent** : analyser, corriger l'implémentation, régénérer la
   procédure **et** un nouveau bloc `📦 Commit proposé`, re-soumettre. Boucler
   jusqu'à validation.

6. **Si les tests passent** : `✅ Étape X terminée et validée.` puis enchaîner
   l'étape suivante.

> Ces tests intermédiaires **complètent** et ne remplacent **jamais** la phase
> finale `🧪 Tests` + `✅ Validation`, qui reste obligatoire et bloquante.

## Étape 🧪 Tests (avant-dernière étape — obligatoire)

Démarre lorsque les étapes d'implémentation (1 à N-2) sont terminées. Tu dois :

1. **Déterminer le type de tests requis** selon cette heuristique :
   - **Tests unitaires** → modification d'une fonction, d'un service ou d'un
     composant isolé.
   - **Tests end-to-end** → modification touchant un flux complet (API → front,
     inter-services, pipeline, etc.).
   - **Les deux** → modification structurelle majeure ou transverse.

2. **Rédiger une procédure de test détaillée pas à pas** directement dans le
   plan, dans une section dédiée entre balises de code. Cette procédure :
   - Respecte **intégralement** la règle `operator-commands-formatting.md`
     (voir `## Prerequisites`).
   - Inclut les commandes de vérification des résultats attendus (ex : `curl`,
     `grep`, `docker ps`, assertions visuelles, etc.).
   - Précise les **résultats attendus** pour chaque vérification (ce que
     l'opérateur doit observer si tout fonctionne).

3. **Afficher la procédure complète ET le commit proposé dans une même
   réponse**, selon ce template obligatoire — les deux blocs sont
   **indissociables** :

   ```
   ### 🧪 Tests finaux

   **Procédure :**

   ```bash
   <commandes de test>
   ```

   **Résultats attendus :** <ce que l'opérateur doit observer>

   ---

   ### 📦 Commit proposé — Pré-tests finaux

   **Fichiers modifiés :**
   - `<fichier>` — <résumé d'une ligne>
   - …

   **Message de commit :**
   ```
   <type>(<scope>): <description> (#<issue>)
   ```

   ---

⏸️ Commit, push si nécessaire, puis exécute la procédure de tests
   dans l'environnement cible et transmets-moi les résultats complets.
   J'attends tes retours avant de passer à l'étape de validation.
   ```

   > Si **aucun fichier n'a été modifié** depuis le dernier commit (ex. : tests
   > finaux après un commit intermédiaire qui couvrait déjà tout), remplacer le
   > bloc `📦 Commit proposé` par :
   > `📦 Aucun commit nécessaire — aucun fichier modifié depuis le dernier commit.`

4. **STOP.** Ne pas passer à l'étape `✅ Validation` tant que les résultats ne
   sont pas reçus.

## Étape ✅ Validation (dernière étape — obligatoire)

Démarre **uniquement** lorsque l'opérateur a transmis les résultats de l'étape
`🧪 Tests`.

- **Si tous les tests passent** → cocher l'étape, puis enchaîner la checklist de
  clôture (plan `status: done`, `roadmap.md`, issue GitHub — voir ci-dessus).
- **Si un ou plusieurs tests échouent** :
  1. Analyser les résultats transmis.
  2. Corriger l'implémentation.
  3. **Revenir à l'étape `🧪 Tests`** : régénérer une procédure de test mise à
     jour (incluant les vérifications de non-régression si pertinent) **et** un
     nouveau bloc `📦 Commit proposé` pour les corrections.
  4. Boucler jusqu'à validation complète.

## Commit d'implémentation pré-tests (référence de format)

Cette section définit les règles du bloc `📦 Commit proposé` utilisé dans les
templates de tests ci-dessus.

1. **Lister les fichiers modifiés** durant l'étape (code, config, plan, etc.)
   avec un résumé d'une ligne par fichier.

2. **Proposer un message de commit** respectant la convention
   **Conventional Commits** et incluant :
   - Le **type** (`feat`, `fix`, `refactor`, `chore`, `docs`…).
   - Le **scope** (composant ou module touché).
   - Une **description concise** de ce qui a été fait.
   - La **référence de l'issue** (`#NNN`).
   - Le **numéro d'étape** pour traçabilité (sauf tests finaux).

3. **Ne PAS exécuter le commit.** L'opérateur décide s'il commit/push
   maintenant (avant les tests) ou après. Le message est une **proposition
   prête à l'emploi**, pas une action automatique.

4. **Si aucun fichier n'a été modifié** depuis le dernier commit (ex. : tests
   finaux après un commit intermédiaire qui couvrait déjà tout), afficher :
   `📦 Aucun commit nécessaire — aucun fichier modifié depuis le dernier commit.`

> **Un commit = un changement logique.** Si une étape touche des périmètres
> clairement distincts (ex. code applicatif + mise à jour doc), proposer
> **deux commits séparés** plutôt qu'un seul.

---

# Workflow : reprise d'un plan existant

> ⚠️ **Même si le prompt de l'utilisateur demande explicitement de « démarrer »,
> « implémenter » ou « tout lancer », ce workflow s'applique intégralement.**
> Un prompt d'action directe (« Démarre les étapes de #109 ») n'est PAS un
> raccourci : il signifie « je veux travailler sur ce plan », pas « saute tous
> les checkpoints ». Voir la **règle anti-court-circuit** dans la garde d'entrée.

1. 🧠 MODE PLAN — lis le fichier plan, affiche l'état :

```
### 📋 Résumé du plan #{ISSUE}
**Statut** : 🟢 active | **Dernière session** : YYYY-MM-DD | **Progression** : 3/7
**Étapes restantes** : 4. [ ] … 5. [ ] …

---
⏸️ Que souhaites-tu faire ?
1. 🚀 Continuer l'implémentation — reprendre à l'étape 4
2. 🔍 Clarifier / recadrer
3. 📝 Modifier le plan
4. 📋 Voir le journal
```

2. **STOP.** Attendre la validation. Ne rien implémenter, ne lire aucun code
   source applicatif, ne lancer aucune commande tant que l'utilisateur n'a pas
   choisi une option.

3. Si option 2 → phase de clarification (format `references/forms.md`) ciblée sur
   les étapes restantes.

4. **Transition vers Phase 7** — Si l'utilisateur choisit d'implémenter
   (option 1) : basculer en Phase 7 **en commençant impérativement par
   l'étape 0** (sélection des tests intermédiaires via `AskUserQuestion`).
   Ne JAMAIS sauter l'étape 0, même si l'utilisateur a dit « démarre tout »
   dans son prompt initial ou dans sa réponse au point d'arrêt.

5. 🔨 MODE ACT — exécuter étape par étape, puis dérouler **obligatoirement** les
   étapes `🧪 Tests` et `✅ Validation` (voir Phase 7) avant de clôturer, et
   mettre à jour journal, issue et `roadmap.md`.

> Si un plan repris ne contient pas encore les étapes `🧪 Tests` / `✅ Validation`
> (plan antérieur à cette convention), **les ajouter** comme deux dernières
> étapes avant de poursuivre.
