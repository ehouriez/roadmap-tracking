---
plan:
  id: '8'
  name: 8-roadmap-tracking-grilling.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/8-roadmap-tracking-grilling.md
status: active
date: 2026-09-12
description: >
  Intégrer la philosophie de grilling (design tree, rounds pré-amorcés, frontier
  réduite) dans les phases 2, 4 et 6 du skill roadmap-tracking pour les plans complexes.
priority: medium
enriched: 2026-09-12
complexity: L
scope:
  modules:
    - SKILL.md
    - references/environment.md
issue:
  id: 8
  url: https://github.com/ehouriez/roadmap-tracking/issues/8
---

# [🔥] Plan #8 - Roadmap Tracking Grilling

## Objectif

Enrichir le skill `roadmap-tracking` avec une phase de grilling contextuelle,
inspirée de la philosophie `mattpocock-skills:grilling`, réimplémentée nativement
pour garantir l'indépendance vis-à-vis du plugin externe et la compatibilité
multi-utilisateurs. Le grilling s'active uniquement sur les plans complexes et
couvre trois moments clés : le cadrage (Phase 2), la validation du plan (Phase 4)
et l'autorisation d'implémentation (Phase 6).

## Périmètre

### Inclus

- Logique de grilling adaptatif en Phase 2 (remplacement de `AskUserQuestion` pour les plans complexes)
- Logique de grilling systématique avant gate en Phase 4 (plans complexes)
- Logique de grilling systématique avant gate en Phase 6 (plans complexes)
- Catégories pré-amorcées phase-spécifiques (Phase 2 : 6 catégories ; Phase 4 : 4 catégories ; Phase 6 : 4 catégories)
- Frontier réduite : catégories pré-amorcées + 1 round de suivi maximum
- Recommandation explicite post-grilling en Phase 4 et Phase 6 avant la gate binaire
- Schéma de configuration `grilling.*` dans `.skill-config.yml` : `grilling.enabled` (bool, opt-out, défaut `true`) + override des catégories par phase
- Documentation du schéma dans `references/environment.md`

### Hors scope

- Modification du skill `mattpocock-skills:grilling` (read-only, plugin tiers)
- Grilling sur les plans simples (comportement `AskUserQuestion` inchangé)
- Grilling en Phase 1, Phase 3, Phase 5 ou Phase 7
- Grilling configurable par phase individuelle (enable/disable per-phase via config)
- Export ou archivage des sessions de grilling dans le fichier plan

## Étapes

