# Rapport d'audit — Plan #000

> Audit en lecture seule de l'implémentation réalisée sur le plan
> `000-roadmap-tracking-agnostic-autonomy-plugin.md` (axes A→E, étapes 1-8).
> Comparaison étape par étape entre ce que le plan demande et ce qui est présent
> dans les fichiers. **Aucun fichier de l'implémentation n'a été modifié.**
>
> Date : 2026-09-11 · Modèle : Claude Opus 4.8 (1M context)

---

**Étape 1 — `references/environment.md`**
- ✅ Conforme : mapping actions génériques `Claude Code | Codex | Fallback` (`environment.md:57-66`), taxonomie tiers + défauts Anthropic (`22-39`), section « Operator Commands Formatting » embarquée / axe A (`136-187`), persona-switch sous-agent (`69-86`), schéma `.skill-config.yml` complet (`105-128`), procédure de détection (`89-102`).
- Aucun écart.

**Étape 2 — `references/autonomous-tests.md`**
- ✅ Conforme : rôles Exécuteur/Vérificateur (`11-21`), boucle test→fix→retest (`24-43`), garde-fou 3 itérations (`54-82`), format de reporting (`86-120`), prompt système Vérificateur reproduit **mot pour mot** le plan L176-193 (`128-147`), fallback inline honnête (`151-169`).
- Aucun écart.

**Étape 3 — `SKILL.md` : agnosticisme modèle/tier**
- ✅ Conforme : Prerequisites auto-suffisants (`SKILL.md:39-46`), matrice complexité→tier (`248-255`), détection du tier actif (`257-269`), 3 gates en tiers (Phase 1.5 `412-428`, re-check Phase 3 `467-472`, gate Phase 7 `612-641`), tags `(taille · tier → modèle)` (`326-334`).
- ⚠️ Partiel : le plan demandait de « renommer `## Compatibilité mode plan` ». La section est devenue `## Compatibilité avec le mode plan` (`521`) — reformulation cosmétique, l'intention (généricité IDE via renvoi `environment.md`) est bien tenue (`530`). Non bloquant.

**Étape 4 — `SKILL.md` : GitHub optionnel**
- ✅ Conforme : listing avec `❌ Local` (`110-112`), détection d'ID et migration conditionnées github (`120-122`), Phase 3 `{ID}` (`481-482`), Phase 5 deux branches (`541-561`), numérotation locale max+1 + `plan.source` (`555-556`), clôture branchée (`712-719`).
- Aucun écart.

**Étape 5 — `SKILL.md` : tests manuel/autonome**
- ✅ Conforme : branches manual/autonomous sur Phase 7 étape 0 (`647-650`), tests intermédiaires (`730-735`), 🧪 Tests (`796-802`), ✅ Validation (`866-874`), reprise (`954-963`) ; suppression étape 0 en autonome ✅ ; `⏸️` de clôture après `PASS` (`800-801`).
- Aucun écart.

**Étape 6 — `SKILL.md` : offre de création `doc/roadmap/`**
- ✅ Conforme : cas préalable « `doc/roadmap/` absent » avec question oui/non puis workflow (`74-91`), rappel en Applicabilité (`74-77`).
- Aucun écart.

**Étape 7 — Fichiers de référence restants**
- ✅ Conforme : `templates.md` front matter nullable + `plan.source` + deux exemples github/local (`templates.md:44-118`), `github-issues.md` guard github (`3-6`), `roadmap-file.md` entrée `[Plan: {id}]` (`53-59`), `forms.md` fallback texte (`5-10`), `migration.md` note github (`3-5`).
- Aucun écart.

**Étape 8 — Packaging plugin (axe E)**
- ✅ Conforme : `hooks/hooks.json` (SessionStart + `test -d` + `AUTOSTART`), `hooks/codex-hooks.json` (sessionStart), `README.md` réécrit (hook embarqué, interrupteur, warning double injection).
- ❌ **Écart critique** : la clé `hooks` de `.claude-plugin/plugin.json:9-12` utilise un format **non reconnu par Claude Code**. `claude plugin validate .` (T1) retourne :
  > `hooks.claude-code: unknown hook event; entry ignored at runtime`
  > `hooks.codex: unknown hook event; entry ignored at runtime`

  Claude Code attend des **noms d'événements** (`SessionStart`…), pas des identifiants d'IDE (`claude-code`/`codex`). Conséquence : **les hooks sont ignorés à l'exécution** → l'objectif central de l'axe E (hook embarqué **actif** au `SessionStart`) **n'est pas atteint**. Ironie : l'implémentation correspond exactement à ce que le test T7 attendait — le test valide donc un format erroné.
