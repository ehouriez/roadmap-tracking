## Contexte

Généralisation du skill `/roadmap-tracking` en vue d'un partage dans l'équipe.
Le socle validé (agnosticisme IDE + fournisseur de modèles) est complété par
**5 axes d'évolution** (A→E). Le tout reste **rétrocompatible** (Claude Code +
GitHub, sans config = comportement v1.3.0) et **sans sur-ingénierie** (config
optionnelle, chaque mode a un défaut par détection).

> Ce document décrit les axes **tels qu'ils ont été tranchés et livrés** (plan
> `1-roadmap-tracking-agnostic-autonomy-plugin.md`, plugin **v2.0.0**). Les
> points laissés ouverts dans la demande initiale y figurent avec la décision
> retenue.

---

## Axes d'évolution

### Axe A — Zéro dépendance aux règles externes

**Problème** : le skill exigeait la présence de `operator-commands-formatting.md`
dans `rules/` du dossier personnel `.claude/` — prérequis fragile et non
portable (un collègue qui clone sans cette règle obtient un comportement dégradé
silencieux).

**Décision retenue** :
- Le contenu de `operator-commands-formatting.md` est **embarqué comme section
  de `references/environment.md`** (« Operator Commands Formatting »), **pas** de
  fichier séparé — cohérent avec « minimiser les fichiers ».
- `SKILL.md ## Prerequisites` réécrit : ne cite plus aucune règle externe, pointe
  vers `references/environment.md`.
- La règle personnelle `~/.claude/rules/operator-commands-formatting.md` peut
  rester chez l'utilisateur mais **n'est plus un prérequis**.
- Le skill est **auto-suffisant** : cloner `skills/roadmap-tracking/` suffit.

### Axe B — Gestion des issues GitHub optionnelle

**Problème** : le skill supposait un projet GitHub avec gestion d'issues, ce qui
n'est pas toujours le cas.

**Décision retenue — 2 modes effectifs** (les 4 cas envisagés initialement se
réduisent à 2 comportements ; privé/public n'est qu'une info descriptive, pas
une branche) :

| Mode | Condition | Comportement |
|---|---|---|
| **`github`** | Projet GitHub (privé ou public), `gh` disponible | Fonctionnement v1.3.x : issues automatiques via `gh`, ID de plan = numéro d'issue |
| **`local`** | Hors GitHub **ou** opt-out utilisateur | Pas d'issue GitHub. Plans sous `./doc/roadmap/`, ID auto-incrémenté localement |

**1. Détection & choix** :
- Au 1er lancement : détecter `.git/`, remote GitHub, `gh auth status`.
- **Proposer** le mode via l'action « poser une question » → **confirmer** →
  **persister** dans `.skill-config.yml` (`issues.mode`).
- Changement de mode = éditer la config (ou commande explicite). Non
  détectable/non confirmé → ne pas bloquer, demander une fois.

**2. Numérotation locale (mode `local`)** :
- ID = `max(préfixes numériques de ./doc/roadmap/*.md) + 1`, entier nu.
- Marqueur `plan.source: local` en front matter ; `issue.id`/`issue.url` = `null`.
- **Concurrence** : pas de verrou distribué (YAGNI). Collision éventuelle
  **résolue par git** au merge — documentée, pas masquée.

**3. Impact workflow (branches conditionnelles explicites, pas de `if` caché)** :
- Règle de démarrage / détection d'ID incohérents / migration : **`github`
  uniquement**. En `local`, le contrôle `plan.id == issue.id` et la migration
  sont désactivés et signalés.
