# Environment & IDE Mapping

Reference loaded at skill invocation. Covers: IDE detection, tier taxonomy,
action mapping, config schema, and operator command formatting (embedded —
no external rule needed).

---

## IDE Detection

| IDE | Detection signal |
|---|---|
| **Claude Code** | System prompt contains "You are powered by the model named…" |
| **Codex** | Codex-specific system prompt or runtime context markers |
| **Fallback** | Any other environment — text-only, no IDE-specific tooling |

Configurable via `.skill-config.yml` (`ide: auto | claude-code | codex`).
When `auto`, derive from system prompt at invocation time.

---

## Tier Taxonomy & Anthropic Defaults

The skill reasons in **tiers**, never in versioned model names.

| Tier | Role | Anthropic default | Override key |
|---|---|---|---|
| `standard` | General work — scoping, plan writing, step implementation | Sonnet (current) | `models.map` |
| `reasoning` | Complex analysis, architecture, multi-file planning | Opus | `models.map` |
| `light` | Out of scope for planning (never recommended by the matrix) | Haiku | — |

Custom model mapping example (`.skill-config.yml`):

```yaml
models:
  map:
    - { name: gpt-5,      tier: reasoning }
    - { name: gpt-5-mini, tier: standard }
```

---

## Model Tier Resolution

To determine the active model's tier at invocation:

1. Read model name from system prompt ("You are powered by the model named …").
2. If `models.map` is configured: match by name → use mapped tier.
3. Otherwise apply Anthropic defaults:
   - Name contains "Sonnet" → `standard` tier.
   - Name contains "Opus"   → `reasoning` tier.
   - Name contains "Haiku"  → `light` tier (always a mismatch with planning matrix).
   - Unknown               → tier undetectable; skip model gate, keep step tags only.

---

## Generic Action Mapping

| Action | Claude Code | Codex | Fallback |
|---|---|---|---|
| **Change model** | `/model <name>` | `/model <name>` | "Switch to a `<tier>` model and restart." |
| **Ask a question** | `AskUserQuestion` tool | `AskUserQuestion` tool (if available) | Output numbered choices as text |
| **Enter plan mode** | `EnterPlanMode` tool | `/plan` (toggle) | State: "entering planning mode" |
| **Exit plan mode** | `ExitPlanMode` tool | `/plan` (toggle) | Inform user: planning phase complete |
| **Detect active model** | System prompt "You are powered by…" | `/model` output or context | Ask the user |

---

## Persona-Switch: Verifier Sub-agent (Autonomous Mode)

For `tests.mode: autonomous` (see `references/autonomous-tests.md`):

