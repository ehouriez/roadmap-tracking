# Module : Planification (Phases 2 à 4)

> **Chargé en Phases 1 à 4** — cadrage interactif, évaluation de complexité,
> grilling adaptatif, proposition et validation du plan. Section canonique de
> la **gate de recommandation de modèle** (référencée par init-scan Phase 1.5
> et par execute Phase 7).

---

## Phase 2 — Cadrage interactif

> 🔍 MODE CADRAGE — aucune écriture, aucune commande.

Lève les ambiguïtés via **grilling** (voir « Grilling adaptatif ») — quel que soit
le niveau de complexité (XS, S, M, L, XL). Catégories d'amorçage par défaut :
**périmètre** (inclus / hors scope), **critères de succès**, **dépendances**
(bloquantes / bloquées), **parties prenantes** (décideurs / impactés),
**alternatives écartées**, **risques identifiés**.

Termine ta compréhension par un court résumé (2-3 phrases) **avant** le premier round de grilling.

### Assistance design (UX/UI)

Si la demande touche à l'**UX ou l'UI** (interface, écran, composant, layout,
navigation, formulaire, état vide/erreur, typographie, couleur, accessibilité,
copy, micro-interactions…) **et** que le skill `impeccable:impeccable` est
disponible, **invoque-le en Phase 2** pour nourrir tes questions de cadrage et
les décisions de design du plan (Phase 3).

> **Référence de réflexion uniquement.** impeccable sert ici à poser de
> meilleures questions et à prendre de meilleures décisions — **pas** à lancer
> son pipeline de production (mocks, comps, sous-agents `impeccable-*`, revue de
> finition). Aucune production design pendant la planification. La production
> réelle reste en **Phase 7**, où impeccable pourra alors être invoqué pour de
> vrai. Cette invocation ne lève aucun point d'arrêt et ne dispense d'aucun.

**STOP.** Attendre les réponses.

---

## Évaluation de complexité et recommandation de modèle

Deux niveaux d'évaluation reposant sur la **même grille de sizing** :

- **Complexité globale** du plan → alimente le champ `complexity` du front
  matter (Phase 5, inchangé) **et** la gate de recommandation de modèle
  (Phase 3). Une seule et même évaluation pour les deux.
- **Complexité par étape** → indépendante de la globale : une étape `XS` peut
  exister dans un plan globalement `L`.

### Grille de sizing

| Taille | Critères indicatifs |
|---|---|
| `XS` | Changement isolé, 1 fichier, pas de logique nouvelle |
| `S` | Quelques fichiers, logique simple, pattern existant à reproduire |
| `M` | Plusieurs fichiers, logique métier modérée, tests à adapter |
| `L` | Transverse, nouvelle architecture ou pattern, coordination multi-composants |
| `XL` | Conception système, impacts structurels, multiples dépendances croisées |

### Matrice complexité → tier

Tier résolu via `references/environment.md § Model Tier & Environment Mapping`. Résumé :

| Tier | Usage | Anthropic default | OpenAI default |
|---|---|---|---|
| `standard` | Planification, implémentation courante | **sonnet** (current) | **luna** (current) |
| `reasoning` | Analyse complexe, architecture, multi-fichiers | **opus** | **sol** |
| `light` | Hors scope — jamais recommandé par la matrice | **haiku** | **terra** |

### Matrice type de tâche → modèle recommandé

| Type de tâche | Modèle recommandé | Justification |
|---|---|---|
| Implémentation simple (XS/S/M, périmètre bien défini) | 🟦 sonnet (standard) | Efficace et économique sur tâches cadrées par le plan |
| Implémentation complexe (L/XL, architecture transverse) | 🟧 opus (reasoning) | One-shot multi-étapes, qualité architecturale |
| Exécution de tests (procédures documentées) | 🟦 sonnet (standard) | Suit fidèlement les procédures du plan |
| Debug trivial (erreur de syntaxe, import, fix local) | 🟦 sonnet (standard) | Correction ciblée dans un périmètre restreint |
| Debug non trivial (root cause non évidente, transverse code/infra) | 🟧 opus (reasoning) | Raisonnement transversal, exploitation du contexte plan |
| Durcissement / fix préventif | 🟧 opus (reasoning) | Correction structurelle + post-mortem |

> Cette matrice complète la matrice complexité → tier (ci-dessus) qui reste
> la référence pour la gate d'entrée Phase 7. La matrice par type de tâche
> est utilisée par la **règle d'escalade "2 strikes"** (voir
> `modules/execute.md`) et comme guide lors des reprises en phase debug.

