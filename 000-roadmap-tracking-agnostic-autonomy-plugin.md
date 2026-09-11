# Plan — `roadmap-tracking` : agnostique IDE/modèles + autonomie + plugin (axes A→E)

## Context

Généralisation du skill `roadmap-tracking` en vue d'un partage dans l'équipe.
Le socle validé (agnosticisme IDE + fournisseur de modèles) est complété par 5
axes : zéro dépendance externe (A), GitHub optionnel (B), exécution des tests par
l'agent (C), cohérence transverse (D), déclenchement par hook + packaging plugin
(E). Le tout doit rester **rétrocompatible** (Claude Code + GitHub, sans config =
comportement v1.3.0 actuel) et **sans sur-ingénierie** (config optionnelle,
chaque mode a un défaut par détection).

## Reprise après `/clear` (à lire en premier)

Ce plan est auto-suffisant pour reprendre l'implémentation dans une session
neuve. Points d'ancrage et dépendances externes à connaître :

- **Repo de travail** : ce fichier vit à la racine du repo de packaging
  (`skills/roadmap-tracking/`, layout « skill à la racine »). Tous les fichiers à
  éditer (`SKILL.md`, `references/*`, `.claude-plugin/*`, `README.md`) y sont.
- **Baseline** : `SKILL.md` = **v1.3.0** (contient déjà Phase 1.5, gate modèle,
  point d'arrêt de bypass, gate Phase 7). C'est la base de la rétrocompat.
- **Numéros de ligne** (L39-46, L91-96…) : valides pour v1.3.0 **avant** toute
  édition ; ils dérivent ensuite → **relire le fichier avant chaque édition**,
  ne pas éditer à l'aveugle sur ces numéros.
- **Dépendance Axe A** : le contenu à embarquer vient de
  `~/.claude/rules/operator-commands-formatting.md` (règle globale, rechargée
  automatiquement dans le system prompt à chaque session → disponible pour
  l'agent). Le recopier dans `references/environment.md`.
- **À re-vérifier (Étape 8, variante Codex)** : la **structure de config exacte**
  du hook Codex (`sessionStart`, fichier/format, modèle de *trust* `/hooks`)
  n'est pas figée ici → re-confirmer en doc/source Codex avant de l'écrire.
- **Faits Codex déjà vérifiés** (inutile de re-chercher) : `/model`, mode `/plan`,
  vrais sous-agents (`spawn_agent`, `agent-roles/` avec `developer_instructions`),
  événements de hook `sessionStart`/`userPromptSubmit` + injection `context`.

## Socle validé (rappel condensé)

- Le skill raisonne en **tiers** (`standard`/`reasoning` ; `light`/Haiku
  hors-scope planification), jamais en versions de modèles.
- Mapping tier↔modèle : **défauts Anthropic embarqués** + surcharge via
  `.skill-config.yml`.
- Points de contact IDE (changer de modèle, poser une question, sortir du mode
  plan, détecter le modèle actif, formater les commandes) abstraits derrière des
  **actions génériques** + mapping `Claude Code | Codex | Fallback` dans un
  nouveau `references/environment.md`.
- Tags d'étape : **`(taille · tier → modèle)`**, modèle résolu à la création.
- Cibles réelles : Claude Code + Codex (`/model`, `/plan`, `/clear`, `/review`
  confirmés en source Codex) ; tout le reste → fallback texte.

---

## Axe A — Zéro dépendance aux règles externes

**Décision** : embarquer le contenu de `operator-commands-formatting.md` comme
**section de `references/environment.md`** (« Formatage des commandes
opérateur »), pas de fichier séparé — cohérent avec « minimiser les fichiers ».
Le skill devient auto-suffisant : cloner `skills/roadmap-tracking/` suffit.

**Impact** :
- `SKILL.md ## Prerequisites` (L39-46) : réécrit, ne cite plus aucune règle
  externe ; pointe vers `references/environment.md`.
- `SKILL.md` L664 & L730 (procédures de tests) : remplacer la référence à la
  règle externe par la section interne.
- La règle personnelle `~/.claude/rules/operator-commands-formatting.md` reste
  chez l'utilisateur mais **n'est plus un prérequis** (le skill ne s'y fie plus).

---

## Axe B — Gestion GitHub optionnelle

**Simplification tranchée** : les 4 modes se réduisent à **2 comportements
effectifs** — `github` (privé/public : identiques d'après le tableau) et `local`
(hors-GitHub / opt-out : identiques). Le privé/public n'est qu'une info
descriptive, pas une branche.

**1. Détection & choix** :
- Au 1er lancement : détecter `.git/`, remote GitHub, `gh auth status`.
- **Proposer** le mode via l'action « poser une question » → **confirmer** →
  **persister** dans `.skill-config.yml` (`issues.mode`).
- Changement de mode = éditer la config (ou commande explicite « change de mode
  issues »). Non détectable/non confirmé → ne pas bloquer, demander une fois.

**2. Numérotation locale (mode `local`)** :
- ID = `max(préfixes numériques de ./doc/roadmap/*.md) + 1`, entier nu.
- Marqueur `plan.source: local` en front matter pour distinguer d'un futur ID
  d'issue.
- **Concurrence** : pas de verrou distribué (YAGNI). Deux créations simultanées
  → collision de nom de fichier / conflit `roadmap.md` **résolu par git** au
  merge. Documenté comme tel, pas masqué.

**3. Impact workflow (branches conditionnelles explicites, pas de `if` caché)** :
- **Règle de démarrage / détection d'ID incohérents (L91-96) + migration
  (L126-152)** : **github uniquement**. En `local`, le contrôle `plan.id ==
  issue.id` et la migration n'ont pas de sens → désactivés, signalés.
- **Phase 3** (template `Fichier: {ID}-slug.md`) : ID = issue (github) ou
  compteur local.
- **Phase 5** (L490-508) : branche github (issue d'abord, puis fichier) vs
  branche local (calcul ID local, fichier direct, aucune issue).
- **Clôture (L631-647)** : github → `gh issue close/comment` ; local → `status:
  done` seul (déjà toléré par L643).
- **Reprise / listing (L82-84)** : colonne « Issue » → « ❌ Local » en mode
  local (déjà partiellement toléré).

**4. Impact fichiers de référence** :
- `github-issues.md` : préfixer « **s'applique en mode `github` uniquement** ».
- `templates.md` : `plan.id` découplé de `issue.id` ; `plan.link`, `issue.id`,
  `issue.url` **nullable** proprement + ajout `plan.source`. `plan.link` en
  local → chemin relatif `doc/roadmap/{id}-slug.md` au lieu d'une URL blob.
- `roadmap-file.md` : format d'entrée alternatif sans `[Issue: #NN]` →
  `[Plan: {id}]` en mode local.

---

## Axe C — Exécution des tests par l'agent (mode autonome)

**2 modes** : `manual` (actuel, **défaut**) / `autonomous` (**opt-in explicite**).

> ⚠️ **Décision rétrocompat** : le mode autonome ne se déclenche **jamais** par
> simple détection d'un accès shell — sinon on casse le comportement v1.3.0
> (manuel). La détection *propose*, la config ou une confirmation *active*.

**Mode autonome — spécifications** :
- Étape 0 de Phase 7 (sélection des tests intermédiaires, L584-606) **supprimée**
  (tous les tests s'exécutent après chaque étape).
- Les procédures de tests restent **écrites dans le plan** (traçabilité).
- Le bloc `📦 Commit proposé` n'apparaît **qu'après** verdict `PASS`, et reste
  **une proposition — jamais exécutée** (respecte ta règle globale « ne jamais
  gérer commit/push »). Le mode autonome n'auto-commit pas.
- `🧪 Tests` finaux : même boucle ; le `⏸️` de clôture se déplace **après** le
  `PASS`.
- Garde-fou : **max 3 itérations** par défaut (voir justification), puis STOP +
  diagnostic + question à l'utilisateur. Interruption manuelle (« stop »)
  possible à tout moment.

**Isolation Vérificateur — décision (vérifiée en source)** :
- **Fait établi** : Claude Code (`Agent`) **et** Codex (`spawn_agent` + rôles
  d'agent avec `developer_instructions`, cf. `codex-rs/agent-roles/`,
  `tools/handlers/multi_agents/`) exposent tous deux de **vrais sous-agents**
  (process/contexte distinct, prompt système dédié). La vraie isolation est donc
  atteignable sur les **deux** IDE cibles.
- **Décision** : **mode autonome = sous-agent réel obligatoire**. Le Vérificateur
  est toujours un sous-agent isolé portant le prompt système dédié → « l'agent
  ne note pas sa propre copie » est réellement tenu.
- **Si l'IDE ne fournit pas de sous-agent** (hors périmètre) : **secours
  auto-check honnête** — l'agent exécute les tests et rapporte factuellement
  observé vs attendu, **sans revendiquer** une indépendance qu'il n'a pas (pas
  de persona « aveugle » simulé). Garantie moindre, mais transparente.
- Mécanisme documenté dans `environment.md` ; `.skill-config.yml`
  (`tests.verifier: auto | subagent | inline`) — `inline` = auto-check honnête.

**Garde-fou = 3 itérations, justification** : itération 1 corrige l'évident,
itération 2 rattrape un cas manqué ; un 3ᵉ échec signale que le diagnostic ou
l'approche est faux → l'humain doit trancher. 3 borne le coût/temps sans brider
l'autonomie utile. Surchargable (`tests.max_iterations`).

**Format de reporting par itération** (transparence, distinction visuelle) :

```
🔁 Itération k/N
─────────────────────────────────
🔨 Exécuteur — implémentation/correction : <résumé 1 ligne>
🔍 Vérificateur — verdict : ❌ FAIL
   Attendu : <…>   Observé : <…>
   Diagnostic factuel : <…>
```
(au `PASS` : `🔍 Vérificateur — verdict : ✅ PASS` + attendu/observé, puis
`📦 Commit proposé`.)

**Prompt système du Vérificateur** (proposé, cas sous-agent) :

```
Tu es le VÉRIFICATEUR. Ton unique rôle : exécuter les tests fournis et
comparer les résultats obtenus aux résultats attendus.

Accès : les tests et leurs résultats UNIQUEMENT. Tu n'as pas accès au code
source d'implémentation et tu ne dois pas chercher à le lire.

Interdits absolus : ne corrige rien, ne suggère aucun fix, ne modifie ni le
code ni les tests. Tu ne proposes pas de solution.

Sortie attendue, exactement :
- Verdict : PASS ou FAIL.
- Pour chaque test : attendu vs observé.
- En cas de FAIL : diagnostic factuel (ce qui diffère), sans hypothèse de
  cause ni recommandation.

Tu es sans mémoire entre invocations : tu ne juges que sur le prompt système
+ les résultats fournis maintenant. Tu n'existes que le temps de rendre ce
verdict.
```

**Impact fichiers** :
- `SKILL.md` : Phase 7 (L539-653), « Tests intermédiaires » (L654-715),
  `🧪 Tests` (L717-778), `✅ Validation` (L780-793), commit format (L795-822),
  reprise (L863-867) → chaque bloc reçoit **deux branches** manuel/autonome. Le
  gros de la mécanique autonome (boucle, reporting, garde-fou) part dans un
  **nouveau `references/autonomous-tests.md`** pour garder SKILL.md lisible ;
  SKILL.md n'orchestre que le branchement.
- `environment.md` : mécanisme de persona-switch par IDE.

---

## Axe D — Cohérence & `.skill-config.yml` unique

Tous les axes convergent vers **un seul** fichier optionnel. Schéma complet :

```yaml
# ./doc/roadmap/.skill-config.yml  — entièrement optionnel, non bloquant
ide: auto                 # auto | claude-code | codex
models:
  active: null            # null = détecter (Claude Code) ou demander
  map:                    # étend les défauts Anthropic (opus/sonnet/haiku)
    - { name: gpt-5,      tier: reasoning }
    - { name: gpt-5-mini, tier: standard }
issues:
  mode: auto              # auto | github | local
tests:
  mode: manual            # manual | autonomous   (manual = défaut)
  max_iterations: 3
  verifier: auto          # auto | subagent | inline
                          #   auto   = sous-agent réel si dispo, sinon inline
                          #   inline = auto-check honnête même contexte (garantie moindre)
```

**Défauts = rétrocompat** : absent + Claude Code + `gh` présent →
`ide:claude-code, issues:github, tests:manual` = comportement v1.3.0. Le fichier
reste optionnel ; chaque champ a un défaut par détection ; **jamais bloquant**.

---

## Axe E — Déclenchement par hook + packaging plugin

**Objectif** : sortir le déclencheur `rules/roadmap-tracking.md` du périmètre des
prérequis externes. Distribution retenue : **plugin installable** (`/plugin
install` depuis un marketplace git interne) embarquant `skills/` + `hooks/`.

**Répartition (validée)** : le **hook injecte**, le **modèle juge**. Le hook ne
fait aucune détection d'intention (tâche sémantique = modèle) ; il ne fait que
la **porte déterministe** + l'injection d'une consigne courte.

> **État existant du repo** : `plugin.json` (v1.0.0, sans clé `hooks`) et
> `marketplace.json` (`source: "."`) déjà présents ; **layout « skill à la
> racine »** (`SKILL.md`, `references/`, `scripts/` à la racine, `.claude-plugin/`
> au même niveau — PAS de sous-dossier `skills/`). Le README documente déjà un
> hook `SessionStart` **opt-in** (`test -d ./doc/roadmap && printf '…'`).

**Deux cas séparés sur deux mécanismes (anti-harcèlement)** :

- **Cas 1 — `doc/roadmap/` présent** → le **hook** (embarqué) injecte la consigne.
- **Cas 2 — `doc/roadmap/` absent** → le hook reste **silencieux** (zéro nag dans
  les projets sans rapport). L'offre de créer `doc/roadmap/` vient du **skill**,
  quand l'utilisateur fait une demande de dev/plan (invocation par le modèle via
  la description). **Ajout SKILL.md** : dans « Applicabilité / Règle de démarrage »,
  si le skill est invoqué sans `doc/roadmap/` → proposer de le créer (question),
  puis dérouler le workflow si accepté.

**1. Déclencheur = hook `SessionStart` embarqué** (décision : `SessionStart`
suffit ; embarqué dans le plugin) :
- Commande shell : si `doc/roadmap/` existe → **injecter une consigne courte**
  (stdout, injecté en contexte) du type : « Projet roadmap-tracking : si le prompt
  concerne la création/analyse/cadrage/implémentation/reprise/test d'un plan,
  invoquer le skill roadmap-tracking et suivre son workflow. » Le **détail des 7
  phases reste dans le skill**.
- Injecté **une fois par session** (économe), **conditionnel** (`test -d` — rien
  hors projet roadmap, donc pas de nag). Pas de dépendance MCP → fiable au
  lancement.
- Interrupteur simple pour couper l'auto-déclenchement même si `doc/roadmap/`
  existe (env var, ex. `ROADMAP_TRACKING_AUTOSTART=off`).
- `userPromptSubmit` écarté : coût par tour non justifié pour un déclencheur qui
  joue surtout en début de session.

**2. Deux variantes de hook** (vérifié en source Codex) :
- Claude Code : `hooks/hooks.json`, événement `SessionStart`.
- Codex : événement `sessionStart` (casse ≠), modèle de *trust* (`/hooks` à
  valider par l'utilisateur, `allow_managed_hooks_only`). Injection via `context`.
- Le plugin embarque les **deux** jeux (patron ponytail).

**3. Packaging plugin** (layout réel du repo à respecter) :
```
roadmap-tracking/            # racine = le plugin
├── .claude-plugin/
│   ├── plugin.json          # AJOUTER la clé "hooks"
│   └── marketplace.json     # existant, inchangé
├── hooks/hooks.json         # variante Claude Code (SessionStart)  [NOUVEAU]
├── hooks/<codex-hooks>      # variante Codex                        [NOUVEAU]
├── SKILL.md                 # à la racine (auto-suffisant, axe A inclus)
├── references/
└── scripts/
```
- Pas de script node nécessaire : la commande `test -d … && printf …` suffit
  (plus léger que ponytail). `hooks/trigger.*` seulement si logique plus riche.

**4. Embarqué (décidé)** : le hook est livré actif dans le plugin (remplace la
section opt-in du README), avec l'interrupteur ci-dessus pour le couper.

**5. Règle `~/.claude/rules/roadmap-tracking.md`** : hors du repo plugin (c'est
ta config perso). Elle n'est **pas un livrable** ici. ⚠️ Sur ta machine, si tu
installes le plugin avec hook embarqué **et** gardes la règle → **double
injection** ; retirer l'une des deux.

**Force d'application** : équivalente à la règle actuelle (consigne NL suivie par
le modèle).

---

## Fichiers impactés — synthèse

| Fichier | Nature |
|---|---|
| `SKILL.md` | Prerequisites, section complexité→tier, 3 gates, mode plan, Phase 5, clôture, Phase 7 (branches manuel/autonome), démarrage/migration conditionnels github, **Applicabilité : proposer de créer `doc/roadmap/` si absent (axe E, cas 2)** |
| `references/environment.md` | **Nouveau** : mapping IDE, tiers+défauts Anthropic, formatage commandes (axe A), persona-switch (axe C), schéma config, détection |
| `references/autonomous-tests.md` | **Nouveau** : boucle vérif/exéc, reporting, garde-fou, prompt Vérificateur |
| `references/github-issues.md` | Conditionné « mode github uniquement » |
| `references/templates.md` | Front matter nullable + `plan.source`, tags `(taille·tier→modèle)`, `plan.link` local |
| `references/roadmap-file.md` | Format d'entrée sans issue (`[Plan: {id}]`) |
| `references/forms.md` | `AskUserQuestion` = mécanisme Claude Code + fallback texte |
| `references/migration.md` | Noter : github uniquement |
| `.claude-plugin/plugin.json` | Existant (axe E) : **ajouter la clé `hooks`** |
| `hooks/hooks.json` + variante Codex | **Nouveau** (axe E) : hook `SessionStart` conditionnel (commande shell `test -d`) |
| `README.md` | (axe E) : documenter le hook embarqué + l'interrupteur, remplacer la section opt-in actuelle |

## Risques identifiés

1. **Bloat / maintenabilité** : 4 axes sur un skill déjà dense. Mitigation :
   pousser la mécanique lourde (autonomous-tests, environment) hors de SKILL.md,
   qui reste orchestrateur. À surveiller — c'est le risque principal.
2. **Isolation du Vérificateur** : réelle via sous-agent (CC + Codex, vérifié) ;
   en secours `inline` (IDE sans sous-agent), garantie moindre mais transparente
   (pas de fausse indépendance revendiquée). Risque résiduel : coût/latence des
   sous-agents par itération ; vigilance à ne pas sur-vendre le verdict `inline`.
3. **Concurrence numérotation locale** : git comme point de réconciliation,
   pas de verrou (assumé).
4. **Rétrocompat** : le mode autonome et les modes local doivent rester
   opt-in/détectés-puis-confirmés ; risque de dérive de comportement par défaut
   si mal câblé → tests de non-régression ciblés.
5. **Double-branche partout** : multiplier manuel/autonome × github/local peut
   créer des combinaisons non testées. Mitigation : matrice de cas explicite.
6. **Axe E — double injection** : règle perso `~/.claude/rules/` + hook plugin
   actifs ensemble → consigne dupliquée. Mitigation : retirer l'une des deux.
7. **Axe E — trust Codex** : l'étape `/hooks` de validation reste manuelle côté
   Codex (le hook n'agit qu'une fois approuvé).
8. **Axe E — layout** : le repo est un plugin « skill à la racine » ; ne pas
   introduire de sous-dossier `skills/` (le plan initial le supposait à tort).

## Vérification

- **Rétrocompat** : dérouler mentalement Claude Code + GitHub sans config →
  identique à v1.3.0 (issues auto, tests manuels, gate Sonnet/Opus).
- **Local + Codex + autonome** : `.skill-config.yml` correspondant → pas
  d'issue, ID local max+1, boucle vérif/exéc avec sous-agent, commit proposé
  après PASS non exécuté.
- **Fallback IDE inconnu** : aucune commande spécifique, tout en texte.
- `grep` anti-adhérence : aucun nom de modèle versionné dans la logique de
  SKILL.md.
- Relecture croisée des renvois `SKILL.md ↔ references/*`.
- **Axe E** : `claude plugin validate .` puis `claude --plugin-dir .` ; session
  dans un projet avec `doc/roadmap/` → consigne `SessionStart` injectée ; sans
  `doc/roadmap/` → hook silencieux (pas de nag), et une demande de dev/plan →
  le skill propose de créer `doc/roadmap/`. Interrupteur `AUTOSTART=off` → pas
  d'injection. Vérifier l'absence de double injection règle perso + hook.

## Étapes d'implémentation

Ordonnées par dépendance. Tag `(taille · tier → modèle)` : modèle résolu sur
l'environnement actif (Claude Code → `standard`=Sonnet, `reasoning`=Opus). Les
étapes 🧪 Tests et ✅ Validation ne portent pas de tag (obligatoires).

**Étape 1 — `references/environment.md` (socle transverse)** `(L · reasoning → Opus)`
Créer le fichier : mapping actions génériques → `Claude Code | Codex | Fallback`
(changer de modèle, poser une question, sortir du mode plan, détecter le modèle
actif) ; taxonomie des tiers + défauts Anthropic ; section « Formatage des
commandes opérateur » (axe A, contenu embarqué) ; mécanisme de persona-switch
sous-agent (axe C) ; schéma complet `.skill-config.yml` ; procédure de détection
d'environnement. *Fondation des étapes 3-6.*

**Étape 2 — `references/autonomous-tests.md` (boucle autonome)** `(L · reasoning → Opus)`
Créer le fichier : contrat Vérificateur/Exécuteur, boucle test→fix→retest,
garde-fou 3 itérations, format de reporting par itération, prompt système du
Vérificateur, secours `inline` honnête. *Dépend de l'étape 1 (mécanisme).*

**Étape 3 — `SKILL.md` : agnosticisme modèle/tier** `(L · reasoning → Opus)`
Réécrire `## Prerequisites` (axe A, plus de règle externe) ; `Matrice complexité
→ tier` ; `Résolution du modèle actif et de son tier` ; les 3 gates (1.5 / 3 /
Phase 7) en tiers + commandes via mapping ; tags `(taille · tier → modèle)` ;
renommer `## Compatibilité mode plan`. *Dépend de l'étape 1.*

**Étape 4 — `SKILL.md` : GitHub optionnel** `(L · reasoning → Opus)`
Brancher `github` / `local` : Applicabilité, démarrage + détection d'ID + migration
conditionnés github, Phase 3 (`{ID}`), Phase 5 (2 branches), clôture, listing.
Numérotation locale max+1 + `plan.source`. *Indépendante de 3, même fichier.*

**Étape 5 — `SKILL.md` : tests manuel/autonome** `(L · reasoning → Opus)`
Ajouter les deux branches (manuel actuel / autonome) sur Phase 7, tests
intermédiaires, `🧪 Tests`, `✅ Validation`, commit, reprise ; suppression de
l'étape 0 en autonome ; `⏸️` de clôture après `PASS`. *Dépend de l'étape 2.*

**Étape 6 — `SKILL.md` : offre de création `doc/roadmap/`** `(S · standard → Sonnet)`
Section Applicabilité / Règle de démarrage : si le skill est invoqué sans
`doc/roadmap/`, proposer de le créer (question) puis dérouler le workflow (axe E,
cas 2). *Indépendante.*

**Étape 7 — Fichiers de référence restants** `(M · standard → Sonnet)`
`templates.md` (front matter nullable + `plan.source`, tags tier, `plan.link`
local) ; `github-issues.md` (préfixe « mode github uniquement ») ; `roadmap-file.md`
(entrée `[Plan: {id}]` locale) ; `forms.md` (fallback texte pour `AskUserQuestion`) ;
`migration.md` (note github uniquement). *Dépend des étapes 3-5 (cohérence).*

**Étape 8 — Packaging plugin (axe E)** `(M · standard → Sonnet)`
`hooks/hooks.json` (SessionStart Claude) + variante Codex (`sessionStart`) avec
`test -d doc/roadmap` + injection consigne + interrupteur `AUTOSTART` ; ajout clé
`hooks` dans `.claude-plugin/plugin.json` ; mise à jour `README.md` (hook embarqué
+ interrupteur, remplace la section opt-in). *Dépend des étapes 1-6.*

**Étape 🧪 Tests** *(obligatoire)*
`claude plugin validate .` ; `claude --plugin-dir .` ; walkthrough rétrocompat
(Claude Code + GitHub sans config = v1.3.0) ; scénario local + autonome ; hook
présent/absent + `AUTOSTART=off` ; `grep` anti-adhérence (aucun modèle versionné
dans la logique) ; matrice de modes (manuel/autonome × github/local).

**Étape ✅ Validation** *(obligatoire)*
Vérifier les résultats des tests, relire les renvois croisés `SKILL.md ↔
references/*`, confirmer l'absence de double injection règle+hook, clôturer.
