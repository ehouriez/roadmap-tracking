---
plan:
  id: '29'
  name: 29-windows-native-python-interpreter-portability.md
  link: doc/roadmap/done/29-windows-native-python-interpreter-portability.md
  source: local
status: done
date: 2026-11-02
description: >
  Introduire la convention ${PY} (résolution agent python3→python→py -3) pour
  rendre l'invocation des scripts Python du skill fiable sous Claude Code
  Windows natif (Git Bash), sans modifier les scripts eux-mêmes.
priority: high
complexity: M
intent: null
scope:
  modules:
    - modules/init-scan.md
    - modules/wrapup.md
    - references/migration.md
    - README.md
issue:
  id: null
  url: null
depends_on:
  - '28'
---

# [🪟] Plan #29 - Windows Native Python Interpreter Portability

## Objectif

Sous Claude Code Windows natif (Git Bash), le littéral `python3` n'existe pas :
Python 3 s'installe comme `python` ou `py -3`. Tous les appels `python3 ${SKILL_DIR}/scripts/X.py`
échouent donc même quand Python est installé. La solution : introduire une convention
`${PY}` (résolution côté agent) en parallèle de `${SKILL_DIR}`, remplacer les
`python3` littéraux dans les fichiers actifs, et documenter Python comme dépendance
assumée.

Cible : **Claude Code Windows natif (Git Bash)**. Codex hors-périmètre (à reprendre
dans un plan dédié quand un environnement de test Codex Windows sera disponible).

## Périmètre

### Inclus

- `modules/init-scan.md` — extension de la convention (ajout `${PY}`) + remplacement des `python3` littéraux
- `modules/wrapup.md` — remplacement des `python3` littéraux
- `references/migration.md` — remplacement des `python3` littéraux
- `README.md` — section Prerequisites Windows + remplacement des `python3` littéraux

### Hors scope

- Codex (noté pour plan futur)
- `done/` (historique, pas des commandes corrigées)
- Port PowerShell des scripts
- Mode dégradé sans Python

## Étapes

