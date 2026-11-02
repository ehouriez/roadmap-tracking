---
plan:
  id: '28'
  name: 28-skill-scripts-path-resolution.md
  link: doc/roadmap/28-skill-scripts-path-resolution.md
  source: local
status: done
date: 2026-11-02
description: >
  Rendre la résolution du chemin des scripts embarqués dans le skill agnostique
  du scope d'installation (project/user/cache) en s'appuyant sur le "Base
  directory for this skill" injecté par le harness, au lieu de chemins relatifs
  ou codés en dur.
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
---

# [🔧] Plan #28 - Skill Scripts Path Resolution

## Objectif

Lorsque le skill est utilisé dans un projet tiers, les commandes `python3 scripts/X.py`
résolvent le chemin relatif au CWD du projet et non à l'arborescence du skill — les
scripts sont introuvables. La cause : trois conventions incohérentes coexistent
(`scripts/X.py` relatif, `~/.claude/skills/…` codé en dur, `~/.claude/plugins/cache/…4.0.0`
figé en version). La solution : convention unique `${SKILL_DIR}/scripts/X.py` où
`${SKILL_DIR}` est le "Base directory for this skill" injecté à chaque chargement.

## Périmètre

### Inclus

- `modules/init-scan.md` — 14 occurrences de chemins fautifs
- `modules/wrapup.md` — 1 occurrence
- `references/migration.md` — 8 occurrences + note de substitution à l'affichage
- `README.md` — 6 chemins figés → commandes de découverte autonome

### Hors scope

- `done/27-scalability-token-architecture.md` — historique, pas des commandes corrigées
- `doc/roadmap/roadmap.md`, `done/INDEX.md` — générés, mentions descriptives
- `doc/rapports/` — documentation d'analyse

## Décisions techniques

| Décision | Choix retenu | Justification |
|---|---|---|
| Variable de substitution | `${SKILL_DIR}` | Alias sémantique du "Base directory for this skill" injecté par le harness à chaque `Skill(...)` — agnostique scope/version |
| Chemin scripts vs `--roadmap-dir` | `${SKILL_DIR}/scripts/X.py` pour le script ; `--roadmap-dir doc/roadmap` **reste relatif CWD projet** | Les scripts sont dans le skill ; le roadmap est dans le projet |
| `$CLAUDE_PLUGIN_ROOT` écarté | Non — vérifié vide dans le shell Bash de l'agent | Ne vit que dans les hooks, inutilisable pour les appels Bash directs |
| Chemins affichés à l'utilisateur | L'agent substitue la valeur réelle de `${SKILL_DIR}` avant affichage | Évite d'afficher une variable non résolue dans les messages utilisateur |
| `README.md` (hors session) | Remplacer les chemins figés par des commandes shell de découverte autonome | Aucun agent dans la boucle pour substituer — l'humain découvre le chemin lui-même |

## Étapes

- [x] Étape 1 — Ajouter section canonique `${SKILL_DIR}` en tête de `modules/init-scan.md` (S · standard → Sonnet)
- [x] Étape 2 — Remplacer les 14 occurrences fautives dans `modules/init-scan.md` (M · standard → Sonnet)
- [x] Étape 3 — Corriger l'occurrence de `modules/wrapup.md` (XS · standard → Sonnet)
- [x] Étape 4 — Corriger les 8 occurrences de `references/migration.md` + note de substitution (S · standard → Sonnet)
- [x] Étape 5 — Corriger `README.md` : 6 chemins figés → commandes de découverte autonome (S · standard → Sonnet)
- [x] Étape 6 — Mettre à jour `.index.json` et `roadmap.md` (XS · standard → Sonnet)
- [x] 🧪 Tests — Grep de non-régression : zéro forme fautive restante ; cohérence `${SKILL_DIR}`
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Tests

### Prérequis pour les tests

```bash
SKILL_DIR=/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking
```

### Procédure de test

```bash
echo "=== No Bare Relative Scripts References ==="
grep -rn "python3 scripts/" "$SKILL_DIR/modules/" "$SKILL_DIR/references/migration.md" && echo "FAIL: bare refs found" || echo "PASS: no bare refs"

echo "=== No Hardcoded Skills Path ==="
grep -rn "~/.claude/skills/roadmap-tracking/scripts" "$SKILL_DIR/modules/" "$SKILL_DIR/references/migration.md" && echo "FAIL: hardcoded path found" || echo "PASS"

echo "=== No Hardcoded Cache Path With Version ==="
grep -rn "plugins/cache/roadmap-tracking" "$SKILL_DIR/modules/" "$SKILL_DIR/references/" && echo "FAIL: hardcoded cache path found" || echo "PASS"

echo "=== SKILL_DIR Convention Present In init-scan ==="
grep -c "SKILL_DIR" "$SKILL_DIR/modules/init-scan.md" | grep -v "^0$" && echo "PASS" || echo "FAIL: SKILL_DIR not found"

echo "=== roadmap-dir NOT Immediately Followed By SKILL_DIR ==="
grep -rn "\-\-roadmap-dir \${SKILL_DIR}" "$SKILL_DIR/modules/" "$SKILL_DIR/references/migration.md" && echo "FAIL: --roadmap-dir incorrectly points to SKILL_DIR" || echo "PASS"
```

**Résultats attendus :** tous les tests affichent `PASS`, aucun `FAIL`.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-11-02 | No bare relative refs | PASS | PASS | ✅ |
| 2026-11-02 | No hardcoded skills path | PASS | PASS | ✅ |
| 2026-11-02 | No hardcoded cache path | PASS | PASS | ✅ |
| 2026-11-02 | SKILL_DIR present in init-scan | PASS (20 occ.) | PASS (20 occ.) | ✅ |
| 2026-11-02 | --roadmap-dir not pointing to SKILL_DIR | PASS | PASS | ✅ |

## Journal de session

### Session 2026-11-02
- ✅ Fait : Cadrage, proposition, validation utilisateur, création du fichier plan
- ✅ Fait : Étapes 1→6 — section canonique + 14 corrections init-scan.md, 1 wrapup.md, 8 migration.md (+ note), 6 README.md → commandes de découverte autonome `find ~/.claude/plugins/cache/roadmap-tracking -name "SKILL.md" | sort -V | tail -1 | xargs dirname`
- ✅ Fait : 🧪 Tests — 5/5 PASS. Zéro forme fautive restante.
- ✅ Validation : fix confirmé en production — autre session a utilisé le chemin complet résolu `…/4.1.0/scripts/build_roadmap.py`. Plan clos.