### Détection du modèle actif et de son tier

Procédure complète et mapping : voir `references/environment.md § Model Tier
Resolution`. Résumé :

- (case-insensitive) Nom contient « sonnet » ou « luna » → tier `standard`.
- (case-insensitive) Nom contient « opus » ou « sol » → tier `reasoning`.
- (case-insensitive) Nom contient « haiku » ou « terra » → tier `light` — toujours en mismatch.
- Inconnu → tier non détectable : ne pas afficher la gate, conserver
  uniquement les tags par étape.

Les mappings personnalisés (`models.map` dans `.skill-config.yml`) priment
sur les défauts Anthropic.

### Gate de recommandation de modèle

Si le modèle actif est détectable, évaluer silencieusement le tier — en
**Phase 1.5** (avant le cadrage), re-jouée en Phase 3 seulement si le cadrage a
changé la classe de complexité, ou lors d'une reprise si les étapes restantes
l'exigent.

**Cas 1 — tier adapté** → **continuer silencieusement** vers la phase suivante.
Aucun affichage, aucun arrêt. *(Fast-path : le bloc `ℹ️` n'apporte pas de valeur
décisionnelle — seul le mismatch justifie une interruption.)*

**Cas 2 — tier non adapté** → afficher le template correspondant (upgrade ou
downgrade), puis **point d'arrêt de bypass** (`⏸️`).

> ⛔ **VERBATIM** — Les deux templates ci-dessous doivent être reproduits
> **mot pour mot**, sans paraphrase ni reformulation. Seules les variables
> `{current_model}` et `{target_model}` sont substituées.
>
> ⛔ **TOKEN = ALIAS** — `{current_model}` et `{target_model}` sont **toujours**
> les alias de tier génériques (`sonnet`, `opus`, `haiku` pour Anthropic ;
> `luna`, `sol`, `terra` pour OpenAI/Codex), jamais la version runtime extraite
> du system prompt (ex. `Sonnet 4.6`, `claude-opus-5`). Voir
> `references/environment.md § Model Tier & Environment Mapping` pour la liste
> des alias et `§ /model alias rule` pour la règle de commande.

**Upgrade** (modèle actif sous-qualifié pour la complexité demandée) :

```
⏸️ Transition recommandée vers un modèle supérieur

Modèle actif : **{current_model}**
Modèle requis : **{target_model}**

Choix disponibles :
- Tape `/model {target_model}` puis `continue` pour basculer sur le modèle recommandé
- Tape `bypass` pour forcer l'exécution sur **{current_model}** (possible dégradation de l'efficacité)
```

**Downgrade** (modèle actif surqualifié — gaspillage de coût) :

```
⏸️ Retour recommandé vers un modèle standard

Modèle actif : **{current_model}**
Modèle requis : **{target_model}**

Choix disponibles :
- Tape `/model {target_model}` puis `continue` pour optimiser vos coûts/performances (recommandé)
- Tape `bypass` pour rester sur **{current_model}**
```

- Le tier **`light`** (Haiku / terra) est toujours en mismatch (cf. matrice) → toujours Cas 2 upgrade.

#### Point d'arrêt de bypass (uniquement en Cas 2)

- **Il s'agit d'un vrai point d'arrêt** : ne rien produire d'autre après le
  template, ne pas enchaîner sur le plan tant que l'utilisateur n'a pas répondu.
- Réponse **`bypass`** (ou équivalent explicite : « continue », « go ») →
  reprendre le workflow immédiatement sur le modèle actif. Le choix est assumé.
- Choix de **changer de modèle** → l'utilisateur utilise la commande de son
  IDE ; le changement prend effet à son **prochain message**, qui relance le
  workflow. Ne jamais prétendre avoir changé le modèle.

> **Limite technique.** Le skill ne peut pas exécuter la commande de changement
> de modèle : c'est une action IDE, aucun outil ne la déclenche. La branche
> « changer de modèle » est donc toujours **manuelle** (arrêt + consigne + attente).

### Re-jeu de la gate sur changement de modèle

Le modèle actif peut changer **en cours de session** (l'utilisateur lance
`/model opus`, `/model sonnet`…). Sans re-jeu, un mismatch introduit après la
première gate passerait inaperçu.

Règle, **sans état externe** :

1. À chaque exécution de la gate (Phase 1.5, entrée Phase 7, reprise),
   **mémoriser le modèle actif évalué** comme « dernier modèle évalué » de la
   session.
