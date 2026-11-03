# Référence — tests-e2e

> Voir aussi : [Explication tests-e2e](explanation-tests-e2e.md)

Fixture e2e dans `tests/my-project--s-solo/` et script de setup dans `scripts/e2e_fresh_install_setup.sh`.

---

## Fixture tests/my-project--s-solo/

Projet représentant un workflow solo local-mode complété.

| Fichier | Description |
|---|---|
| `doc/roadmap/.skill-config.yml` | `collaborative: false`, `mode: auto` (solo local) |
| `doc/roadmap/roadmap.md` | Table simplifiée (plan #1 done) |
| `doc/roadmap/1-weather-forecast-script.md` | Plan `status: done`, journal de session réel avec bug fix documenté |
| `weather_forecast.py` | Implémentation produite par le workflow testé |
| `test.md` | Plan actif (`status: active`, `plan.source: local`, `issue.id: null`) |

**Note** : `test.md` (plan `weather-tomorrow`, racine du repo fixture) et `1-weather-forecast-script.md` (plan `weather-forecast`, dans `done/`) sont deux plans distincts représentant des états différents.

---

## Script scripts/e2e_fresh_install_setup.sh

```bash
./e2e_fresh_install_setup.sh [TEST_ROOT]
```

- `TEST_ROOT` défaut : `/tmp/roadmap-tracking/tests`
- Idempotent : `rm -rf TEST_ROOT` puis recrée
- `set -euo pipefail`

Crée 6 repos git de fixture déterministes :

| Repo | Scénario couvert |
|---|---|
| `project-github-private` | Remote GitHub + `gh` authentifié |
| `project-github-optout` | Remote GitHub + `.skill-config.yml` `issues.mode: local` |
| `project-no-github` | Pas de remote GitHub, numérotation locale, 1 plan existant (`plan.id: '2'`) |
| `project-existing-plans` | Plans conformes avec progression partielle (plan #7 actif, plan #9 done) |
| `project-existing-plans-unexpected-format` | Plans non conformes (4 cas) |
| `project-fresh` | Projet vierge sans `doc/roadmap/` |

Chaque repo : `git init` + `git config user.*` (active la détection de mode basée sur le remote git).

**Simulation GitHub** : remote `https://github.com/...` — aucun appel API réel.

---

## Cas de non-conformité (project-existing-plans-unexpected-format)

| Cas | Description |
|---|---|
| 1 | Pas de front matter du tout |
| 2 | Front matter sans `issue.id` |
| 3 | Front matter partiel |
| 4 | Pas de front matter, pas de structure d'étapes standard |

---

## Cas ID local (project-no-github)

Contient un plan avec `plan.id: '2'` : vérifie que la nouvelle création attribue l'ID 3 (max + 1).

---

## Cas GitHub opt-out (project-github-optout)

Démontre que la présence d'un remote GitHub seul ne suffit pas à activer le mode `github` si `.skill-config.yml` déclare `issues.mode: local`.
