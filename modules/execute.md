# Module : Exécution (Phases 5 à 7)

> **Chargé en Phases 5 à 7** — création du plan/issue/roadmap, validation avant
> implémentation, implémentation étape par étape, tests intermédiaires, étapes
> obligatoires 🧪 Tests et ✅ Validation, format de commit. La checklist de
> clôture est dans `modules/wrapup.md`.

---

## Phase 5 — Act limité (création du plan)

> 🔨 MODE ACT (PLAN) — écriture LIMITÉE au plan, à l'issue et au roadmap.

**UNIQUEMENT et dans cet ordre** — deux branches selon le mode `issues` détecté :

> **Détection préalable de `issues.mode` (obligatoire avant de choisir la branche).**
> Exécuter la procédure de détection définie dans `references/environment.md § Skill Configuration Schema` :
> `.git/` présent **et** remote GitHub **et** `gh auth status` réussit → mode `github` ;
> sinon → mode `local`. **Ne jamais choisir `local` par défaut sans avoir vérifié.**
> Si `.skill-config.yml` contient `issues.mode: github` ou `issues.mode: local`, utiliser
> cette valeur directement sans relancer la détection.

#### Mode `github`

0. **Prérequis** : s'assurer que `./doc/roadmap/` existe (`mkdir -p ./doc/roadmap`) ; si `./doc/roadmap/roadmap.md` est absent, l'initialiser depuis `references/roadmap-file.md`.
1. Créer ou rattacher l'issue GitHub, récupérer son **numéro** (voir `references/github-issues.md`).
2. Créer `./doc/roadmap/{ISSUE}-nom-du-plan.md` avec ce numéro comme ID (voir `references/templates.md`).
3. **Mettre à jour l'issue** : ajouter `Plan: doc/roadmap/{ISSUE}-nom-du-plan.md` au début du corps de l'issue (voir `references/github-issues.md`).
4. Mettre à jour `./doc/roadmap/roadmap.md` avec `[Issue: #NN]` (voir `references/roadmap-file.md`).

> Si aucune issue ne peut être créée maintenant, utiliser le fallback
> `draft-nom.md` décrit dans `references/templates.md`, à renommer plus tard.

#### Mode `local`

0. **Prérequis** : s'assurer que `./doc/roadmap/` existe (`mkdir -p ./doc/roadmap`) ; si `./doc/roadmap/roadmap.md` est absent, l'initialiser depuis `references/roadmap-file.md`.
1. Calculer l'**ID local** = `max(ensemble des IDs déjà pris) + 1` (entier nu, ex. `5`), où l'ensemble réunit **à la fois** les préfixes numériques des noms de fichiers `./doc/roadmap/*.md` **et** les `plan.id` déclarés dans leur front matter. Prendre l'union des deux évite qu'un plan sans préfixe de fichier (mais avec un `plan.id` en front matter) provoque une collision d'ID. Si aucun plan existant : commencer à `1`.
2. Créer `./doc/roadmap/{ID}-nom-du-plan.md` avec `plan.source: local` dans le front matter et `issue.id: null` / `issue.url: null` (voir `references/templates.md`).
3. Mettre à jour `./doc/roadmap/roadmap.md` avec `[Plan: {id}]` au lieu de `[Issue: #NN]` (voir `references/roadmap-file.md`).

> Pas de verrou distribué sur la numérotation locale : deux créations simultanées
> → collision de nom de fichier / conflit `roadmap.md` résolus par git au merge.
> Documenté comme tel, pas masqué.

**Interdit ici :** lire/modifier/créer du code source, lancer build/test/install,
réfléchir à l'implémentation, proposer du code.

Puis confirme et pose le point d'arrêt :