| IDE | Sub-agent mechanism |
|---|---|
| **Claude Code** | `Agent` tool — **fresh agent only** (NOT a fork: a fork inherits the parent's full context and breaks Verifier isolation) |
| **Codex** | `spawn_agent` with `developer_instructions` (see `codex-rs/agent-roles/`) |
| **Fallback** | No real sub-agent → use `inline` honest self-check |

The `tests.verifier` config key controls behavior:

| Value | Behavior |
|---|---|
| `auto` | Real sub-agent if available; else `inline` |
| `subagent` | Force real sub-agent (error if not available) |
| `inline` | Honest same-context self-check — no isolation claimed |

---

## Environment Detection Procedure

At skill invocation:

1. Read `.skill-config.yml` if present — use `ide:` value if not `auto`.
2. If `auto` or absent:
   - Check system prompt for "You are powered by the model named" → Claude Code.
   - Check for Codex runtime markers → Codex.
   - Otherwise → Fallback.
3. Read `models.active` if set; otherwise detect from system prompt.
4. Resolve tier: apply `models.map` first, then Anthropic defaults above.
5. Read `issues.mode` (auto → detect `.git/` + remote GitHub + `gh auth status`).
6. Read `tests.mode`. If **set** (`manual` or `autonomous`), use it. If **unset**
   (key/file absent or `null`), do **not** silently assume a mode here: SKILL.md
   Phase 7 proposes `manual` vs `autonomous` once and persists the choice. Until
   resolved, the effective fallback is `manual` (retrocompat).

---

## Skill Configuration Schema

`.skill-config.yml` is **entirely optional**, located at `./doc/roadmap/.skill-config.yml`.
Absent file + Claude Code + `gh` present = v1.3.x behavior (full retrocompat).

```yaml
# ./doc/roadmap/.skill-config.yml — entirely optional, non-blocking
ide: auto                 # auto | claude-code | codex
models:
  active: null            # null = detect (Claude Code) or ask
  map:                    # extends Anthropic defaults
    - { name: gpt-5,      tier: reasoning }
    - { name: gpt-5-mini, tier: standard }
issues:
  mode: auto              # auto | github | local
tests:
  mode: manual            # manual | autonomous | null (unset → proposed at Phase 7, then persisted)
  max_iterations: 3       # autonomous mode only
  verifier: auto          # auto | subagent | inline
grilling:
  enabled: true           # true (default, opt-out) | false — grilling on L/XL plans
  categories:             # optional per-phase override of default prompting categories
    phase2: []            # scoping — default: scope, success criteria, dependencies, stakeholders, alternatives, risks
    phase4: []            # plan validation — default: requirement coverage, step feasibility, unaddressed risks, sequencing
    phase6: []            # implementation gate — default: implementation risks, test coverage, rollback, existing-feature impact
```

When `tests.mode` is **unset** (key or file absent, or `null`), SKILL.md Phase 7
proposes `manual` vs `autonomous` once and writes the answer back here. A **set**
value is honored as-is and never re-proposed. Effective fallback before the first
answer: `manual` (retrocompat).

**Defaults = retrocompat**: absent config + Claude Code + `gh` present →
`ide: claude-code`, `issues: github`, `tests: manual` = v1.3.x behavior.
Every field has a detection-based default; never blocking.

Issues mode `auto` detection:
- `.git/` present + remote GitHub URL + `gh auth status` succeeds → `github`.
- Otherwise → `local`.

---

## Grilling

Controls the adaptive grilling defined in SKILL.md § « Grilling adaptatif ».

| Key | Default | Effect |
|---|---|---|
| `grilling.enabled` | `true` | Opt-out toggle. `true` = grilling runs on `L`/`XL` plans in Phases 2, 4, 6. `false` = phases keep their pre-grilling behavior regardless of complexity. |
| `grilling.categories.phase2` | (built-in) | Overrides the default Phase 2 prompting categories. Empty list / absent → use SKILL defaults. |
| `grilling.categories.phase4` | (built-in) | Overrides the default Phase 4 prompting categories. |
| `grilling.categories.phase6` | (built-in) | Overrides the default Phase 6 prompting categories. |

Each `categories.phaseN` value is a list of free-text category labels. When
provided and non-empty, it **replaces** the built-in list for that phase; the
grilling mechanics (trigger on `L`/`XL`, reduced frontier, round format) are
unchanged. Per-phase enable/disable is intentionally **not** supported — a
single global `enabled` flag keeps the surface minimal.

---

## Operator Commands Formatting

This section applies **every time** a shell command must be presented to the
operator for manual execution in an external environment (test VM, container,
remote host, etc.).

### Rules

1. **One command = one line.** Never use trailing `\` to split a command
   across multiple lines.

2. **No inline comments.** Never use `# comment` above or beside a command.

3. **Echo header per logical group.** Each command — or tightly related group
   of consecutive commands (e.g. `cd` + `ls`) — must be preceded by:
   ```
   echo "=== Description In Capitalized English ==="
   ```
   The description must be in **English**, **Capitalized**, and describe the
   **intent** of the following command(s).

4. **Blank line separation.** Separate each logical group (echo + command(s))
   with exactly one blank line for readability.

5. **Copy-paste ready.** The entire block must be directly copy-pastable into
   a bash/zsh terminal without editing. No placeholders unless explicitly
   documented with a preceding `echo` explaining what to replace.

### Correct example

```bash
echo "=== Get Main Branch ==="
git checkout main

echo "=== Align Exactly With Remote Main ==="
git reset --hard origin/main

echo "=== Check Current Status ==="
git status
```

### Incorrect examples

```bash
# récupère la branche main
git checkout \
    main
```

```bash
git checkout main  # get main branch
```
