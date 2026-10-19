# roadmap-tracking

> **v4.0.0 — Breaking change.** See [What changed](#whats-new-in-v400) and
> [update instructions](#update) before upgrading an existing project.

## What's new in v4.0.0

**Scalability & Token Architecture** (plan #27) — removes the fixed startup
token cost that became untenable at 500+ plans (~70 K tokens measured on a
real 285-plan project).

| Improvement | Detail |
|---|---|
| **Index-first startup** | Reads `.index.json` (~few KB) instead of `roadmap.md` (~275 KB) — **−82 % startup tokens** |
| **Generated roadmap.md** | Built from front matter (single source of truth) — zero manual drift |
| **Lazy listing** | Active + blocked only, sorted by priority, with `+ N done` counter and verbal filters |
| **4 new scripts** | `build_roadmap.py`, `doctor.py`, `normalize_status.py`, `split_context.py` |
| **Auto-normalisation** | `normalize_status.py` maps legacy statuses (`in-progress`→`active`, `cancelled`→`archived`) and moves misplaced plans to `done/` / `archived/` |
| **Integrity audit** | `doctor.py` — status vs folder, orphan deps, stale index, broken links |
| **CONTEXT.md budget** | Core bounded at ≤ 200 l. / 15 KB ; overflow sections split to `context/*.md` on-demand via `split_context.py` |
| **Universal index guard A.1** | Fires before any listing/resume — absent index triggers generation + normalisation + doctor |
| **`aide migration`** | Step-by-step adoption guide for existing projects |
| **`archived/` directory** | Renamed from `_archives/` — consistent past-participle naming with `done/` |

### Upgrade an existing project

After updating the plugin, the skill detects and proposes every required
migration step automatically at session start. Or run manually:

```bash
echo "=== Generate Index ==="
python3 ~/.claude/plugins/cache/roadmap-tracking/roadmap-tracking/4.0.0/scripts/build_roadmap.py --roadmap-dir doc/roadmap --write

echo "=== Normalise Statuses And Move Misplaced Plans ==="
python3 ~/.claude/plugins/cache/roadmap-tracking/roadmap-tracking/4.0.0/scripts/normalize_status.py --roadmap-dir doc/roadmap --write

echo "=== Run Integrity Audit ==="
python3 ~/.claude/plugins/cache/roadmap-tracking/roadmap-tracking/4.0.0/scripts/doctor.py --roadmap-dir doc/roadmap
```

### Update the plugin

**Claude Code** — from a session launched in any project:

```
/plugin marketplace update roadmap-tracking
/plugin update roadmap-tracking
/clear
```

**Codex** — from a session launched in any project:

```
/plugin update roadmap-tracking
/clear
```

---

A Claude Code skill (packaged as a plugin) to **frame, plan, track and trace**
any development, configuration or architecture request through:

- plan files in `./doc/roadmap/{id}-slug.md`,
- a consolidated backlog in `./doc/roadmap/roadmap.md`,
- linked GitHub issues *(optional — local mode available)*.

Drives a strict **7-phase workflow** — silent analysis, interactive scoping,
plan proposal, validation, plan creation, validation, then step-by-step
implementation — with hard stop points between planning and coding.

## Quickstart (5 min)

> **Existing project** — adopting roadmap-tracking on a project that already has
> plans or a `roadmap.md` not yet managed by this skill.

```bash
echo "=== Install The Plugin ==="
claude plugin marketplace add ehouriez/roadmap-tracking
claude plugin install roadmap-tracking@roadmap-tracking

echo "=== Open Your Project In Claude Code ==="
cd /path/to/your/project && claude
```

Inside the session, the skill fires automatically and asks:
1. **Solo or collaborative?** (stored in `.skill-config.yml`)
2. **Reconcile?** — if plans are out of place or the index is stale, it proposes
   running `normalize_status.py` and `build_roadmap.py` for you.

To adopt manually or migrate an existing `roadmap.md`:

```bash
echo "=== Generate Index And Roadmap From Front Matter ==="
python3 ~/.claude/plugins/cache/roadmap-tracking/roadmap-tracking/latest/scripts/build_roadmap.py --roadmap-dir doc/roadmap --write

echo "=== Normalise Legacy Statuses And Move Misplaced Plans ==="
python3 ~/.claude/plugins/cache/roadmap-tracking/roadmap-tracking/latest/scripts/normalize_status.py --roadmap-dir doc/roadmap

echo "=== Apply When Output Looks Correct ==="
python3 ~/.claude/plugins/cache/roadmap-tracking/roadmap-tracking/latest/scripts/normalize_status.py --roadmap-dir doc/roadmap --write
```

> Type `aide migration` inside any Claude Code session with the skill active to
> get the full step-by-step adoption guide.

---

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
    - { name: sol,    tier: reasoning }   # OpenAI / Codex
    - { name: luna,   tier: standard }    # OpenAI / Codex
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