```
### ✅ Plan créé (🔨 MODE ACT — exécuté)

- 📄 Fichier créé : `./doc/roadmap/{ISSUE-ou-ID}-nom-du-plan.md`
- 🔗 Issue GitHub : #XX (créée / mise à jour / manuel) *(mode github)* — ou : ❌ Local (ID {n}) *(mode local)*
- 📋 roadmap.md : mis à jour
- 📊 Complexity : {taille} · {tier} → {modèle}

---
⏸️ POINT D'ARRÊT 2 — Le plan est créé. Que souhaites-tu faire ?
1. 🚀 Commencer l'implémentation — je démarre l'étape 1
2. ⚡ Commencer l'implémentation — démarrer toutes les étapes en one-shot
3. 📝 Modifier le plan
4. 🛑 Arrêter ici

---

💾 Tout le contexte du plan courant est sauvegardé dans {INTRO_FICHIERS} :
- `{PLAN_COURANT}` (plan courant)
{PLANS_LIES}
ℹ️ Tu peux exécuter `/clear`, puis coller le message ci-dessous dans la nouvelle
   conversation pour repartir sur une session neuve — rien ne sera perdu.

> Reprends le plan `{PLAN_COURANT}`.
```

> **Variables du bloc ci-dessus :** `{PLAN_COURANT}` = valeur de `plan.name` du front matter. `{INTRO_FICHIERS}` = `le fichier plan` si aucun plan lié, `les fichiers plans` sinon. `{PLANS_LIES}` = une ligne `- \`#YYY-slug.md\`` par plan référencé dans les champs `blocks` / `blockedBy` / `depends_on` du front matter (ligne absente si aucun lien).

> **Fast-path (plans XS/S/M)** : choisir 1 ou 2 démarre directement la **Phase 7** —
> Phase 6 supprimée. Le POINT D'ARRÊT 2 sert de double validation création + implémentation.
>
> **Plans L/XL** : choisir 1 ou 2 déclenche d'abord la **Phase 6** (grilling risques
> d'implémentation + gate binaire) avant de passer à la Phase 7.

**STOP.** Attendre la réponse.

## Phase 6 — Validation avant implémentation *(plans L/XL uniquement)*

> **Fast-path (plans XS/S/M)** : si l'utilisateur a choisi « Commencer
> l'implémentation » (option 1 ou 2) au POINT D'ARRÊT 2 de la Phase 5, la
> Phase 6 est **supprimée** — passer directement à la Phase 7. La confirmation
> Phase 5 sert de validation création + implémentation.
>
> Phase 6 s'applique uniquement aux plans **L/XL**, ou lorsque l'utilisateur
> a choisi « Modifier le plan » puis relancé l'implémentation.

### Grilling avant la gate (plans complexes)

Pour un plan `L`/`XL` avec grilling actif (voir « Grilling adaptatif » dans `modules/plan.md`), mener
un grilling **avant** d'afficher la gate ci-dessous. Catégories d'amorçage par
défaut : **risques d'implémentation**, **couverture des tests prévus**, **plan
de rollback**, **impacts sur les features existantes**.

