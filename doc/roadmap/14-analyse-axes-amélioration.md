---
plan:
  id: 14
  name: 14-analyse-axes-amélioration.md
  link: doc/roadmap/14-analyse-axes-amélioration.md
  source: local
status: done
date: 2026-09-13
description: >
  Analyse et proposition d'amélioration du skill roadmap-tracking.
priority: high
complexity: M
intent: null
scope:
  modules:
    - SKILL.md
    - README.md
    - .skill-config.yml
    - references/environment.md
    - references/templates.md
    - hooks/hooks.json
    - hooks/codex-hooks.json
    - .codex-plugin/plugin.json  # NEW
issue:
  id: 14
  url: https://github.com/ehouriez/roadmap-tracking/issues/14
---

# Plan d'implémentation — Axes d'amélioration du skill roadmap-tracking

## Contexte et décisions confirmées

Le skill `/roadmap-tracking` fonctionne via un **hook `SessionStart`** qui injecte une
instruction textuelle à chaque début de session. Le fichier `.skill-config.yml`
(`./doc/roadmap/.skill-config.yml`) est la seule source de vérité persistée entre sessions.

**Décisions utilisateur confirmées :**
- `session.intent` : lié au **front matter du plan** (Option A), pas au `.skill-config.yml` global.
- Axe D (estimation surcoût) : **à implémenter** dans ce cycle.
- Axe E (système d'aide) : **à implémenter** dans ce cycle.

---

## Problèmes diagnostiqués

### Problème 1 — Axe B original : architecturalement cassé

Le désengagement « prototypage » proposé dans la synthèse pose une question en Phase 2
mais **ne persiste rien**. À la session suivante, le hook recharge le skill et repose
la question. L'état « désengagé » est perdu entre sessions → serpent qui se mord la queue.

**Solution** : `session.intent` persisté dans le **front matter du plan courant** (pas
dans `.skill-config.yml` global, pour éviter les collisions entre plans parallèles),
remis à `null` automatiquement à la clôture.

### Problème 2 — `--force` : option fantôme

`/roadmap-tracking --force` n'est pas parsable dans Claude Code/Codex. Les skills ne
reçoivent pas d'arguments CLI.

**Solution** : champ `mode:` dans `.skill-config.yml` + formulations verbales reconnues.

---

## User Review Required

> [!IMPORTANT]
> **`session.intent` dans le front matter** : Le champ `intent` est ajouté au front matter
> YAML du plan courant. Cela implique que chaque fichier plan peut porter `intent: prototype`
> ou `intent: production`. Le champ est **invisible dans le listing** (non affiché dans le
> tableau récapitulatif) et **non obligatoire** (rétrocompat totale avec les plans existants).

> [!WARNING]
> **Axe D — Estimation du surcoût** : Les estimations affichées (`~1 000 000 tokens`,
> `~$1,70`, `~8 min`) sont des **ordres de grandeur empiriques** tirés de la synthèse,
> pas des valeurs calculées dynamiquement. Le skill affichera une estimation calibrée
> sur la complexité estimée (XS/S/M/L/XL), sans calcul réel. Acceptable ?

> [!NOTE]
> **Axe E — Aide à la demande** : L'aide est générée **à la volée par l'LLM** depuis le
> contenu du SKILL.md, pas depuis un fichier statique. Elle est donc toujours à jour avec
> le skill, sans maintenance séparée. La note de bienvenue n'apparaît qu'une seule fois
> (flag `help.welcomed: true` dans `.skill-config.yml`), au premier démarrage du skill
> dans le projet.

---

## Schéma `.skill-config.yml` mis à jour

```yaml
# ./doc/roadmap/.skill-config.yml — entirely optional, non-blocking
ide: auto
models:
  active: null
  map: []
issues:
  mode: auto
tests:
  mode: null
  max_iterations: 3
  verifier: auto
grilling:
  enabled: true
  categories:
    phase2: []
    phase4: []
    phase6: []
roadmap-tracking:
  collaborative: false       # Axe A — projet multi-collaborateurs ?
  mode: auto                 # Axe A — auto | lightweight | full | off
  last-calibration: null     # Axe A — date ISO de la dernière calibration
  help:
    welcomed: false          # Axe E — true = note de bienvenue déjà affichée
```

## Ajout au front matter des plans (Axe B)

```yaml
# Champ optionnel, non obligatoire (rétrocompat totale)
intent: null                 # null | prototype | production
                             # Remis à null automatiquement à la clôture du plan
```

---

## Proposed Changes

### Axe A — Auto-calibrage selon le contexte collaboratif

**Priorité : 🥇 P1 | Effort : S**

Permet au skill de se désengage automatiquement sur les tâches XS/S solo, et de
passer en mode `lightweight` sur les tâches S collaboratives.

---

#### [MODIFY] [SKILL.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/SKILL.md)

**Section « Règle de démarrage »** — Ajout d'un bloc A.0 (initialisation config) :

- Si `.skill-config.yml` absent **ou** `roadmap-tracking.collaborative` absent :
  poser la question via `AskUserQuestion` + persister + consigner `last-calibration`.
- Si présent : lire la valeur sans redemander.

**Section « Phase 1 — Analyse initiale »** — Ajout de la matrice de décision :

| Complexité | `collaborative` | `mode: auto` → action |
|---|---|---|
| XS | - | Désengagement (écrire plan, afficher template, STOP) |
| S | `false` | Désengagement (écrire plan, afficher template, STOP) |
| S | `true` | Mode `lightweight` (plan + commits, sans ⏸️ intermédiaires) |
| M | - | Mode `lightweight` |
| L, XL | - | Mode `full` (workflow complet) |

Si `mode:` est `full`, `lightweight` ou `off` : ignorer la matrice, appliquer directement.

**Nouveau template de désengagement** (remplace `--force`) :

```
ℹ️ Skill /roadmap-tracking — Désengagement automatique

Complexité estimée : [XS|S] [· mode solo]
Le surcoût du workflow structuré (checkpoints, commits intermédiaires,
phases de validation) n'est pas justifié pour cette complexité.

✅ Plan rédigé dans : doc/roadmap/[nom-du-plan].md
📋 Implémente-le directement avec un prompt explicite.

💡 Pour forcer le workflow complet sur les prochaines tâches :
   Dis-moi « mode workflow complet »
   → Je mettrai à jour doc/roadmap/.skill-config.yml (mode: full).
```

**Nouvelles formulations verbales** ajoutées aux triggers et à la garde d'entrée :

| L'utilisateur dit | Action |
|---|---|
| « mode workflow complet » / « force le workflow » | Écrit `mode: full` + confirme |
| « mode lightweight » / « mode allégé » | Écrit `mode: lightweight` + confirme |
| « désactive le skill » / « mode off » | Écrit `mode: off` + confirme |
| « remets le mode auto » | Écrit `mode: auto` + confirme |
| « projet collaboratif » / « multi-collaborateurs » | Écrit `collaborative: true` + confirme |
| « projet solo » | Écrit `collaborative: false` + confirme |

---

#### [MODIFY] [environment.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/references/environment.md)

**Section « Skill Configuration Schema »** — Ajout des clés `roadmap-tracking.mode`,
`roadmap-tracking.collaborative`, `roadmap-tracking.last-calibration` avec leurs valeurs
par défaut et leur sémantique.

---

### Axe B — Détection du prototypage (remplacé)

**Priorité : 🥇 P1 | Effort : S**

Remplace la question éphémère de Phase 2 (non persistée) par un champ `intent`
persisté dans le **front matter du plan courant**.

---

#### [MODIFY] [SKILL.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/SKILL.md)

**Section « Phase 2 — Cadrage interactif »** — Ajout d'une question préalable :

> Avant les questions de cadrage habituelles, si le plan courant n'a pas encore de
> champ `intent` dans son front matter (ou si c'est un nouveau plan) : poser la
> question via `AskUserQuestion` **en première position** :
> « Cette tâche relève-t-elle d'une expérimentation / prototypage rapide ? »
> - **Oui** → écrire `intent: prototype` dans le front matter du plan → afficher
>   le template de désengagement prototypage → STOP. Ne pas rédiger de plan.
> - **Non** → écrire `intent: production` → continuer normalement.

Si `intent` est déjà fixé dans le front matter : ne pas reposer la question.

| `intent` au démarrage | Comportement |
|---|---|
| `null` (nouveau plan) | Poser la question en Phase 2 |
| `prototype` | Afficher le désengagement directement → STOP |
| `production` | Continuer normalement |

**Section clôture Phase 7 (✅ Validation)** — Ajout du reset :

> Lors de la clôture d'un plan (`status: done`), remettre `intent: null` dans le
> front matter du plan clôturé.

**Nouveau template de désengagement prototypage** :

```
ℹ️ Skill /roadmap-tracking — Mode prototypage détecté

Le workflow structuré (plan, phases, checkpoints) ralentirait ton itération
sans apporter de valeur sur une expérimentation.

💡 Utilise un prompt explicite directement.
   Exemple : « Implémente [X] et montre-moi le résultat. »

Si tu changes d'avis et veux tracer ce travail :
   Dis-moi « finalement je veux tracer ça »
   → Je reprendrai le workflow normalement.
```

**Nouvelles formulations verbales** reconnues :

| L'utilisateur dit | Action |
|---|---|
| « finalement je veux tracer ça » | Écrit `intent: production` → reprend le workflow |
| « remets en mode normal » | Écrit `intent: null` → repose la question |

---

#### [MODIFY] [templates.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/references/templates.md)

**Section « Front matter YAML »** — Ajout du champ `intent` (optionnel) :

```yaml
intent: null    # null | prototype | production — géré par le skill, non obligatoire
```

---

### Axe C — Mode lightweight

**Priorité : absorbé par Axe A | Effort : 0**

Entièrement couvert par le champ `mode: lightweight` introduit en Axe A.
Pas de travail séparé.

---

### Axe D — Estimation préalable du surcoût token

**Priorité : 🥉 P3 | Effort : XS | Dépendance : Axe A (complexité déjà estimée)**

Afficher une estimation du surcoût quand le skill détecte un **cas limite** :
complexité S avec `collaborative: true` (mode lightweight au lieu de off).
Ne jamais afficher sur chaque invocation.

---

#### [MODIFY] [SKILL.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/SKILL.md)

**Section « Phase 1 — Analyse initiale »** — Juste avant d'appliquer la matrice de
décision, si le cas est S+collaboratif (mode `lightweight` au lieu de `off`) :

```
📊 Estimation du surcoût skill pour ce plan (complexité S, mode collaboratif) :
   - Tokens supplémentaires estimés  : ~400 000 (+15 %)  [mode lightweight]
   - Coût supplémentaire estimé      : ~$0,70
   - Durée supplémentaire estimée    : ~4 min

   Le workflow allégé (sans checkpoints ⏸️) sera appliqué.
   Pour le workflow complet, dis « mode workflow complet ».
```

Table de calibrage des estimations par complexité et mode :

| Complexité | Mode | Tokens Δ | Coût Δ | Durée Δ |
|---|---|---|---|---|
| S | lightweight | ~400 000 | ~$0,70 | ~4 min |
| M | lightweight | ~600 000 | ~$1,10 | ~6 min |
| L | full | ~1 000 000 | ~$1,70 | ~8 min |
| XL | full | ~1 500 000 | ~$2,50 | ~12 min |

> Ces valeurs sont des ordres de grandeur empiriques calibrés sur la synthèse
> comparative — elles ne sont pas calculées dynamiquement.

---

### Axe E — Système d'aide contextuel

**Priorité : 🥈 P2 | Effort : S | Dépendance : Axes A, B (documente la config complète)**

---

#### [MODIFY] [SKILL.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/SKILL.md)

**Section « Applicabilité »** — Ajout d'un **troisième cas d'exception** (après
« culture générale » et « urgences ») :

```
Il ne s'applique PAS pour :
[...existants...]
+ Demandes d'aide sur le skill lui-même :
  « aide », « aide workflow », « aide config », « aide planification »,
  « aide plans », « aide tests », « aide git », « aide intégrations »,
  « aide roadmap », « help »
  → Afficher l'aide demandée et STOP.
     Aucune règle de démarrage. Aucun listing de plans.
     Aucune vérification de doc/roadmap/.
     Fonctionne même si le projet n'a jamais eu le skill.
```

> **Pourquoi « Applicabilité » et pas seulement la « Règle de démarrage » ?**
> La règle de démarrage est déjà en aval du hook — si le hook a injecté l'instruction,
> la règle de démarrage s'active en premier. L'exception doit être déclarée **avant**
> la règle de démarrage, au niveau de l'applicabilité globale du skill, pour être
> prise en compte dès le premier token de décision.

**Nouvelle section « Système d'aide »**, insérée après « Applicabilité » :

##### Note de bienvenue (première exécution uniquement)

Déclencheur : `.skill-config.yml` absent **ou** `help.welcomed` absent/`false`.

Après la question de calibrage collaboratif (Axe A.0), afficher :

```
💡 /roadmap-tracking — Aide disponible à tout moment

Pour obtenir de l'aide sur le skill, dis :
  « aide »               → Aide complète (toutes les features)
  « aide workflow »      → Phases, reprise, urgences, checkpoints
  « aide config »        → .skill-config.yml, modes, modèles
  « aide planification » → Sizing, grilling, désengagement, surcoût
  « aide plans »         → Front matter, format, incohérences, clôture
  « aide tests »         → Tests intermédiaires, finaux, mode autonomous
  « aide git »           → Commits, migration de plans, issues GitHub
  « aide intégrations »  → Skill impeccable (UX/UI), IDE

Cette note n'apparaîtra qu'une seule fois.
```

Puis écrire `help.welcomed: true` dans `.skill-config.yml`.

##### Aide à la demande

L'aide est **générée à la volée** depuis le contenu du SKILL.md et des references.
Elle est donc toujours synchrone avec le skill, sans maintenance séparée.

Déclencheur : phrases reconnues **sans déclencher le workflow** (exception à la
règle de démarrage, comme les questions de culture générale) :

| L'utilisateur dit | Contenu affiché |
|---|---|
| « aide » | Aide complète : toutes les catégories ci-dessous |
| « aide workflow » | Phases 1→7, reprise, urgences, signaux de mode, anti-court-circuit |
| « aide config » | `.skill-config.yml` complet, tous les champs, modes, modèles |
| « aide planification » | Grille de sizing, gate modèle, grilling, désengagement A, surcoût D |
| « aide plans » | Front matter, template, listing, incohérences, clôture, mode dégradé |
| « aide tests » | Tests intermédiaires, étape 🧪, étape ✅, mode autonomous, règle ⛔ |
| « aide git » | Commits 📦, migration, issues, `.migration-declined` |
| « aide intégrations » | Skill `impeccable`, mapping IDE, actions génériques |

Chaque aide par catégorie se termine par :

```
💡 Pour l'aide complète : « aide »
   Pour une autre catégorie : « aide [workflow|config|planification|plans|tests|git|intégrations] »
```

---

#### [MODIFY] [environment.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/references/environment.md)

**Section « Skill Configuration Schema »** — Ajout de la clé `help.welcomed`.

---

#### [MODIFY] [hooks/hooks.json](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/hooks/hooks.json)

**Instruction injectée par le hook `SessionStart`** — Ajout d'une exception symétrique
à celle déjà présente pour les commandes CLI :

> « Exception : si le premier prompt est une demande d'aide sur le skill
> (`aide`, `aide workflow`, `aide config`, `aide planification`, `aide plans`,
> `aide tests`, `aide git`, `aide intégrations`, `aide roadmap`, `help`),
> afficher uniquement l'aide demandée sans lancer la règle de démarrage
> (pas de listing de plans, pas de vérification de `doc/roadmap/`,
> pas de question nouveau plan / reprise). »

Cela garantit qu'une demande d'aide en conversation fraîche — **même sur un projet
sans `doc/roadmap/` ou complètement hors contexte de développement** — n'active
pas le workflow et n'affiche aucune question de démarrage.

#### [MODIFY] [hooks/codex-hooks.json](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/hooks/codex-hooks.json)

**Même exception que `hooks.json`**, mais adaptée au **format JSON Codex**
(`hookSpecificOutput` structuré) à la place du `printf` texte brut de Claude Code.

---

### Intégration native Codex

**Objectif** : réduire la friction à l'installation Codex. Actuellement, l'utilisateur
doit pointer manuellement vers `codex-hooks.json`. Avec un manifest `.codex-plugin/plugin.json`,
Codex découvre le hook automatiquement quand le plugin est installé.

> [!NOTE]
> **La commande `/hooks` reste incompressible** — c'est une contrainte de sécurité
> Codex explicitement documentée (source : [learn.chatgpt.com/docs/hooks](https://learn.chatgpt.com/docs/hooks)) :
> *"Installing or enabling a plugin doesn't automatically trust its hooks; Codex
> skips plugin-bundled hooks until you review and trust the current hook definition."*
> La seule échappée (`--dangerously-bypass-hook-trust`) est un contournement
> non recommandé et à usage unique. Le README sera mis à jour pour être explicite.

#### [NEW] [.codex-plugin/plugin.json](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/.codex-plugin/plugin.json)

```json
{
  "name": "roadmap-tracking",
  "hooks": "./hooks/codex-hooks.json"
}
```

Déclenche l'auto-découverte de `codex-hooks.json` par Codex lors de l'installation
du plugin. Sans ce fichier, Codex cherche `hooks/hooks.json` par défaut — qui est
le hook Claude Code (format texte brut incompatible).

> **Convention Codex** (doc ligne 381-396) :
> *"By default, Codex looks for `hooks/hooks.json` inside the plugin root.
> A plugin manifest can override that default with a `hooks` entry in
> `.codex-plugin/plugin.json`."*

#### [MODIFY] [README.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/README.md)

Section `## Hooks` — mise à jour :
- Ajouter la mention que Codex découvre maintenant le hook automatiquement via `.codex-plugin/plugin.json`.
- Conserver et clarifier la note sur `/hooks` (obligatoire, one-time, par design de sécurité Codex).

---

## Récapitulatif des fichiers modifiés

| Fichier | Axes | Nature |
|---|---|---|
| [`SKILL.md`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/SKILL.md) | A, B, D, E | Principal — règles, phases, templates, triggers |
| [`references/environment.md`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/references/environment.md) | A, E | Schema config (nouveaux champs) |
| [`references/templates.md`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/references/templates.md) | B | Champ `intent` dans le front matter |
| [`hooks/hooks.json`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/hooks/hooks.json) | E | Exception aide — format texte brut (Claude Code) |
| [`hooks/codex-hooks.json`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/hooks/codex-hooks.json) | E | Exception aide — format JSON `hookSpecificOutput` (Codex) |
| [`README.md`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/README.md) | Codex | Mise à jour install Codex + clarification `/hooks` obligatoire |
| **[NEW]** [`.codex-plugin/plugin.json`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/.codex-plugin/plugin.json) | Codex | Manifest Codex — auto-découverte de `codex-hooks.json` |

**Aucun autre fichier modifié.** (`forms.md`, `roadmap-file.md`, `github-issues.md`,
`migration.md`, `autonomous-tests.md`, `scripts/`, `.claude-plugin/` → inchangés.)

---

## Ordre d'implémentation recommandé

```
1. environment.md           → schéma config mis à jour (A + E)
2. templates.md             → champ intent (B)
3. SKILL.md                 → Axe A (calibrage + matrice + templates + triggers)
4. SKILL.md                 → Axe B (intent + Phase 2 + reset clôture + triggers)
5. SKILL.md                 → Axe D (estimation surcoût, inséré dans Phase 1)
6. SKILL.md                 → Axe E (Applicabilité exception + système d'aide complet)
7. hooks/hooks.json         → Axe E (exception aide — format Claude Code)
8. hooks/codex-hooks.json   → Axe E (exception aide — format Codex JSON)
9. .codex-plugin/plugin.json → [NEW] manifest Codex (auto-découverte codex-hooks.json)
10. README.md               → mise à jour section Hooks (install Codex + note /hooks)
```

---

## Verification Plan

### Vérification manuelle post-implémentation

| Scénario | Comportement attendu |
|---|---|
| Premier lancement sur projet neuf | Question collaboratif → note de bienvenue → listing plans |
| Second lancement (`.skill-config.yml` présent) | Pas de re-question, pas de note |
| Tâche XS → complexité estimée XS | Désengagement automatique + template |
| Tâche S + `collaborative: false` | Désengagement automatique |
| Tâche S + `collaborative: true` | Mode lightweight + estimation surcoût |
| Réponse « Oui » à la question prototypage | `intent: prototype` écrit + désengagement + STOP |
| Plan clôturé (`status: done`) | `intent: null` remis dans le front matter |
| `mode: full` dans config | Workflow complet ignorant la matrice |
| Phrase verbale « mode workflow complet » | `mode: full` écrit + confirmation |
| Phrase « aide tests » | Aide tests affichée SANS déclencher le workflow |
| Phrase « aide » | Aide complète affichée SANS déclencher le workflow |
| Même phrases dans Codex | Même comportement via `codex-hooks.json` |

### Aucun test automatisé requis

Les modifications sont des instructions en langage naturel dans des fichiers Markdown.
La vérification est comportementale (prompts de test dans Claude Code/Codex).

---

## Note de développement — `/hooks` Codex

La commande `/hooks` est **non contournable de façon propre** dans Codex.
Source : [learn.chatgpt.com/docs/hooks](https://learn.chatgpt.com/docs/hooks).

| Mécanisme | Supprime `/hooks` ? | Recommandé |
|---|---|---|
| Plugin installé + `.codex-plugin/plugin.json` | ❌ Non | ✅ Oui |
| `--dangerously-bypass-hook-trust` | ✅ Oui | ❌ Non (one-off, risqué) |
| Managed hook via `requirements.toml` enterprise | ✅ Oui | Hors scope (usage enterprise) |

Le README documente `/hooks` comme étape one-time obligatoire — cette note confirme
que c'est la position correcte, basée sur la documentation officielle Codex.

---

## Journal de session

| Date | Action | Détails |
|---|---|---|
| 2026-09-13 | Analyse et cadrage | Validation de l'architecture : `intent` dans le front matter du plan (Option A), persistance Axe A/E dans `.skill-config.yml`, spécifications des 5 axes d'amélioration. |
| 2026-09-13 | Étape 1 : `references/environment.md` | Ajout des paramètres `roadmap-tracking.collaborative`, `mode`, `last-calibration`, `help.welcomed` et documentation de la sémantique et de la matrice de décision. |
| 2026-09-13 | Étape 2 : `references/templates.md` | Ajout du champ `intent` optionnel (`null` \| `prototype` \| `production`) dans la table des attributs et dans les exemples de front matter (GitHub & Local). |
| 2026-09-13 | Étapes 3 à 6 : `SKILL.md` | • **Axe E** : Ajout de l'exception d'aide dans `Applicabilité` et création de la section `Système d'aide` (aide à la demande et note de bienvenue mono-occurrence).<br>• **Axe A** : Ajout du bloc A.0 (initialisation config collaborative) dans la Règle de démarrage standard, matrice de décision auto-calibrage dans Phase 1, templates de désengagement automatique, triggers verbaux de changement de mode.<br>• **Axe B** : Question préalable sur l'intention (prototypage vs production) en première position en Phase 2, template de désengagement prototypage, triggers verbaux, et réinitialisation automatique `intent: null` lors de la clôture de plan (Phase 7).<br>• **Axe D** : Affichage préalable d'estimation de surcoût token pour le cas limite S collaboratif (mode lightweight) + table empirique de calibrage. |
| 2026-09-13 | Étape 7 : `hooks/hooks.json` | Ajout de l'exception d'aide (`aide`, `help`, etc.) dans l'instruction textuelle de début de session `SessionStart` (Claude Code). |
| 2026-09-13 | Étape 8 : `hooks/codex-hooks.json` | Ajout de l'exception d'aide dans le payload JSON `hookSpecificOutput` de `sessionStart` (Codex). |
| 2026-09-13 | Étape 9 : `.codex-plugin/plugin.json` | Création du manifest plugin Codex pointant vers `./hooks/codex-hooks.json` pour auto-découverte native. |
| 2026-09-13 | Étape 10 : `README.md` | Documentation de l'auto-découverte du hook Codex via `.codex-plugin/plugin.json`, clarification de l'étape de validation `/hooks` obligatoire, et mise à jour de l'exemple de configuration. |
| 2026-09-13 | Étape 11 : Clôture du plan | Mise à jour du statut (`status: done`, `intent: null`) et journal de session rédigé. |

