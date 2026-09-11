#!/usr/bin/env bash
#
# e2e_fresh_install_setup.sh — deterministic teardown + setup for the
# roadmap-tracking fresh-install e2e test suite (plan step 10).
#
# Creates a set of fixture projects under a test root, each a standalone local
# git repo, covering the skill's usage cases. Idempotent: running it N times
# recreates the exact same fixtures with no cumulative side effects.
#
# GitHub is SIMULATED: "github" fixtures get a github.com origin remote so the
# skill's mode-detection (git remote + gh auth) resolves to `github`, but NO
# GitHub API call is ever made (no repo/issue creation).
#
# Usage: bash scripts/e2e_fresh_install_setup.sh [TEST_ROOT]
set -euo pipefail

TEST_ROOT="${1:-/tmp/roadmap-tracking/tests}"

# --- Teardown ---------------------------------------------------------------
rm -rf "$TEST_ROOT"
mkdir -p "$TEST_ROOT"

# --- Helpers ----------------------------------------------------------------
init_repo() {
  # $1 = project dir name
  local dir="$TEST_ROOT/$1"
  mkdir -p "$dir"
  git -C "$dir" init -q
  git -C "$dir" config user.email "test@example.com"
  git -C "$dir" config user.name "E2E Test"
}

add_github_remote() {
  # $1 = project dir name ; $2 = fake repo slug
  git -C "$TEST_ROOT/$1" remote add origin "https://github.com/ehouriez/$2.git"
}

# ============================================================================
# 1. project-github-private — GitHub remote, gh authenticated, mode auto→github
# ============================================================================
init_repo "project-github-private"
add_github_remote "project-github-private" "fake-private-app"
mkdir -p "$TEST_ROOT/project-github-private/doc/roadmap"
cat > "$TEST_ROOT/project-github-private/doc/roadmap/roadmap.md" <<'EOF'
# Roadmap Fake Private App

> Backlog actif. Dernière mise à jour : 2026-09-11.

## Contexte

Backlog consolidé : plans nommés d'après leur issue GitHub (voir `doc/roadmap/`).

---

## À faire

## Fait
EOF

# ============================================================================
# 2. project-github-optout — GitHub remote BUT config forces issues.mode: local
# ============================================================================
init_repo "project-github-optout"
add_github_remote "project-github-optout" "fake-optout-app"
mkdir -p "$TEST_ROOT/project-github-optout/doc/roadmap"
cat > "$TEST_ROOT/project-github-optout/doc/roadmap/.skill-config.yml" <<'EOF'
# opt-out of GitHub issues despite a GitHub remote
ide: auto
issues:
  mode: local
tests:
  mode: manual
EOF
cat > "$TEST_ROOT/project-github-optout/doc/roadmap/roadmap.md" <<'EOF'
# Roadmap Fake Optout App

> Backlog actif. Dernière mise à jour : 2026-09-11.

## Contexte

Backlog consolidé (mode local, opt-out GitHub).

---

## À faire

## Fait
EOF

# ============================================================================
# 3. project-no-github — no GitHub remote, local numbering, one existing plan
# ============================================================================
init_repo "project-no-github"
mkdir -p "$TEST_ROOT/project-no-github/doc/roadmap"
cat > "$TEST_ROOT/project-no-github/doc/roadmap/2-existing-local.md" <<'EOF'
---
plan:
  id: '2'
  name: 2-existing-local.md
  link: doc/roadmap/2-existing-local.md
  source: local
status: active
date: 2026-09-01
description: >
  Existing local plan used to verify max+1 numbering.
priority: medium
complexity: S
issue:
  id: null
  url: null
---

# [🔧] Plan #2 - Existing Local

## Objectif

Plan local existant pour valider la numérotation max+1.

## Périmètre

### Inclus
- Rien (fixture)

### Hors scope
- Tout le reste

## Étapes

- [ ] Étape 1 — Placeholder (XS · standard → Sonnet)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test
- [ ] ✅ Validation — Vérifier les résultats et clôturer
EOF
cat > "$TEST_ROOT/project-no-github/doc/roadmap/roadmap.md" <<'EOF'
# Roadmap No GitHub

> Backlog actif. Dernière mise à jour : 2026-09-11.

## Contexte

Backlog consolidé (mode local).

---

## À faire

### [Plan: 2] Existing Local [PRIORITÉ: MOYENNE] [Complexité: S] 🟢

Plan : [`2-existing-local.md`](2-existing-local.md)

Plan local existant pour valider la numérotation max+1.

---

## Fait
EOF

# ============================================================================
# 4. project-existing-plans — conformant plans (per references/templates.md)
# ============================================================================
init_repo "project-existing-plans"
add_github_remote "project-existing-plans" "fake-existing"
mkdir -p "$TEST_ROOT/project-existing-plans/doc/roadmap"
cat > "$TEST_ROOT/project-existing-plans/doc/roadmap/7-conformant-active.md" <<'EOF'
---
plan:
  id: '7'
  name: 7-conformant-active.md
  link: https://github.com/ehouriez/fake-existing/blob/main/doc/roadmap/7-conformant-active.md
status: active
date: 2026-08-20
enriched: 2026-09-05
description: >
  Fully conformant active plan for resume testing.
priority: high
complexity: M
scope:
  modules:
    - src/api/
issue:
  id: 7
  url: https://github.com/ehouriez/fake-existing/issues/7
---

# [🔧] Plan #7 - Conformant Active

## Objectif