Comme en Phase 4, le grilling **prépare** la gate sans la remplacer : conclure
par une **recommandation explicite** (ex. : « 1 blocage identifié — recommande
de revoir le plan avant d'implémenter ») avant d'afficher la table. L'utilisateur
garde le dernier mot.

Plan `XS`/`S`/`M`, ou `grilling.enabled: false` → afficher directement la gate.

| Réponse | Action |
|---|---|
| « 1 » / « implémenter » / « go » | Phase 7 |
| « 2 » / « modifier » | Revenir au plan |
| « 3 » / « stop » | Fin de session |

> ⚠️ Seule une réponse explicite à ce point d'arrêt autorise l'implémentation.

Afficher également (après le tableau) :

```
---

💾 Tout le contexte du plan courant est sauvegardé dans {INTRO_FICHIERS} :
- `{PLAN_COURANT}` (plan courant)
{PLANS_LIES}
ℹ️ Tu peux exécuter `/clear`, puis coller le message ci-dessous dans la nouvelle
   conversation pour repartir sur une session neuve — rien ne sera perdu.

> Reprends le plan `{PLAN_COURANT}` — j'ai validé la proposition, on passe à l'implémentation.
```

> (Variables : voir note § Phase 5 POINT D'ARRÊT 2.)

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
  *(Exception fast-track : ⏸️ supprimé — voir § « Mode fast-track » ci-dessous.)*
- [ ] L'étape 0 ci-dessous va être exécutée MAINTENANT (ou a déjà été exécutée
  dans cette session pour ce même ensemble d'étapes).
  *(Exception fast-track : étape 0 supprimée — voir § « Mode fast-track » ci-dessous.)*

### Mode fast-track (XS/S-solo)

Si la matrice Axe A a résolu en « Fast-track Phase 7 » (complexité XS, ou S +
`collaborative: false`, en `mode: auto`) :

```
FAST-TRACK — RÈGLES D'ENTRÉE PHASE 7

- SKIP : ⏸️ pré-implémentation (checklist ci-dessus : exception appliquée).
- SKIP : § « Proposition du mode de tests » (ne pas lire ni poser la question).
- SKIP : étape 0 (sélection des tests intermédiaires).
- SKIP : tous les ⏸️ intermédiaires de Phase 7.
- Gate modèle : appliquer normalement (§ ci-dessous).
- Commit unique (📦) proposé en fin d'implémentation.
- ✅ Validation one-shot en fin (pas de boucle).
```

Passer directement à la gate modèle, puis à l'étape 1.

---

### Gate modèle d'entrée (groupée, une seule fois par séquence)

À l'entrée de la Phase 7, **avant l'étape 0**, vérifier une seule fois
l'alignement du modèle sur la **séquence d'étapes demandée** (pas étape par
étape) :

1. Parmi les **étapes d'implémentation** à exécuter (exclure `🧪 Tests` et
   `✅ Validation`), retenir le **tier le plus exigeant** d'après leurs tags
   `(taille · tier → modèle)` — `reasoning` prime sur `standard`.
2. Comparer au tier du modèle actif (voir « Détection du modèle actif et de son
   tier »).
3. Appliquer la gate selon la section canonique « Gate de recommandation de
   modèle » (avec « Détection du modèle actif » et « Re-jeu de la gate » —
   toutes dans `modules/plan.md`), **symétrie stricte** (mismatch dans les deux sens) :
   - **Adapté** (tier actif = tier requis par la séquence) → **continuer
     silencieusement** vers l'étape 0. *(Fast-path : aucun affichage pour Cas 1.)*
   - **Sous-dimensionné** (au moins une étape exige `reasoning` alors que le tier
     actif est `standard` ou `light`) → bloc `⚠️` nommant les étapes concernées,
     recommander un modèle `reasoning` (voir `references/environment.md §
     Generic Action Mapping`).
   - **Surdimensionné** (séquence entièrement `standard` alors que le tier actif
     est `reasoning`) → bloc `⚠️`, recommander un modèle `standard` (surqualifié
     = gaspillage).
   - Dans les deux cas de mismatch → **point d'arrêt de bypass `⏸️`** : attendre
     `bypass` (continuer sur le modèle actif) ou un switch manuel via la commande
     IDE puis relance avec `continue`. Ne pas entamer l'étape 0 tant que l'utilisateur n'a pas
     répondu.

> Une seule gate pour toute la séquence : ne pas la rejouer à chaque étape. Si
> le plan est antérieur aux tags par étape, s'appuyer sur la complexité globale.
> Si le modèle actif n'est pas détectable, ne pas afficher de gate.
>
> **Exception — changement de modèle.** Si le modèle actif diffère du dernier
> modèle évalué (l'utilisateur a changé de modèle depuis la dernière gate),
> rejouer la gate même à l'intérieur d'une séquence déjà entamée (voir « Re-jeu
> de la gate sur changement de modèle »).

### Proposition du mode de tests (entrée Phase 7, avant l'étape 0)

À l'entrée de la Phase 7, **après la gate modèle et avant l'étape 0**, résoudre
le mode de tests :

1. **Lire `tests.mode` dans `./doc/roadmap/.skill-config.yml`.**
   - **Fixé** (`manual` ou `autonomous`) → l'utiliser tel quel, ne rien
     proposer. Passer à la suite (étape 0 en `manual`, étape 1 en `autonomous`).
   - **Non fixé** (clé absente, fichier absent, ou `tests.mode: null`) →
     **proposer** (étape 2 ci-dessous).

2. **Proposer via `AskUserQuestion`** (une seule fois) :
   « L'environnement de test de ce projet est-il directement accessible depuis cet IDE ? » — 2 options :
   - **Non → tests en mode `Manuel`** : je te propose les procédures de test, tu les exécutes et me transmets les résultats. (`manual`)
   - **Oui → tests en mode `Autonome`** : un agent vérificateur indépendant (si disponible) exécute et vérifie les tests après chaque étape. (`autonomous`)

3. **Persister le choix** dans `./doc/roadmap/.skill-config.yml` sous
   `tests.mode` (créer le fichier et la clé `tests:` s'ils sont absents, sans
   écraser les autres clés). L'opérateur n'est plus resollicité aux sessions
   suivantes. **Après écriture, afficher** :
   > ✅ Mode de tests `<manual|autonomous>` enregistré dans
   > `./doc/roadmap/.skill-config.yml`.
   > Pour réinitialiser : supprime la clé `tests.mode` dans ce fichier
   > (ou supprime le fichier entièrement) — le choix te sera reproposé à la
   > prochaine session.

4. **Enchaîner selon le mode retenu** : `manual` → étape 0 ; `autonomous` →
   étape 1 directement (l'étape 0 est supprimée, voir `references/autonomous-tests.md`).

> **Signal de proposition = « config non fixée », pas « accès shell détecté ».**
> L'accès Bash étant quasi toujours présent en Claude Code, se baser sur lui
> reproposerait à chaque session. « `tests.mode` non fixé » est un signal stable
> et non redondant : proposé une fois, persisté, jamais reposé.

---

0. **Sélection des tests intermédiaires (avant de commencer la 1ʳᵉ étape).**

   > **Mode `autonomous`** : cette étape 0 est **supprimée** — tous les tests
   > s'exécutent après chaque étape automatiquement via la boucle
   > Exécuteur/Vérificateur. Passer directement à l'étape 1.
   > *(Fast-path : aucune question de sélection, aucun tour supplémentaire.)*
   > Voir `references/autonomous-tests.md`.

   > **Mode one-shot** (option ⚡ choisie au POINT D'ARRÊT 2 ou au point d'arrêt
   > de reprise) : cette étape 0 est **supprimée** — aucun test intermédiaire,
   > enchaîner directement l'étape 1. Les étapes `🧪 Tests` et `✅ Validation`
   > finales restent obligatoires.

   **Mode `manual`** (défaut) : quand l'opérateur demande l'implémentation
   d'une ou plusieurs étapes (« Démarre l'étape 3 », « Exécute les étapes 1 et
   4 », « Enchaîne les étapes 3 à 7 », voire une seule étape) :
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
3. À la fin de chaque étape d'implémentation :

   **Mode `manual`** — selon la sélection de l'étape 0 :
   - **Non sélectionnée** → `✅ Étape X terminée.` et enchaîner directement
     l'étape suivante, sans attendre de retour.
   - **Sélectionnée** → dérouler la **procédure de tests unitaires
     intermédiaires** (voir ci-dessous) incluant le **bloc `📦 Commit proposé`**
     obligatoire, **STOP** en attente des résultats, puis
     `✅ Étape X terminée et validée.` une fois les tests passés.

   **Mode `autonomous`** → déclencher la **boucle Exécuteur/Vérificateur** définie
   dans `references/autonomous-tests.md`. Le `📦 Commit proposé` et le `⏸️` ne
   s'affichent qu'après un verdict `PASS`.
4. Une fois les étapes d'implémentation (1 à N-2) terminées, dérouler
   **obligatoirement** l'étape `🧪 Tests` puis l'étape `✅ Validation` (voir
   ci-dessous). Ces deux étapes ne sont **jamais** optionnelles, que des tests
   intermédiaires aient eu lieu ou non.
5. En fin de session, mettre à jour : journal de session du plan, issue GitHub,
   `roadmap.md` si nécessaire.

> **Clôture d'un plan validé.** Dès que toutes les étapes sont livrées ET
> validées, dérouler la **checklist de clôture COMPLÈTE** —
> voir `modules/wrapup.md § Clôture d'un plan validé` (plan `status: done`,
> `roadmap.md`, issue GitHub). Ne rien omettre.

## Tests unitaires intermédiaires (optionnels, par étape)

> **Mode `autonomous`** : cette section ne s'applique pas. La boucle
> Exécuteur/Vérificateur de `references/autonomous-tests.md` prend le relais.

**Mode `manual`** (défaut) : ne s'applique qu'aux étapes **sélectionnées** à
l'étape 0 de la Phase 7. À la fin de l'implémentation d'une étape sélectionnée :

1. **Déterminer les tests unitaires pertinents** ciblés sur le périmètre de
   **cette étape uniquement**.

> ⛔ **Règle zero-lookup — `### Prérequis pour les tests` obligatoire avant toute procédure.**
> Créer ou mettre à jour la section `### Prérequis pour les tests` dans `## Tests`
> du fichier plan **avant** d'écrire `### Procédure de test` (voir
> `references/templates.md`). Elle doit contenir toutes les valeurs, chemins
> absolus, variables d'environnement et commandes de setup nécessaires à
> l'exécution — copier-coller direct sans recherche manuelle (zero-lookup).
>
> **Heuristique** : avant d'écrire `### Prérequis pour les tests`, lister d'abord
> toutes les commandes de la procédure et relever chaque valeur non dérivable
> de l'environnement standard (chemins absolus, IDs, ports, noms de services).
> Ces valeurs sont exactement ce qui doit figurer dans les prérequis.

2. **Rédiger une procédure de tests unitaires détaillée pas à pas** dans la
   section `## Tests` du fichier plan (voir `references/templates.md`), entre
   balises de code. Cette procédure :
   - Respecte **intégralement** les règles de formatage des commandes
     (voir `references/environment.md § Operator Commands Formatting`).
   - Inclut les commandes de vérification des résultats attendus.
   - Précise les **résultats attendus** pour chaque vérification.

3. **Écrire d'abord la procédure dans la section `## Tests` du fichier plan**
   (appel outil Edit/Write — OBLIGATOIRE avant tout affichage dans le chat),
   puis dans le chat afficher **uniquement une référence et le commit proposé**
   — les deux blocs sont **indissociables** :

   ```
   ### 🧪 Tests intermédiaires — Étape X/N

   **Procédure :** → voir section `## Tests` de `NNN-slug.md` (écrite à l'instant).

   **Résultats attendus :** <résumé bref — détail dans la section `## Tests` du plan>

   ---

   📦 Commit (→ voir section « Commit d'implémentation pré-tests (référence de format) », step X).

   ---

   ⏸️ Commit, push si nécessaire, puis exécute la procédure de tests
   dans l'environnement cible et transmets-moi les résultats complets.
   J'attends tes retours avant de passer à l'étape suivante.

   ---

   💾 Tout le contexte du plan courant est sauvegardé dans {INTRO_FICHIERS} :
   - `{PLAN_COURANT}` (plan courant)
   {PLANS_LIES}
   ℹ️ Tu peux exécuter `/clear`, puis coller le message ci-dessous dans la nouvelle
      conversation pour repartir sur une session neuve — rien ne sera perdu.

   > Reprends le plan `{PLAN_COURANT}` — voici les résultats des tests intermédiaires de l'étape {X} :
   ```

4. **STOP.** Ne pas passer à l'étape suivante tant que les résultats ne sont pas
   reçus.

5. **Si les tests échouent** :
   1. Analyser les résultats transmis.
   2. **Mettre à jour la section `## Diagnostic en cours`** du fichier plan
      (voir `references/templates.md`) :
      - Ajouter les hypothèses éliminées par cette session.
      - Documenter les pistes ouvertes non encore vérifiées.
      - Lister les vérifications à jouer (commandes concrètes).
      - Mettre à jour le compteur de strikes dans le tableau des blocs en échec.
      Si la section n'existe pas encore, la créer à la volée.
   3. Corriger l'implémentation.
   4. **Vérifier la règle "2 strikes"** (voir « Règle d'escalade "2 strikes" »
      ci-dessous) avant de re-soumettre les tests.
   5. Régénérer la procédure de tests intermédiaires **et** un nouveau bloc
      `📦 Commit proposé` pour les corrections.
   6. Boucler jusqu'à validation de cette étape.

6. **Si les tests passent** : **consigner les résultats reçus dans la section
   `## Tests` du fichier plan** (ligne dans le tableau « Résultats joués et
   vérifiés » : date, test, attendu, observé, verdict), puis
   `✅ Étape X terminée et validée.` et enchaîner l'étape suivante.

> Ces tests intermédiaires **complètent** et ne remplacent **jamais** la phase
> finale `🧪 Tests` + `✅ Validation`, qui reste obligatoire et bloquante.

## Étape 🧪 Tests (avant-dernière étape — obligatoire)

> **Mode `autonomous`** : la boucle Exécuteur/Vérificateur a déjà tourné après
> chaque étape d'implémentation. Cette étape `🧪 Tests` reste **obligatoire** —
> elle correspond aux tests finaux E2E / non-régression, exécutés dans la même
> boucle mais sur l'ensemble du plan. Le `⏸️` se place après le `PASS` final.
> La procédure, les résultats attendus **et** les résultats vérifiés sont écrits
> dans la section `## Tests` du plan comme dans la boucle par étape. Voir
> `references/autonomous-tests.md`.

**Mode `manual`** (défaut) : démarre lorsque les étapes d'implémentation (1 à
N-2) sont terminées. Tu dois :

1. **Déterminer le type de tests requis** selon cette heuristique :
   - **Tests unitaires** → modification d'une fonction, d'un service ou d'un
     composant isolé.
   - **Tests end-to-end** → modification touchant un flux complet (API → front,
     inter-services, pipeline, etc.).
   - **Les deux** → modification structurelle majeure ou transverse.

> ⛔ **Règle zero-lookup — `### Prérequis pour les tests` obligatoire avant toute procédure.**
> Créer ou mettre à jour la section `### Prérequis pour les tests` dans `## Tests`
> du fichier plan **avant** d'écrire `### Procédure de test` (voir
> `references/templates.md`). Elle doit contenir toutes les valeurs, chemins
> absolus, variables d'environnement et commandes de setup nécessaires à
> l'exécution — copier-coller direct sans recherche manuelle (zero-lookup).