- Phase 5 : branche `github` (issue d'abord, puis fichier) vs branche `local`
  (calcul ID local, fichier direct, aucune issue).
- Clôture : `github` → `gh issue close/comment` ; `local` → `status: done` seul.
- Reprise / listing : colonne « Issue » → `❌ Local` en mode `local`.

**4. Impact fichiers de référence** :
- `github-issues.md` et `migration.md` : préfixés « **mode `github`
  uniquement** ».
- `templates.md` : `plan.id` découplé de `issue.id` ; `plan.link`, `issue.id`,
  `issue.url` **nullable** proprement + ajout `plan.source`. En `local`,
  `plan.link` = chemin relatif `doc/roadmap/{id}-slug.md`.
- `roadmap-file.md` : format d'entrée alternatif `[Plan: {id}]` (sans issue).

### Axe C — Exécution des tests par l'agent (mode autonome)

**Problème** : le skill supposait que l'agent n'a **pas** accès à l'env de test
(il rédige une procédure, attend les résultats de l'opérateur). Or certains IDE
(Claude Code shell, Codex sandbox) permettent à l'agent d'exécuter les tests.

**Décision retenue — 2 modes** : `manual` (actuel, **défaut**) / `autonomous`
(**opt-in explicite**).

> ⚠️ **Rétrocompat** : le mode autonome ne se déclenche **jamais** par simple
> détection d'un accès shell — sinon on casse le comportement v1.3.0. La
> détection *propose*, la config ou une confirmation *active*.

**Mode autonome — spécifications** :
- **L'étape 0 de la Phase 7 est supprimée** (tous les tests s'exécutent après
  chaque étape, pas de question sur les tests intermédiaires).
- **Les procédures de tests restent écrites dans le plan** (traçabilité).
- Le bloc `📦 Commit proposé` n'apparaît **qu'après** verdict `PASS` et reste
  **une proposition — jamais exécutée** (règle globale « ne jamais gérer
  commit/push »). Le mode autonome n'auto-commit pas.
- `🧪 Tests` finaux : même boucle ; le `⏸️` de clôture se déplace **après** le
  `PASS`.

#### Architecture à deux rôles : Vérificateur ≠ Exécuteur

La boucle test→fix→retest repose sur une **séparation stricte des rôles** :
l'agent qui implémente (Exécuteur) n'est **jamais** celui qui juge les résultats
(Vérificateur). Principe : **« L'agent ne note pas sa propre copie. »**

**Contrat du Vérificateur** : exécute les tests et compare obtenu vs attendu ;
accès aux **résultats uniquement** (aveugle au code d'implémentation) ; ne
corrige/suggère/modifie **jamais** ; sortie = verdict `PASS`/`FAIL` + diagnostic
factuel ; sans mémoire entre itérations ; existe le temps de rendre le verdict.

**Contrat de l'Exécuteur** : implémente, analyse root causes, corrige, met à jour
les tests ; ne juge jamais ses propres résultats ; seul un verdict `PASS` du
Vérificateur autorise la sortie de boucle.

**Isolation — décision (vérifiée en source)** : Claude Code (`Agent`) **et**
Codex (`spawn_agent` + rôles d'agent) exposent de **vrais sous-agents**. Donc :
- **Mode autonome = sous-agent réel obligatoire** — le Vérificateur est toujours
  un **fresh agent** isolé (pas un *fork* : un fork hériterait du contexte parent
  et casserait l'isolation) portant le prompt système dédié.
- **IDE sans sous-agent** (hors périmètre) : **secours `inline` = auto-check
  honnête** — l'agent exécute et rapporte factuellement observé vs attendu, sans
  revendiquer une indépendance qu'il n'a pas.
- Mécanisme documenté dans `references/environment.md` ; config
  `tests.verifier: auto | subagent | inline`.

**Garde-fou = 3 itérations (décidé)** : itération 1 corrige l'évident, itération
2 rattrape un cas manqué ; un 3ᵉ échec signale que le diagnostic/l'approche est
faux → l'humain tranche. Puis STOP + diagnostic + question à l'utilisateur.
Interruption manuelle (« stop ») possible à tout moment. Surchargable via
`tests.max_iterations`.

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

**Prompt système du Vérificateur (livré)** :

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

**Impact fichiers** : le gros de la mécanique autonome (boucle, reporting,
garde-fou, prompt Vérificateur, fallback inline) part dans un **nouveau
`references/autonomous-tests.md`** ; `SKILL.md` n'orchestre que le branchement
(chaque bloc de Phase 7 reçoit deux branches `manual`/`autonomous`).

### Axe D — Cohérence & `.skill-config.yml` unique

Tous les axes convergent vers **un seul** fichier optionnel :

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

### Axe E — Déclenchement par hook + packaging plugin

**Objectif** : sortir le déclencheur `~/.claude/rules/roadmap-tracking.md` du
périmètre des prérequis externes. Distribution retenue : **plugin installable**
(`/plugin install` depuis un marketplace git interne) embarquant `skills/` +
`hooks/`.

**Répartition (validée)** : le **hook injecte**, le **modèle juge**. Le hook ne
fait aucune détection d'intention (tâche sémantique = modèle) ; il n'est que la
**porte déterministe** + l'injection d'une consigne courte.

**Deux cas séparés (anti-harcèlement)** :
- **Cas 1 — `doc/roadmap/` présent** → le hook embarqué injecte la consigne.
- **Cas 2 — `doc/roadmap/` absent** → hook **silencieux** (zéro nag). L'offre de
  créer `doc/roadmap/` vient du **skill**, sur demande de dev/plan.

**1. Déclencheur = hook `SessionStart` embarqué** :
- Commande shell : si `doc/roadmap/` existe → injecter une consigne courte
  (stdout injecté en contexte) invitant à invoquer le skill ; le détail des 7
  phases reste dans le skill.
- Injecté **une fois par session**, **conditionnel** (`test -d`).
- Interrupteur `ROADMAP_TRACKING_AUTOSTART=off` pour couper l'auto-déclenchement.
- `userPromptSubmit` écarté (coût par tour non justifié).

**2. Deux variantes de hook** (vérifié en source Codex) :
- Claude Code : `hooks/hooks.json`, événement `SessionStart`.
- Codex : `hooks/codex-hooks.json`, événement `SessionStart` (PascalCase),
  handler `type: command` émettant un JSON `hookSpecificOutput.additionalContext`
  (format confirmé en source `openai/codex`). Modèle de *trust* Codex : le hook
  n'agit qu'une fois approuvé via `/hooks`.
- ⚠️ **Ambiguïté résiduelle non tranchée** : activation d'un hook de plugin côté
  Codex via le manifest vs via un `hooks.json` déposé en dossier de config — à
  trancher lors d'un vrai déploiement Codex.

**3. Packaging plugin** (layout réel « skill à la racine ») :
```
roadmap-tracking/            # racine = le plugin
├── .claude-plugin/
│   ├── plugin.json          # clé "hooks": "./hooks/hooks.json" ; version 2.0.0
│   └── marketplace.json     # existant
├── hooks/hooks.json         # variante Claude Code (SessionStart)
├── hooks/codex-hooks.json   # variante Codex (SessionStart)
├── SKILL.md                 # à la racine (auto-suffisant, axe A inclus)
├── references/
└── scripts/
```
Pas de sous-dossier `skills/`. Pas de script node : `test -d … && printf …`
suffit côté Claude Code.

**4. Embarqué (décidé)** : le hook est livré actif dans le plugin (remplace la
section opt-in du README), avec l'interrupteur pour le couper.

**5. Règle `~/.claude/rules/roadmap-tracking.md`** : hors du repo plugin (config
perso), **pas un livrable**. ⚠️ Sur une machine qui installe le plugin (hook
embarqué) **et** garde la règle → **double injection** ; retirer l'une des deux.

---

## Contraintes transverses

- **Rétrocompatibilité stricte** : Claude Code, sans `.skill-config.yml`, projet
  GitHub → **exactement** le comportement v1.3.0.
- **Pas de sur-ingénierie** : config optionnelle, chaque mode a un fallback par
  détection automatique.
- **Workflow inchangé** : les 7 phases, points d'arrêt et règles absolues
  restent ; seuls les **mécanismes sous-jacents** (issues, tests, commandes IDE,
  persona switch, déclenchement) deviennent adaptatifs.
- **Un seul fichier de config** : `.skill-config.yml` centralise tout (IDE,
  modèles, mode issues, mode tests, mécanisme Vérificateur).
- **Maintenabilité** : chaque point de variabilité modifiable à un seul endroit ;
  mécanique lourde (autonomous-tests, environment) hors de `SKILL.md`, qui reste
  orchestrateur.

## Livrable — état livré (plugin v2.0.0)

Le plan d'architecture a été produit, **approuvé**, puis **implémenté**. Livré :

1. **Les 5 axes A→E intégrés** au skill.
2. **Fichiers créés** : `references/environment.md` (socle transverse : mapping
   IDE, tiers+défauts Anthropic, formatage commandes, persona-switch, schéma
   config, détection) et `references/autonomous-tests.md` (boucle vérif/exéc,
   reporting, garde-fou, prompt Vérificateur, fallback inline).
3. **Fichiers modifiés** : `SKILL.md` (Prerequisites, complexité→tier, gates,
   Phase 5 github/local, clôture conditionnelle, Phase 7 manual/autonomous,
   démarrage/migration github-only, offre création `doc/roadmap/`),
   `github-issues.md` + `migration.md` (guard github), `templates.md` (front
   matter nullable + `plan.source`), `roadmap-file.md` (`[Plan: {id}]`),
   `forms.md` (fallback texte AskUserQuestion).
4. **Packaging** : `.claude-plugin/plugin.json` (clé `hooks`, version `2.0.0`),
   `hooks/hooks.json` (Claude Code) + `hooks/codex-hooks.json` (Codex),
   `README.md` réécrit (features v2.0.0, hook embarqué, warning double injection).
5. **Décisions tranchées** : emplacement axe A = `environment.md` ; 2 modes issues
   (`github`/`local`) ; garde-fou = 3 itérations ; Vérificateur = sous-agent réel
   (fresh agent, pas de fork) + fallback `inline` ; schéma `.skill-config.yml`
   complet.
6. **Validation** : `claude plugin validate .` → passed ; grille de tests
   **T1→T13 = 13/13 ✅**.

**Points ouverts** : activation du hook Codex (manifest vs dossier de config) —
non bloquant, à trancher lors d'un vrai déploiement Codex.

## Risques identifiés

1. **Bloat / maintenabilité** (risque principal) : 5 axes sur un skill dense →
   mécanique lourde poussée hors de `SKILL.md` (orchestrateur).
2. **Isolation Vérificateur** : réelle via sous-agent (CC + Codex) ; `inline` =
   garantie moindre mais transparente. Vigilance coût/latence, ne pas sur-vendre
   le verdict `inline`.
3. **Concurrence numérotation locale** : git = point de réconciliation, pas de
   verrou (assumé).
4. **Rétrocompat** : modes autonome/local doivent rester opt-in/confirmés → tests
   de non-régression ciblés.
5. **Double-branche partout** : `manual`/`autonomous` × `github`/`local` → matrice
   de cas explicite pour couvrir les combinaisons.
6. **Axe E — double injection** : règle perso + hook plugin → retirer l'une.
7. **Axe E — trust Codex** : étape `/hooks` manuelle côté Codex.
8. **Axe E — layout** : plugin « skill à la racine », pas de sous-dossier
   `skills/`.
