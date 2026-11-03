# Référence — plugin-config

Deux manifestes de plugin pour les marketplaces Claude Code et Codex.

---

## .claude-plugin/plugin.json

```json
{
  "name": "roadmap-tracking",
  "description": "Frame, plan, track and trace dev/config/architecture requests through plan files, a consolidated roadmap.md and linked GitHub issues (strict 7-phase workflow).",
  "version": "4.2.0",
  "author": { "name": "Emmanuel Houriez" },
  "homepage": "https://github.com/ehouriez/roadmap-tracking",
  "repository": "https://github.com/ehouriez/roadmap-tracking",
  "license": "MIT"
}
```

Claude Code découvre `hooks/hooks.json` par convention à l'installation (pas de champ `hooks` explicite dans le manifeste).

---

## .codex-plugin/plugin.json

Identique à `.claude-plugin/plugin.json` avec un champ supplémentaire :

```json
{
  "name": "roadmap-tracking",
  "version": "4.2.0",
  "author": { "name": "Emmanuel Houriez" },
  "homepage": "https://github.com/ehouriez/roadmap-tracking",
  "repository": "https://github.com/ehouriez/roadmap-tracking",
  "license": "MIT",
  "hooks": "./hooks/codex-hooks.json"
}
```

Codex exige que le chemin du fichier hooks soit déclaré explicitement via la clé `hooks`.

---

## Métadonnées partagées

| Champ | Valeur |
|---|---|
| `name` | `roadmap-tracking` |
| `version` | `4.2.0` |
| `author` | Emmanuel Houriez |
| `homepage` | `https://github.com/ehouriez/roadmap-tracking` |
| `license` | MIT |

---

## Fichier .claude-plugin/marketplace.json

Présent dans `.claude-plugin/` ; gère les métadonnées spécifiques à la marketplace Claude Code (indexation, tags, description longue).

---

## Installation

```bash
echo "=== Add Public Marketplace ==="
claude plugin marketplace add ehouriez/roadmap-tracking

echo "=== Install Skill Plugin ==="
claude plugin install roadmap-tracking@roadmap-tracking
```

```bash
echo "=== Install Codex Plugin ==="
/plugin install roadmap-tracking@roadmap-tracking
```
