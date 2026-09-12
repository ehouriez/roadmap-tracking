# Synthèse comparative — Implémentation avec et sans skill /roadmap-tracking

## TLDR

L'exécution **sans skill (A)** est **1,7× moins chère** ($2,38 vs $4,11) et **2,6× plus rapide** (4m52 vs 12m42).
L'exécution **avec skill (B)** produit un résultat **qualitativement supérieur** : version bump sémantique, checkpoints structurés avec blocs `⏸️` explicites, garde-fou « aucun commit si rien n'a changé », et une charge cognitive utilisateur quasi nulle (1 ligne de prompt vs 10).

**Règle de choix** : pour une tâche de complexité S dont le périmètre est bien cadré et le risque d'effet de bord faible, le mode sans skill suffit. Dès que la tâche implique de la traçabilité, des commits intermédiaires, ou un workflow multi-phases avec checkpoints, le surcoût du skill est amorti par la valeur structurelle qu'il apporte.

---

## 1. Comparaison factuelle

| Critère | Sans skill (A) | Avec skill (B) | Δ | Avantage |
|---|---|---|---|---|
| **Coût total** | $2,38 | $4,11 | +$1,73 (+72 %) | A |
| **Tokens totaux (Σ)** | 2 827 976 | 3 872 586 | +1 044 610 (+37 %) | A |
| **Tokens output** | 20 748 | 48 570 | +27 822 (+134 %) | A |
| **Tokens input (estimé¹)** | ~2 807 228 | ~3 824 016 | +1 016 788 (+36 %) | A |
| **Durée d'exécution** | 4m 52s | 12m 42s | +7m 50s (×2,6) | A |
| **Longueur du prompt** | 10 lignes, 5 étapes explicites | 1 ligne | — | B |
| **Charge cognitive utilisateur** | Moyenne — doit orchestrer le workflow, anticiper les cas d'erreur, structurer les étapes | Minimale — délègue l'orchestration au skill | — | B |
| **Version produite** | 2.5.7 (pas de bump) | 2.6.0 (bump mineur) | — | B |
| **Structure des checkpoints** | Non cadrée — l'agent implémente d'un bloc sans pause intermédiaire (point d'attention #1 de la revue) | Blocs `⏸️` explicites avec instructions de commit, push et attente de retours avant passage à l'étape suivante | — | B |
| **Gestion des commits** | Non spécifiée dans le prompt (point d'attention #4 de la revue) | Intégrée : blocs `📦 Commit proposé` formatés + garde-fou « aucun commit si rien n'a changé » | — | B |
| **Robustesse / gestion d'erreur** | Stop-on-failure explicite (étape 5) mais asymétrique (étape 4 ne dit pas de s'arrêter) | Gérée par le workflow du skill — pas de micro-pilotage nécessaire | — | B |
| **Pertinence des tests** | Risque de tests superficiels — l'agent doit inventer la procédure (point d'attention #2 de la revue) | Procédure de tests intégrée au workflow skill, avec attente de résultats complets avant validation | — | B |
| **Traçabilité** | Plan créé mais pas de checkpoints intermédiaires documentés | Plan + phases + checkpoints + commits intermédiaires tracés | — | B |

> ¹ Tokens input estimés = Σ total − tokens output.

### Détail du diff produit

L'exécution B a produit **4 améliorations structurelles** absentes de l'exécution A :

| # | Modification (B uniquement) | Impact |
|---|---|---|
| 1 | Version bump `2.5.7` → `2.6.0` | Traçabilité sémantique de la release |
| 2 | Réécriture des blocs checkpoint post-implémentation avec `📦 Commit` + `⏸️` explicites et formatés | L'utilisateur humain reçoit un point d'arrêt clair avec action attendue |
| 3 | Ajout d'un checkpoint identique pour la phase de validation finale | Symétrie du workflow — pas de cas oublié |
| 4 | Garde-fou : « Si aucun fichier n'a été modifié depuis le dernier commit → `📦 Aucun commit nécessaire` » | Évite les commits vides, réduit le bruit dans l'historique Git |

L'exécution A a produit des modifications fonctionnellement correctes mais **sans ces garde-fous structurels**.

---

## 2. Avantages et inconvénients

### Sans skill (A)

| | Détail |
|---|---|
| ✅ **Coût maîtrisé** | $2,38 — presque moitié prix. Pour une tâche S, c'est significatif. |
| ✅ **Rapidité** | 4m52 — feedback loop court, itération rapide. |
| ✅ **Transparence** | Le prompt contient l'intégralité du workflow — pas de boîte noire. |
| ✅ **Pas de dépendance** | Fonctionne sans skill installé, portable entre projets. |
| ⚠️ **Charge cognitive** | L'utilisateur doit penser à l'orchestration, aux commits, aux cas d'erreur. |
| ⚠️ **Pas de checkpoints** | L'agent implémente tout d'un bloc — une erreur intermédiaire n'est détectée qu'aux tests finaux. |
| ⚠️ **Tests potentiellement superficiels** | Sans cadre, l'agent invente la procédure de test — risque de validation faible. |
| ⚠️ **Pas de version bump** | L'agent ne pense pas à bumper la version — absence de convention sémantique. |

### Avec skill (B)

| | Détail |
|---|---|
| ✅ **Charge cognitive minimale** | 1 ligne de prompt — l'orchestration est déléguée. |
| ✅ **Qualité structurelle supérieure** | Checkpoints, commits formatés, garde-fou commit vide, version bump. |
| ✅ **Traçabilité native** | Chaque phase est documentée, chaque transition est un point d'arrêt explicite. |
| ✅ **Robustesse** | Le workflow du skill gère les cas limites que l'utilisateur oublierait. |
| ✅ **Reproductibilité** | Le même skill produit le même workflow à chaque invocation — pas de variance de prompt. |
| ⚠️ **Coût ×1,7** | $4,11 — le skill injecte son propre contexte (rules, workflow, templates) → +37 % de tokens input. |
| ⚠️ **Durée ×2,6** | 12m42 — les checkpoints et pauses allongent mécaniquement l'exécution. |
| ⚠️ **Output ×2,3** | 48 570 tokens output — le skill génère plus de texte structurel (blocs checkpoint, plans, mises à jour). |
| ⚠️ **Opacité partielle** | Le workflow est dans le skill — l'utilisateur doit connaître le skill pour comprendre ce qui va se passer. |

---

## 3. Analyse du ratio coût/valeur

### Le surcoût brut

| Métrique | Δ absolu | Δ relatif |
|---|---|---|
| Coût | +$1,73 | +72 % |
| Durée | +7m 50s | +161 % |
| Tokens output | +27 822 | +134 % |

### Ce que le surcoût achète

| Valeur ajoutée | Quantifiable ? | Impact projet |
|---|---|---|
| Version bump sémantique | Oui (présent/absent) | Traçabilité des releases — critique en contexte collaboratif |
| Checkpoints `⏸️` explicites | Oui (0 vs 2) | Détection précoce d'erreurs — évite le « tout casse à la fin » |
| Garde-fou commit vide | Oui (présent/absent) | Hygiène Git — évite le bruit dans l'historique |
| Blocs `📦 Commit` formatés | Oui (présent/absent) | Conventions de commit respectées sans effort |
| Charge cognitive utilisateur | Qualitatif | 1 ligne vs 10 lignes + 4 points d'attention à anticiper |

### Verdict coût/valeur

Pour une **tâche unitaire de complexité S** réalisée par un utilisateur qui connaît bien le workflow :
- Le surcoût de **$1,73** est **difficile à justifier** si l'objectif est uniquement fonctionnel.
- L'exécution A produit un résultat **fonctionnellement correct** à moindre coût.

Pour une **tâche récurrente** ou dans un **contexte d'équipe** :
- Le surcoût est **amorti** par la reproductibilité, la traçabilité et l'absence de charge cognitive.
- Le coût du « prompt raté » (oubli d'un cas, tests superficiels, pas de version bump) n'apparaît pas dans les métriques tokens mais se paie en dette technique.

**Point de bascule estimé** : dès que le temps passé à rédiger et debugger un prompt explicite dépasse ~3 minutes, le skill devient rentable en coût total (temps humain + tokens).

---

## 4. Recommandation

| Contexte | Approche recommandée | Justification |
|---|---|---|
| Tâche S, one-shot, périmètre clair, utilisateur expert | **Sans skill** | Le coût et la vitesse priment. L'utilisateur sait ce qu'il fait et n'a pas besoin de garde-fous. |
| Tâche S, récurrente ou réalisée par plusieurs personnes | **Avec skill** | La reproductibilité et la standardisation du workflow justifient le surcoût. |
| Tâche M/L, multi-phases, risque d'effets de bord | **Avec skill** | Les checkpoints intermédiaires et la gestion d'erreur intégrée deviennent critiques. Le ratio coût/valeur s'inverse. |
| Expérimentation / prototypage rapide | **Sans skill** | Feedback loop court, itération rapide, pas besoin de traçabilité. |
| Production / livraison client | **Avec skill** | La traçabilité (commits, version bump, plan mis à jour) est une exigence, pas un luxe. |

**En résumé** : le skill `/roadmap-tracking` n'est pas un optimiseur de coûts tokens — c'est un **optimiseur de coûts cognitifs et de qualité structurelle**. Il coûte plus cher en tokens mais moins cher en attention humaine et en dette technique. Le choix dépend de ce qu'on optimise.

---

## 5. Axes d'amélioration

Les constats de cette synthèse convergent vers un même levier : **le skill devrait savoir quand il n'est pas rentable et se désengager de lui-même**, plutôt que de toujours dérouler l'intégralité de son workflow.

---

### Axe A — Auto-calibrage selon le contexte collaboratif

**Idée d'origine** : poser une question à l'utilisateur pour savoir si le projet est multi-collaborateurs, persister la réponse, et adapter le comportement du skill en fonction de la complexité estimée.

**Version consolidée** :

#### A.0 — Initialisation de la configuration

Au **premier déclenchement du skill dans un projet** (détection : absence du fichier `doc/roadmap/.skill-config.yml`), le skill :

1. Crée `doc/roadmap/.skill-config.yml` avec les valeurs par défaut :
   ```yaml
   # Auto-generated by /roadmap-tracking skill — editable manually
   roadmap-tracking:
     collaborative: false        # Projet géré par plusieurs collaborateurs
     last-calibration: null      # Date ISO de la dernière calibration
   ```
2. Pose la question :
   > Ce projet est-il géré par plusieurs collaborateurs ? (oui/non)
3. Met à jour la clé `collaborative` selon la réponse.
4. Consigne la date dans `last-calibration`.

**Si le fichier existe déjà**, le skill ne repose pas la question — il lit la valeur persistée. L'utilisateur peut modifier le fichier manuellement à tout moment.

> **Pourquoi persister plutôt que redemander ?**
> - Évite une question répétitive à chaque invocation.
> - Permet à un utilisateur de changer le mode sans relancer le skill (édition directe du YAML).
> - Donne une source de vérité versionnable dans Git — un nouveau collaborateur voit immédiatement la configuration.

#### A.1 — Désengagement sur complexité XS (quel que soit le mode collaboratif)

Lors de la première estimation de complexité globale du plan :

| Complexité estimée | Action |
|---|---|
| **XS** | Le skill **termine l'écriture complète du plan**, puis affiche un message de désengagement (voir template ci-dessous) et **s'arrête**. |

Justification : une tâche XS ne bénéficie jamais des checkpoints, commits intermédiaires ou phases de validation du skill — le overhead est systématiquement supérieur à la valeur ajoutée, même en contexte collaboratif.

#### A.2 — Désengagement conditionnel sur complexité S

| Complexité estimée | `collaborative` | Action |
|---|---|---|
| **S** | `false` | Le skill termine l'écriture du plan, affiche le message de désengagement, et **s'arrête**. |
| **S** | `true` | Le skill **continue son workflow normalement** — la traçabilité et la standardisation justifient le surcoût en contexte multi-collaborateurs. |

#### A.3 — Complexité M, L, XL : workflow complet

Aucun désengagement — le skill déroule l'intégralité de son workflow. Le rapport montre que c'est précisément sur ces complexités que le ratio coût/valeur s'inverse en faveur du skill.

#### Template de désengagement

```
ℹ️ Le skill /roadmap-tracking a estimé la complexité de ce plan à [XS|S].
[En mode solo, le|Le] surcoût du workflow structuré (checkpoints, commits
intermédiaires, phases de validation) n'est pas justifié pour cette complexité.

✅ Le plan a été rédigé intégralement dans : doc/roadmap/[nom-du-plan].md
📋 Vous pouvez l'implémenter directement avec un prompt explicite.

Le skill se désactive pour cette tâche. Pour forcer son utilisation,
relancez avec l'option : `/roadmap-tracking --force`
```

> **Point de robustesse — option `--force`** : le désengagement ne doit jamais être un mur. Si l'utilisateur a une raison légitime de vouloir le workflow complet sur une tâche S en solo (ex. : démonstration, audit, formation), `--force` bypasse la logique de calibrage.

---

### Axe B — Détection des contextes d'expérimentation

**Idée d'origine** : détecter depuis le prompt que la tâche est un prototypage rapide, et poser la question explicitement.

**Version consolidée** :

#### B.0 — Pourquoi ne pas détecter automatiquement depuis le prompt ?

La détection heuristique de l'intention « expérimentation » à partir du texte du prompt est **fragile** :
- Faux positifs : « Expérimente l'ajout de retry sur les appels API » → ce n'est pas du prototypage, c'est une implémentation.
- Faux négatifs : « Implémente un proof-of-concept pour le nouveau pipeline » → c'est du prototypage, mais le mot « implémente » ne le trahit pas.

**Recommandation** : ne pas tenter de classifier automatiquement. Intégrer la question dans la **phase de questions ciblées** (qui existe déjà dans le workflow du skill) — c'est plus fiable et plus transparent.

#### B.1 — Question ajoutée à la phase de questions ciblées

Lors de la phase initiale de questions, le skill pose systématiquement :

> Cette tâche relève-t-elle d'une expérimentation ou d'un prototypage rapide ? (oui/non)

Position dans la séquence : **première question** — si la réponse est « oui », les questions suivantes deviennent inutiles.

#### B.2 — Comportement selon la réponse

| Réponse | Action |
|---|---|
| **Oui** | Le skill affiche le message de désengagement (voir template ci-dessous) et **s'arrête immédiatement** — il ne rédige pas de plan. |
| **Non** | Le skill continue normalement sa phase de questions ciblées puis son workflow. |

Différence clé avec l'axe A : ici, le skill **ne produit pas de plan** — un prototypage rapide n'a pas besoin de plan structuré. Le skill se retire avant d'avoir consommé des tokens de rédaction.

#### Template de désengagement (prototypage)

```
ℹ️ Le skill /roadmap-tracking n'est pas adapté aux expérimentations
et prototypages rapides. Son workflow structuré (plan, phases, checkpoints)
ralentirait votre itération sans apporter de valeur.

💡 Recommandation : utilisez un prompt explicite directement.
Exemple : « Implémente [X] et montre-moi le résultat. »

Le skill se désactive pour cette tâche. Pour forcer son utilisation,
relancez avec l'option : /roadmap-tracking --force
```

---

### Axe C — Mode allégé (lightweight)

Les axes A et B raisonnent en **binaire** : le skill est actif ou il se désactive. Un troisième axe permettrait une **graduation** :

| Mode | Déclencheur | Comportement |
|---|---|---|
| **Off** | XS, ou prototypage, ou S solo | Le skill se désengage (axes A/B). |
| **Lightweight** | S collaboratif, ou M avec peu de phases | Le skill rédige le plan et gère les commits, mais **supprime les checkpoints `⏸️` intermédiaires** — il n'attend pas de validation humaine entre chaque phase. |
| **Full** | L, XL, ou `--force` | Workflow complet avec tous les checkpoints, phases de validation, et blocs `⏸️`. |

**Impact estimé sur les tokens** : le mode lightweight réduirait les tokens output de ~30-40 % (suppression des blocs `⏸️`, des instructions d'attente, et des résumés intermédiaires) tout en conservant la traçabilité des commits et le version bump.

Configuration possible dans `.skill-config.yml` :

```yaml
roadmap-tracking:
  collaborative: true
  mode: auto           # auto | lightweight | full | off
  last-calibration: 2026-09-12T23:17:03Z
```

En mode `auto` (défaut), le skill applique la matrice de décision des axes A/B/C. Les autres valeurs forcent un mode spécifique.

---

### Axe D — Estimation préalable du surcoût token

Avant de dérouler son workflow, le skill pourrait **estimer son propre overhead** et l'afficher à l'utilisateur :

```
📊 Estimation du surcoût skill pour ce plan (complexité S) :
   - Tokens supplémentaires estimés : ~1 000 000 (+37 %)
   - Coût supplémentaire estimé : ~\$1,70
   - Durée supplémentaire estimée : ~8 min

   Continuer avec le skill ? (oui/non)
```

**Limites** : l'estimation reste approximative (elle dépend du nombre de phases, de la taille des fichiers à modifier, etc.). Mais elle rend le compromis **explicite** plutôt qu'implicite — l'utilisateur décide en connaissance de cause.

> **Attention** : cet axe ne doit pas devenir un frein systématique. Le message ne doit apparaître que lorsque le skill détecte un cas limite (S solo, par exemple) — pas sur chaque invocation.

---

### Synthèse des axes et priorité d'implémentation

| Axe | Effort estimé | Impact coût tokens | Impact UX | Priorité suggérée |
|---|---|---|---|---|
| **A** — Auto-calibrage collaboratif | S | Élevé — évite le workflow complet sur XS/S solo | Moyen — 1 question one-shot | 🥇 P1 |
| **B** — Détection prototypage | XS | Élevé — court-circuite le skill avant toute consommation | Élevé — évite la frustration sur les POC | 🥇 P1 |
| **C** — Mode lightweight | M | Moyen — réduit ~30-40 % des tokens output en mode intermédiaire | Élevé — graduation plutôt que binaire | 🥈 P2 |
| **D** — Estimation surcoût | S | Faible (le surcoût est affiché, pas réduit) | Moyen — transparence décisionnelle | 🥉 P3 |

**Dépendances** : l'axe C dépend de A (il faut connaître la complexité et le mode collaboratif pour choisir entre lightweight et full). Les axes A et B sont indépendants et peuvent être implémentés en parallèle.