Plan conforme pour tester la reprise (résumé, point d'arrêt).

## Périmètre

### Inclus
- src/api/

### Hors scope
- Le reste

## Étapes

- [x] Étape 1 — Setup initial (S · standard → Sonnet)
- [ ] Étape 2 — Logique métier (M · standard → Sonnet)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test
- [ ] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|

## Journal de session

### Session 2026-09-05
- ✅ Fait : Étape 1 (setup initial).
- 📋 Prochain : Étape 2.
EOF
cat > "$TEST_ROOT/project-existing-plans/doc/roadmap/9-conformant-done.md" <<'EOF'
---
plan:
  id: '9'
  name: 9-conformant-done.md
  link: https://github.com/ehouriez/fake-existing/blob/main/doc/roadmap/9-conformant-done.md
status: done
date: 2026-07-10
enriched: 2026-07-30
description: >
  Fully conformant closed plan.
priority: medium
complexity: S
issue:
  id: 9
  url: https://github.com/ehouriez/fake-existing/issues/9
---

# [✅] Plan #9 - Conformant Done

## Objectif

Plan conforme clôturé.

## Étapes

- [x] Étape 1 — Fait (XS · standard → Sonnet)
- [x] 🧪 Tests — Exécutés
- [x] ✅ Validation — Validé
EOF
cat > "$TEST_ROOT/project-existing-plans/doc/roadmap/roadmap.md" <<'EOF'
# Roadmap Existing Plans

> Backlog actif. Dernière mise à jour : 2026-09-11.

## Contexte

Backlog consolidé.

---

## À faire

### [Issue: #7] Conformant Active [PRIORITÉ: HAUTE] [Complexité: M] 🟢

Plan : [`7-conformant-active.md`](7-conformant-active.md)

Plan conforme actif.

---

## Fait

### Plans livrés

- **[Issue: #9] `#9` — Conformant Done** (2026-07-30) 🔵 — Livré.
  [`9-conformant-done.md`](9-conformant-done.md)
EOF

# ============================================================================
# 5. project-existing-plans-unexpected-format — 4 mandatory non-conformant files
# ============================================================================
init_repo "project-existing-plans-unexpected-format"
add_github_remote "project-existing-plans-unexpected-format" "fake-messy"
UF="$TEST_ROOT/project-existing-plans-unexpected-format/doc/roadmap"
mkdir -p "$UF"

# 5a — no front matter at all (raw markdown)
cat > "$UF/plan-no-frontmatter.md" <<'EOF'
# Refonte du module de paiement

Ce document décrit la refonte du module de paiement. Il n'y a aucun front
matter YAML ici, juste du markdown libre.

## Ce qu'il faut faire

- Migrer vers le nouveau PSP
- Ajouter les webhooks
- Tester en sandbox
EOF

# 5b — front matter present but no issue.id / issue.url
cat > "$UF/plan-frontmatter-no-issue.md" <<'EOF'
---
plan:
  id: '3'
  name: plan-frontmatter-no-issue.md
  link: doc/roadmap/plan-frontmatter-no-issue.md
status: active
date: 2026-08-01
description: >
  Plan avec front matter mais sans rattachement d'issue.
priority: low
complexity: S
---

# [🔧] Plan - Sans Issue

## Objectif

Vérifier la gestion d'un plan sans bloc issue.

## Étapes

- [ ] Étape 1 — Placeholder (XS · standard → Sonnet)
- [ ] 🧪 Tests — Procédure de test
- [ ] ✅ Validation — Clôturer
EOF

# 5c — partial front matter: plan.id present, plan.name absent, status/complexity missing
cat > "$UF/plan-frontmatter-partial.md" <<'EOF'
---
plan:
  id: '4'
  link: doc/roadmap/plan-frontmatter-partial.md
date: 2026-08-05
description: >
  Front matter partiellement rempli (name, status, complexity manquants).
priority: high
issue:
  id: null
  url: null
---

# Plan partiel

## Objectif

Tester la tolérance à un front matter incomplet.

## Étapes

- [ ] Faire quelque chose
- [ ] Autre chose
EOF

# 5d — no front matter AND no issue reference, non-standard step structure
cat > "$UF/plan-no-frontmatter-no-issue.md" <<'EOF'
Notes de refonte — brouillon

On veut réorganiser l'architecture. Pas de structure standard, pas d'étapes
numérotées, pas d'issue, pas de YAML.

TODO en vrac :
  * repenser les couches
  * virer le legacy
  * (peut-être) réécrire le cache

Fin des notes.
EOF

# roadmap.md referencing some of the non-conformant plans (robustness test)
cat > "$UF/roadmap.md" <<'EOF'
# Roadmap Messy Project

> Backlog actif. Dernière mise à jour : 2026-09-11.

## Contexte

Backlog consolidé avec des plans non conformes.

---

## À faire

### [Issue: #3] Sans Issue [PRIORITÉ: BASSE] [Complexité: S] 🟢

Plan : [`plan-frontmatter-no-issue.md`](plan-frontmatter-no-issue.md)

Plan référencé sans numéro d'issue réel.

---

### Refonte paiement (sans métadonnées)

Plan : [`plan-no-frontmatter.md`](plan-no-frontmatter.md)

Entrée non standard référençant un plan sans front matter.

---

## Fait
EOF

# ============================================================================
# 6. project-fresh — pristine, NO doc/roadmap at all
# ============================================================================
init_repo "project-fresh"
echo "# Fresh Project" > "$TEST_ROOT/project-fresh/README.md"

echo "Setup complete under: $TEST_ROOT"
find "$TEST_ROOT" -maxdepth 2 -type d | sort
