# Rapport d'Audit & Améliorations — roadmap-tracking
## Date : 2026-10-17
## Contexte : Projet de référence Auxitum (287 plans réels, IDs jusqu'à #359)

> Méthodologie : lecture intégrale de la codebase du skill ; cartographie
> Auxitum par listing/comptage/grep uniquement ; échantillon de 7 plans (ossature
> + front matter, pas le corps). Aucune lecture exhaustive des 287 plans.
> Les estimations tokens reposent sur l'heuristique ≈ 4 octets/token (voir §9.4).

---

## 1. Synthèse exécutive

Le skill est **mature et solidement conçu** : architecture modulaire à chargement
conditionnel, garde d'entrée renforcée par 3 hooks, désengagement auto selon
complexité, mode local/github, tests autonomes. La robustesse *comportementale*
(anti-bypass, traçabilité) est excellente.

**Le vrai risque de scalabilité n'est pas le workflow — c'est l'hydratation de
session.** Sur Auxitum, deux fichiers sont lus quasi intégralement à **chaque
démarrage** : `roadmap.md` (**194 Ko ≈ 49 600 tokens**) et `CONTEXT.md`
(**81 Ko ≈ 20 800 tokens**), soit **~70 000 tokens de coût fixe par session,
avant toute action utile**. Ce coût croît linéairement avec le nombre de plans
et ne sera pas tenable à 500/1000 plans.

Les 3 propositions utilisateur attaquent les bons symptômes mais **une partie est
déjà implémentée** (sous-dossier `done/`, exclusion du listing — plan #25) et
**certaines aggraveraient le coût** (multiplication de dossiers = churn de `git mv`
+ réécriture de liens à chaque transition de statut).

Le levier à plus fort impact est unique et transversal aux 3 propositions :
**faire de `roadmap.md` un artefact GÉNÉRÉ depuis le front matter des plans, et
faire lire au skill un index compact (~3-5 Ko) plutôt que le fichier narratif
complet.** Gain estimé : **~60 000 tokens/session** (de ~70 K à ~10 K), tout en
supprimant la dérive d'intégrité (8 plans mal placés détectés, vocabulaire de
statut divergent).

Priorités : **P1** = index généré + listing paresseux + validation d'intégrité ;
**P2** = segmentation `CONTEXT.md` avec budget ; **P3** = capitalisation auto
encadrée.

---

## 2. Analyse de la codebase

### 2.1 Architecture actuelle

Structure (lecture complète, volume ~14 700 lignes dont la moitié = plans de la
roadmap interne du skill lui-même) :

| Zone | Fichiers | Rôle |
|---|---|---|
| **Point d'entrée** | `SKILL.md` (254 l.) | Front matter, règles absolues, résumé des 7 phases, hydratation CONTEXT |
| **Modules workflow** | `modules/{init-scan,plan,execute,wrapup}.md` (426/416/659/158) | Chargement conditionnel par phase |
| **Références** | `references/*.md` (7 fichiers) | environment, templates, roadmap-file, forms, github-issues, migration, autonomous-tests — chargés à la demande |
| **Hooks** | `hooks/{hooks.json,pretooluse_gate.py,codex-hooks.json}` | SessionStart + UserPromptSubmit (texte) + PreToolUse (deny one-shot) |
| **Scripts** | `scripts/{migrate_plan_ids.py (528 l.),e2e_fresh_install_setup.sh}` | Migration ID + setup tests E2E |
| **Config** | `.skill-config.yml` | ide / models / issues / tests / grilling / roadmap-tracking |

