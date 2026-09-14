# Module : Initialisation & scan

> **Chargé au tour 1** de toute session (démarrage, aide, reprise, prompt
> d'action directe). Contient la garde d'entrée non sautable, la règle de
> démarrage, la détection/migration d'ID, la Phase 1 (analyse + auto-calibrage)
> et la Phase 1.5 (gate modèle).

---

## Système d'aide (Axe E)

### Aide à la demande

L'aide est **générée à la volée** depuis le contenu du SKILL.md et des references.
Elle est toujours synchrone avec le skill, sans maintenance séparée.

Déclencheur : phrases reconnues **sans déclencher le workflow** (exception à la
règle de démarrage, comme les questions de culture générale) :

| L'utilisateur dit | Contenu affiché |
|---|---|
| `aide` | Aide complète : toutes les catégories ci-dessous |
| `aide workflow` | Phases 1→7, reprise, urgences, signaux de mode, anti-court-circuit |
| `aide config` | `.skill-config.yml` complet, tous les champs, modes, modèles |
| `aide planification` | Grille de sizing, gate modèle, grilling, désengagement A, surcout D |
| `aide plans` | Front matter, template, listing, incohérences, clôture, mode dégradé |
| `aide tests` | Tests intermédiaires, étape 🧪, étape ✅, mode autonomous, règle ⛔ |
| `aide git` | Commits 📦, migration, issues, `.migration-declined` |
| `aide intégrations` | Skill `impeccable`, mapping IDE, actions génériques |
| `aide roadmap` | Alias de `aide` — aide complète |
| `help` | Alias de `aide` — aide complète |

Chaque aide par catégorie se termine par :

```
💡 Pour l'aide complète : « aide »
   Pour une autre catégorie : « aide [workflow|config|planification|plans|tests|git|intégrations] »
```

### Note de bienvenue (première exécution uniquement)

Déclencheur : `.skill-config.yml` absent **ou** `roadmap-tracking.help.welcomed` absent/`false`.

Après la question de calibrage collaboratif (bloc A.0 ci-dessous), afficher :

```
💡 /roadmap-tracking — Aide disponible à tout moment

Pour obtenir de l'aide sur le skill, dis :
  « aide »               → Aide complète (toutes les features)
  « aide workflow »      → Phases, reprise, urgences, checkpoints
  « aide config »        → .skill-config.yml, modes, modèles
  « aide planification » → Sizing, grilling, désengagement, surcout
  « aide plans »         → Front matter, format, incohérences, clôture
  « aide tests »         → Tests intermédiaires, finaux, mode autonomous
  « aide git »           → Commits, migration de plans, issues GitHub
  « aide intégrations »  → Skill impeccable (UX/UI), IDE

Cette note n'apparaîtra qu'une seule fois.
```

Puis écrire `roadmap-tracking.help.welcomed: true` dans `.skill-config.yml`.

---

## Règle de démarrage

### Cas préalable : `doc/roadmap/` absent

Si le répertoire `./doc/roadmap/` n'existe **pas** dans le projet courant :

> « Ce projet n'a pas encore de répertoire `doc/roadmap/`. Souhaites-tu le créer
> pour activer le suivi de plans roadmap-tracking ? (oui / non) »

- **Oui** → `mkdir -p ./doc/roadmap` + initialiser `roadmap.md` → dérouler la
  règle de démarrage standard ci-dessous.
- **Non** → Traiter le prompt normalement sans le workflow. Si, plus tard
  dans la **même session**, une demande implique une modification de fichier
  du projet, le skill re-propose la création de `doc/roadmap/` **une seule
  fois**. Si l'utilisateur refuse à nouveau, consigner l'avertissement suivant
  et continuer sans le workflow :
  > ⚠️ `doc/roadmap/` absent et création refusée — ce travail ne sera pas
  > suivi par roadmap-tracking.

---

### Démarrage standard (quand `doc/roadmap/` est présent)

#### Bloc A.0 — Initialisation de la configuration (Axe A)

**Avant de lister les plans**, lire `./doc/roadmap/.skill-config.yml` :

- Si le fichier est **absent** ou si la clé `roadmap-tracking.collaborative` est **absente** :
  Poser via `AskUserQuestion` :
  > « Ce projet est-il travaillé par plusieurs collaborateurs (branches simultanées,
  > PR en parallèle, équipe) ? »
  > - **Non, projet solo** → écrire `collaborative: false` dans `.skill-config.yml`
  > - **Oui, multi-collaborateurs** → écrire `collaborative: true`
  >
  > Puis écrire `mode: auto` et `last-calibration: <date ISO du jour>`.

- Si le fichier et la clé sont **présents** : lire la valeur sans redemander.

Après le bloc A.0, si `roadmap-tracking.help.welcomed` est absent/`false` :
**afficher la note de bienvenue** (voir « Système d'aide — Note de bienvenue » ci-dessus)
puis écrire `help.welcomed: true` dans `.skill-config.yml`.

Si l'utilisateur ne référence pas un plan existant dans son premier prompt :

1. **Lister les plans existants** (mémoires, contexte projet, et inspection de
   `./doc/roadmap/`) **impérativement sous forme de tableau markdown** — voir
   « ⛔ Règle absolue — format des rapports ». Ne JAMAIS rendre ce listing en
   format `clé: valeur` (`#: 1` / `Fichier: …` / `Statut: …`), en lignes
   séparées par des filets (`───`), ni en puces : le gabarit ci-dessous est
   contraignant.

✅ **SEUL format autorisé** :

```
### 📋 Plans existants

| # | Fichier | Statut | Résumé | Issue GitHub |
|---|---------|--------|--------|--------------|
| 1 | `27-nom.md` | 🟢 Active | Description (front matter ou ligne "Description") | `#27` ou ❌ Non rattachée |
```

❌ **Formats INTERDITS** — ne jamais produire ceci :

```
#: 1
Fichier: 27-nom.md
Statut: 🟢 Active
Résumé: Description
────────────────────────────────────────
#: 2
Fichier: 28-autre.md
```

> **Mode `local`** : la colonne « Issue GitHub » affiche `❌ Local` pour tous les
> plans sans issue rattachée. Les contrôles d'ID et la migration (ci-dessous) ne
> s'appliquent qu'en mode `github`.

> **Plans non conformes (listing tolérant).** Un fichier `./doc/roadmap/*.md`
> peut ne pas respecter `references/templates.md` (front matter absent, partiel,
> ou bloc `issue` manquant). Le listing est **tolérant et ne crashe jamais** :
> - **Toujours lister le fichier**, même sans front matter exploitable.
> - Pour toute colonne non dérivable (`Statut`, `Résumé`, `Issue GitHub`),
>   afficher `⚠️` (donnée manquante) plutôt qu'une valeur inventée. Le `Résumé`
>   retombe sur la 1ʳᵉ ligne de titre `#` ou la 1ʳᵉ ligne non vide du fichier.
> - Ajouter une note sous le tableau récapitulant les fichiers non conformes
>   détectés (ex. « ⚠️ 2 plan(s) non conforme(s) : `x.md` (pas de front matter),
>   `y.md` (front matter partiel : `status`, `complexity` manquants) »).
> - La reprise d'un plan non conforme suit la branche dédiée (voir
>   « Workflow : reprise d'un plan existant § Plan non conforme »).

2. **Demander** : « Souhaites-tu repartir d'un de ces plans existants (indique
   le numéro) ou créer un nouveau plan pour cette session ? »
3. **Attendre la réponse** avant de traiter le prompt.

## Détection d'ID de plan incohérents

> **Mode `github` uniquement.** En mode `local`, le contrôle `plan.id ==
> issue.id` et la migration n'ont pas de sens — ils sont désactivés. Si le mode
> est `local`, passer directement à la question « Nouveau plan ou reprise ? ».

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


---

## ⛔ Garde d'entrée — checkpoint universel (OBLIGATOIRE)

Ce checkpoint s'exécute **à chaque invocation du skill**, quel que soit le
contexte (nouveau plan, reprise, prompt d'action directe). Il est **non
sautable** et constitue la **toute première action** du skill.

> **Renfort mécanique (Claude Code).** Ce checkpoint n'est plus seulement
> textuel. Deux hooks le soutiennent (voir `hooks/hooks.json`) :
> - `UserPromptSubmit` réinjecte, à chaque tour, la préséance de cette garde sur
>   les directives de style/rythme concurrentes (« shortest path », « don't
>   stop », « résous la tâche ») — celles-ci régissent le *comment* après
>   engagement du skill, jamais le *si* de son invocation.
> - `PreToolUse` (`Write|Edit|MultiEdit|NotebookEdit`) refuse **une seule fois
>   par session** le premier appel d'outil mutant sur un projet ayant adopté le
>   skill (`doc/roadmap/` présent), injectant la directive **au moment exact où
>   l'implémentation démarre**, puis s'auto-désarme. Ce n'est pas un mur : si le
>   skill a déjà été consulté (y compris pour se désengager), il suffit de
>   réémettre l'appel. Les écritures dans `doc/roadmap/` ne sont jamais
>   interceptées. Kill-switch : `ROADMAP_TRACKING_AUTOSTART=off`.

### Interdit avant ce checkpoint

Tant que la checklist ci-dessous n'est pas satisfaite, il est **interdit** de :
- Lire du code source applicatif (hors fichiers plan/roadmap).
- Écrire ou modifier un fichier.
- Lancer une commande shell liée au développement (build, test, install, etc.).
- Produire du code ou du pseudo-code.
- Accéder en lecture ou en écriture aux fichiers du skill (`SKILL.md`, `references/`, `scripts/`) **sans avoir chargé le skill via `Skill({skill: "roadmap-tracking:roadmap-tracking"})`**. La lecture directe de ces fichiers est elle-même le vecteur du bypass : elle court-circuite le workflow avant même que celui-ci puisse s'imposer.

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

4. **`tests.mode` résolu ?**
   → Si on entre en implémentation : lire `tests.mode` dans
   `./doc/roadmap/.skill-config.yml`.
   → **Fixé** (`manual` ou `autonomous`) → continuer.
   → **Non fixé** (clé absente, fichier absent, ou `null`) → poser
   **MAINTENANT** la question `AskUserQuestion` « L'environnement de test de ce
   projet est-il directement accessible depuis cet IDE ? » et persister le choix
   dans `.skill-config.yml` avant de continuer. Ne pas passer à l'item 5 tant
   que ce choix n'est pas persisté.

5. **Phase 7 étape 0 exécutée ?**
   → **Mode `autonomous`** : cette étape est supprimée — passer directement à
   l'implémentation.
   → **Mode `manual`** : la question `AskUserQuestion` sur les tests
   intermédiaires a-t-elle été posée ?
   → Si non : la poser **MAINTENANT**, avant la première ligne de code.

### Règle anti-court-circuit

Les formulations d'action directe de l'utilisateur — « Démarre », « Implémente »,
« Lance toutes les étapes », « Go », « Fais le », « Enchaîne tout » — expriment
une **intention**, pas une **autorisation de sauter les checkpoints**.

**Traduction obligatoire :**

| L'utilisateur dit | Ce que ça signifie pour le skill |
|---|---|
| « Démarre toutes les étapes de #109 » | Reprendre #109 → résumé → `⏸️` → résoudre `tests.mode` → Phase 7 étape 0 (mode `manual`) → implémenter |
| « Implémente l'étape 3 » | Reprendre le plan → `⏸️` → résoudre `tests.mode` → Phase 7 étape 0 (mode `manual`) → implémenter |
| « Go » / « Fais tout » | ≠ autorisation de bypass. Dérouler le workflow normalement |
| « Continue » / « Reprends » | Reprendre le plan → résumé → `⏸️` → choix utilisateur |

> **Principe : aucune formulation utilisateur, aussi impérative soit-elle,
> n'autorise à sauter un point d'arrêt `⏸️`, la résolution de `tests.mode`
> ou l'étape 0 de la Phase 7.**

> **Bypass tacite — cas à risque élevé.** Certaines formes de prompt invitent
> à implémenter directement sans déclencher de signal d'alerte apparent :
>
> | Forme de prompt | Risque | Traduction obligatoire |
> |---|---|---|
> | Analyse détaillée + fixes proposés fournis dans le prompt | Paraît « déjà planifié » → saut vers l'implémentation | L'analyse est une **entrée de cadrage**, pas un plan validé. Dérouler le workflow normalement (Phase 1 → Phase 5 → `⏸️` → Phase 7). |
> | Prompt visiblement structuré comme une spec (structure soignée, sections titrées, tableaux, comportement attendu explicite) — qu'il provienne de l'agent lui-même, d'un agent tiers ou de l'utilisateur | Ressemble à une spec finalisée prête à implémenter — risque de bypass supérieur à une analyse utilisateur, car la qualité de cadrage est professionnelle par nature | La qualité de rédaction d'un prompt n'a aucune incidence sur le workflow. Un prompt bien cadré est une meilleure **entrée de cadrage**, pas une autorisation de sauter des phases. Dérouler le workflow normalement. |
> | Changement « petit » ou « évident » | Justifie mentalement le bypass | La taille du changement n'exempte d'aucune phase. |
> | Demande portant sur le skill lui-même ou ses fichiers de référence | Hors scope apparent | Le skill s'applique à son propre code autant qu'à tout autre projet. |
> | Demande impliquant `SKILL.md`, `references/` ou `scripts/` + lecture directe sans invocation préalable | L'agent lit les fichiers du skill comme une tâche de maintenance ordinaire — le skill n'a jamais été chargé via `Skill({skill: "roadmap-tracking:roadmap-tracking"})` | Invoquer le skill en premier. Tout accès en lecture ou en écriture aux fichiers du skill est interdit avant cette invocation. La lecture directe **est** le bypass. |
> | `bypass` donné explicitement par l'utilisateur (gate modèle) | Valide uniquement pour la **gate modèle** | ≠ autorisation de sauter les checkpoints du workflow. |
>
> Dans tous ces cas : **créer le plan d'abord, implémenter ensuite, jamais les deux ensemble.**
>
> **Principe général — aucun facteur d'exemption.** Ni la source du prompt
> (utilisateur, agent lui-même, agent tiers, copier-coller d'une spec externe), ni sa qualité
> de structuration (sections titrées, tableaux, exemples, comportement attendu
> déjà formulé) ne constituent un facteur d'exemption. Plus un prompt est
> structuré, plus le risque de bypass tacite est élevé — pas l'inverse.


---

## Phase 1 — Analyse initiale (silencieuse)

> 🧠 MODE PLAN — aucune écriture, aucune commande.

Analyse silencieusement le prompt pour identifier : objectif principal,
périmètre probable, zones d'ombre, dépendances avec d'autres plans, nécessité
d'un découpage en lots, et **complexité pressentie — globale et par étape** —
selon la grille de sizing (voir « Évaluation de complexité et recommandation de
modèle » dans `modules/plan.md` — en Phase 1, charger init-scan + plan
ensemble). Cette évaluation alimente la gate modèle (Phase 1.5 ci-dessous),
les tags d'étape (Phase 3) et le champ `complexity` du front matter (Phase 5).

#### Matrice de décision auto-calibrage (Axe A)

Après l'analyse de complexité, lire `roadmap-tracking.mode` dans `.skill-config.yml` :

- **`mode: full` | `mode: lightweight` | `mode: off`** (valeur explicite) : ignorer la matrice, appliquer directement.
- **`mode: auto`** (ou absent) : appliquer la matrice selon `collaborative` :

| Complexité | `collaborative` | Action |
|---|---|---|
| `XS` | *any* | **Désengagement automatique** → écrire plan, afficher template de désengagement, **TERMINER LA RÉPONSE** (voir garde ci-dessous) |
| `S` | `false` | **Désengagement automatique** → écrire plan, afficher template de désengagement, **TERMINER LA RÉPONSE** (voir garde ci-dessous) |
| `S` | `true` | **Mode `lightweight`** (plan + commits, sans ⏸️ intermédiaires) + afficher estimation surcout |
| `M` | *any* | **Mode `lightweight`** (plan + commits, sans ⏸️ intermédiaires) |
| `L`, `XL` | *any* | **Mode `full`** (workflow complet 7 phases) |

**Template de désengagement automatique (XS / S solo)** :

```
ℹ️ Skill /roadmap-tracking — Désengagement automatique

Complexité estimée : [XS|S] [· mode solo]
Le surcout du workflow structuré (checkpoints, commits intermédiaires,
phases de validation) n'est pas justifié pour cette complexité.

✅ Plan rédigé dans : doc/roadmap/[nom-du-plan].md
📋 Implémente-le directement avec un prompt explicite.

💡 Pour forcer le workflow complet sur les prochaines tâches :
   Dis-moi « mode workflow complet »
   → Je mettrai à jour doc/roadmap/.skill-config.yml (mode: full).

⛔ GARDE DE DÉSENGAGEMENT — RÉPONSE TERMINÉE ICI
   Aucune phase du workflow (Phase 2 à Phase 7) ne sera démarrée.
   Aucun outil (Write, Edit, Bash, Read de code source) ne sera appelé.
   Attendre le prochain prompt utilisateur.
```

---

## ⛔ Règle absolue — Garde dure de désengagement automatique (Axe A)

```
⛔ GARDE DURE — DÉSENGAGEMENT AUTOMATIQUE

SI la matrice Axe A résout en « Désengagement automatique »
   (Complexité XS, OU Complexité S + collaborative: false)
ALORS :
  1. Écrire le fichier plan (UNIQUEMENT l'outil Write sur doc/roadmap/*.md).
  2. Afficher le template de désengagement ci-dessus.
  3. TERMINER LA RÉPONSE IMMÉDIATEMENT.

IL EST FORMELLEMENT INTERDIT DE :
  - Entamer ou mentionner la Phase 1.5, 2, 3, 4, 5, 6 ou 7.
  - Appeler un outil autre que Write (plan uniquement) : pas de Bash,
    pas d'Edit sur du code source, pas de Read de code applicatif.
  - Implémenter, analyser, cadrer, ou proposer quoi que ce soit
    au-delà du plan sommaire déjà écrit.
  - Interpréter la demande utilisateur initiale comme une autorisation
    implicite de continuer le workflow.

SEULE SORTIE DE GARDE : l'utilisateur dit explicitement
  « mode workflow complet » (→ écrire mode: full dans .skill-config.yml
   et redémarrer le workflow normalement) ou « continue ».
Toute autre formulation (« go », « oui », « implémente ») est traitée
comme un nouveau prompt entrant, pas comme un bypass de cette garde.
```

**Estimation du surcout (cas `S` + `collaborative: true` — mode `lightweight`) (Axe D)** :

```
📊 Estimation du surcoût skill pour ce plan (complexité [S|M], mode collaboratif) :
   - Tokens supplémentaires estimés  : ~[1 000 000 (+35 %) | 1 700 000 (+30 %)]  [mode lightweight]
   - Coût supplémentaire estimé      : ~[$1,70 | $2,80] (ref. Sonnet)
   - Durée supplémentaire estimée    : ~[2 | 4] min

   Le workflow allégé (sans checkpoints ⏸️) sera appliqué.
   Pour le workflow complet, dis « mode workflow complet ».
```

Table de calibrage des estimations par complexité et mode (calibrées sur métriques réelles Sonnet S & M, non calculées dynamiquement) :

| Complexité | Mode | Tokens Δ | Coût Δ (ref. Sonnet) | Durée Δ |
|---|---|---|---|---|
| `S` | lightweight | ~1 000 000 | ~$1,70 | ~2 min |
| `M` | lightweight | ~1 700 000 | ~$2,80 | ~4 min |
| `L` | full | ~2 800 000 | ~$4,80 | ~7 min |
| `XL` | full | ~4 500 000 | ~$7,50 | ~11 min |

**Triggers verbaux — changement de mode en cours de session** :

| L'utilisateur dit | Action |
|---|---|
| « mode workflow complet » / « force le workflow » | Écrit `mode: full` dans `.skill-config.yml` + confirme |
| « mode lightweight » / « mode allégé » | Écrit `mode: lightweight` + confirme |
| « désactive le skill » / « mode off » | Écrit `mode: off` + confirme |
| « remets le mode auto » | Écrit `mode: auto` + confirme |
| « projet collaboratif » / « multi-collaborateurs » | Écrit `collaborative: true` + confirme |
| « projet solo » | Écrit `collaborative: false` + confirme |

**Ne rien proposer.** Si la garde de désengagement s'est déclenchée, la réponse est **déjà terminée** — ne pas passer à la Phase 1.5. Sinon, passer à la Phase 1.5.

## Phase 1.5 — Gate modèle (avant le cadrage)

> 🧠 MODE PLAN — aucune écriture, aucune commande.

Sur la base de la **complexité globale pressentie** en Phase 1, évaluer la gate
selon la section canonique « Gate de recommandation de modèle » (dans
`modules/plan.md`). Rationnel : le cadrage (Phase 2) est la partie interactive
la plus exigeante en jugement ; choisir le bon modèle **avant** de la mener
aligne l'effort là où il compte.

- **Cas 1 — modèle adapté** → **continuer silencieusement** vers la Phase 2.
  *(Fast-path : aucun affichage, aucun arrêt — tour non consommé.)*
- **Cas 2 — modèle non adapté** → bloc `⚠️`, **puis point d'arrêt de bypass
  `⏸️`** : s'arrêter et attendre la réponse (`bypass` pour continuer sur le
  modèle actif, ou switch manuel via `/model` puis relance). Ne pas entamer le
  cadrage tant que l'utilisateur n'a pas répondu.

Se référer à la section canonique pour les formats exacts et le comportement
complet. Si le modèle actif n'est pas détectable, ne pas afficher de gate.
Mémoriser le modèle évalué (voir « Re-jeu de la gate sur changement de modèle »).
