# Roadmap roadmap-tracking

> Backlog actif. L'historique détaillé est archivé dans `_archives/`.
> Dernière mise à jour : 2026-09-15.

## Contexte

Backlog consolidé : plans nommés d'après leur issue GitHub (voir `doc/roadmap/`).
- « À faire » : travaux restants, triés par priorité.
- « Fait » : ce qui a été livré et validé.

---

## À faire


---

## Fait

### Plans livrés (2026-09-15)

- **[Plan: 21] `#21` — Intégration recommandations audit #129** (2026-09-15) 🔵 — 4 axes d'amélioration intégrés : matrice type de tâche → modèle recommandé, règle d'escalade "2 strikes" (proxy comportemental anti-errance), section `## Diagnostic en cours` dans le template de plan, rationale proxy vs budget chiffré. 4 remédiations post-audit appliquées (procédure échec tests intermédiaires, Diagnostic hors template actif, colonne Usage, case-insensitive).
  [`21-roadmap-tracking-Integration-recommandations-audit-#129.md`](21-roadmap-tracking-Integration-recommandations-audit-#129.md)

- **[Issue: #12] `#12` — Add /clear block at Phase 5+ gates** (2026-09-14) 🔵 — Bloc informatif `/clear` injecté à 5 gates (Phase 5 POINT D'ARRÊT 2, Phase 6, tests intermédiaires, 🧪 Tests finaux, reprise wrapup). 10/10 tests PASS. Économie estimée 20K–250K tokens selon la phase et la complexité du plan.
  [`12-session-clear-gate-suggestion.md`](12-session-clear-gate-suggestion.md)

### Plans livrés (2026-09-14)

- **[Plan: 20] `#20` — Fix XS/S-solo disengagement → fast-track Phase 7** (2026-09-14) 🔵 — Désengagement automatique supprimé. Remplacé par fast-track Phase 7 : plan écrit → implémentation directe sans phases 2-6, sans ⏸️, sans tests.mode question, commit unique en fin. 5/5 étapes, 6/6 tests PASS.
  [`20-fix-xs-s-solo-disengagement-fast-track.md`](20-fix-xs-s-solo-disengagement-fast-track.md)

- **[Plan: 19] `#19` — Lock Model Gate Template** (2026-09-14) 🔵 — Verrouillage déterministe des templates upgrade/downgrade de la gate modèle (`⛔ VERBATIM` + `⛔ TOKEN = ALIAS`), support multi-fournisseur Anthropic + OpenAI/Codex (`sol`/`luna`/`terra`). 6/6 tests PASS.
  [`19-lock-model-gate-template.md`](19-lock-model-gate-template.md)

### Plans livrés (2026-09-14)

- **[Plan: 18] `#18` — Levier L2 : Élimination des tours superflus / Fast-path** (2026-09-14) 🔵 — Gate modèle Cas 1 silencieuse, Phase 1.5 sans arrêt (Cas 1), Phase 6 fusionnée dans Phase 5 pour plans XS/S/M. −2 tours plans simples, ~29 200 tokens économisés. Version 3.1.0 → 3.2.0. 8/8 tests PASS.
  [`18-roadmap-tracking-optimisation-tokens-elimination-tours-superflus-fast-path.md`](18-roadmap-tracking-optimisation-tokens-elimination-tours-superflus-fast-path.md)

- **[Plan: 17] `#17` — Compression sémantique noyau SKILL.md (L3)** (2026-09-14) 🔵 — Densification sémantique du noyau post-scission P1 : 274 → 209 lignes (−23,7 %), ~820 tokens/tour économisés. Version 3.0.0 → 3.1.0. 7/7 tests PASS.
  [`17-roadmap-tracking-optimisation-tokens-architecture-compression-semantique.md`](17-roadmap-tracking-optimisation-tokens-architecture-compression-semantique.md)

- **[Plan: 16] `#16` — Scission modulaire SKILL.md (L1)** (2026-09-14) 🔵 — SKILL.md monolithique (1 590 lignes) scindé en noyau (274 lignes) + 4 modules à chargement conditionnel. −48 % tokens skill sur 18 tours. Version 2.8.0 → 3.0.0. 10/10 tests PASS. Note: L'implémentation réelle aboutit à
**4 modules** : `modules/templates.md` a été créé puis supprimé.
  [`16-roadmap-tracking-optimisation-tokens-architecture-scission-modulaire.md`](16-roadmap-tracking-optimisation-tokens-architecture-scission-modulaire.md)

### Plans livrés (2026-09-13)

- **[Issue: #8] `#8` — Grilling adaptatif phases 2/4/6** (2026-09-12) 🔵 — Intégration du grilling (design tree, rounds pré-amorcés, frontier réduite) pour les plans complexes L/XL. Validé.
  [`8-roadmap-tracking-grilling.md`](8-roadmap-tracking-grilling.md)

- **[Plan: 15] `#15` — Robustesse hooks mécaniques anti-bypass** (2026-09-13) 🔵 — Garde mécanique (`UserPromptSubmit` + `PreToolUse` one-shot/session) contre le court-circuit du skill par les modes système. 8/8 tests PASS. Version 2.8.0.
  [`15-robustesse-hooks-mecaniques-anti-bypass.md`](15-robustesse-hooks-mecaniques-anti-bypass.md)

### Plans livrés (2026-09-12)

- **[Plan: 12] `#12` — SKILL.md Compression P1** (2026-09-12) 🔵 — gabarits commit fusionnés en section canonique + 2 renvois ; version 2.5.7 → 2.6.0. (-29 lignes, ~2 %).
  [`12-skill-compression-p1.md`](12-skill-compression-p1.md)

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
