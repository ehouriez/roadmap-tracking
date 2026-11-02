---
plan:
  id: '29'
  name: 29-windows-native-python-interpreter-portability.md
  link: doc/roadmap/29-windows-native-python-interpreter-portability.md
  source: local
status: active
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

- [ ] Étape 1 — Étendre la convention dans `init-scan.md` : documenter `${PY}` (algorithme de résolution, note Codex hors-périmètre) (S · standard → Sonnet)
- [ ] Étape 2 — Remplacer les `python3` littéraux dans `init-scan.md` par `${PY}` (S · standard → Sonnet)
- [ ] Étape 3 — Remplacer les `python3` littéraux dans `wrapup.md` par `${PY}` (XS · standard → Sonnet)
- [ ] Étape 4 — Remplacer les `python3` littéraux dans `references/migration.md` par `${PY}` (S · standard → Sonnet)
- [ ] Étape 5 — Mettre à jour `README.md` : section Prerequisites Windows + remplacement des `python3` (S · standard → Sonnet)
- [ ] 🧪 Tests — self-check anti-régression (grep python3 = 0 fichiers actifs) + matrice manuelle Windows
- [ ] ✅ Validation — Vérifier les résultats et clôturer

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
echo "=== Detect Python Interpreter ==="
PY=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || command -v py 2>/dev/null) && echo "Found: $PY" || echo "NOT FOUND"

echo "=== Verify Python Version ==="
$PY --version

echo "=== Run Doctor Script ==="
$PY "$SKILL_DIR/scripts/doctor.py" --roadmap-dir doc/roadmap

echo "=== Run Build Roadmap Dry-run ==="
$PY "$SKILL_DIR/scripts/build_roadmap.py" --roadmap-dir doc/roadmap
```

**Résultats attendus :**
- T2-a : `Found: /c/Python3xx/python.exe` ou similaire
- T2-b : `Python 3.x.x`
- T2-c : rapport doctor sans erreur d'invocation Python
- T2-d : listing roadmap généré sans erreur

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|

## Journal de session

### Session 2026-11-02

- ✅ Fait : Cadrage Plan #29, décisions techniques, création du fichier plan
- 📋 Prochain : Étape 1 — Extension convention `${PY}` dans init-scan.md
