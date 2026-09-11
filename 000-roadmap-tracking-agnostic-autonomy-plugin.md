# Plan — `roadmap-tracking` : agnostique IDE/modèles + autonomie + plugin (axes A→E)

> ⚠️ **Ambiguïté à confirmer (déploiement Codex).** `plugin-json-spec.md:215`
> note que la validation du scaffold marketplace rejette le champ `hooks` dans
> le manifest — alors que le field guide le liste comme valide (`:18`, `:65`).
> L'activation d'un hook de plugin côté Codex passe donc peut-être par un
> `hooks.json` déposé dans un dossier de config plutôt que par le manifest.
> Point à trancher au moment d'un vrai déploiement Codex.

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

- **Répertoire de travail** : la session de reprise démarre **directement dans**
  `/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/` (l'utilisateur
  s'y positionne via `cd` avant de lancer l'agent). C'est la racine du repo de
  packaging (layout « skill à la racine »). Tous les fichiers à éditer sont donc
  en **chemins relatifs** depuis le CWD : ce plan (`000-…-plugin.md`), `SKILL.md`,
  `references/*`, `.claude-plugin/*`, `README.md`, `scripts/*`.
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

**✅ Étape 1 — `references/environment.md` (socle transverse)** `(L · reasoning → Opus)`
Créer le fichier : mapping actions génériques → `Claude Code | Codex | Fallback`
(changer de modèle, poser une question, sortir du mode plan, détecter le modèle
actif) ; taxonomie des tiers + défauts Anthropic ; section « Formatage des
commandes opérateur » (axe A, contenu embarqué) ; mécanisme de persona-switch
sous-agent (axe C) ; schéma complet `.skill-config.yml` ; procédure de détection
d'environnement. *Fondation des étapes 3-6.*

**✅ Étape 2 — `references/autonomous-tests.md` (boucle autonome)** `(L · reasoning → Opus)`
Créer le fichier : contrat Vérificateur/Exécuteur, boucle test→fix→retest,
garde-fou 3 itérations, format de reporting par itération, prompt système du
Vérificateur, secours `inline` honnête. *Dépend de l'étape 1 (mécanisme).*

**✅ Étape 3 — `SKILL.md` : agnosticisme modèle/tier** `(L · reasoning → Opus)`
Réécrire `## Prerequisites` (axe A, plus de règle externe) ; `Matrice complexité
→ tier` ; `Résolution du modèle actif et de son tier` ; les 3 gates (1.5 / 3 /
Phase 7) en tiers + commandes via mapping ; tags `(taille · tier → modèle)` ;
renommer `## Compatibilité mode plan`. *Dépend de l'étape 1.*

**✅ Étape 4 — `SKILL.md` : GitHub optionnel** `(L · reasoning → Opus)`
Brancher `github` / `local` : Applicabilité, démarrage + détection d'ID + migration
conditionnés github, Phase 3 (`{ID}`), Phase 5 (2 branches), clôture, listing.
Numérotation locale max+1 + `plan.source`. *Indépendante de 3, même fichier.*

**✅ Étape 5 — `SKILL.md` : tests manuel/autonome** `(L · reasoning → Opus)`
Ajouter les deux branches (manuel actuel / autonome) sur Phase 7, tests
intermédiaires, `🧪 Tests`, `✅ Validation`, commit, reprise ; suppression de
l'étape 0 en autonome ; `⏸️` de clôture après `PASS`. *Dépend de l'étape 2.*

**✅ Étape 6 — `SKILL.md` : offre de création `doc/roadmap/`** `(S · standard → Sonnet)`
Section Applicabilité / Règle de démarrage : si le skill est invoqué sans
`doc/roadmap/`, proposer de le créer (question) puis dérouler le workflow (axe E,
cas 2). *Indépendante.*

**✅ Étape 7 — Fichiers de référence restants** `(M · standard → Sonnet)`
`templates.md` (front matter nullable + `plan.source`, tags tier, `plan.link`
local) ; `github-issues.md` (préfixe « mode github uniquement ») ; `roadmap-file.md`
(entrée `[Plan: {id}]` locale) ; `forms.md` (fallback texte pour `AskUserQuestion`) ;
`migration.md` (note github uniquement). *Dépend des étapes 3-5 (cohérence).*

**✅ Étape 8 — Packaging plugin (axe E)** `(M · standard → Sonnet)`
`hooks/hooks.json` (SessionStart Claude) + variante Codex (`sessionStart`) avec
`test -d doc/roadmap` + injection consigne + interrupteur `AUTOSTART` ; ajout clé
`hooks` dans `.claude-plugin/plugin.json` ; mise à jour `README.md` (hook embarqué
+ interrupteur, remplace la section opt-in). *Dépend des étapes 1-6.*