**Flux d'exécution** : SessionStart (hook texte) → invocation skill → lire
`environment.md` → charger `init-scan.md` (garde d'entrée) → lire `CONTEXT.md` →
Phase 1 (analyse+calibrage) → 1.5 (gate modèle) → 2 (cadrage/grilling) → 3
(proposition) → 4 (⏸️) → 5 (création plan, ⏸️) → 6 (L/XL only) → 7 (implémentation
+ 🧪 Tests + ✅ Validation). Fast-path XS/S/M : −2 tours.

### 2.2 Forces identifiées

| # | Force | Preuve |
|---|---|---|
| 1 | **Modularité à chargement conditionnel** | `SKILL.md` ne charge jamais >1 module hors Phase 1 — limite le contexte résident |
| 2 | **Garde d'entrée défense-en-profondeur** | 3 couches : texte SessionStart + rappel UserPromptSubmit + `PreToolUse` deny mécanique one-shot auto-désarmant (`pretooluse_gate.py`) |
| 3 | **Désengagement auto (Axe A)** | Matrice complexité × collaboratif → le skill se retire sur XS/S-solo, évite le surcoût sur tâches triviales |
| 4 | **Rétrocompatibilité totale** | Config entièrement optionnelle ; défauts = comportement v1.3.x |
| 5 | **Mode local sans `gh`** | ID compteur = max(fichiers ∪ front matter)+1 — portable |
| 6 | **Traçabilité forte** | Règle ⛔ « tests écrits dans le plan AVANT le chat », clôture 4-supports, correction proactive d'incohérences |
| 7 | **`done/` déjà en place** | `init-scan.md` exclut `done/` du listing (plan #25) — proposition A partiellement anticipée |
| 8 | **Fail-open systématique** | `pretooluse_gate.py` ne bloque jamais le travail sur erreur |

### 2.3 Faiblesses et dettes techniques

| # | Faiblesse | Gravité | Preuve concrète |
|---|---|---|---|
| F1 | **`roadmap.md` hand-maintenu, non généré** | 🔴 Élevée | 1137 lignes, sync manuelle → dérive garantie à l'échelle |
| F2 | **Pas d'index machine-lisible** | 🔴 Élevée | Lister les plans = parser 194 Ko de narratif, ou lire 69 front matter |
| F3 | **Vocabulaire de statut divergent de la réalité** | 🟠 Moyenne | `roadmap-file.md` définit `active/done/blocked/archived` ; Auxitum utilise aussi `in-progress` (×2) et `cancelled` (×1) — non reconnus par la correction proactive |
| F4 | **Dérive d'intégrité non détectée** | 🟠 Moyenne | 8 plans en racine avec statut terminal/non-standard ; 2 `archived` sans `_archives/` (dossier inexistant) ; 3 `done` jamais déplacés |
| F5 | **`CONTEXT.md` sans borne** | 🟠 Moyenne | Déjà 1243 lignes / 81 Ko, lu intégralement à chaque session |
| F6 | **Aucune commande de validation/santé** | 🟠 Moyenne | F3/F4 ne seraient jamais remontés sans un `doctor` |
| F7 | **Pas d'observabilité portfolio** | 🟡 Faible | Aucune vue stats sans lecture de plans (ce rapport a dû la reconstruire par grep) |

### 2.4 Analyse du coût token par opération du skill

| Opération | Mécanisme | Coût token estimé | Scalabilité |
|---|---|---|---|
| **Hydratation CONTEXT.md** | Lecture intégrale au démarrage | ~20 800 tok (Auxitum) | ❌ croît sans borne |
| **Listing des plans** | Lecture `roadmap.md` + inspection `doc/roadmap/` | ~49 600 tok si `roadmap.md` lu en entier | ❌ linéaire en nb plans |
| **Chargement d'un module** | 1 module ciblé | ~1 500-2 600 tok | ✅ constant |
| **Chargement d'une référence** | À la demande | ~800-1 500 tok | ✅ constant |
| **Lecture d'un plan repris** | 1 plan (médiane 6,5 Ko) | ~1 600 tok (max 58 Ko ≈ 14 500 tok pour `30-saas-v2`) | 🟡 dépend du plan |

> **Constat central** : les deux premières lignes (hydratation + listing) dominent
> et sont **toutes deux proportionnelles au volume**. Tout le reste est borné par
> la modularité. **C'est là, et seulement là, que se joue la scalabilité.**

---

## 3. Analyse de l'utilisation réelle (Auxitum)

### 3.1 Arborescence et volumétrie

```
doc/roadmap/
├── roadmap.md          194 Ko · 1137 lignes
├── CONTEXT.md           81 Ko · 1243 lignes
├── .skill-config.yml  (collaborative:false, mode:auto, tests:manual)
├── <69 plans actifs>.md  609 Ko (médiane 6,5 Ko, moy 9 Ko, max 58 Ko)
└── done/
    └── <216 plans>.md   ~1,1 Mo
```

- **287 fichiers plan** (71 racine / 216 `done/`), IDs jusqu'à #359.
- **Pas de `_archives/`** alors que 2 plans portent `status: archived`.
- Taille totale `doc/roadmap/` : **3,7 Mo**.

### 3.2 Répartition statistique par statut

Front matter des 69 plans racine (hors roadmap/CONTEXT) :

| Statut | Nb | Dans l'enum officiel ? | Observation |
|---|---|---|---|
| `active` | 52 | ✅ | Nominal |
| `blocked` | 9 | ✅ | Nominal |
| `in-progress` | 2 | ❌ | Hors vocabulaire — non géré par la correction proactive |
| `done` | 3 | ✅ mais **mal placé** (devrait être dans `done/`) | Dérive de clôture |
| `archived` | 2 | ✅ mais **sans destination** (`_archives/` absent) | Dérive |
| `cancelled` | 1 | ❌ | Hors vocabulaire |

Complexité (racine) : L=20, M=25, S=17, XL=4, XS=3.
Priorité : high=27, medium=34, low=8.

Dans `roadmap.md` : 83 entrées `###`, 160 `[Issue:`, **209 liens `done/`**,
194 icônes 🔵 (done) vs 58 🟢 (actif) vs 13 🔴 (bloqué).

### 3.3 Patterns d'usage observés

- **Deux générations de plans coexistent** : plans récents (`123`, `200`, `287`,
  `354`) conformes au template (`## Objectif / Périmètre / Étapes / Décisions /
  Tests / Journal`) ; plans legacy massifs (`30-saas-v2` = mini-roadmap avec
  releases/wireframes, `14-UI-UX` = 401 lignes multi-lots) antérieurs au template.
  Le skill tolère les deux (branche « plan non conforme »), ce qui est une force.
- **`roadmap.md` tient un rôle double** : backlog `À faire` (lignes 196-911) **et**
  historique `Fait` (912-1137) **et** une table « chemin critique » en tête
  (1-195) mêlant actif et done. C'est trois artefacts dans un seul fichier.
- **`CONTEXT.md` est utilisé avec discipline** : « RÈGLES ABSOLUES », pièges
  catégorisés, références au plan d'origine (`#348`, `#349`). Mais il grossit —
  la capitalisation que propose la Proposition C **a déjà commencé spontanément**.
- Tests tracés dans 33/71 plans actifs (cohérent : tous ne sont pas implémentés).

### 3.4 Points de friction identifiés

| # | Friction | Impact |
|---|---|---|
| P1 | Lister les plans impose de lire ~49,6 K tok de narratif | Coût fixe par session |
| P2 | `roadmap.md` doit être édité à la main à chaque transition | Dérive F3/F4 |
| P3 | Statuts `in-progress`/`cancelled` acceptés en pratique mais invisibles pour les règles | Incohérences silencieuses |
| P4 | Aucun moyen de voir « où en est le portefeuille » sans tout lire | Pas de pilotage |
| P5 | `CONTEXT.md` entier injecté même si 10 % est pertinent pour la tâche | Gaspillage |

### 3.5 Estimation du coût token actuel d'une session type

**Session type « reprise d'un plan M »** (hypothèse, ≈4 o/tok) :

| Poste | Tokens |
|---|---|
| Hydratation `CONTEXT.md` | ~20 800 |
| Listing (lecture `roadmap.md`) | ~49 600 |
| Chargement modules init-scan + plan + wrapup | ~4 000 |
| Lecture du plan repris (médiane) | ~1 600 |
| **Coût fixe d'amorçage** | **~76 000 tok** |

> ⚠️ **Non vérifié précisément** : la quantité exacte de `roadmap.md` effectivement
> lue dépend du comportement du modèle (lecture intégrale vs partielle head/tail).
> Le chiffre ci-dessus est le **plafond** si lecture intégrale — qui est le cas
> par défaut aujourd'hui, aucune instruction du skill ne borne cette lecture.

---

## 4. Évaluation des propositions utilisateur

### 4.1 Proposition A — Archivage des plans « done »

✅ **Forces**
- Attaque un vrai poste de coût ; les 225 lignes `## Fait` + 209 liens `done/`
  alourdissent `roadmap.md`.
- **Partiellement déjà faite** : `done/` existe, le listing l'exclut (plan #25).

⚠️ **Risques / Limites**
- Le gros du coût de `roadmap.md` n'est **pas** la section `Fait` (225 l.) mais la
  section `À faire` (715 l.) — purger les done ne règle que ~20 % du fichier.
- **Purger** (supprimer) détruirait la traçabilité que `init-scan.md` revendique
  explicitement (« le skill peut et doit lire `done/` pour récupérer du contexte »).
  8 plans actifs référencent déjà un plan `done/` dans leur corps.

💰 **Impact tokens** : positif mais **modeste** si on se limite à retirer `Fait`
de `roadmap.md` (~10 K tok). Le vrai gain vient de ne plus lire `roadmap.md` du
tout (voir §5.1), pas de tailler sa section done.

🔄 **Contre-proposition**
- Ne pas purger : **séparer**. `roadmap.md` ne contient QUE le backlog actif.
  L'historique « Fait » vit dans un **index `done/INDEX.md` généré** (1 ligne/plan),
  jamais lu au démarrage, consultable sur demande ou par recherche.
- Seuil d'archivage configurable **non pertinent** : la clôture déplace déjà vers
  `done/` (plan #25). Il manque juste de **retirer l'entrée de `roadmap.md`** à la
  clôture et de l'écrire dans l'index done. C'est une correction de la checklist
  de clôture (`wrapup.md`), pas un nouveau mécanisme.

🏗️ **Migration 287 plans** : script `prune_done_from_roadmap.py` qui retire de
`roadmap.md` toute entrée dont le plan est dans `done/` et régénère `done/INDEX.md`.
Idempotent, dry-run, rollback = git.

### 4.2 Proposition B — Organisation par statut avec sous-dossiers

**Sous-question 1 — racine = active, OU dossier `active/` dédié ?**
→ **Garder la racine pour « en cours » (active + blocked + in-progress), `done/`
pour le terminal. Ne PAS créer `active/`.** Un dossier `active/` ajouterait un
`git mv` à la création ET à la clôture pour zéro gain ; la racine joue déjà ce
rôle. Introduire `active/` casserait aussi tous les liens relatifs existants.

**Sous-question 2 — `roadmap-<statut>.md` suffixés OU `roadmap.md` uniforme ?**
→ **Un seul `roadmap.md` (généré), jamais de fichiers suffixés par statut.** N
fichiers de suivi = N sources à synchroniser = multiplication de F1/F3/F4. Le
statut est une **donnée** (front matter), pas une **localisation**.

✅ **Forces** : navigation par dossier intuitive ; lecture ciblée d'un seul fichier.

⚠️ **Risques / Limites**
- **Churn de transition** : chaque changement de statut = `git mv` + réécriture de
  tous les liens entrants. À 350+ plans avec transitions fréquentes
  (active→blocked→active→done), c'est une source d'erreurs majeure. **La dérive
  F4 (8 plans mal placés) prouve que même avec 1 seul déplacement (clôture) la
  synchro échoue déjà.** Multiplier les dossiers multiplierait la dérive.
- Un plan `blocked` qui redevient `active` reviendrait de `blocked/` vers racine :
  double mouvement, liens cassés deux fois.

💰 **Impact tokens** : un `roadmap.md` éclaté par statut **réduit** la lecture (le
skill ne lit que le fichier du statut pertinent) — MAIS le même gain, en mieux,
est obtenu par un **index compact généré** sans aucun déplacement de fichier.

🔄 **Contre-proposition** : **statut dans le front matter (déjà le cas) + index
généré + un seul `roadmap.md` actif généré.** Zéro `git mv` sur transition, zéro
lien à réécrire, et la lecture ciblée est obtenue en interrogeant l'index.
Officialiser le vocabulaire : ajouter `in-progress` et `cancelled` à l'enum **ou**
les mapper (`in-progress`→`active`, `cancelled`→`archived`) — trancher avec
l'utilisateur.

🏗️ **Migration** : aucune réorganisation de dossiers (on ne crée pas `blocked/`
etc.). Seulement : normaliser le vocabulaire de statut + déplacer les 3 `done` et
2 `archived` mal placés + créer `_archives/`.

### 4.3 Proposition C — Capitalisation contextuelle (CONTEXT.md)

**État réel : CONTEXT.md existe déjà, fait 81 Ko / 1243 lignes, et est lu
intégralement à chaque session.** La Proposition C ne crée pas le mécanisme — elle
l'**automatise**, donc elle **accélère un problème déjà présent**.

✅ **Forces** : capitaliser les pièges (ex. le piège `COPILOT_VERIFIER_ENABLED` vs
`VERIFIER_ENABLED` documenté dans l'actuel CONTEXT.md) évite des régressions
coûteuses. La discipline actuelle (catégorisation implicite, réf. plan d'origine)
est bonne.

⚠️ **Risques / Limites**
- **Gouffre à tokens confirmé, pas hypothétique** : à 1243 lignes déjà, l'auto-ajout
  sans borne mène à un fichier de plusieurs centaines de Ko lu à chaque session.
- Critère « crucial » flou → pollution. Risque de faux positifs (le modèle juge
  « crucial » ce qui est trivial).

💰 **Impact tokens** : **négatif si non borné.** Chaque entrée auto-ajoutée est
re-payée à **chaque session future**. C'est le poste le plus dangereux à l'échelle.

🔄 **Contre-proposition (encadrement strict)**
1. **Segmenter** : un `CONTEXT.md` court (uniquement « RÈGLES ABSOLUES », toujours
   chargé, **budget dur ex. 200 lignes / 15 Ko**) + un dossier `context/` de notes
   thématiques (`context/pieges.md`, `context/deploiement.md`…) **chargées à la
   demande** selon la pertinence pour la tâche.
2. **Capture gatée OUI/NON/instructions** (conforme à la contrainte 6) avec
   **catégorisation obligatoire** (⚠️ piège / 🔗 dépendance / 📌 contrainte / 💡 insight)
   et **référence au plan d'origine** (déjà pratiqué).
3. **Révision périodique** : à chaque clôture de plan, proposer de purger les
   entrées CONTEXT devenues obsolètes (le piège résolu par le plan clos).
4. **Garde-fou de budget** : si `CONTEXT.md` dépasse le seuil, le skill **refuse
   l'ajout** et propose de basculer vers un fichier thématique.

🏗️ **Migration** : scinder l'actuel CONTEXT.md (84 Ko) en noyau « règles
absolues » + fichiers thématiques. Semi-manuel (jugement éditorial), un script
peut pré-découper par titres `##`.

---

## 5. Propositions complémentaires

### 5.1 [P1] `roadmap.md` et index GÉNÉRÉS depuis le front matter

- **Problème** : F1+F2+P1+P2. `roadmap.md` est hand-maintenu (dérive) et lu en
  entier (~49,6 K tok).
- **Solution** : un script `build_roadmap.py` scanne le front matter de tous les
  plans (racine + `done/`) et **génère** :
  - `roadmap.md` (backlog actif uniquement, trié priorité puis ID) ;
  - `.index.tsv` ou `.index.json` compact : 1 ligne/plan `{id, status, priority,
    complexity, title, deps, path}` — **quelques Ko** ;
  - `done/INDEX.md` (historique).
  Le skill **lit l'index** pour lister/filtrer, pas le narratif.
- **Bénéfice** : source de vérité unique = les plans. Zéro dérive. Listing en
  **~3-5 K tok** au lieu de ~49,6 K.
- **Impact tokens** : 🟢🟢🟢 **−45 000 tok/session** (le plus gros levier).
- **Complexité** : moyenne (le parseur de front matter existe déjà dans
  `migrate_plan_ids.py` — réutilisable).
- **Migration** : `build_roadmap.py --check` compare l'index généré au `roadmap.md`
  existant et liste les écarts (détecte F3/F4) ; `--write` régénère.

### 5.2 [P1] Listing paresseux / pagination

- **Problème** : même avec un index, afficher 71 (puis 350+) lignes sature le chat.
- **Solution** : le listing lit l'index et n'affiche **par défaut que les plans
  actifs/bloqués triés par priorité**, avec un compteur (« + 216 done, dis "voir
  done" »). Filtres : `plans high`, `plans blocked`, `plans #250-300`.
- **Impact tokens** : 🟢🟢 ne charge que le pertinent.
- **Complexité** : faible (dépend de 5.1).

### 5.3 [P1] Commande de validation d'intégrité (`aide doctor`)

- **Problème** : F3/F4/F6 — dérives invisibles (8 plans mal placés, 2 statuts
  hors enum, `_archives/` manquant).
- **Solution** : `scripts/doctor.py` (ou catégorie d'aide `aide doctor`) qui
  vérifie : statut vs dossier, statut ∈ enum, dépendances réciproques,
  liens `done/` orphelins, `updated_at` cohérent, index à jour. Rapport tableau,
  **corrections proposées** (jamais auto-destructrices).
- **Bénéfice** : rattrape la dérive avant qu'elle s'accumule ; rassure les
  nouveaux collègues.
- **Impact tokens** : 🟢 ne lit que les front matter.
- **Complexité** : moyenne.

### 5.4 [P2] Observabilité portfolio sans lecture des plans

- **Problème** : F7+P4. Impossible de piloter sans tout lire.
- **Solution** : `aide stats` → tableau généré depuis l'index (nb par statut /
  priorité / complexité, plans bloqués, âge moyen). Exactement ce que ce rapport
  a reconstruit par grep — à industrialiser.
- **Impact tokens** : 🟢 lit l'index (quelques Ko).
- **Complexité** : faible (dépend de 5.1).

### 5.5 [P2] Officialiser le vocabulaire de statut

- **Problème** : F3. `in-progress`/`cancelled` utilisés mais non reconnus.
- **Solution** : trancher — soit étendre l'enum (`active/in-progress/blocked/done/
  cancelled/archived`), soit mapper les intrus. Mettre à jour `roadmap-file.md`,
  `templates.md`, icônes.
- **Impact tokens** : neutre.
- **Complexité** : faible — **décision utilisateur requise** (❓ à confirmer).

### 5.6 [P3] Onboarding des 4-5 collègues

- **Problème** : prise en main.
- **Solution** : section README « Quickstart 5 min » + la note de bienvenue
  existante (Axe E) ; un `aide` déjà généré à la volée. Ajouter un
  `aide migration` pour l'adoption sur un projet existant non suivi.
- **Impact tokens** : neutre.
- **Complexité** : faible.

### 5.7 [P3] Borne de lecture explicite de `roadmap.md` (quick win immédiat)

- **Problème** : rien dans le skill ne borne la lecture de `roadmap.md`
  aujourd'hui → lecture intégrale par défaut.
- **Solution transitoire** (avant 5.1) : instruire `init-scan.md` de lire
  `roadmap.md` en **head 50 + tail 30 + grep** (comme cette mission l'a fait),
  jamais en entier. Déjà la méthode recommandée par la mission — à inscrire dans
  le skill lui-même.
- **Impact tokens** : 🟢🟢 **−40 K tok/session dès maintenant**, sans refactor.
- **Complexité** : très faible — **à faire en premier** (effet immédiat, zéro
  dépendance).

---

## 6. Plan de migration pour les plans existants

### 6.1 Stratégie globale de rattrapage

Ordre, du moins risqué au plus structurant, chaque étape idempotente + dry-run :

1. **Normaliser le vocabulaire** de statut (5.5) — après décision utilisateur.
2. **Déplacer les plans mal placés** : 3 `done`→`done/`, 2 `archived`→`_archives/`
   (créer le dossier), via `git mv`.
3. **Générer l'index + régénérer `roadmap.md`** (5.1) ; comparer avant/après.
4. **Scinder `CONTEXT.md`** (4.3) — semi-manuel.
5. **Activer les quick wins** : borne de lecture (5.7), listing paresseux (5.2).

### 6.2 Scripts proposés

| Script | Rôle | Réutilise |
|---|---|---|
| `build_roadmap.py` | Génère index + `roadmap.md` + `done/INDEX.md` | parseur front matter de `migrate_plan_ids.py` |
| `doctor.py` | Audit intégrité (statut/dossier/deps/liens) | idem |
| `normalize_status.py` | Mappe/valide le vocabulaire de statut | idem |
| `prune_done_from_roadmap.py` | (optionnel si `build_roadmap` régénère) | — |

Tous : `--dry-run` par défaut, `--write` explicite, sortie tableau, aucune
suppression destructive, `git` comme rollback.

### 6.3 Estimation de l'effort

| Lot | Effort | Risque |
|---|---|---|
| Quick win 5.7 (borne lecture) | ~XS (édit `init-scan.md`) | Très faible |
| 5.1 `build_roadmap.py` + index | ~L (parseur + génération + tests) | Moyen |
| 5.3 `doctor.py` | ~M | Faible |
| Déplacements 6.1.2 | ~S (script + revue) | Faible (git mv) |
| Scission CONTEXT | ~M (jugement éditorial) | Faible |

### 6.4 Procédure de rollback

Tout passe par `git` : `git mv` pour les déplacements, régénération idempotente
pour les fichiers générés. Rollback = `git checkout -- doc/roadmap/` ou
`git reset --hard` sur la branche de migration. Aucune donnée n'est supprimée :
les plans `done/` restent, seules les **vues** (`roadmap.md`, index) sont
régénérées.

---

## 7. Matrice de priorisation

| Amélioration | Impact UX | Impact Token | Complexité | Priorité |
|---|---|---|---|---|
| 5.7 Borne de lecture `roadmap.md` | Moyen | 🟢🟢 −40 K/session | Très faible | **P0 (quick win)** |
| 5.1 Index + `roadmap.md` généré | Élevé | 🟢🟢🟢 −45 K/session | Moyenne | **P1** |
| 5.3 `doctor.py` intégrité | Élevé | 🟢 | Moyenne | **P1** |
| 5.2 Listing paresseux | Élevé | 🟢🟢 | Faible | **P1** |
| 4.3 Segmentation CONTEXT + budget | Moyen | 🟢🟢 −15 K/session | Moyenne | **P2** |
| 5.4 `aide stats` | Moyen | 🟢 | Faible | **P2** |
| 5.5 Vocabulaire statut | Faible | Neutre | Faible | **P2** |
| 4.1 `done/INDEX.md` (séparation) | Faible | 🟢 | Faible | **P2** |
| 4.3 Capitalisation auto gatée | Moyen | 🟡 (si borné) | Moyenne | **P3** |
| 5.6 Onboarding | Moyen | Neutre | Faible | **P3** |
| 4.2 Dossiers par statut | Faible | 🟡 | Élevée | **❌ Déconseillé** |

---

## 8. Estimation globale des gains tokens

Session type « reprise plan M » (≈4 o/tok ; hypothèses §9.4) :

| Poste | Avant | Après (P0+P1+P2) | Gain |
|---|---|---|---|
| Hydratation CONTEXT.md | ~20 800 | ~4 000 (noyau segmenté) | −16 800 |
| Listing (roadmap.md → index) | ~49 600 | ~4 000 (index compact) | −45 600 |
| Modules + plan repris | ~5 600 | ~5 600 | 0 |
| **Coût fixe d'amorçage** | **~76 000** | **~13 600** | **−62 400 (~−82 %)** |

> ⚠️ **Estimations, non mesurées.** Le gain réel dépend du comportement de lecture
> du modèle et de la part de `roadmap.md`/`CONTEXT.md` réellement ingérée
> aujourd'hui. L'ordre de grandeur (division par ~5 du coût d'amorçage) est robuste
> car il découle d'un principe simple : **lire un index de quelques Ko au lieu de
> ~275 Ko de narratif.** Projection 500/1000 plans : sans P1, l'amorçage dépasse
> 100 K tok ; avec P1, il reste quasi constant (l'index croît ~linéairement mais
> en Ko, pas en dizaines de Ko) — **c'est la seule approche qui tient dans la durée.**

---

## 9. Annexes

### 9.1 Arborescence complète analysée (listing)

- **Skill** : `SKILL.md`, `README.md`, `modules/{init-scan,plan,execute,wrapup}.md`,
  `references/{environment,templates,roadmap-file,forms,github-issues,migration,autonomous-tests}.md`,
  `hooks/{hooks.json,codex-hooks.json,pretooluse_gate.py}`,
  `scripts/{migrate_plan_ids.py,e2e_fresh_install_setup.sh}`,
  `doc/{audits,rapports,roadmap/done}`, `.claude/` (openspec), `openspec/`.
- **Auxitum** : `roadmap.md`, `CONTEXT.md`, `.skill-config.yml`, 69 plans actifs
  racine, `done/` (216 plans). Pas de `_archives/`.

### 9.2 Échantillon de plans analysés (justification)

| Plan | Taille | Pourquoi retenu |
|---|---|---|
| `30-saas-v2.md` | 56,7 Ko | Plus gros plan — legacy free-form (mini-roadmap) |
| `341-ria-prompt-guardrails.md` | 28,4 Ko | 2e plus gros, récent |
| `14-UI-UX-REFONTE-ORCHESTRATOR.md` | 26,2 Ko | Plan UX multi-lots legacy |
| `287-fix-streaming-cost-trailers.md` | ~5 Ko | `blocked`, conforme template |
| `200-fix-plan-stream-json-parse-loop.md` | 3,5 Ko | Fix récent conforme |
| `354-rag-hybride-semantique.md` | ~9 Ko | `blocked` récent, template complet |
| `123-orchestrator-user-quotas.md` | 1,9 Ko | Plus petit — squelette non cadré |

Couverture : statuts (active/blocked), tailles (1,9→57 Ko), générations
(legacy free-form vs template récent), complexités (S→XL).

### 9.3 Utilisation du skill /impeccable:impeccable

**Décision : non invoqué, à dessein.** `impeccable` est un skill de design
d'**interfaces visuelles** (sites, dashboards, composants, typo, couleur, layout).
Or `roadmap-tracking` est un skill **conversationnel/CLI** : son « UX » est faite
de messages chat, tableaux markdown, `AskUserQuestion` et points d'arrêt — aucune
surface graphique sur laquelle `impeccable` aurait prise. L'invoquer aurait de
plus chargé un gros skill, **en contradiction avec la contrainte tokens de la
mission**.

**Principes d'`impeccable` transférés quand même** (sans l'outil) :
- *Progressive disclosure* → propositions 5.2 (listing paresseux) et 4.3
  (CONTEXT segmenté) : ne montrer/charger que le pertinent.
- *Réduction de charge cognitive* → afficher le backlog actif trié, masquer les
  done derrière une commande.
- *Hiérarchie visuelle* → la règle ⛔ « listing en tableau markdown » du skill est
  déjà alignée avec ce principe.

Si tu souhaites une passe `impeccable` ciblée (ex. sur un futur dashboard HTML du
portfolio), elle aurait du sens **à ce moment-là**, pas sur le skill texte actuel.

### 9.4 Méthodologie d'estimation des coûts tokens

- **Heuristique** : ≈ 4 octets/token (standard pour texte latin/markdown). Mesure
  réelle impossible sans accès au tokenizer runtime → tous les chiffres sont des
  **estimations** signalées comme telles.
- **Mesures brutes** (vérifiées) : `stat`/`wc`/`du` sur les fichiers ;
  `roadmap.md` = 193,8 Ko, `CONTEXT.md` = 81,2 Ko.
- **Comptages** : `grep -c`, `find | wc -l`, `grep '^status:' | sort | uniq -c`.
- **Non vérifié** : la part exacte de chaque fichier réellement lue par le modèle
  à l'exécution (dépend du comportement d'ingestion) — d'où le cadrage en
  « plafond si lecture intégrale ».
- **Référence antérieure** : `doc/audits/0-rationalisation-tokens-SYNTHESE.md`
  (métriques Sonnet réelles : session avec skill = 3,87 M tokens, +37 % vs sans) —
  cohérent avec un coût d'amorçage élevé.