- [x] Étape 1 — Étendre la convention dans `init-scan.md` : documenter `${PY}` (algorithme de résolution, note Codex hors-périmètre) (S · standard → Sonnet)
- [x] Étape 2 — Remplacer les `python3` littéraux dans `init-scan.md` par `${PY}` (S · standard → Sonnet)
- [x] Étape 3 — Remplacer les `python3` littéraux dans `wrapup.md` par `${PY}` (XS · standard → Sonnet)
- [x] Étape 4 — Remplacer les `python3` littéraux dans `references/migration.md` par `${PY}` (S · standard → Sonnet)
- [x] Étape 5 — Mettre à jour `README.md` : section Prerequisites Windows + remplacement des `python3` (S · standard → Sonnet)
- [x] 🧪 Tests — self-check anti-régression (grep python3 = 0 fichiers actifs) + matrice manuelle Windows
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Mécanisme de résolution | Convention `${PY}` côté agent (résolution avant exécution Bash) | Shell-agnostique par construction — marche sous bash, Git Bash, et future reprise Codex sans refonte |
| Algorithme de résolution | `python3` → `python` → `py -3` (premier trouvé) | Ordre de priorité : Linux/macOS/WSL d'abord, Windows natif ensuite, fallback `py` launcher |
| Périmètre Windows | Git Bash uniquement pour ce plan | Codex requiert un environnement de test Windows réel ; hors-périmètre temporaire |
| Portage PowerShell | Rejeté | Doublerait la logique métier des scripts (2 sources de vérité) ; maintenance permanente |
| Documentation Python | README (section Prerequisites) + convention init-scan | Préserve le budget tokens SKILL.md (plans #13/#17/#18) |

## Tests

### Prérequis pour les tests

```bash
SKILL_DIR=/home/ehouriez/.claude/plugins/cache/roadmap-tracking/roadmap-tracking/4.1.0
PROJ_DIR=/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking
```

### Procédure de test

#### Test T1 — Self-check anti-régression (automatisé)

```bash
echo "=== Check No Bare python3 Literals In Active Files ==="
grep -rn "python3 " modules/init-scan.md modules/wrapup.md references/migration.md README.md | grep -v "python3 " | wc -l
```

> Résultat attendu : 0 occurrences de `python3 ` (espace après) dans les fichiers actifs.
> Les `${PY}` remplacent tous les `python3 <script>` ; les mentions textuelles de
> `python3` dans du prose (ex. "Sous Linux, python3 est...") restent acceptables si
> elles ne sont pas des commandes exécutables.

Commande précise de vérification :

```bash
echo "=== Grep Executable python3 Calls ==="
grep -rEn "^\s*(python3 \$\{SKILL_DIR\}|python3 \"|python3 ')" modules/init-scan.md modules/wrapup.md references/migration.md README.md
```

> Résultat attendu : aucune ligne — toutes les invocations sont `${PY} ${SKILL_DIR}/scripts/…`.

#### Test T2 — Matrice manuelle Windows (Git Bash)

À exécuter sur un poste Windows avec Python 3 installé via `python.exe` (pas `python3`) :

```bash
echo "=== Resolve Skill Install Directory (Windows home) ==="
SKILL_DIR=$(find ~/.claude/plugins/cache/roadmap-tracking -maxdepth 3 -name "SKILL.md" | sort -V | tail -1 | xargs dirname)

echo "=== Resolve Python Interpreter (skips Store stub) ==="
PY=$(python3 -c "import sys; print(sys.executable)" 2>/dev/null || python -c "import sys; print(sys.executable)" 2>/dev/null || py -c "import sys; print(sys.executable)" 2>/dev/null)
[ -n "$PY" ] && echo "Found: $PY" || echo "NOT FOUND"

echo "=== Verify Python Version ==="
"$PY" --version

echo "=== Run Doctor Script ==="
"$PY" "$SKILL_DIR/scripts/doctor.py" --roadmap-dir doc/roadmap

echo "=== Run Build Roadmap Dry-run ==="
"$PY" "$SKILL_DIR/scripts/build_roadmap.py" --roadmap-dir doc/roadmap
```

**Résultats attendus :**
- T2-a : `Found: /c/Python3xx/python.exe` ou similaire
- T2-b : `Python 3.x.x`
- T2-c : rapport doctor sans erreur d'invocation Python
- T2-d : listing roadmap généré sans erreur

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-11-02 | T1 — Grep executable python3 calls | 0 occurrence | 0 occurrence | ✅ |
| 2026-11-02 | T1b — ${PY} count in init-scan.md | > 0 | 23 | ✅ |
| 2026-11-02 | T1c — ${PY} count in wrapup.md | > 0 | 1 | ✅ |
| 2026-11-02 | T1d — ${PY} count in migration.md | > 0 | 9 | ✅ |
| 2026-11-02 | T1e — PY resolver count in README | 2 (un par bloc) | 2 | ✅ |
| 2026-11-02 | T1f — python3 restants in init-scan | prose uniquement | résolveur + tableau plateforme | ✅ |
| 2026-11-02 | T1g — python3 restants in migration.md | prose uniquement | note algorithme | ✅ |
| 2026-11-02 | T1h — python3 restants in README | prose uniquement | résolveurs + tableau + note Windows | ✅ |
| 2026-11-02 | T2-a — PY resolver (WSL, CWD incorrect) | Found: interpreter | Found: /usr/bin/python3 | ⚠️ CWD |
| 2026-11-02 | T2-c/d — scripts (WSL, CWD incorrect) | scripts OK | ❌ not a directory: doc/roadmap | ⚠️ CWD |
| 2026-11-02 | T2-iter2 : Store stub détecté | resolver saute le stub WindowsApps | `command -v` trouvait le stub sans sauter | 🐛 Bug trouvé |
| 2026-11-02 | Fix : resolver `import sys` anti-stub | `import sys` fail sur stub → fallback | Corrigé dans init-scan.md + README.md | ✅ Fix appliqué |
| 2026-11-02 | T2-a PowerShell — PY resolver (Windows natif) | Found: vrai Python, pas le stub | Found: C:\...\Python314\python.exe | ✅ |
| 2026-11-02 | T2-b PowerShell — Python version | Python 3.x.x | Python 3.14.3 | ✅ |
| 2026-11-02 | T2-c PowerShell — doctor.py | ✅ aucune incohérence | ✅ doctor — aucune incohérence détectée. | ✅ |
| 2026-11-02 | T2-d PowerShell — build_roadmap.py dry-run | would write 29 plans | Would write index for 29 plans (mode: github). | ✅ |
| — | Note env. T2 PowerShell | Windows natif, $SKILL_DIR résolu via %USERPROFILE%\.claude\ (plugin installé côté Windows). | — | — |
| — | Note WSL | Pas de stub en WSL (python3 = vrai binaire). Fix `import sys` neutre en WSL, bénéfique Windows. Aucune correction WSL requise. | — | — |
| 2026-11-02 | T2-e Git Bash — PY resolver (import sys) | vrai Python trouvé, stub sauté | Python 3.14.3 | ✅ |
| 2026-11-02 | T2-f Git Bash — doctor.py (1ère passe) | rapport OK | ❌ mauvais SKILL_DIR : find récursif → sous-skill SKILL.md | 🐛 Bug SKILL_DIR |
| 2026-11-02 | Fix SKILL_DIR find : -maxdepth 3 | find trouve uniquement SKILL.md racine | README.md corrigé (-maxdepth 3 dans les 2 blocs) | ✅ Fix appliqué |
| 2026-11-02 | T2-g Git Bash — doctor.py (avec -maxdepth 3) | ✅ aucune incohérence | ✅ doctor — aucune incohérence détectée. | ✅ |

## Journal de session

### Session 2026-11-02

- ✅ Fait : Cadrage Plan #29, décisions techniques, création du fichier plan
- ✅ Fait : Étape 1 — Extension convention ${PY} dans init-scan.md
- ✅ Fait : Étape 2 — Remplacement python3 → ${PY} dans init-scan.md (16 occurrences)
- ✅ Fait : Étape 3 — Remplacement python3 → ${PY} dans wrapup.md (1 occurrence)
- ✅ Fait : Étape 4 — Remplacement python3 → ${PY} dans migration.md (8 occurrences) + note ${PY}
- ✅ Fait : Étape 5 — README.md : section Prerequisites + résolveurs PY dans les deux blocs bash
- ✅ Fait : 🧪 Tests T1-T1h — self-check anti-régression : 0 invocation python3 exécutable restante
- ✅ Fait : T2 — Matrice complète PowerShell + Git Bash (2 bugs trouvés et corrigés : stub Store → import sys, find récursif → -maxdepth 3)
- ✅ Fait : ✅ Validation — tous les tests passent, plan clôturé