- ⚠️ Partiel : le plan (lignes 33-35, « À re-vérifier Étape 8 ») imposait de **re-confirmer la structure de config exacte du hook Codex** (`sessionStart`, format, trust `/hooks`) en source Codex avant de l'écrire. Le journal de session est **muet** sur cette vérification ; `codex-hooks.json` emploie `"context": "inject"` — non tracé comme vérifié.

---

### Écarts transverses (hors découpage par étape)

- ⚠️ **Incohérence de version** (Axe D — cohérence) : `SKILL.md:16` porte encore `version: "1.3.0"` alors que `plugin.json:8` = `2.0.0` et que `README.md:14` annonce « Key features (v2.0.0) ». Le plan ne demandait pas explicitement le bump de SKILL.md, mais l'axe D visait la cohérence transverse.
- ⚠️ **Isolation Vérificateur affaiblie** (Axe C, plan L145-147 « sous-agent isolé, process/contexte distinct ») : `environment.md:75` mappe Claude Code sur « `Agent` tool — fresh agent **or fork** ». Un *fork* **hérite du contexte complet** de l'agent parent — il ne satisfait donc pas l'isolation exigée (« l'agent ne note pas sa propre copie »). Seul « fresh agent » est réellement isolé. Proposer le fork comme équivalent contredit la décision du plan.

---

### Synthèse

- **Étapes conformes** : 5/8 (1, 2, 4, 6, 7) sans réserve.
- **Étapes avec réserve mineure** : 2/8 (3 = renommage cosmétique ; conforme sur le fond).
- **Étapes avec écart critique** : 1/8 (**8**).

**Écarts critiques (bloquants)**
1. `.claude-plugin/plugin.json:9-12` — format de la clé `hooks` invalide → hooks **ignorés au runtime**, axe E non fonctionnel. Bloque le livrable principal de l'étape 8.

**Écarts mineurs (non bloquants)**
1. Vérification du format hook Codex (`codex-hooks.json`, `context: inject`) non tracée — exigée par le plan L33-35.
2. Incohérence de version `SKILL.md` (1.3.0) vs `plugin.json`/`README` (2.0.0).
3. `environment.md:75` propose « fork » comme sous-agent Vérificateur → casse l'isolation exigée (Axe C).
4. Cosmétique : renommage de section `## Compatibilité avec le mode plan` (Étape 3).

**Point de méthode** : le test T7 de la procédure valide le format `hooks` erroné (il vérifie sa présence, pas sa validité runtime). T1 est le seul test qui a détecté le défaut. La grille de tests contient donc un angle mort à corriger — hors scope de cet audit (aucune correction proposée ici).

---

## Suivi des correctifs (post-audit — Étape 9 du plan)

Correctifs appliqués le 2026-09-11 (Opus 4.8) en réponse à cet audit.

| Écart | Sévérité | Statut | Détail |
|---|---|---|---|
| `plugin.json` clé `hooks` invalide | Critique | ✅ Corrigé | Remplacé par `"hooks": "./hooks/hooks.json"` (chemin string, format Claude Code reconnu). `claude plugin validate .` → **Validation passed** sans warning. Le fichier `hooks/codex-hooks.json` reste sur disque (artefact Codex documenté) mais n'est **plus déclaré** dans le manifest → plus de warning. |
| Version `SKILL.md` | Mineur | ✅ Corrigé | `metadata.version` : `1.3.0` → `2.0.0`, aligné sur `plugin.json` et `README.md`. |
| Isolation Vérificateur (« fork ») | Mineur | ✅ Corrigé | `environment.md` : le mécanisme sous-agent Claude Code ne mentionne plus « fork » (qui hérite du contexte parent) — uniquement « fresh agent » réellement isolé. |
| Format hook Codex (`sessionStart` / `context: inject`) | Mineur | ✅ Corrigé | Vérifié en source `openai/codex` : le format initial était triplement erroné (`sessionStart` au lieu de `SessionStart` PascalCase ; structure sans niveau `{"hooks":[…]}` ; champ `context:"inject"` inexistant ; `printf` texte brut alors que `parse_session_start` exige un JSON `hookSpecificOutput.additionalContext`). `hooks/codex-hooks.json` réécrit au format correct (`config/src/hooks_tests.rs:13-57`, `output_parser.rs:93-98`, schéma `session-start.command.output`). Command vérifié : stdout parse en JSON valide. **Ambiguïté résiduelle** : `plugin-json-spec.md:215` indique que la validation marketplace Codex rejette le champ `hooks` du manifest → l'activation passe peut-être par un `hooks.json` en dossier de config plutôt que par le manifest ; à trancher au déploiement Codex réel. |
| Renommage section `## Compatibilité avec le mode plan` | Cosmétique | ➖ Non traité | Conforme sur le fond, aucune action requise. |
