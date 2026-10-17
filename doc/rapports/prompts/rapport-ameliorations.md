# 🛠️ Mission : Audit & Amélioration du Skill roadmap-tracking

## Contexte

Le skill `/roadmap-tracking:roadmap-tracking` gagne en adoption : 4 à 5 collègues vont prochainement le télécharger et l'installer. Il est impératif de le rendre **robuste**, **scalable** et de garantir une **expérience utilisateur fluide et agréable**. Le projet Auxitum, qui sert de référence d'utilisation réelle, compte **plus de 350 plans** — ce qui en fait un excellent stress-test de scalabilité.

- **Codebase du skill** : `/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking`
- **Exemple d'utilisation réelle (projet Auxitum, 350+ plans)** : `/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/auxitum/doc/roadmap/`

---

## ⚠️ Contrainte critique : Optimisation de la consommation de tokens

Le volume de 350+ plans représente un **risque majeur d'explosion du quota de tokens**. Toute l'analyse DOIT respecter une stratégie de lecture économe :

### Règles de lecture obligatoires

1. **JAMAIS de lecture exhaustive de tous les plans** — ne lis JAMAIS le contenu de chaque fichier plan individuellement
2. **Arborescence d'abord** : utilise des commandes de listing (`find`, `ls -R`, `tree`) pour cartographier la structure sans lire le contenu des fichiers
3. **Fichiers structurels uniquement** : lis en priorité les fichiers de gouvernance et de suivi :
   - `roadmap.md` (fichier de suivi principal)
   - `CONTEXT.md` (s'il existe)
   - `README.md`, fichiers de configuration du skill
   - Fichiers source du skill (prompts, instructions, scripts)
4. **Échantillonnage représentatif** : pour comprendre la structure d'un plan individuel, sélectionne un échantillon de **5 à 8 plans maximum**, choisis pour couvrir :
   - Des statuts différents (active, done, in-progress, blocked…)
   - Des niveaux de complexité variés (simple vs multi-étapes)
   - Des plans anciens vs récents
5. **Comptage et statistiques** : préfère compter les fichiers (`find ... | wc -l`, `grep -c`) plutôt que de lire leur contenu pour quantifier la volumétrie
6. **Lecture partielle** : si un fichier est volumineux (ex : `roadmap.md` avec 350+ entrées), lis les **50 premières lignes** et les **30 dernières lignes** pour identifier la structure, puis utilise `grep` ou `wc -l` pour quantifier le reste

### Budget indicatif par phase

| Phase | Stratégie | Coût estimé |
|-------|-----------|-------------|
| Codebase du skill | Lecture complète (volume faible) | Modéré |
| Arborescence Auxitum | Listing + comptage uniquement | Faible |
| roadmap.md Auxitum | Head/tail + grep statistique | Faible |
| Échantillon de plans | 5-8 fichiers max | Maîtrisé |
| Rédaction du rapport | Synthèse | Modéré |

---

## Phase 1 — Analyse approfondie

### 1.1 Analyse de la codebase du skill

Parcours **intégralement** le répertoire du skill (volume limité, lecture complète autorisée) :

```
/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking
```

Pour chaque fichier pertinent, identifie et documente :

- **Architecture globale** : structure des fichiers, points d'entrée, flux d'exécution
- **Logique métier** : comment les plans sont créés, suivis, déplacés, archivés
- **Gestion des statuts** : quels statuts existent, comment les transitions sont gérées
- **Points de fragilité** : gestion d'erreurs, cas limites, hypothèses implicites
- **Scalabilité** : comportement attendu avec 50, 200, 350, 500+ plans — identifie les **goulots d'étranglement** en termes de tokens consommés par le skill lui-même lors de son utilisation
- **UX actuelle** : interactions avec l'utilisateur, clarté des messages, friction identifiable
- **Coût token du skill** : identifie les opérations du skill qui lisent/écrivent le plus de contenu et qui génèrent la plus grande consommation de tokens lors de l'usage quotidien

### 1.2 Analyse de l'arborescence d'utilisation réelle (350+ plans)

Analyse le répertoire Auxitum **en respectant strictement les règles d'optimisation tokens** :

```
/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/auxitum/doc/roadmap/
```

**Étape 1 — Cartographie** (listing uniquement, pas de lecture de contenu) :
- Arborescence complète via `find` ou `tree`
- Comptage total de fichiers et dossiers
- Répartition par statut (comptage par dossier/pattern)

**Étape 2 — Fichiers structurels** (lecture autorisée) :
- `roadmap.md` principal : head/tail + comptage de lignes + grep pour statistiques
- `CONTEXT.md` s'il existe
- Tout fichier d'index ou de configuration

**Étape 3 — Échantillonnage** (5-8 plans max) :
- Sélectionne un échantillon représentatif et justifie le choix
- Lis uniquement ces plans pour comprendre la structure type

**Étape 4 — Synthèse quantitative** :
- Nombre total de plans par statut
- Taille estimée du `roadmap.md` (lignes, sections)
- Ratio plans actifs vs done vs autres
- Estimation du coût token d'une opération typique du skill sur ce volume

---

## Phase 2 — Challenge des propositions utilisateur

Évalue rigoureusement chacune des propositions ci-dessous **en tenant compte du volume de 350+ plans comme réalité opérationnelle**. Pour chaque proposition, fournis :

- ✅ **Forces** : ce que la proposition apporte
- ⚠️ **Risques / Limites** : effets de bord, complexité induite, régressions possibles
- 💰 **Impact sur la consommation de tokens** : la proposition réduit-elle ou aggrave-t-elle le coût token ?
- 🔄 **Contre-proposition ou amélioration** : ta recommandation argumentée
- 🏗️ **Impact sur l'existant** : plan de migration/rattrapage pour les 350+ plans déjà créés

### Proposition A — Archivage des plans « done »

> Avec 350+ plans, les références des plans "done" dans `doc/roadmap/roadmap.md` prennent énormément de place. Sont-elles vraiment utiles ? L'arborescence devient complexe et le fichier roadmap.md coûte cher en tokens à chaque lecture par le skill.

Questions de challenge :

- Faut-il purger, archiver, ou résumer les plans "done" ?
- Un mécanisme d'archivage automatique avec seuil configurable est-il pertinent ?
- Les plans "done" doivent-ils rester consultables ? Si oui, sous quelle forme ?
- Quel impact sur la traçabilité et l'historique du projet ?
- **Quel est le gain token estimé** si on retire les plans "done" du fichier principal ?

### Proposition B — Organisation par statut avec sous-dossiers

> Créer des dossiers par statut (`in-progress/`, `blocked/`, `done/`, etc.) avec chacun son propre fichier de suivi `roadmap.md`.

Sous-questions à trancher :

1. **Le répertoire racine `doc/roadmap/` doit-il servir exclusivement aux plans "active"** OU **faut-il créer un dossier `active/` dédié avec son propre `roadmap.md`** ?
   - Évalue les deux approches en termes de clarté, cohérence, et simplicité de navigation
2. **Les fichiers de suivi doivent-ils être suffixés par statut** (ex : `roadmap-in-progress.md`) OU **garder un nom uniforme `roadmap.md`** dans chaque dossier ?
   - Évalue l'impact sur les références croisées, la maintenabilité, et l'outillage

Questions de challenge :

- Combien de statuts distincts sont réellement nécessaires ? Risque de prolifération ?
- Comment gérer la transition d'un plan d'un dossier/statut à un autre sans casser les références ?
- Faut-il un fichier index/maître qui agrège la vue d'ensemble de tous les statuts ?
- **Quel est l'impact token ?** Un `roadmap.md` éclaté par statut est-il plus économe qu'un fichier unique, sachant que le skill ne lirait que le fichier du statut pertinent ?

### Proposition C — Capitalisation contextuelle automatique (CONTEXT.md)

> Lorsqu'un agent IA découvre une information cruciale (piège, dépendance cachée, contrainte technique...), le skill doit proposer à l'utilisateur de la consigner dans `doc/roadmap/CONTEXT.md`. L'utilisateur répond OUI, NON, ou fournit des instructions complémentaires.

Questions de challenge :

- Quels critères l'agent doit-il utiliser pour qualifier une information comme « cruciale » ?
- Le `CONTEXT.md` doit-il être global ou par plan/statut ?
- Faut-il catégoriser les entrées (⚠️ piège, 🔗 dépendance, 📌 contrainte, 💡 insight) ?
- Comment éviter la pollution du fichier avec des informations de faible valeur ?
- Faut-il un mécanisme de révision/nettoyage périodique du `CONTEXT.md` ?
- **Le `CONTEXT.md` risque-t-il de devenir lui aussi un gouffre à tokens** avec 350+ plans ? Faut-il le segmenter ?

---

## Phase 3 — Propositions complémentaires

Au-delà des propositions utilisateur, identifie **tes propres axes d'amélioration**, en portant une attention particulière au **coût token à grande échelle**. Considère notamment (liste non exhaustive) :

- **Économie de tokens à l'usage** : le skill peut-il adopter des stratégies de lecture sélective, de lazy-loading, de cache ou de résumé pour limiter la consommation de tokens lors de son exécution quotidienne sur un projet de 350+ plans ?
- **Validation & intégrité** : vérification de cohérence entre l'arborescence fichier et les fichiers de suivi
- **Onboarding** : facilité de prise en main pour un nouveau collègue qui installe le skill
- **Résilience** : gestion des erreurs, recovery après interruption, idempotence des opérations
- **Observabilité** : dashboards, statistiques, vues synthétiques du portfolio de plans — **générées sans lire tous les plans**
- **Performance** : optimisation des lectures/écritures fichier à grande échelle
- **Conventions & documentation** : clarté du README, exemples, guide de contribution
- **Extensibilité** : facilité d'ajout de nouveaux statuts, métadonnées, workflows
- **Interopérabilité** : compatibilité avec d'autres skills (notamment `/impeccable:impeccable` pour l'UX)
- **Pagination / virtualisation** : mécanisme pour ne charger que les N plans pertinents selon l'opération en cours

