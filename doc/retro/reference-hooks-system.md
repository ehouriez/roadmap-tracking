# Référence — hooks-system

> Voir aussi : [Explication hooks-system](explanation-hooks-system.md)

Trois artefacts dans `hooks/` qui injectent des directives de contrôle de flux à l'initialisation de session, à chaque prompt utilisateur et au premier appel d'outil mutant.

---

## Vue d'ensemble

| Fichier | IDE cible | Événements couverts |
|---|---|---|
| `hooks/hooks.json` | Claude Code | `SessionStart`, `UserPromptSubmit`, `PreToolUse` |
| `hooks/codex-hooks.json` | Codex | `SessionStart` |
| `hooks/pretooluse_gate.py` | Claude Code | Déclenché par `PreToolUse` |

**Kill-switch global** : variable d'environnement `ROADMAP_TRACKING_AUTOSTART=off`.

---

## hooks.json — Claude Code

Trois hooks :

### SessionStart

Injecte la directive de contrôle de flux (français) dans le contexte de session avant le premier prompt.

```bash
test "${ROADMAP_TRACKING_AUTOSTART:-on}" != "off" && printf '...' || true
```

Fail-open via `|| true`.

### UserPromptSubmit

Réinjecte un rappel de préséance à chaque tour utilisateur.

```bash
test "${ROADMAP_TRACKING_AUTOSTART:-on}" != "off" && printf '...' || true
```

### PreToolUse

- **Matcher** : `Write|Edit|MultiEdit|NotebookEdit` (outils mutants uniquement)
- **Commande** : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/pretooluse_gate.py" || true`
- `CLAUDE_PLUGIN_ROOT` injecté par Claude Code au chargement du plugin

---

## codex-hooks.json — Codex

Un seul hook `SessionStart` avec enveloppe JSON `hookSpecificOutput`.

Message en **anglais** (fiabilité d'instruction-following supérieure sur les modèles OpenAI).

Déclaré dans `.codex-plugin/plugin.json` via la clé `hooks`.

---

## pretooluse_gate.py

### Interface

- **Entrée** : payload JSON PreToolUse sur stdin
- **Sortie** : JSON allow/deny sur stdout
- **Exit code** : toujours 0

### Logique

```
1. Lire le payload JSON (stdin)
2. Vérifier ROADMAP_TRACKING_AUTOSTART != "off"
3. Résoudre le marqueur de session :
   {tempdir}/roadmap_tracking_gate_{session_id}.lock
4. SI marqueur absent
   ET doc/roadmap/ présent dans CWD
   ET cible n'est pas un fichier plan (target_is_plan_file() == False)
   → Écrire le marqueur (auto-désarmement)
   → Retourner JSON de refus
5. SINON → Retourner JSON d'autorisation
```

### `target_is_plan_file()`

Vérifie que `doc/roadmap/` apparaît dans le chemin absolu normalisé du fichier cible. Si vrai → jamais intercepté.

### Clé `session_id`

Lue depuis le payload JSON. Si absente ou `"unknown"` → toutes les sessions partagent le même marqueur.

### Comportement fail-open

Tout payload malformé ou exception → autorisation inconditionnelle.

### Effet one-shot

Le gate intercepte exactement une fois par session (via le fichier marqueur). Une fois désarmé, toutes les écritures suivantes passent sans interception.

---

## Cas limites notables

| Situation | Comportement |
|---|---|
| `session_id` absent ou `"unknown"` | Toutes sessions partagent le même marqueur |
| Payload JSON malformé | Fail-open (autorisation) |
| Écriture du marqueur échoue (tmp read-only) | Deny émis mais gate non désarmée |
| Cible dans `doc/roadmap/` | Jamais interceptée (`target_is_plan_file()`) |
