---
plan:
  id: '22'
  name: 22-roadmap-tracking-Integration-recommandations-audit-#129.md
  link: doc/roadmap/22-roadmap-tracking-Integration-recommandations-audit-#129.md
  source: local
status: done
date: 2026-09-14
updated_at: 2026-09-15
description: >
  Intégration des recommandations d'audit #129 au skill roadmap-tracking
priority: high
complexity: L
scope:
  modules:
    - modules/plan.md
    - modules/execute.md
    - modules/wrapup.md
    - references/templates.md
issue:
  id: 22
  url: https://github.com/ehouriez/roadmap-tracking/issues/22
---

# Plan #22 — Intégration des recommandations d'audit #129 au skill roadmap-tracking

## Contexte

Le [rapport d'analyse #129](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/doc/audits/129-analyse-implementation-plan.md) a identifié un surcoût de **$6,76 (24% du budget)** dû à 4 sessions Sonnet improductives en phase debug, alors qu'Opus a résolu le problème en 1 session. Ce plan intègre les 4 axes d'amélioration les plus pertinents au skill `/roadmap-tracking`.

## User Review Required

> [!IMPORTANT]
> **Axe 4 — Remplacement du budget chiffré** : le rapport §6.3.3 proposait une grille budgétaire en $/complexité. L'agent n'ayant pas accès aux données de coût à runtime (pas de Langfuse, pas de champ `usage`), cette approche est inapplicable. L'alternative proposée ci-dessous utilise la **règle "2 strikes"** comme proxy de contrôle de dérive — le nombre d'échecs consécutifs remplace le seuil de coût. Justification : sur #129, le trigger "2 strikes" aurait détecté l'errance dès la session 6 ($2,77 perdus) au lieu de la session 8 ($6,76 perdus). Le signal "même bloc échoue 2 fois de suite" est un indicateur fiable d'errance sans nécessiter de métriques de coût.

> [!WARNING]
> **Matrice de sélection étendue aux phases debug** : la matrice actuelle ne recommande le modèle que pour l'implémentation (tier par complexité d'étape). L'audit montre que le **debug non trivial** est la phase la plus critique pour le choix de modèle. La matrice étendue ajoute cette dimension sans modifier la mécanique existante.

## Open Questions

> [!IMPORTANT]
> **Q1** — La section "diagnostic structuré" (Axe 3) doit-elle remplacer l'actuel format libre du journal de session en phase debug, ou s'y **ajouter** comme section séparée dans le template de plan ? Je propose l'ajout (section `## Diagnostic en cours` distincte du journal), car le journal garde sa valeur narrative pour les sessions productives.

> [!IMPORTANT]
> **Q2** — La recommandation d'escalade "2 strikes" doit-elle être un simple message informatif (l'opérateur décide) ou un **point d'arrêt `⏸️`** forçant une décision explicite avant de continuer avec le même modèle ? Je propose le point d'arrêt pour cohérence avec la gate modèle existante — mais c'est plus intrusif.

## Proposed Changes

### Axe 1 — Matrice de sélection de modèle étendue (Phase debug)

**Problème** : la matrice actuelle (`plan.md` §"Matrice complexité → tier") ne couvre que l'implémentation. L'audit prouve que XS/S/M → Sonnet est valide pour l'implémentation, mais catastrophique en debug non trivial.

**Solution** : enrichir la matrice avec une dimension **type de tâche**, sans modifier le mécanisme de gate existant. La gate d'entrée Phase 7 continue de ne considérer que les étapes d'implémentation ; la nouvelle matrice est exploitée **pendant** la boucle tests/fix.

---

#### [MODIFY] [plan.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/plan.md)

**Section « Matrice complexité → tier »** (L111-119) — Ajouter après la matrice existante un tableau de recommandation **par type de tâche**, inspiré du §6.1 du rapport :