2. À **chaque nouvelle entrée de gate**, comparer le modèle actif au dernier
   modèle évalué :
   - **Identique** → appliquer les règles de re-jeu propres à la phase
     (Phase 1.5 : jouée une fois ; Phase 3 : seulement si le cadrage a changé
     la classe de complexité ; entrée Phase 7 : jouée une fois par séquence).
   - **Différent** → **toujours rejouer la gate immédiatement** (Cas 1 silencieux /
     Cas 2 `⚠️` + point d'arrêt de bypass), quel que soit l'état de re-jeu de la
     phase. Le changement de modèle prime sur les conditions de re-jeu
     habituelles. Mettre ensuite à jour le dernier modèle évalué.
3. Si le modèle actif n'est pas détectable, il n'y a pas de comparaison
   possible : ne pas afficher de gate (comportement inchangé).

> La comparaison porte sur le **modèle** (donc son tier résolu), pas sur la
> complexité : un passage `opus → sonnet` alors que les étapes restantes sont
> `standard` fait disparaître un mismatch (Cas 2 → Cas 1) tout autant qu'un
> passage inverse en crée un.

### Tag d'étape

Chaque **étape d'implémentation** porte un tag compact en fin de ligne :
`(XS · standard → Sonnet)`, `(M · standard → Sonnet)`, `(L · reasoning → Opus)`…

Format : `(taille · tier → modèle)` — taille selon la grille, tier selon la
matrice, modèle résolu au moment de la création depuis le mapping de
`references/environment.md`. Les étapes `🧪 Tests` et `✅ Validation` ne portent
**jamais** de tag (obligatoires et systématiques, non sizées).

---

## Grilling adaptatif (section canonique)

Le **grilling** est un interrogatoire ciblé qui stress-teste la réflexion de
l'utilisateur avant une décision structurante. Il est **réutilisé** par les
Phases 2, 4 et 6, chacune avec ses propres **catégories d'amorçage** (définies
dans la phase). Cette section définit son déclencheur, sa mécanique et son
format — les phases n'en répètent que les catégories.

### Déclencheur : complexité globale

En **Phase 2**, le grilling s'active pour **toutes les complexités** (XS, S, M,
L, XL). En Phases 4 et 6, il reste réservé aux plans `L`/`XL` (comportement
inchangé). Aucune nouvelle évaluation : on réutilise la complexité déjà établie
en Phase 1.

### Toggle de configuration

Lire `grilling.enabled` dans `./doc/roadmap/.skill-config.yml` :

| Valeur | Effet |
|---|---|
| absente / `true` | Grilling actif (défaut) |
| `false` | Grilling désactivé dans les Phases 4 et 6 — **sans effet sur la Phase 2** |

> ⚠️ La Phase 2 ignore `grilling.enabled` : le grilling y est **toujours actif**,
> quelle que soit la valeur de ce champ.

### Mécanique : frontier réduite

Le grilling se déroule en **rounds**, mappé comme un arbre de décision : chaque
décision tranchée ouvre les questions qui en dépendaient. Contrairement à un
grilling exhaustif, la profondeur est **bornée (« frontier réduite »)** :

1. **Round d'amorçage** : poser en un seul round toutes les **catégories
   pré-amorcées de la phase** dont les prérequis sont déjà connus. Chaque
   question est numérotée et accompagnée de ta **réponse recommandée**.
2. **Round de suivi (max 1)** : uniquement si des réponses du round d'amorçage
   ouvrent des zones d'ombre évidentes. Poser ces questions de suivi, puis
   **stop**.
3. **Fin** : le grilling s'arrête dès que les catégories sont couvertes + le
   round de suivi éventuel est traité. Ne pas dériver vers la conception
   d'architecture profonde — le grilling **cadre**, il ne conçoit pas.

Les catégories peuvent être surchargées par phase via
`grilling.categories.phase2 | phase4 | phase6` dans `.skill-config.yml` (voir
`references/environment.md § Grilling`). À défaut, utiliser les catégories par
défaut définies dans la phase.

### Format d'un round

```
❓ **Q1** — **<titre>** : <corps, éventuellement à choix multiples>

➡️ <ta réponse recommandée>

---

❓ **Q2** — **<titre>** : <corps>

➡️ <ta réponse recommandée>
```

**STOP** après chaque round, attendre les réponses de l'utilisateur avant le
suivant.

### Trouver les faits soi-même

Les **faits** (contenu de fichiers, état du dépôt, configuration) sont à
récupérer par tes propres outils, jamais demandés à l'utilisateur. Seules les
**décisions** lui sont posées. Une question dont la réponse dépend d'un fait non
encore établi attend que le fait soit récupéré.

