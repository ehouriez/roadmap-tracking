---
plan:
  id: 16
  source: local
  slug: robustesse-hooks-mecaniques-anti-bypass
  status: done
  complexity: M
  priority: high
  intent: production
  created_at: "2026-09-13"
  updated_at: "2026-09-13"
  issue:
    id: 16
    url: https://github.com/ehouriez/roadmap-tracking/issues/16
  comment: "Session de test avec succès: `claude --resume 35146e7b-b5bc-4b83-9b68-a1f5554e7398`"
---

# 16 — Robustesse du skill face aux modes système : garde mécanique (hooks)

## Objectif

Rendre le déclenchement du skill **robuste face aux directives système
concurrentes** (Ponytail « shortest path », Auto mode « don't stop »,
inertie « résous la tâche »). Le correctif du plan 14 avait durci le **texte**
injecté (SessionStart « NON NÉGOCIABLE »). Un test réel a montré que ce texte,
pourtant présent et adjacent au premier prompt, est **quand même** court-circuité :
une guerre de priorité texte-contre-texte est structurellement instable.

Le seul levier réellement définitif dans Claude Code est **mécanique** : un hook
qui refuse l'outil, pas un hook qui persuade.

## Analyse causale

- La directive roadmap-tracking demande une **action supplémentaire** (invoquer
  un skill). Ponytail/Auto ne font que **biaiser l'action déjà en cours**.
  Ajouter-une-action perd contre biaiser-l'action-courante sous inertie.
- SessionStart injecte **une fois** au boot. Même adjacent au 1ᵉʳ prompt, le
  texte perd ; et sur les tours suivants il s'éloigne dans le contexte.
- Aucun renfort de majuscules/emphase ne gagne cette guerre de façon définitive.

## Solution retenue

Deux hooks Claude Code (vérifiés via la doc officielle), **Option 1** validée par
l'utilisateur (garde mécanique uniquement sur les projets ayant adopté le skill) :

1. **`UserPromptSubmit`** — réinjecte à **chaque tour** un rappel de préséance
   nommant explicitement les modes concurrents (ils régissent le *comment* après
   engagement, jamais le *si* de l'invocation). Couvre le cold-start (projet sans
   `doc/roadmap/`) par un nudge fort. S'applique partout.
2. **`PreToolUse`** (`Write|Edit|MultiEdit|NotebookEdit`) — **ralentisseur
   one-shot par session** : refuse le **premier** appel d'outil mutant sur un
   projet ayant adopté le skill (`doc/roadmap/` présent), injectant la directive
   **au moment exact où l'implémentation démarre** (seul instant où le bypass
   turn-1 pouvait être intercepté), puis s'auto-désarme (marqueur
   `session_id`). Compatible désengagement (XS/proto) : ce n'est pas un mur, il
   suffit de réémettre l'appel après consultation du skill. N'intercepte jamais
   les écritures dans `doc/roadmap/`. Kill-switch `ROADMAP_TRACKING_AUTOSTART=off`.

**Codex** : support des événements `UserPromptSubmit`/`PreToolUse` **non vérifié**
→ traité conservativement (texte SessionStart de préséance uniquement, aucun
hook mécanique ajouté).

## Périmètre

**Inclus :**
- `hooks/pretooluse_gate.py` — nouveau script de garde (fail-open, one-shot/session).
- `hooks/hooks.json` — ajout des événements `UserPromptSubmit` et `PreToolUse`.
- `hooks/codex-hooks.json` — phrase de préséance dans le texte SessionStart.
- `SKILL.md` — note « Renfort mécanique » dans la garde d'entrée.
- Versioning plugin (2.7.2 → 2.8.0).

**Hors périmètre :**
- Blocage mécanique global (Option 2) — écarté (intrusif sur repos tiers).
- Support mécanique Codex — non vérifié, non implémenté.
- Rattrapage de roadmap.md pour les plans 13/14 manquants (gap préexistant).

## Étapes

