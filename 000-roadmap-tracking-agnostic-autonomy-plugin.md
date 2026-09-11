# Plan — `roadmap-tracking` : agnostique IDE/modèles + autonomie + plugin (axes A→E)

## Context

Généralisation du skill `roadmap-tracking` en vue d'un partage dans l'équipe.
Le socle validé (agnosticisme IDE + fournisseur de modèles) est complété par 5
axes : zéro dépendance externe (A), GitHub optionnel (B), exécution des tests par
l'agent (C), cohérence transverse (D), déclenchement par hook + packaging plugin
(E). Le tout doit rester **rétrocompatible** (Claude Code + GitHub, sans config =
comportement v1.3.0 actuel) et **sans sur-ingénierie** (config optionnelle,
chaque mode a un défaut par détection).

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

**1. Conversion du déclencheur en hook `userPromptSubmit`** :
- Script (node, comme ponytail) recevant `cwd`/`CLAUDE_PROJECT_DIR` par stdin.
- Logique : si `doc/roadmap/` existe dans le projet → **injecter une consigne
  courte** (exit 0 + stdout Claude / entrée `context` Codex) du type : « Projet
  roadmap-tracking : si le prompt concerne la création/analyse/cadrage/
  implémentation/reprise/test d'un plan, invoquer le skill roadmap-tracking et
  suivre son workflow. » Le **détail des 7 phases reste dans le skill**, pas
  dans l'injection (coût token maîtrisé).
- Injection **conditionnelle** → aucun surcoût sur les projets non-roadmap.
- Détection d'intention (créer/cadrer/reprendre…) faite par le **modèle** à
  partir de la consigne + du prompt réel — comme la règle actuelle.

**2. Deux variantes de hook** (vérifié en source Codex) :
- Claude Code : `hooks/hooks.json`, événement `UserPromptSubmit`.
- Codex : événement `userPromptSubmit` (casse ≠), modèle de *trust* (`/hooks` à
  valider par l'utilisateur, `allow_managed_hooks_only`). Injection via entrée
  `context`.
- Le plugin embarque les **deux** jeux (patron ponytail).

**3. Packaging plugin** :
```
roadmap-tracking-plugin/
├── .claude-plugin/plugin.json      # manifeste (name, hooks, description)
├── hooks/hooks.json                # variante Claude Code
├── hooks/<codex-hooks>             # variante Codex
├── hooks/trigger.mjs               # script de déclenchement conditionnel
└── skills/roadmap-tracking/        # le skill (auto-suffisant, axe A inclus)
```
- Installer le plugin apporte skill + hook ensemble : **plus aucune règle
  externe** requise.

**4. Prérequis dégradable** : `node` sur le PATH (comme ponytail). Absent → le
skill fonctionne toujours, seul l'auto-déclenchement se tait (pas d'erreur).

**5. Retrait de la règle** : `rules/roadmap-tracking.md` devient redondant pour
les utilisateurs du plugin. ⚠️ Sur ta propre machine (règle + plugin présents),
risque de **double injection** → retirer la règle à l'install du plugin.

**Force d'application** : identique à la règle actuelle (consigne NL suivie par
le modèle), voire meilleure (réinjectée fraîche chaque tour, conditionnelle).

---

## Fichiers impactés — synthèse

| Fichier | Nature |
|---|---|
| `SKILL.md` | Prerequisites, section complexité→tier, 3 gates, mode plan, Phase 5, clôture, Phase 7 (branches manuel/autonome), démarrage/migration conditionnels github |
| `references/environment.md` | **Nouveau** : mapping IDE, tiers+défauts Anthropic, formatage commandes (axe A), persona-switch (axe C), schéma config, détection |
| `references/autonomous-tests.md` | **Nouveau** : boucle vérif/exéc, reporting, garde-fou, prompt Vérificateur |
| `references/github-issues.md` | Conditionné « mode github uniquement » |
| `references/templates.md` | Front matter nullable + `plan.source`, tags `(taille·tier→modèle)`, `plan.link` local |
| `references/roadmap-file.md` | Format d'entrée sans issue (`[Plan: {id}]`) |
| `references/forms.md` | `AskUserQuestion` = mécanisme Claude Code + fallback texte |
| `references/migration.md` | Noter : github uniquement |
| `.claude-plugin/plugin.json` | **Nouveau** (axe E) : manifeste plugin |
| `hooks/hooks.json` + variante Codex + `hooks/trigger.mjs` | **Nouveau** (axe E) : hook de déclenchement conditionnel |
| `rules/roadmap-tracking.md` | **Retiré** (axe E) : remplacé par le hook ; contenu résumé en consigne injectée |

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
6. **Axe E — double injection** : règle `rules/` + hook plugin actifs ensemble →
   consigne dupliquée. Mitigation : retirer la règle à l'install.
7. **Axe E — dépendances** : `node` sur le PATH (dégradable), étape de *trust*
   Codex manuelle, coût token par tour (mitigé par injection conditionnelle).

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
- **Axe E** : installer le plugin sur un projet avec `doc/roadmap/` → la consigne
  s'injecte ; sur un projet sans → rien. `node` absent → skill OK, pas d'erreur.
  Vérifier l'absence de double injection règle+hook.

## Ordre de rédaction proposé (après approbation)

1. `references/environment.md` (socle A + agnostic + persona-switch).
2. `references/autonomous-tests.md` (axe C).
3. `SKILL.md` (branchements + gates + prerequisites).
4. `templates.md`, `github-issues.md`, `roadmap-file.md`, `forms.md`,
   `migration.md`.
5. **Axe E** : `.claude-plugin/plugin.json`, `hooks/` (variantes Claude+Codex +
   `trigger.mjs`), retrait de `rules/roadmap-tracking.md`.
