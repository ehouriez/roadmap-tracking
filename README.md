# roadmap-tracking

A Claude Code skill (packaged as a plugin) to **frame, plan, track and trace**
any development, configuration or architecture request through:

- plan files in `./doc/roadmap/{issue}-slug.md` (named after the linked GitHub issue),
- a consolidated backlog in `./doc/roadmap/roadmap.md`,
- linked GitHub issues.

It drives a strict **7-phase workflow** — silent analysis, interactive scoping,
plan proposal, validation, plan/issue/roadmap creation, validation, then
step-by-step implementation — with hard stop points between planning and coding.

## Install

```
/plugin marketplace add ehouriez/roadmap-tracking
/plugin install roadmap-tracking@roadmap-tracking
/reload-plugins
```

The skill is then invoked as `/roadmap-tracking:roadmap-tracking` (plugin skills
are always namespaced). It is also model-invoked automatically when a task
matches its description (a dev/config/architecture request, a reference to an
existing plan, or on demand).

## Optional: auto-trigger at session start

By default the skill is invoked by the model when relevant, or on demand. If you
want it to run its startup rule **unconditionally at the first prompt** of every
session in a project that has a `doc/roadmap/` directory, add a `SessionStart`
hook to your own configuration.

Create `hooks/hooks.json` (in your `.claude/` or in a personal plugin):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "test -d ./doc/roadmap && printf 'This project has doc/roadmap/. Before handling the first prompt, invoke the roadmap-tracking skill to run its startup rule (list plans, detect inconsistent IDs). On any reference to an existing plan, follow its resume workflow. On a new dev/config/architecture request, follow its new-plan workflow.' || true"
          }
        ]
      }
    ]
  }
}
```

This is intentionally **opt-in**: it fires on every session and is a personal
preference, not shipped enabled in the plugin.

## Local development

```
claude plugin validate .
claude --plugin-dir .
```

## License

MIT
