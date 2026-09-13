# roadmap-tracking

A Claude Code skill (packaged as a plugin) to **frame, plan, track and trace**
any development, configuration or architecture request through:

- plan files in `./doc/roadmap/{id}-slug.md`,
- a consolidated backlog in `./doc/roadmap/roadmap.md`,
- linked GitHub issues *(optional — local mode available)*.

Drives a strict **7-phase workflow** — silent analysis, interactive scoping,
plan proposal, validation, plan creation, validation, then step-by-step
implementation — with hard stop points between planning and coding.

## Key features

| Feature | Description |
|---|---|
| **Multi-IDE** | Claude Code, Codex, or any IDE (fallback text mode) |
| **IDE-agnostic tiers** | Reasons in `standard`/`reasoning` tiers, not model versions |
| **GitHub optional** | `issues.mode: github` (default) or `local` (counter-based IDs, no `gh` needed) |
| **Autonomous tests** | `tests.mode: autonomous` — Executor/Verifier loop with real sub-agents |
| **Self-contained** | No external rule files needed — all formatting rules embedded |
| **Embedded hook** | `SessionStart` hook fires automatically when `doc/roadmap/` exists |

## Install

```bash
echo "=== Add Public Marketplace From GitHub ==="
claude plugin marketplace add ehouriez/roadmap-tracking

echo "=== Install The Skill Plugin ==="
claude plugin install roadmap-tracking@roadmap-tracking

echo "=== Verify Marketplace ==="
claude plugin marketplace list

echo "=== Verify Plugin Installation ==="
claude plugin list
```

The skill is then available as `/roadmap-tracking:roadmap-tracking` and is also
model-invoked automatically when a task matches its description.

## Update

From a fresh session launched in the repo:

```bash
echo "=== Start A Fresh Session In The Repo ==="
cd /path/to/your/project && claude
```

Then inside the session:

```
/plugin marketplace update roadmap-tracking
/plugin update roadmap-tracking
/clear
```

## Uninstall

```bash
echo "=== Uninstall Plugin ==="
claude plugin uninstall roadmap-tracking@roadmap-tracking

echo "=== Remove Marketplace ==="
claude plugin marketplace remove roadmap-tracking
```

## Auto-trigger at session start

The plugin ships with an **embedded `SessionStart` hook** that fires
automatically when `doc/roadmap/` exists in the current project. No manual
configuration needed.

The hook injects a short instruction at session start. The model then invokes
the skill before handling the first prompt.

### Disable the hook

Set `ROADMAP_TRACKING_AUTOSTART=off` in your environment to suppress the
injection while keeping the plugin active:

```bash
export ROADMAP_TRACKING_AUTOSTART=off
```

### Double-injection warning

If you also have a personal rule `~/.claude/rules/roadmap-tracking.md` that
triggers the skill, you will get **duplicate injection**. Remove one of the
two:
- Keep the personal rule → remove the plugin hook (set `AUTOSTART=off`).
- Keep the embedded hook → remove the personal rule.

## Hooks

| IDE | File | Event | Language |
|---|---|---|---|
| Claude Code | `hooks/hooks.json` | `SessionStart` | French |
| Codex | `hooks/codex-hooks.json` | `sessionStart` | English |

**Language rationale**: `hooks.json` is written in French because the skill itself is in French and Claude Code (multilingual) handles it natively. `codex-hooks.json` is in English because it targets the Codex API, where English yields more reliable instruction-following from underlying models.

**Codex integration**: Codex automatically discovers `hooks/codex-hooks.json` via `.codex-plugin/plugin.json` upon plugin installation. However, following Codex's security model, plugin-bundled hooks must still be validated once via the `/hooks` command before they become active (`allow_managed_hooks_only`). This is an intentional one-time user review step.

## Configuration (optional)

All behavior has sensible defaults. Customize via `./doc/roadmap/.skill-config.yml`:

```yaml
ide: auto                 # auto | claude-code | codex
models:
  map:
    - { name: gpt-5,      tier: reasoning }
    - { name: gpt-5-mini, tier: standard }
issues:
  mode: auto              # auto | github | local
tests:
  mode: manual            # manual | autonomous
  max_iterations: 3
  verifier: auto          # auto | subagent | inline
roadmap-tracking:
  collaborative: false    # false = solo (default) | true = multi-collaborator
  mode: auto              # auto | lightweight | full | off
```

Absent config + Claude Code + `gh` present = v1.3.x behavior (full retrocompat).

## Local development

```
claude plugin validate .
claude --plugin-dir .
```

## License

MIT