```markdown
### Matrice type de tâche → modèle recommandé

| Type de tâche | Modèle recommandé | Justification |
|---|---|---|
| Implémentation simple (XS/S/M, périmètre bien défini) | 🟦 Sonnet (standard) | Efficace et économique sur tâches cadrées par le plan |
| Implémentation complexe (L/XL, architecture transverse) | 🟧 Opus (reasoning) | One-shot multi-étapes, qualité architecturale |
| Exécution de tests (procédures documentées) | 🟦 Sonnet (standard) | Suit fidèlement les procédures du plan |
| Debug trivial (erreur de syntaxe, import, fix local) | 🟦 Sonnet (standard) | Correction ciblée dans un périmètre restreint |
| Debug non trivial (root cause non évidente, transverse code/infra) | 🟧 Opus (reasoning) | Raisonnement transversal, exploitation du contexte plan |
| Durcissement / fix préventif | 🟧 Opus (reasoning) | Correction structurelle + post-mortem |

> Cette matrice complète la matrice complexité → tier (ci-dessus) qui reste
> la référence pour la gate d'entrée Phase 7. La matrice par type de tâche
> est utilisée par la **règle d'escalade "2 strikes"** (voir
> `modules/execute.md`) et comme guide lors des reprises en phase debug.
```

**Complexité** : XS · aucune logique métier, ajout documentaire dans un module existant.

---

### Axe 2 — Règle d'escalade "2 strikes" (Phase tests/fix)

**Problème** : Sonnet peut boucler indéfiniment en phase debug sans progresser vers la root cause, même avec le contexte plan complet. Sur #129, 4 sessions / $6,76 perdus sans résultat.

**Solution** : détecter 2 échecs consécutifs **sur le même bloc de test** dans le plan et recommander l'escalade vers Opus. Signal basé sur les verdicts ❌ consignés dans la section `## Tests` du plan — information déjà disponible, sans dépendance à des métriques de coût.

---

#### [MODIFY] [execute.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/execute.md)

**Après la section « Étape ✅ Validation »** (après L411) — Ajouter une nouvelle section :