- [x] Étape 1 — Analyser SKILL.md et cartographier les points d'insertion exacts pour Phase 2, Phase 4 et Phase 6 (XS · standard → Sonnet)
- [x] Étape 2 — Implémenter le grilling adaptatif en Phase 2 : branche complexité (Phase 1 gate réutilisée), rounds pré-amorcés 6 catégories + 1 round suivi, plans simples inchangés (M · reasoning → Opus)
- [x] Étape 3 — Implémenter le grilling avant gate en Phase 4 : bloc systématique 4 catégories + frontier réduite + recommandation pré-gate (S · reasoning → Opus)
- [x] Étape 4 — Implémenter le grilling avant gate en Phase 6 : bloc systématique 4 catégories + frontier réduite + recommandation pré-gate (S · reasoning → Opus)
- [x] Étape 5 — Documenter le schéma `grilling.*` dans `references/environment.md` (clés, valeurs par défaut, exemples de config) (S · standard → Sonnet)
- [ ] Étape 6 — Mettre à jour `roadmap.md` (entrée #8 "À faire") et bumper la version du plugin (XS · standard → Sonnet)
- [ ] 🧪 Tests — Valider le comportement sur un plan simple (grilling absent) et un plan complexe (grilling actif en Phase 2, 4, 6)
- [ ] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|---|---|---|
| Approche d'intégration | Réimplémentation de la philosophie grilling dans SKILL.md | `mattpocock-skills:grilling` est read-only et multi-utilisateurs sans garantie d'installation |
| Déclencheur du grilling | Réutilisation de l'évaluation de complexité Phase 1 (même seuil que gate modèle) | Cohérence interne, zéro nouvelle logique d'évaluation (YAGNI) |
| Plans simples | `AskUserQuestion` existant inchangé | Évite la friction inutile sur les plans non complexes |
| Profondeur grilling Phase 2 | Frontier réduite : catégories pré-amorcées + 1 round de suivi | Évite l'exploration architecture sans fin ; le grilling cadre le plan, pas le code |
| Catégories Phase 2 | Périmètre, critères de succès, dépendances, parties prenantes, alternatives écartées, risques identifiés | Angles morts les plus fréquents en contexte entreprise lors du scoping |
| Catégories Phase 4 | Complétude des exigences couvertes, faisabilité des étapes, risques non adressés, cohérence du séquencement | Stress-test du plan proposé avant approbation |
| Catégories Phase 6 | Risques d'implémentation, couverture des tests prévus, plan de rollback, impacts sur les features existantes | Stress-test de l'approche d'implémentation avant d'écrire du code |
| Comportement sortie Phase 4/6 | Recommandation explicite ("N blocages — recommande de retourner en Phase X") puis gate binaire | Informe sans retirer l'agentivité ; l'utilisateur garde le dernier mot |
| Grilling Phase 4/6 | Systématique pour les plans complexes (non opt-outable par plan) | L'opt-out per-plan garantit le contournement systématique en contexte entreprise |
| Config `.skill-config.yml` | `grilling.enabled` (global) + `grilling.categories.phaseN` (override par phase) | YAGNI modéré : use case principal = catégories custom ; per-phase disable = YAGNI |
| État par défaut | `grilling.enabled: true` (opt-out) | Opt-in = jamais utilisé en entreprise (personne ne lit les changelogs) |
| Structure d'implémentation | Section canonique unique « Grilling adaptatif » dans SKILL.md, référencée par Phase 2/4/6 | DRY : mécanique définie une fois, chaque phase n'apporte que ses catégories |

## Tests

### Procédure de test

```bash
echo "=== Vérifier Comportement Plan Simple ==="
claude --no-config

echo "=== Vérifier Comportement Plan Complexe Phase 2 ==="
claude --no-config

echo "=== Vérifier Grilling Phase 4 Avant Gate ==="
claude --no-config

echo "=== Vérifier Grilling Phase 6 Avant Gate ==="
claude --no-config

echo "=== Vérifier Opt-Out Via Config ==="
claude --no-config
```

**Résultats attendus :**
- Plan simple → `AskUserQuestion` en Phase 2, aucun grilling en Phase 4/6
- Plan complexe Phase 2 → rounds de grilling pré-amorcés (6 catégories) + 1 round suivi
- Plan complexe Phase 4 → grilling 4 catégories + recommandation + gate go/modify/stop
- Plan complexe Phase 6 → grilling 4 catégories + recommandation + gate implement/modify/stop
- `grilling.enabled: false` dans `.skill-config.yml` → comportement pré-#8 sur toutes les phases

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|

## Journal de session

### Session 2026-09-12
- ✅ Fait : Étapes 1-5 livrées hors workflow roadmap-tracking (plugin désinstallé en cours de session, implémentation directe post-grilling).
  - SKILL.md : section canonique « Grilling adaptatif » (déclencheur L/XL, toggle `grilling.enabled`, frontier réduite, format des rounds, règle « faits vs décisions »).
  - SKILL.md Phase 2 : branche complexité — grilling (6 catégories) remplace `AskUserQuestion` pour les plans complexes ; simples inchangés.
  - SKILL.md Phase 4 : grilling (4 catégories) + recommandation explicite avant la gate binaire.
  - SKILL.md Phase 6 : grilling (4 catégories) + recommandation explicite avant la gate binaire.
  - references/environment.md : clés `grilling.*` dans le schéma + sous-section `## Grilling`.
- 🔧 Écart : structure DRY retenue (section canonique unique référencée par les 3 phases) plutôt qu'une logique dupliquée par phase.
- 🚧 Blocages : issue GitHub #8 jamais créée (référencée dans le front matter mais absente du repo distant) — à créer ou à neutraliser.
- 📋 Prochain : Étape 6 (mise à jour `roadmap.md` + bump version plugin), puis 🧪 Tests et ✅ Validation.
