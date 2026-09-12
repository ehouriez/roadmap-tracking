# Roadmap roadmap-tracking

> Backlog actif. L'historique détaillé est archivé dans `_archives/`.
> Dernière mise à jour : 2026-09-12.

## Contexte

Backlog consolidé : plans nommés d'après leur issue GitHub (voir `doc/roadmap/`).
- « À faire » : travaux restants, triés par priorité.
- « Fait » : ce qui a été livré et validé.

---

## À faire

- **[Issue: #8] `#8` — Grilling adaptatif phases 2/4/6** (2026-09-12) 🟢 — Intégration du grilling (design tree, rounds pré-amorcés, frontier réduite) pour les plans complexes L/XL.
  [`8-roadmap-tracking-grilling.md`](8-roadmap-tracking-grilling.md)

---

## Fait

### Plans livrés (2026-09-12)

- **[Issue: #11] `#11` — Harden applicability rules and startup rule** (2026-09-12) 🔵 — Critère objectif fichier-touché, traçabilité post-fix urgences, suppression one-shot, principe directeur avant exclusions, re-proposition doc/roadmap/ adaptative.
  [`11-applicabilite-regle-demarrage-hardening.md`](11-applicabilite-regle-demarrage-hardening.md)

- **[Issue: #10] `#10` — Invocation guard pour les fichiers du skill** (2026-09-12) 🔵 — Règle « Interdit avant ce checkpoint » + entrée bypass tacite couvrant la lecture directe des fichiers du skill ; détection obligatoire de `issues.mode` en Phase 5.
  [`10-roadmap-tracking-invocation-guard.md`](10-roadmap-tracking-invocation-guard.md)

- **[Issue: #9] `#9` — One-shot implementation option + complexity in breakpoints** (2026-09-12) 🔵 — Ajout `📊 Complexity :` en Phase 5 et reprise ; option `⚡ one-shot` qui enchaîne toutes les étapes sans tests intermédiaires ; note Phase 7 step 0.
  [`9-roadmap-tracking-one-shot-complexity.md`](9-roadmap-tracking-one-shot-complexity.md)

### Plans livrés (2026-09-11)

- **[Issue: #4] `#4` — Format tableau obligatoire pour tous les rapports** (2026-09-11) 🔵 — Règle absolue « format des rapports » + instruction de listing renforcée (interdiction du format clé-valeur).
  [`4-roadmap-tracking-rapport-format-tableau.md`](4-roadmap-tracking-rapport-format-tableau.md)

- **[Issue: #7] `#7` — Résolution tests.mode non-sautable dans la garde d'entrée** (2026-09-11) 🔵 — Nouvel item 4 dans la checklist pré-action ; table anti-court-circuit mise à jour.
  [`7-roadmap-tracking-tests-mode-garde-entree.md`](7-roadmap-tracking-tests-mode-garde-entree.md)

- **[Issue: #6] `#6` — Proposition du mode de tests axée sur l'accessibilité de l'environnement** (2026-09-11) 🔵 — Question Phase 7 recentrée sur « l'env de test est-il accessible à l'agent ? » + message de reset post-persistance + version `2.2.0`.
  [`6-roadmap-tracking-tests-mode-accessibilite.md`](6-roadmap-tracking-tests-mode-accessibilite.md)

- **[Issue: #5] `#5` — Proposition autonomous + re-jeu gate modèle** (2026-09-11) 🔵 — Proposition `manual`/`autonomous` à l'entrée Phase 7 avec persistance `.skill-config.yml` ; re-jeu de la gate modèle au changement de modèle en cours de session.
  [`5-roadmap-tracking-autonomous-proposal-model-gate-replay.md`](5-roadmap-tracking-autonomous-proposal-model-gate-replay.md)

- **[Issue: #3] `#3` — Correction des findings e2e** (2026-09-11) 🔵 — F1 listing tolérant, F2 branche reprise non conforme, F3 numérotation union, F4 limite github documentée.
  [`3-roadmap-tracking-corrections-findings-e2e.md`](3-roadmap-tracking-corrections-findings-e2e.md)

- **[Issue: #1] `#1` — roadmap-tracking : agnostique IDE/modèles + autonomie + plugin (axes A→E)** (2026-09-11) 🔵 — Généralisation du skill (5 axes), packaging plugin v2.0.0.
  [`1-roadmap-tracking-agnostic-autonomy-plugin.md`](1-roadmap-tracking-agnostic-autonomy-plugin.md)

- **[Issue: #2] `#2` — roadmap-tracking : tests e2e d'installation fraîche (black-box)** (2026-09-11) 🔵 — Campagne e2e 18/24 ✅ PASS, 6 ⚠️ PARTIAL, 0 ❌ FAIL ; 4 findings → plan #3.
  [`2-roadmap-tracking-tests-e2e-autonomes.md`](2-roadmap-tracking-tests-e2e-autonomes.md)