**✅ Étape 9 — Correctifs post-audit** `(M · standard → Sonnet)`
Corrige les écarts relevés dans `000-roadmap-tracking-agnostic-autonomy-plugin-AUDIT.md`.
*Dépend des étapes 1-8. À exécuter avant les tests obligatoires.*

- **[Critique] `.claude-plugin/plugin.json` — clé `hooks` au format invalide.**
  Le format `{ "claude-code": …, "codex": … }` fait échouer `claude plugin
  validate` (`unknown hook event; entry ignored at runtime`) → les hooks sont
  **ignorés au runtime**, axe E non fonctionnel. Corriger avec le format
  reconnu par Claude Code (référence au fichier `hooks/hooks.json` embarquant
  l'événement `SessionStart`). Le fichier `hooks/codex-hooks.json` reste dans
  le repo comme artefact Codex documenté (README), mais n'est **plus référencé**
  dans `plugin.json` (manifest Claude Code) pour ne pas déclencher de warning.
- **[Mineur] Vérification du hook Codex.** Confirmer le format `sessionStart` +
  `context: inject` de `hooks/codex-hooks.json` en source/doc Codex (exigé par
  la note « Reprise après /clear » L33-35 du plan). Signaler si non vérifiable.
- **[Mineur] Cohérence de version.** Aligner `SKILL.md` (`metadata.version`) sur
  `2.0.0` (déjà porté par `plugin.json` et `README.md`).
- **[Mineur] Isolation du Vérificateur.** `references/environment.md` : retirer
  « fork » du mécanisme de sous-agent Claude Code (un fork hérite du contexte
  parent → casse l'isolation exigée par l'axe C). Ne conserver que « fresh
  agent » réellement isolé.

**Étape 🧪 Tests** *(obligatoire)*

> **Procédure complète — à exécuter avant l'étape ✅ Validation.**
> Chaque test produit un résultat à reporter dans le Journal de session.
> Tous les tests sont exécutés dans le répertoire
> `/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/`.

---

### T1 — Validation du plugin

**Objectif** : vérifier que `plugin.json` est syntaxiquement valide et que le
plugin est installable.

```bash
echo "=== Validate Plugin Manifest ==="
claude plugin validate .
```

**Résultat attendu** : sortie sans erreur (ou avertissements non bloquants
uniquement). Un message de succès ou « Plugin is valid ».

---

### T2 — grep anti-adhérence (modèles versionnés + règle externe)

**Objectif** : aucune référence résiduelle à un nom de modèle versionné ni à
l'ancienne règle externe dans la logique du skill.

```bash
echo "=== Grep Versioned Model Names ==="
grep -rn "sonnet-3\|opus-3\|haiku-3\|claude-3\|gpt-4\|(· Sonnet)\|(· Opus)" SKILL.md references/

echo "=== Grep External Rule Reference ==="
grep -rn "operator-commands-formatting" SKILL.md references/
```

**Résultat attendu** : les deux commandes retournent **zéro ligne**.

---

### T3 — Walkthrough rétrocompatibilité (comportement v1.3.x)

**Objectif** : confirmer que l'absence de `.skill-config.yml` + Claude Code +
`gh` disponible → comportement identique à v1.3.x (issues auto, tests manuels,
gates sur Sonnet/Opus).

**Protocole** : lecture mentale du SKILL.md, sans fichier `.skill-config.yml`
dans `./doc/roadmap/`.

1. Ouvrir `SKILL.md` et simuler mentalement un démarrage standard :
   - Vérifier que la **Règle de démarrage** liste les plans existants.
   - Vérifier que la **gate modèle Phase 1.5** utilise bien les tiers
     (`standard`/`reasoning`) et non des noms versionnés.
   - Vérifier que la **Phase 5** emprunte la branche **mode `github`** (défaut
     sans config).
   - Vérifier que **l'étape 0** de Phase 7 est bien présente en mode `manual`
     (défaut).
   - Vérifier que la **clôture** exécute `gh issue close/comment`.

2. Confirmer les valeurs par défaut de `references/environment.md` :
   ```bash
   echo "=== Check Default Config Values ==="
   grep -A 15 "entirely optional" references/environment.md
   ```
   **Attendu** : `ide: auto`, `issues.mode: auto`, `tests.mode: manual`.

**Résultat attendu** : toutes les vérifications passent — comportement v1.3.x
préservé sans config.

---

### T4 — Scénario mode `local` (Phase 5 + templates)

**Objectif** : la branche `local` de Phase 5 est correctement implémentée et
`templates.md` contient le front matter nullable + `plan.source`.

1. Lire la **Phase 5 branche `local`** dans `SKILL.md` :
   ```bash
   echo "=== Read Phase 5 Local Branch ==="
   grep -A 20 "Mode \`local\`" SKILL.md | head -30
   ```
   **Attendu** :
   - Calcul ID = `max(préfixes numériques) + 1`.
   - `plan.source: local` dans le front matter.
   - `issue.id: null` / `issue.url: null`.
   - Mise à jour `roadmap.md` avec `[Plan: {id}]`.

2. Vérifier `references/templates.md` :
   ```bash
   echo "=== Check Templates Local Front Matter ==="
   grep -n "plan\.source\|plan\.link\|issue\.id.*null\|issue\.url.*null" references/templates.md
   ```
   **Attendu** : présence de `plan.source`, `plan.link` chemin relatif en mode
   local, `issue.id: null`, `issue.url: null`.

3. Vérifier `references/roadmap-file.md` :
   ```bash
   echo "=== Check Roadmap File Local Entry ==="
   grep -n "\[Plan:" references/roadmap-file.md
   ```
   **Attendu** : au moins une ligne montrant `[Plan: {id}]`.

---

### T5 — Scénario mode `autonomous` (Phase 7)

**Objectif** : la branche `autonomous` de Phase 7 supprime l'étape 0 et pointe
vers `references/autonomous-tests.md`.

```bash
echo "=== Check Autonomous Branch Phase 7 ==="
grep -n "autonomous\|étape 0.*supprimée\|autonomous-tests" SKILL.md | head -20
```

**Attendu** :
- En mode `autonomous` : l'étape 0 (sélection tests intermédiaires) est
  **supprimée** ou marquée non applicable.
- Le renvoi vers `references/autonomous-tests.md` est présent.
- Le `📦 Commit proposé` n'apparaît qu'après `PASS` (jamais exécuté).

Vérifier le contenu de `references/autonomous-tests.md` :
```bash
echo "=== Check Autonomous Tests Reference ==="
grep -n "PASS\|FAIL\|Vérificateur\|Exécuteur\|max_iterations\|inline\|subagent" references/autonomous-tests.md | head -20
```
**Attendu** : présence de la boucle, du garde-fou 3 itérations, du prompt
Vérificateur, et du fallback `inline` honnête.

---

### T6 — Hook `SessionStart` présent et silencieux

**Objectif** :
- (T6a) Le hook injecte la consigne quand `doc/roadmap/` **existe**.
- (T6b) Le hook est **silencieux** quand `doc/roadmap/` est **absent**.
- (T6c) L'interrupteur `ROADMAP_TRACKING_AUTOSTART=off` coupe l'injection.

```bash
echo "=== Test Hook With doc/roadmap Present ==="
mkdir -p /tmp/test-roadmap-present/doc/roadmap
cd /tmp/test-roadmap-present
HOOK_CMD=$(cat /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/hooks/hooks.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['hooks']['SessionStart'][0]['hooks'][0]['command'])")
eval "$HOOK_CMD" && echo "OUTPUT ABOVE (should contain injection message)" || echo "EMPTY (unexpected)"

echo "=== Test Hook Without doc/roadmap ==="
cd /tmp
HOOK_CMD2=$(cat /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking/hooks/hooks.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['hooks']['SessionStart'][0]['hooks'][0]['command'])")
eval "$HOOK_CMD2" && echo "EMPTY = OK (silent)" || echo "EMPTY = OK (silent)"

echo "=== Test Hook With AUTOSTART=off ==="
cd /tmp/test-roadmap-present
ROADMAP_TRACKING_AUTOSTART=off eval "$HOOK_CMD" && echo "EMPTY = OK (disabled)" || echo "EMPTY = OK (disabled)"
```

**Résultats attendus** :
- T6a : la commande affiche le message d'injection (roadmap-tracking skill).
- T6b : aucune sortie (silencieux).
- T6c : aucune sortie (interrupteur actif).

Nettoyage :
```bash
echo "=== Cleanup Temp Dir ==="
rm -rf /tmp/test-roadmap-present
```

---

### T7 — Vérification structure `plugin.json` (clé `hooks`)

**Objectif** : `.claude-plugin/plugin.json` contient bien la clé `hooks` avec
les deux variantes Claude Code et Codex.

```bash
echo "=== Check Plugin JSON Hooks Key ==="
cat .claude-plugin/plugin.json
```

**Attendu** (format Claude Code reconnu — chemin string, PAS un objet
`{claude-code, codex}` qui serait ignoré au runtime) :
```json
"hooks": "./hooks/hooks.json"
```
`hooks/codex-hooks.json` reste sur disque (artefact Codex) mais **n'est pas
déclaré** dans le manifest. Vérifier en complément que `claude plugin validate .`
passe **sans warning** `unknown hook event`.

---

### T8 — Vérification guards `github` dans les fichiers de référence

**Objectif** : `github-issues.md` et `migration.md` signalent clairement qu'ils
ne s'appliquent qu'en mode `github`.

```bash
echo "=== Check GitHub-Only Guards ==="
head -10 references/github-issues.md
echo "---"
head -10 references/migration.md
```

**Attendu** : les deux fichiers commencent (ou contiennent en tête) par un
avertissement explicite « mode `github` uniquement ».

---

### T9 — Absence de double injection règle perso + hook

**Objectif** : identifier si `~/.claude/rules/roadmap-tracking.md` (règle
perso) est active en parallèle du hook embarqué — les deux ensemble causent une
double injection.

```bash
echo "=== Check Personal Rule File ==="
ls -la ~/.claude/rules/roadmap-tracking.md 2>/dev/null && echo "FICHIER PRÉSENT — double injection possible" || echo "ABSENT ou chemin différent"

echo "=== Check Windows Path Rule File ==="
ls -la "/mnt/c/Users/emmanuel.houriez/.claude/rules/roadmap-tracking.md" 2>/dev/null && echo "FICHIER PRÉSENT — double injection possible" || echo "ABSENT ou chemin différent"
```

**Résultat attendu** : si la règle perso **est présente** (cas probable), noter
qu'une des deux sources doit être désactivée avant déploiement réel du plugin
(la règle perso OU le hook embarqué, pas les deux). Ce test est informatif, il
ne bloque pas la validation.

---

### T10 — Matrice de modes : vérification croisée des combinaisons

**Objectif** : s'assurer que toutes les combinaisons (2 × 2 = 4) sont couvertes
sans divergence dans `SKILL.md`.

Lire les sections Phase 5, Phase 7, clôture pour chaque combinaison :

```bash
echo "=== Check All Mode Combinations Coverage ==="
grep -n "mode \`github\`\|mode \`local\`\|mode \`manual\`\|mode \`autonomous\`\|Mode \`github\`\|Mode \`local\`\|Mode \`manual\`\|Mode \`autonomous\`" SKILL.md
```

**Attendu** : chaque combinaison (github+manual, github+autonomous, local+manual,
local+autonomous) est mentionnée ou couverte par les branches conditionnelles.

---

### T11 — Relecture croisée `SKILL.md ↔ references/*`

**Objectif** : tous les renvois `SKILL.md → references/*.md` pointent vers des
sections qui existent réellement.

```bash
echo "=== Extract All References Cross-Links ==="
grep -n "references/" SKILL.md
```

Pour chaque fichier mentionné, vérifier qu'il existe et que la section
référencée (§ ou titre) est présente :

```bash
echo "=== List All Reference Files ==="
ls references/

echo "=== Check Environment Section Headers ==="
grep "^##" references/environment.md

echo "=== Check Autonomous Tests Section Headers ==="
grep "^##" references/autonomous-tests.md

echo "=== Check Templates Section Headers ==="
grep "^##" references/templates.md
```

**Attendu** : tous les fichiers cités dans `SKILL.md` existent, et les sections
§ référencées correspondent à des en-têtes `##` présents dans ces fichiers.

---

### Grille de résultats à reporter

| Test | Description | Statut | Notes |
|---|---|---|---|
| T1 | `claude plugin validate .` | ⬜ | |
| T2 | grep anti-adhérence | ⬜ | |
| T3 | Rétrocompat v1.3.x | ⬜ | |
| T4 | Mode `local` Phase 5 + templates | ⬜ | |
| T5 | Mode `autonomous` Phase 7 | ⬜ | |
| T6a | Hook présent → injection | ⬜ | |
| T6b | Hook absent → silencieux | ⬜ | |
| T6c | `AUTOSTART=off` → silencieux | ⬜ | |
| T7 | `plugin.json` clé `hooks` | ⬜ | |
| T8 | Guards `github` références | ⬜ | |
| T9 | Double injection règle+hook | ⬜ | |
| T10 | Matrice modes 2×2 | ⬜ | |
| T11 | Renvois croisés `SKILL.md ↔ references/*` | ⬜ | |

**Étape ✅ Validation** *(obligatoire)*
Vérifier les résultats des tests, relire les renvois croisés `SKILL.md ↔
references/*`, confirmer l'absence de double injection règle+hook, clôturer.

---

## Journal de session

### Session 2026-09-11

**Modèle actif** : Claude Sonnet 4.6 (1M context) — tier `standard`

**✅ Fait** : étapes 1 à 8 complètes.

- **Étape 1** : `references/environment.md` créé — mapping IDE, tiers+défauts
  Anthropic, persona-switch, schéma `.skill-config.yml`, procédure de détection,
  section « Operator Commands Formatting » embarquée (axe A).
- **Étape 2** : `references/autonomous-tests.md` créé — boucle Exécuteur/Vérificateur,
  garde-fou 3 itérations, format de reporting, prompt système Vérificateur,
  fallback inline honnête.
- **Étapes 3-6** : `SKILL.md` modifié en 26 édits chirurgicaux —
  Prerequisites auto-suffisants, matrice → tier, tags `(taille·tier→modèle)`,
  gates avec tiers et commandes IDE génériques, Phase 5 deux branches
  github/local avec compteur local max+1 + `plan.source`, guards github-only
  sur ID detection et migration, branches manual/autonomous sur step 0, tests
  intermédiaires, 🧪 Tests, ✅ Validation et reprise, offre création
  `doc/roadmap/` absente.
- **Étape 7** : 5 fichiers de référence mis à jour — `templates.md` (front
  matter nullable + `plan.source` + deux exemples github/local + tag format
  tier), `github-issues.md` et `migration.md` (guard mode github uniquement),
  `roadmap-file.md` (exemple `[Plan: {id}]` local), `forms.md` (fallback texte
  AskUserQuestion).
- **Étape 8** : `hooks/hooks.json` (Claude Code SessionStart + interrupteur
  `AUTOSTART`) + `hooks/codex-hooks.json` (Codex sessionStart) créés,
  `.claude-plugin/plugin.json` mis à jour (clé `hooks`, version 2.0.0),
  `README.md` réécrit (features v2.0.0, hook embarqué, warning double injection,
  config optionnelle).

**grep anti-adhérence** : aucune référence résiduelle à `operator-commands-formatting.md`
ni à l'ancien format de tag `(· Sonnet)` / `(· Opus)` dans `SKILL.md` et les
références.

**📋 Prochain** : étapes 🧪 Tests et ✅ Validation à exécuter :
- `claude plugin validate .`
- Walkthrough rétrocompat (absent config + CC + gh = v1.3.x)
- Scénario local + autonome
- Hook présent/absent + `AUTOSTART=off`
- Relecture croisée `SKILL.md ↔ references/*`
- Vérifier absence de double injection règle perso + hook

**🚧 Blocages** : aucun.

### Session 2026-09-11 (bis) — Audit + correctifs (Étape 9)

**Modèle actif** : Claude Opus 4.8 (1M context) — tier `reasoning`

**Audit** : rapport d'écarts complet écrit dans
`000-roadmap-tracking-agnostic-autonomy-plugin-AUDIT.md` — 5/8 étapes conformes,
1 écart critique (plugin.json), 3 écarts mineurs.

**✅ Correctifs appliqués** :
- **[Critique]** `.claude-plugin/plugin.json` : clé `hooks` corrigée en
  `"./hooks/hooks.json"` (format string reconnu ; format vérifié via doc Claude
  Code). `claude plugin validate .` → **Validation passed**, plus aucun warning.
  `hooks/codex-hooks.json` conservé mais non déclaré dans le manifest.
- **[Mineur]** `SKILL.md` `metadata.version` → `2.0.0`.
- **[Mineur]** `references/environment.md` : « fork » retiré du mécanisme
  sous-agent Vérificateur (isolation axe C préservée — fresh agent uniquement).

**✅ Hook Codex vérifié et corrigé** : format confirmé en source `openai/codex`
(clone `/tmp/codex-src`). Le format initial était triplement erroné
(`sessionStart` vs `SessionStart` PascalCase ; structure sans niveau
`{"hooks":[…]}` ; `context:"inject"` inexistant ; `printf` brut alors que
`parse_session_start` exige un JSON `hookSpecificOutput.additionalContext`).
`hooks/codex-hooks.json` réécrit au format correct ; command vérifié (stdout
parse en JSON valide, `hookEventName: SessionStart`). Ambiguïté résiduelle sur
l'activation via manifest vs `hooks.json` en dossier de config (voir AUDIT.md).

**📋 Prochain** : ré-exécuter la grille de tests 🧪 (T1 repasse ✅ ; corriger
l'angle mort du test T7 qui validait le format `hooks` erroné), puis
✅ Validation.

**🚧 Blocages** : aucun.