---

## Phase 4 — Utilisation du skill /impeccable:impeccable

Si le skill `/impeccable:impeccable` peut contribuer à améliorer la recherche de la meilleure UX, **utilise-le activement** dans ton analyse. Documente dans le rapport comment et où il a été utilisé et ce qu'il a apporté.

---

## Phase 5 — Rapport final

### Format de sortie

Produis un rapport Markdown exhaustif à enregistrer sous :

```
/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/doc/rapports/
```

**Nom du fichier** : `rapport-ameliorations-YYYY-MM-DD.md` (date du jour)

### Structure attendue du rapport

```markdown
# Rapport d'Audit & Améliorations — roadmap-tracking
## Date : YYYY-MM-DD
## Contexte : Projet de référence à 350+ plans

### 1. Synthèse exécutive
<!-- Résumé en 10 lignes max des conclusions clés -->
<!-- Inclure : estimation de l'impact token des recommandations -->

### 2. Analyse de la codebase
#### 2.1 Architecture actuelle
#### 2.2 Forces identifiées
#### 2.3 Faiblesses et dettes techniques
#### 2.4 Analyse du coût token par opération du skill

### 3. Analyse de l'utilisation réelle (Auxitum — 350+ plans)
#### 3.1 Arborescence et volumétrie
#### 3.2 Répartition statistique par statut
#### 3.3 Patterns d'usage observés
#### 3.4 Points de friction identifiés
#### 3.5 Estimation du coût token actuel d'une session type

### 4. Évaluation des propositions utilisateur
#### 4.1 Proposition A — Archivage des plans « done »
#### 4.2 Proposition B — Organisation par statut
#### 4.3 Proposition C — Capitalisation contextuelle (CONTEXT.md)
<!-- Chaque section inclut l'analyse d'impact token -->

### 5. Propositions complémentaires
#### 5.x [Titre de chaque proposition]
<!-- Pour chaque proposition :
- Problème identifié
- Solution proposée
- Bénéfice attendu
- Impact sur la consommation de tokens
- Complexité d'implémentation (faible/moyenne/élevée)
- Plan de migration/rattrapage pour les 350+ plans existants
-->

### 6. Plan de migration pour les 350+ plans existants
#### 6.1 Stratégie globale de rattrapage
#### 6.2 Script(s) de migration proposé(s)
#### 6.3 Estimation de l'effort de migration
#### 6.4 Procédure de rollback

### 7. Matrice de priorisation
<!-- Tableau : Amélioration | Impact UX | Impact Token | Complexité | Priorité -->

### 8. Estimation globale des gains tokens
<!-- Comparaison avant/après sur une session type avec 350+ plans -->

### 9. Annexes
#### 9.1 Arborescence complète analysée (listing)
#### 9.2 Échantillon de plans analysés (justification du choix)
#### 9.3 Utilisation du skill /impeccable:impeccable
#### 9.4 Méthodologie d'estimation des coûts tokens
```

---

## Contraintes impératives

1. **Économie de tokens PENDANT cette mission** : respecte scrupuleusement les règles de lecture de la section "Optimisation de la consommation de tokens" — ne lis jamais les 350+ plans un par un
2. **Exhaustivité analytique** : compense l'absence de lecture exhaustive par des analyses statistiques et un échantillonnage rigoureux
3. **Rétrocompatibilité** : chaque amélioration DOIT prévoir un mécanisme de rattrapage/migration pour les 350+ plans existants
4. **Pragmatisme** : priorise les améliorations par ratio impact/effort, avec le coût token comme critère de premier ordre
5. **Argumentation** : chaque recommandation doit être justifiée par des observations concrètes issues de l'analyse
6. **Autonomie de l'utilisateur** : les mécanismes proposés doivent toujours laisser le dernier mot à l'utilisateur (confirmation OUI/NON/instructions)
7. **Projection** : considère la scalabilité pour 500, 1000+ plans — les solutions proposées doivent tenir dans la durée