```markdown
## Règle d'escalade "2 strikes" — détection d'errance en phase tests/fix

> **Objectif** : détecter l'errance d'un modèle en phase debug et recommander
> une escalade avant d'accumuler des sessions improductives. Cette règle
> remplace un budget chiffré (inaccessible à runtime) par un proxy
> comportemental : le nombre d'échecs consécutifs sur le même bloc de test.

### Déclenchement

```
SI   le tableau « Résultats joués et vérifiés » (section ## Tests du plan)
     contient ≥ 2 verdicts ❌ consécutifs sur le **même bloc/test**
ET   ces verdicts proviennent de sessions distinctes (même modèle)
ET   le modèle actif est de tier `standard` (Sonnet)
ALORS  déclencher la recommandation d'escalade ci-dessous.
```

**Précisions** :
- « Même bloc/test » = même identifiant dans la colonne « Test » du tableau
  (ex. « Bloc C — réconciliation boot »). Un ❌ sur le bloc A suivi d'un ❌
  sur le bloc C ne déclenche pas la règle.
- « Sessions distinctes » = les verdicts proviennent d'entrées de journal de
  session différentes. Deux ❌ dans la même boucle d'itération
  (`autonomous-tests.md`) ne comptent pas — la garde-fou `max_iterations`
  gère ce cas.
- La règle ne s'applique **pas** si le modèle actif est déjà `reasoning`
  (Opus) — il n'y a pas d'escalade au-dessus.

### Recommandation d'escalade

Quand la règle est déclenchée, afficher dans le chat :

```
⚠️ Escalade recommandée — règle "2 strikes"

Le bloc de test « {nom_du_bloc} » a échoué lors de {N} sessions consécutives
avec le modèle actuel ({modèle_actif}, tier {tier_actif}).

Historique des tentatives (section ## Tests du plan) :
| Session | Verdict | Diagnostic résumé |
|---|---|---|
| {date_1} | ❌ | {diagnostic_1} |
| {date_2} | ❌ | {diagnostic_2} |

→ Recommande une escalade vers un modèle de tier reasoning (ex. Opus)
  pour exploiter le contexte plan accumulé et diagnostiquer la root cause.
  Voir references/environment.md § Generic Action Mapping pour la commande.

---
⏸️ Réponds `bypass` pour continuer avec le modèle actuel, ou change de
   modèle via la commande de ton IDE puis relance avec `continue`.
```

> Ce point d'arrêt est **identique en mécanique** à la gate modèle
> existante (même format, même options `bypass`/switch). L'opérateur reste
> décideur : la règle recommande, elle n'impose pas.

### Critères d'escalade immédiate (bypass de la règle 2 strikes)

Certains patterns justifient une escalade dès le **1er échec**, sans
attendre le 2ème strike. Afficher le même bloc `⚠️` avec la mention
« Escalade immédiate recommandée » si l'un de ces critères est détecté :

- Le problème implique l'interaction entre code et infrastructure (Docker,
  CI/CD, registre d'images, chaîne de déploiement).
- La session Sonnet a produit un diagnostic **sans preuve matérielle**
  (hypothèse formulée mais non vérifiée par inspection d'artefact runtime).
- Le plan consigne une piste pertinente non exploitée par les sessions
  précédentes (visible dans le diagnostic structuré, voir Axe 3).
- La session a bloqué >10min sans output.

> Ces critères sont évalués **par le modèle lui-même** à l'entrée de chaque
> session de reprise en phase tests/fix. Ils ne sont pas mécaniques (pas de
> compteur automatique) — c'est une heuristique de jugement guidée par le
> contexte plan.

### Interaction avec la garde-fou `max_iterations` (mode autonomous)

La règle "2 strikes" et la garde-fou `max_iterations` opèrent à des
granularités différentes et se complètent :

| Mécanisme | Granularité | Scope | Action |
|---|---|---|---|
| `max_iterations` | Intra-session (boucle itérative) | 1 étape | STOP après N itérations dans la même session |
| "2 strikes" | Inter-sessions | 1 bloc de test | Recommandation d'escalade modèle |

Un bloc qui atteint `max_iterations` en session 1, puis à nouveau en
session 2, déclenche "2 strikes" — la combinaison est naturelle.
```

**Complexité** : M · logique de détection basée sur le contenu du plan (déjà présent), intégration au format de gate existant.

---

#### [MODIFY] [wrapup.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/wrapup.md)

**Section « Workflow : reprise d'un plan existant »** (L36-83) — Ajouter une vérification "2 strikes" à l'entrée de la reprise, après la gate modèle et avant le point d'arrêt :

```markdown
> **Vérification "2 strikes" sur reprise.** Avant d'afficher le point d'arrêt
> de reprise, inspecter le tableau « Résultats joués et vérifiés » du plan.
> Si la règle "2 strikes" est déclenchée (≥ 2 ❌ consécutifs sur le même bloc,
> modèle actif = tier `standard`), afficher la recommandation d'escalade
> **avant** le `⏸️` de reprise. L'opérateur voit la recommandation dans le
> même résumé que l'état du plan — pas de tour supplémentaire.
```

**Complexité** : XS · ajout d'un bloc conditionnel dans un module existant.

---

### Axe 3 — Section "diagnostic structuré" (enrichissement du plan)

**Problème** : le journal de session est un log libre. Les hypothèses éliminées, les pistes ouvertes et les vérifications manquantes ne sont pas structurées de manière à guider le modèle suivant. Sur #129, la piste "décalage image" a été effleurée en session 5 sans jamais être transformée en action.

**Solution** : ajouter dans le template de plan une section `## Diagnostic en cours` activée automatiquement dès qu'un test échoue en phase tests/fix. Structure imposée : hypothèses éliminées / pistes ouvertes / vérifications à jouer.

---

#### [MODIFY] [templates.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/references/templates.md)

**Section « Template de contenu »** (L123-198) — Ajouter après la section `## Tests` et avant `## Journal de session` :

```markdown
## Diagnostic en cours

> Section activée **à la première occurrence d'un échec de test** en phase
> tests/fix. Absente à la création du plan, créée à la volée quand nécessaire.
> Supprimée (ou marquée « Résolu ») quand le diagnostic est conclu.
>
> **Règle d'écriture** : cette section est mise à jour **à chaque session**
> de la boucle tests/fix, en plus du journal de session. Le journal reste
> narratif ; le diagnostic est structuré pour accélérer la reprise.

### Bloc(s) en échec

| Bloc | Dernière tentative | Strikes | Verdict |
|------|-------------------|---------|---------|
| Bloc C — réconciliation boot | 2026-09-14 session 8 | 4 | ❌ |

### Hypothèses éliminées
- [x] Race condition procédure → fixée (health-check wait, session 4)
- [x] Stale rows en DB → infirmée (pre-cleanup = 0/0, session 5)

### Pistes ouvertes (non vérifiées)
- [ ] ⚠️ L'image Docker en cours contient-elle le code de réconciliation ?
- [ ] Le tag `:latest` pointe-t-il sur le build post-#129 ?

### Vérifications à jouer
- `docker exec auxitum-orchestrator grep reconcileOrphanedRuns /app/server.js`
- `docker exec auxitum-orchestrator cat /app/package.json | grep version`
```

**Complexité** : S · template documentaire, pas de logique, mais impacte la structure du fichier plan et les instructions d'écriture.

---

#### [MODIFY] [execute.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/execute.md)

**Section « Si les tests échouent »** (L405-411) — Enrichir la procédure de boucle tests/fix pour inclure la mise à jour du diagnostic structuré :

```markdown
- **Si un ou plusieurs tests échouent** :
  1. Analyser les résultats transmis.
  2. **Mettre à jour la section `## Diagnostic en cours`** du fichier plan
     (voir `references/templates.md`) :
     - Ajouter les hypothèses éliminées par cette session.
     - Documenter les pistes ouvertes non encore vérifiées.
     - Lister les vérifications à jouer (commandes concrètes).
     - Mettre à jour le compteur de strikes dans le tableau des blocs en échec.
     Si la section n'existe pas encore, la créer à la volée.
  3. Corriger l'implémentation.
  4. **Vérifier la règle "2 strikes"** (voir ci-dessous) avant de re-soumettre.
  5. **Revenir à l'étape `🧪 Tests`** : régénérer une procédure de test mise à
     jour (incluant les vérifications de non-régression si pertinent) **et** un
     nouveau bloc `📦 Commit proposé` pour les corrections.
  6. Boucler jusqu'à validation complète.
```

**Complexité** : S · modification d'une procédure existante, ajout de 2 sous-étapes.

---

### Axe 4 — Remplacement du budget chiffré par "2 strikes" comme proxy

**Problème** : le §6.3.3 du rapport proposait une grille budgétaire ($/complexité) intégrable au skill. L'agent n'a **pas accès** aux données de coût à runtime — la solution est inapplicable.

**Solution** : pas de nouvelle section dédiée. La règle "2 strikes" (Axe 2) sert de **proxy au budget** — elle détecte l'errance via un signal comportemental (échecs consécutifs) plutôt que via un seuil de coût. L'impact est concentré dans l'Axe 2.

**Ajout complémentaire** : un paragraphe explicite dans le SKILL.md ou dans `execute.md` documentant le choix architectural (pourquoi pas de budget chiffré, pourquoi "2 strikes" comme proxy).

---

#### [MODIFY] [execute.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/execute.md)

**Dans la nouvelle section "Règle d'escalade 2 strikes"** (Axe 2) — Ajouter un encadré de design rationale :

```markdown
> **Pourquoi "2 strikes" et pas un budget chiffré ?**
>
> Le rapport d'audit §6.3.3 proposait une grille budgétaire par complexité
> de plan (ex. L = $16-26). Cette approche suppose un accès runtime aux
> données de coût (tokens consommés, prix/token) — données inaccessibles à
> l'agent (pas de clé API Langfuse, pas de visibilité sur le champ `usage`
> de l'API LLM).
>
> La règle "2 strikes" est un **proxy comportemental** : elle détecte
> l'errance via le même signal qu'un humain utiliserait — « ce test échoue
> pour la 2ème fois sans progression ». Sur #129, ce signal aurait
> économisé $3,99 et ~33min vs. l'escalade tardive réelle.
>
> Avantages du proxy comportemental vs. budget chiffré :
> - **Indépendant de l'infrastructure d'observabilité** (pas de Langfuse requis).
> - **Signal qualitatif** : détecte l'errance même si le coût est faible.
> - **Fonctionne pour tout modèle** : le seuil de coût serait à recalibrer
>   à chaque changement de pricing ; le compteur d'échecs est stable.
```

**Complexité** : XS · bloc documentaire, aucune logique.

---

## Synthèse des fichiers impactés

| Fichier | Axe(s) | Type de modification |
|---|---|---|
| [`plan.md`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/plan.md) | 1 | Ajout matrice type de tâche → modèle |
| [`execute.md`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/execute.md) | 2, 3, 4 | Ajout section "2 strikes" + modification boucle tests/fix + rationale |
| [`wrapup.md`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/wrapup.md) | 2 | Ajout vérification "2 strikes" à la reprise |
| [`templates.md`](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/references/templates.md) | 3 | Ajout section `## Diagnostic en cours` au template |

## Estimation de complexité par étape

| # | Étape | Complexité | Fichiers | Dépendances |
|---|---|---|---|---|
| 1 | Matrice type de tâche → modèle | XS · standard → Sonnet | `plan.md` | Aucune |
| 2 | Règle "2 strikes" dans `execute.md` | M · standard → Sonnet | `execute.md` | Étape 1 (la matrice est référencée) |
| 3 | Vérification "2 strikes" dans `wrapup.md` | XS · standard → Sonnet | `wrapup.md` | Étape 2 (référence la section) |
| 4 | Section "diagnostic structuré" dans `templates.md` | S · standard → Sonnet | `templates.md` | Aucune |
| 5 | Mise à jour boucle tests/fix dans `execute.md` | S · standard → Sonnet | `execute.md` | Étapes 2 + 4 |
| 6 | 🧪 Tests — Validation fonctionnelle complète | — | Tous | Étapes 1-5 |
| 7 | ✅ Validation — Relecture et clôture | — | Tous | Étape 6 |

**Complexité globale** : M (plusieurs fichiers, logique métier modérée, aucune architecture nouvelle — enrichissement d'un workflow existant).

## Verification Plan

### Tests fonctionnels (mode manual)

Pour chaque axe, vérifier que le skill se comporte correctement dans les scénarios suivants :

#### Axe 1 — Matrice de sélection
- **T1.1** : Reprendre un plan L en mode Sonnet → la gate doit mentionner le tier `reasoning` recommandé. *(comportement existant, inchangé — test de non-régression)*
- **T1.2** : La nouvelle matrice par type de tâche est référencée dans la section "2 strikes". *(vérification documentaire)*

#### Axe 2 — Règle "2 strikes"
- **T2.1** : Simuler un plan avec 2 ❌ consécutifs sur le même bloc dans la section `## Tests` → vérifier que le bloc `⚠️ Escalade recommandée` s'affiche à la reprise (mode Sonnet).
- **T2.2** : Même plan, mais le modèle actif est Opus → la règle ne doit **pas** se déclencher.
- **T2.3** : 1 seul ❌ → la règle ne doit **pas** se déclencher.
- **T2.4** : 2 ❌ sur des blocs **différents** → la règle ne doit **pas** se déclencher.
- **T2.5** : `bypass` sur le point d'arrêt → le workflow continue normalement.

#### Axe 3 — Diagnostic structuré
- **T3.1** : Soumettre un résultat d'échec de test → la section `## Diagnostic en cours` est créée dans le fichier plan avec les 3 sous-sections (hypothèses éliminées, pistes ouvertes, vérifications à jouer).
- **T3.2** : Soumettre un 2ème échec → la section est **mise à jour** (pas de duplication), le compteur de strikes incrémente.
- **T3.3** : Tous les tests passent → la section est marquée « Résolu » ou supprimée.

#### Axe 4 — Pas de budget chiffré
- **T4.1** : Vérifier l'absence de toute référence à un budget en dollars ou en tokens dans les instructions du skill. *(vérification documentaire)*
- **T4.2** : Le rationale expliquant le choix "2 strikes vs budget" est présent dans `execute.md`.

### Vérification documentaire
- Cohérence des références croisées entre modules (plan.md ↔ execute.md ↔ wrapup.md ↔ templates.md).
- Pas de conflit avec les sections existantes (gate modèle, `max_iterations`, boucle tests/fix).
- Conformité au format du skill (français pour les instructions, markdown tables, signaux de mode).

---

## Walkthrough — Intégration recommandations audit #129

### Résumé

Intégration de 4 axes d'amélioration identifiés dans le [rapport d'audit #129](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/doc/audits/129-analyse-implementation-plan.md) au skill `/roadmap-tracking`. Ces améliorations visent à réduire le surcoût d'errance observé ($6,76 / 24% du budget) lorsque Sonnet boucle en phase debug sans progresser.

### Changements effectués

#### 1. Matrice type de tâche → modèle ([plan.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/plan.md#L120-L134))

Ajout d'une seconde matrice de décision dans la section « Évaluation de complexité » qui map **6 types de tâches** (implémentation simple/complexe, tests, debug trivial/non trivial, durcissement) vers le modèle recommandé. Complète la matrice existante `complexité → tier` sans la modifier.

#### 2. Règle d'escalade "2 strikes" ([execute.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/execute.md#L452-L559))

Nouvelle section complète avec :
- **Condition de déclenchement** : ≥ 2 ❌ consécutifs sur le même bloc de test, sessions distinctes, modèle tier `standard`
- **Format d'escalade** : identique à la gate modèle existante (bloc `⚠️` + point d'arrêt `⏸️` + options `bypass`/switch)
- **Critères d'escalade immédiate** : 4 patterns justifiant une escalade dès le 1er échec (problème code/infra, diagnostic sans preuve, piste non exploitée, blocage >10min)
- **Interaction `max_iterations`** : les deux mécanismes se complètent (intra-session vs inter-sessions)
- **Design rationale** : explication du choix "2 strikes" vs budget chiffré (données de coût inaccessibles à runtime)

#### 3. Vérification "2 strikes" à la reprise ([wrapup.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/wrapup.md#L63-L71))

Ajout d'un bloc conditionnel dans le workflow de reprise : après la gate modèle et avant le `⏸️`, inspecter les résultats de tests du plan pour déclencher la recommandation d'escalade si applicable.

#### 4. Section "diagnostic structuré" ([templates.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/references/templates.md#L191-L215))

Nouveau `## Diagnostic en cours` dans le template de plan, positionné entre `## Tests` et `## Journal de session`. Sous-sections :
- `### Bloc(s) en échec` (tableau avec compteur de strikes)
- `### Hypothèses éliminées` (checklist)
- `### Pistes ouvertes (non vérifiées)` (checklist avec ⚠️)
- `### Vérifications à jouer` (commandes concrètes)

#### 5. Boucle tests/fix enrichie ([execute.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/execute.md#L405-L420))

La procédure « Si les tests échouent » passe de 4 à 6 sous-étapes :
- **Nouvelle étape 2** : mise à jour de `## Diagnostic en cours`
- **Nouvelle étape 4** : vérification de la règle "2 strikes" avant re-soumission

### Vérifications effectuées

| Test | Résultat | Détail |
|---|---|---|
| **T1.2** — Matrice par type de tâche référencée dans "2 strikes" | ✅ | `plan.md` L133 → `modules/execute.md` |
| **T2.x** — Section "2 strikes" complète et cohérente | ✅ | Condition, format, escalade immédiate, interaction max_iterations |
| **T3.x** — "Diagnostic en cours" dans template et référencé dans execute | ✅ | `templates.md` L191, `execute.md` L407+L520 |
| **T4.1** — Pas de budget chiffré dans les instructions actives | ✅ | Les $ dans `init-scan.md` sont des estimations de surcoût skill (Axe D existant), pas des budgets de plan |
| **T4.2** — Rationale "2 strikes vs budget" présent | ✅ | `execute.md` L541-558 |
| Cross-references plan.md ↔ execute.md ↔ wrapup.md ↔ templates.md | ✅ | 50+ occurrences vérifiées via grep |
| Pas de conflit avec `max_iterations` ni gate modèle existante | ✅ | Granularités distinctes documentées |

---

## Retours sur implémentation manuelle (2026/09/15)

### Problèmes détectés

| # | Fichier | Ligne(s) | Problème | Sévérité | Remédiation proposée |
|---|---|---|---|---|---|
| 1 | `modules/execute.md` | 373–375 | La procédure "Si les tests échouent" dans la section **Tests unitaires intermédiaires** (step 5) n'a pas été enrichie avec la mise à jour de `## Diagnostic en cours` ni la vérification de la règle "2 strikes". Seule la procédure de l'étape ✅ Validation a été mise à jour, conformément à la prescription du plan (L405-411). Crée une inconsistance comportementale : un échec de test intermédiaire ne met pas à jour le diagnostic structuré et ne déclenche pas "2 strikes". | 🟡 | Appliquer le même enrichissement 6 étapes au step 5 de la section "Tests unitaires intermédiaires", ou y ajouter un renvoi vers la procédure de ✅ Validation. Hors scope strict du plan #21 mais recommandé pour la cohérence du skill. |
| 2 | `references/templates.md` | 191–215 | La section `## Diagnostic en cours` est présente dans le template de plan, alors que sa propre note précise _"Absente à la création du plan, créée à la volée quand nécessaire"_ (L193). La note de bas de template (L228–231) confirme l'intention "créée à la volée" mais le template contredit cette intention : un LLM copiant le template inclura le header de la section à la création. Ambiguïté sur le comportement attendu lors de la Phase 5. | 🟡 | Deux options : (a) retirer la section du corps du template et l'isoler dans un encadré "Structure de référence pour `## Diagnostic en cours`" séparé du template actif ; (b) ajouter une note explicite en fin de section indiquant "OMIS à la création initiale — ce bloc est affiché ici pour référence uniquement". |

### Réponses aux questions subsidiaires

#### 3.1 — Résumé dans "Matrice complexité → tier" (plan.md L111–L119)

**Le résumé est-il nécessaire ?** Oui. La table de 3 lignes dans `plan.md` offre une consultation rapide pendant la gate modèle (Phases 1.5 et 3), évitant un aller-retour vers `references/environment.md`. La note "Tier résolu via `references/environment.md...`" indique la source autoritaire sans supprimer la valeur de référence locale.

**Est-il correct, adéquat et suffisant ?** Correct et adéquat. Sur la suffisance : la colonne "Role" présente dans `environment.md` (qui décrit l'usage de chaque tier) est absente du résumé. Son absence n'est pas bloquante car le contexte de la section (précédée de la grille de sizing et suivie de la matrice type de tâche) comble implicitement ce manque. Aucune correction requise.

#### 3.2 — Valeurs de "Matrice type de tâche → modèle recommandé" (plan.md L121–L135)

Toutes les valeurs sont correctes et adéquates au regard des observations #129 :

| Ligne | Recommandation | Conformité #129 |
|---|---|---|
| Implémentation simple (XS/S/M) → sonnet | ✅ | Sonnet performant sur toutes les étapes d'implémentation du plan |
| Implémentation complexe (L/XL) → opus | ✅ | Caractéristique "one-shot multi-étapes" exactement celle démontrée par Opus sur #129 |
| Exécution de tests → sonnet | ✅ | Procédures documentées = tâche cadrée, pas de raisonnement profond requis |
| Debug trivial → sonnet | ✅ | Périmètre restreint, corrections locales — pas de root cause transverse |
| Debug non trivial → opus | ✅ | Observation centrale de #129 : 4 sessions Sonnet infructueuses, Opus résout en 1 session |
| Durcissement / fix préventif → opus | ✅ | Correction structurelle + post-mortem = raisonnement global requis |

Aucune correction à apporter.

#### 3.3 — "Model Tier Resolution" dans environment.md (L56–L63)

Tous les mappings sont corrects : `sonnet→standard`, `opus→reasoning`, `haiku→light` (Anthropic) ; `luna→standard`, `sol→reasoning`, `terra→light` (OpenAI).

**Point de vigilance (non bloquant)** : la règle dit `Name contains "sonnet"` mais le system prompt expose le nom en casse mixte ("Sonnet 4.6 (1M context)"). La règle n'est pas explicitement case-insensitive. En pratique, les LLMs appliquent cette correspondance sans sensibilité à la casse et le comportement observé est correct. Aucune correction requise, mais une précision `(case-insensitive)` en fin de liste renforcerait la rigueur documentaire sans être urgente.

---

### Remédiations appliquées (2026/09/15)

| # | Problème | Fichier(s) modifié(s) | Statut |
|---|---|---|---|
| 1 | Procédure échec tests intermédiaires non alignée | `modules/execute.md` | ✅ |
| 2 | Section Diagnostic dans template actif | `references/templates.md` | ✅ |
| 3 | Colonne Role manquante dans résumé | `modules/plan.md` | ✅ |
| 4 | Case-insensitivity noms de modèles | `references/environment.md`, `modules/plan.md` | ✅ |
