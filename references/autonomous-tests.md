# Autonomous Test Mode

Reference for `tests.mode: autonomous` (opt-in). Default mode is `manual` —
see SKILL.md Phase 7.

> ⚠️ Autonomous mode never activates from shell-access detection alone.
> Detection *proposes*; explicit config or user confirmation *activates*.
>
> **Where the proposal happens.** When `tests.mode` is unset in
> `./doc/roadmap/.skill-config.yml`, SKILL.md Phase 7 ("Proposition du mode de
> tests") asks the operator to pick `manual` or `autonomous` and persists the
> choice to the config. The signal is "config unset", never "shell access
> detected" — Bash access is nearly always present in Claude Code and would
> re-propose every session.

---

## Roles

| Role | Responsibility |
|---|---|
| **Executor** | Implements or corrects code; runs tests; reports raw results. |
| **Verifier** | Receives test results only; renders PASS/FAIL verdict; never touches code. |

The Verifier is always a real sub-agent when the IDE supports it (Claude Code,
Codex — see `references/environment.md § Persona-Switch`). When unavailable:
`inline` honest self-check applies (see below).

---

## Iteration Loop

For each implementation step in Phase 7 (autonomous mode):

```
Step 0 is SUPPRESSED — all tests run after every step automatically.

repeat up to max_iterations (default 3, override via tests.max_iterations):
  Executor: implement / correct the step
  Executor: run all relevant tests, collect raw results
  Verifier: render verdict (PASS or FAIL)
  if PASS:
    display 📦 Commit proposé
    ⏸️ STOP — wait for operator acknowledgement
    proceed to next step
  if FAIL and iteration < max_iterations:
    continue loop
  if iteration == max_iterations and still FAIL:
    STOP + structured diagnosis + ask operator to decide
```

Notes:
- The `📦 Commit proposé` block appears **only after PASS** and is a
  proposal, never auto-executed (respects the global "never manage
  commit/push" rule).
- The `⏸️` stop point moves to **after PASS** (not after tests).
- Manual interrupt ("stop") is always possible at any iteration.

---

## Guard: Max Iterations

Default: **3 iterations**.

Rationale:
- Iteration 1: fixes the obvious error.
- Iteration 2: catches a missed case.
- Iteration 3 fail: diagnosis or approach is wrong → the human must decide.

Three bounds cost/time without curbing useful autonomy. Override:

```yaml
tests:
  max_iterations: 5
```

When max is reached, display:

```
⛔ Garde-fou — 3/3 itérations atteintes sans PASS.

Dernier diagnostic Vérificateur :
  Attendu : <…>
  Observé : <…>
  Diagnostic : <…>

Je m'arrête. Souhaites-tu : (a) diagnostiquer ensemble, (b) changer
d'approche, (c) continuer manuellement ?
```

---

## Iteration Report Format

Per-iteration display (transparent, visually distinct):

```
🔁 Itération k/N
─────────────────────────────────
🔨 Exécuteur — implémentation/correction : <one-line summary>
🔍 Vérificateur — verdict : ❌ FAIL
   Attendu : <…>   Observé : <…>
   Diagnostic factuel : <…>
```

On PASS:

```
🔁 Itération k/N
─────────────────────────────────
🔨 Exécuteur — implémentation/correction : <one-line summary>
🔍 Vérificateur — verdict : ✅ PASS
   Attendu : <…>   Observé : <…>

📦 Commit proposé — Étape X/N

**Fichiers modifiés :**
- `<file>` — <one-line summary>

**Message de commit :**
```
<type>(<scope>): <description> (#<issue>, step X)
```

---
⏸️ Commit et push si nécessaire, puis confirme pour passer à l'étape suivante.
```

---

## Verifier System Prompt (Real Sub-agent)

Pass this as the Verifier's system prompt when spawning a sub-agent:

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

---

## Inline Fallback (IDE Without Sub-agents)

When `tests.verifier: inline` (or `auto` resolves to `inline`):

- The Executor runs the tests itself and reports factually: observed vs expected.
- **No independence claim**: the report explicitly states
  `(auto-check — même contexte, garantie moindre)`.
- No Verifier persona, no isolation pretense.
- The `📦 Commit proposé` and loop mechanics remain identical.
- Inline format:

```
🔁 Itération k/N
─────────────────────────────────
🔨 Exécuteur — implémentation/correction : <one-line summary>
🔍 Auto-check (même contexte — garantie moindre) — verdict : ❌ FAIL
   Attendu : <…>   Observé : <…>
   Diagnostic factuel : <…>
```