---

## Phase 3 — Proposition du plan

> 🧠 MODE PLAN — aucune écriture, aucune commande.

En intégrant les réponses de cadrage, propose la structure complète (sans
l'écrire).

**Re-check gate modèle (conditionnel).** La gate a déjà été jouée en Phase 1.5.
Ne la **re-déclencher ici que si** le cadrage (Phase 2) a fait **changer la
classe de complexité globale** — donc le modèle recommandé — par rapport à
l'estimation pressentie. Dans ce cas, rejouer la gate (Cas 1 `ℹ️` / Cas 2 `⚠️`
+ point d'arrêt de bypass) selon la section canonique. Sinon, **ne pas la
répéter** et enchaîner directement sur le plan.

Présenter le plan (chaque étape d'implémentation portant son tag
`(taille · modèle)`) :

```
### 📝 Plan proposé (🧠 MODE PLAN — rien n'est encore écrit)

**Issue** : Créer `#XX — Titre` ou rattacher à `#YY` (son numéro = ID du plan)
  *(mode `github`)* — ou : **ID local** calculé en Phase 5, pas d'issue GitHub *(mode `local`)*
**Fichier** : `{ISSUE-ou-ID}-nom-du-plan.md`
**Priorité** : high | **Complexité** : L

**Objectif** : ...
**Périmètre** : Inclus / Hors scope
**Étapes** :
1. Extraire les métriques (XS · standard → Sonnet)
2. Implémenter le DAG de dépendances inter-plans (L · reasoning → Opus)
3. Ajouter les endpoints REST (M · standard → Sonnet)
4. 🧪 Tests — Rédiger et exécuter la procédure de test
5. ✅ Validation — Vérifier les résultats et clôturer
**Lots** (si applicable) : Lot 1 (étapes 1-3) … Lot 2 (étapes 4-6) …

---
⏸️ POINT D'ARRÊT 1 — Valides-tu cette proposition ? (oui / modifier / questions / annuler)
```

> Les deux dernières étapes `🧪 Tests` et `✅ Validation` sont **obligatoires** et
> doivent **toujours** figurer dans la proposition, quel que soit le nombre
> d'étapes d'implémentation. Elles sont non supprimables, non fusionnables, et
> ne portent **pas** de tag `(taille · modèle)`.
>
> Chaque étape d'implémentation reçoit une évaluation de complexité **propre**
> (indépendante de la complexité globale du plan) et son tag compact en fin de
> ligne. Garder les descriptions courtes : le tag ne doit pas les alourdir.

**STOP.** Attendre validation.

## Phase 4 — Validation de la proposition

### Grilling avant la gate (plans complexes)

Pour un plan `L`/`XL` avec grilling actif (voir « Grilling adaptatif »), mener
un grilling **avant** d'afficher la gate ci-dessous. Catégories d'amorçage par
défaut : **complétude des exigences couvertes**, **faisabilité des étapes**,
**risques non adressés dans le plan**, **cohérence du séquencement des étapes**.

Le grilling **ne remplace pas** la gate : il la prépare. À l'issue, produire une
**recommandation explicite** avant d'afficher la table (ex. : « 2 blocages
identifiés — recommande de retourner en Phase 2 avant de valider », ou « aucun
blocage — la proposition tient »). L'utilisateur garde le dernier mot via la gate.

Plan `XS`/`S`/`M`, ou `grilling.enabled: false` → afficher directement la gate.

| Réponse | Action |
|---|---|
| « oui » / « go » / « valide » | Phase 5 — **création du plan/issue/roadmap UNIQUEMENT** |
| « modifier » + corrections | Rester en phase 3, réajuster |
| « questions » | Revenir en phase 2 si nouvelles zones d'ombre |
| « annuler » | Abandonner |

> ⚠️ « oui » = autorisation de CRÉER LE PLAN, pas d'implémenter.

## Compatibilité avec le mode plan

Les phases 1→4 sont en lecture seule et se déroulent normalement en mode plan.
La phase 5 est la première à mutier le dépôt (plan file, issue, roadmap).

**Claude Code** : utiliser l'action « Exit plan mode » (`ExitPlanMode` tool)
avec le plan validé comme contenu d'approbation. Le point d'arrêt `⏸️` de la
phase 4 et l'approbation `ExitPlanMode` ne font alors qu'un seul gate.

**Autres IDE** : voir `references/environment.md § Generic Action Mapping` pour
l'équivalent « Exit plan mode » dans ton environnement.

Ne jamais tenter de `Write`/`gh`/`git` tant que le mode plan est actif.