2. **Rédiger une procédure de test détaillée pas à pas** dans la section
   `## Tests` du fichier plan (voir `references/templates.md`), entre balises de
   code. Cette procédure :
   - Respecte **intégralement** les règles de formatage des commandes
     (voir `references/environment.md § Operator Commands Formatting`).
   - Inclut les commandes de vérification des résultats attendus (ex : `curl`,
     `grep`, `docker ps`, assertions visuelles, etc.).
   - Précise les **résultats attendus** pour chaque vérification (ce que
     l'opérateur doit observer si tout fonctionne).

3. **Écrire d'abord la procédure dans la section `## Tests` du fichier plan**
   (appel outil Edit/Write — OBLIGATOIRE avant tout affichage dans le chat),
   puis dans le chat afficher **uniquement une référence et le commit proposé**
   — les deux blocs sont **indissociables** :

   ```
   ### 🧪 Tests finaux

   **Procédure :** → voir section `## Tests` de `NNN-slug.md` (écrite à l'instant).

   **Résultats attendus :** <résumé bref — détail dans la section `## Tests` du plan>

   ---

   📦 Commit (→ voir section « Commit d'implémentation pré-tests (référence de format) »).

   ---

⏸️ Commit, push si nécessaire, puis exécute la procédure de tests
   dans l'environnement cible et transmets-moi les résultats complets.
   J'attends tes retours avant de passer à l'étape de validation.

   ---

   💾 Tout le contexte du plan courant est sauvegardé dans {INTRO_FICHIERS} :
   - `{PLAN_COURANT}` (plan courant)
   {PLANS_LIES}
   ℹ️ Tu peux exécuter `/clear`, puis coller le message ci-dessous dans la nouvelle
      conversation pour repartir sur une session neuve — rien ne sera perdu.

   > Reprends le plan `{PLAN_COURANT}` — voici les résultats des tests finaux :
   ```

   > Si **aucun fichier n'a été modifié** depuis le dernier commit (ex. : tests
   > finaux après un commit intermédiaire qui couvrait déjà tout), remplacer le
   > bloc `📦 Commit proposé` par :
   > `📦 Aucun commit nécessaire — aucun fichier modifié depuis le dernier commit.`

4. **STOP.** Ne pas passer à l'étape `✅ Validation` tant que les résultats ne
   sont pas reçus.

## Étape ✅ Validation (dernière étape — obligatoire)

> **Mode `autonomous`** : démarre après le `PASS` final de la boucle
> Exécuteur/Vérificateur sur les tests finaux. Le Vérificateur a déjà rendu son
> verdict — il a été **consigné dans la section `## Tests` du plan** par la
> boucle (voir `references/autonomous-tests.md`). Reprendre ces résultats
> persistés comme source de vérité pour la checklist de clôture ci-dessous.

**Mode `manual`** (défaut) : démarre **uniquement** lorsque l'opérateur a
transmis les résultats de l'étape `🧪 Tests`.

> **Avant toute clôture — consigner les résultats.** Écrire les résultats
> transmis par l'opérateur dans le tableau « Résultats joués et vérifiés » de la
> section `## Tests` du fichier plan (date, test, attendu, observé, verdict).
> C'est un prérequis de la règle « ⛔ traçabilité des tests dans le fichier
> plan » : sans cette consignation, la validation ne peut pas être clôturée.

- **Si tous les tests passent** → consigner les résultats (ci-dessus), cocher
  l'étape, puis enchaîner la checklist de clôture (plan `status: done`,
  `roadmap.md`, issue GitHub — voir ci-dessus).
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
  4. **Vérifier la règle "2 strikes"** (voir « Règle d'escalade \"2 strikes\" »
     ci-dessous) avant de re-soumettre les tests.
  5. **Revenir à l'étape `🧪 Tests`** : régénérer une procédure de test mise à
     jour (incluant les vérifications de non-régression si pertinent) **et** un
     nouveau bloc `📦 Commit proposé` pour les corrections.
  6. Boucler jusqu'à validation complète.

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
ET   le modèle actif est de tier standard (Sonnet ou Luna)
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
- La session avec modèle de tier `standard` (Sonnet ou Luna) a produit un diagnostic **sans preuve matérielle**
  (hypothèse formulée mais non vérifiée par inspection d'artefact runtime).
- Le plan consigne une piste pertinente non exploitée par les sessions
  précédentes (visible dans la section `## Diagnostic en cours`).
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