- [x] Étape 1 — Écrire `hooks/pretooluse_gate.py` (fail-open, gate one-shot/session, allow-list `doc/roadmap/`) (M · standard → Sonnet)
- [x] Étape 2 — Ajouter les hooks `UserPromptSubmit` + `PreToolUse` dans `hooks/hooks.json` (S · standard → Sonnet)
- [x] Étape 3 — Renforcer le texte SessionStart de `hooks/codex-hooks.json` (préséance modes) (XS · standard → Sonnet)
- [x] Étape 4 — Documenter le renfort mécanique dans `SKILL.md` (garde d'entrée) (XS · standard → Sonnet)
- [x] Étape 5 — Bump de version 2.7.2 → 2.8.0 (plugin.json, SKILL.md, codex plugin.json) (XS · standard → Sonnet)
- [x] 🧪 Tests — Validation JSON + tests fonctionnels de la gate + validation live en session Claude Code
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Tests

### Procédure de test

```bash
echo "=== Validate Hook JSON Syntax ==="
python3 -c "import json; json.load(open('hooks/hooks.json', encoding='utf-8')); print('hooks.json OK')"

echo "=== Validate Codex Hook JSON Syntax ==="
python3 -c "import json; json.load(open('hooks/codex-hooks.json', encoding='utf-8')); print('codex-hooks.json OK')"

echo "=== Compile Gate Script ==="
python3 -m py_compile hooks/pretooluse_gate.py

echo "=== Gate Denies First Mutating Call In Adopted Project ==="
PROJ=$(mktemp -d); mkdir -p "$PROJ/doc/roadmap"; SID="t-$$"; rm -f "${TMPDIR:-/tmp}/roadmap-tracking-gate-$SID"
echo "{\"cwd\":\"$PROJ\",\"session_id\":\"$SID\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$PROJ/src/app.py\"}}" | python3 hooks/pretooluse_gate.py

echo "=== Gate Allows Second Call Same Session ==="
echo "{\"cwd\":\"$PROJ\",\"session_id\":\"$SID\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$PROJ/src/app.py\"}}" | python3 hooks/pretooluse_gate.py

echo "=== Gate Allows Plan-File Target ==="
rm -f "${TMPDIR:-/tmp}/roadmap-tracking-gate-$SID"
echo "{\"cwd\":\"$PROJ\",\"session_id\":\"$SID\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$PROJ/doc/roadmap/15-x.md\"}}" | python3 hooks/pretooluse_gate.py

echo "=== Gate Allows Non-Adopted Project ==="
BARE=$(mktemp -d)
echo "{\"cwd\":\"$BARE\",\"session_id\":\"$SID\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$BARE/x.py\"}}" | python3 hooks/pretooluse_gate.py

echo "=== Gate Allows When Kill-Switch Off ==="
rm -f "${TMPDIR:-/tmp}/roadmap-tracking-gate-$SID"
echo "{\"cwd\":\"$PROJ\",\"session_id\":\"$SID\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$PROJ/x.py\"}}" | ROADMAP_TRACKING_AUTOSTART=off python3 hooks/pretooluse_gate.py

rm -rf "$PROJ" "$BARE"
```

**Résultats attendus :**
- Les deux JSON parsent sans erreur ; le script compile.
- Cas 1 → sortie JSON `permissionDecision: "deny"` avec la raison.
- Cas 2, 3, 4, 5 → **sortie vide** (allow).

### Validation live (opérateur — obligatoire avant `done`)

La gate n'agit qu'une fois le plugin **réinstallé/mis à jour** et la **session
Claude Code redémarrée** (les hooks sont chargés au boot). Procédure :

1. Mettre à jour le plugin depuis ce repo, redémarrer Claude Code.
2. Sur un projet **avec** `doc/roadmap/`, au 1ᵉʳ prompt de dev, tenter d'écrire
   du code → le 1ᵉʳ `Write/Edit` doit être **refusé une fois** avec la directive.
3. Vérifier que la réémission (ou l'invocation du skill) passe ensuite.
4. Sur un projet **sans** `doc/roadmap/`, vérifier **aucun** blocage (nudge UPS
   seulement).

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-13 | `hooks.json` JSON valide | pas d'erreur | `valid JSON` | ✅ PASS |
| 2026-09-13 | `codex-hooks.json` JSON valide | pas d'erreur | `valid JSON` | ✅ PASS |
| 2026-09-13 | `pretooluse_gate.py` compile | pas d'erreur | `gate compiles` | ✅ PASS |
| 2026-09-13 | Cas 1 — 1ᵉʳ write projet adopté | DENY + raison | JSON deny émis | ✅ PASS |
| 2026-09-13 | Cas 2 — 2ᵉ write même session | allow (vide) | sortie vide | ✅ PASS |
| 2026-09-13 | Cas 3 — cible fichier plan | allow (vide) | sortie vide | ✅ PASS |
| 2026-09-13 | Cas 4 — projet non adopté | allow (vide) | sortie vide | ✅ PASS |
| 2026-09-13 | Cas 5 — kill-switch off | allow (vide) | sortie vide | ✅ PASS |
| 2026-09-13 | Validation live en session Claude Code | refus 1×/session | 5/5 PASS rejoués manuellement par l'opérateur dans le terminal | ✅ PASS |

## Journal de session

### Session 2026-09-13

- Analyse causale : texte-vs-texte ininstable ; seul un refus d'outil (mécanique)
  est définitif. Cf. reproduction du bypass en début de session.
- Vérifié via `claude-code-guide` : `UserPromptSubmit` réinjecte à chaque tour ;
  `PreToolUse` refuse via `permissionDecision: "deny"` ; `${CLAUDE_PLUGIN_ROOT}`
  résout la racine du plugin ; support hooks Codex au-delà de SessionStart **non
  vérifié** (traité conservativement).
- Implémentation : script gate fail-open one-shot/session + 2 hooks + note SKILL
  + préséance Codex. Tests fonctionnels 8/8 PASS ; validation live à jouer.
