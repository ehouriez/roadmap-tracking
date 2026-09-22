# Roadmap roadmap-tracking

> Backlog actif. L'historique détaillé est archivé dans `_archives/`.
> Dernière mise à jour : 2026-09-22.

## Contexte

Backlog consolidé : plans nommés d'après leur issue GitHub (voir `doc/roadmap/`).
- « À faire » : travaux restants, triés par priorité.
- « Fait » : ce qui a été livré et validé.

---

## À faire

*(aucun plan actif)*

---

## Fait

### Plans livrés (2026-09-22)

- **[Issue: #26] `#26` — Autonomous Test Prerequisites** (2026-09-22) 🔵 — Ajout de `### Prérequis pour les tests` avant `### Procédure de test` dans `references/templates.md`. Règle ⛔ zero-lookup imposant la section dans `modules/execute.md` (tests intermédiaires + tests finaux). Modes `manual` et `autonomous` couverts. 6/6 tests PASS.
  [`26-autonomous-test-prerequisites.md`](done/26-autonomous-test-prerequisites.md)

- **[Issue: #24] `#24` — Phase 2 : Intégration méthodologie grilling (frontier illimitée)** (2026-09-22) 🔵 — Remplacement de la frontier réduite (cap 2 rounds) par la méthodologie complète : design tree, rounds illimités, terminaison frontier vide + confirmation, résumé structuré vers Phase 3. Mise à jour `modules/plan.md` § Grilling adaptatif + `references/forms.md`. 10/10 tests PASS.
  [`24-phase2-grilling-frontier-methodology.md`](done/24-phase2-grilling-frontier-methodology.md)

- **[Issue: #25] `#25` — Gestion des plans clôturés dans done/** (2026-09-22) 🔵 — Plans `status: done` déplacés dans `doc/roadmap/done/`. Listing init-scan exclut `done/` (seul le reste à faire affiché). Règle explicite : le skill peut lire `done/` pour du contexte. Migration 23 plans existants. 10/10 tests PASS.
  [`25-done-subfolder-plan-management.md`](done/25-done-subfolder-plan-management.md)

---

### Plans livrés (2026-09-15)

- **[Issue: #23] `#23` — Phase 2 Grilling Obligatoire** (2026-09-15) 🔵 — Phase 2 obligatoire toutes complexités (XS→XL). Fast-track XS/S-solo supprimé (→ mode lightweight). Grilling universel en Phase 2, `AskUserQuestion` supprimé. Bypass `intent:prototype` retiré. `grilling.enabled` ignoré en Phase 2. 7/7 tests PASS.
  [`23-phase2-grilling-obligatoire.md`](done/23-phase2-grilling-obligatoire.md)

- **[Issue: #22] `#22` — Intégration recommandations audit #129** (2026-09-15) 🔵 — 4 axes d'amélioration intégrés : matrice type de tâche → modèle recommandé, règle d'escalade "2 strikes" (proxy comportemental anti-errance), section `## Diagnostic en cours` dans le template de plan, rationale proxy vs budget chiffré. 4 remédiations post-audit appliquées (procédure échec tests intermédiaires, Diagnostic hors template actif, colonne Usage, case-insensitive).
  [`22-roadmap-tracking-Integration-recommandations-audit-#129.md`](done/22-roadmap-tracking-Integration-recommandations-audit-#129.md)

- **[Issue: #12] `#12` — Add /clear block at Phase 5+ gates** (2026-09-14) 🔵 — Bloc informatif `/clear` injecté à 5 gates (Phase 5 POINT D'ARRÊT 2, Phase 6, tests intermédiaires, 🧪 Tests finaux, reprise wrapup). 10/10 tests PASS. Économie estimée 20K–250K tokens selon la phase et la complexité du plan.
  [`12-session-clear-gate-suggestion.md`](done/12-session-clear-gate-suggestion.md)

### Plans livrés (2026-09-14)

- **[Issue: #21] `#21` — Fix XS/S-solo disengagement → fast-track Phase 7** (2026-09-14) 🔵 — Désengagement automatique supprimé. Remplacé par fast-track Phase 7 : plan écrit → implémentation directe sans phases 2-6, sans ⏸️, sans tests.mode question, commit unique en fin. 5/5 étapes, 6/6 tests PASS.
  [`21-fix-xs-s-solo-disengagement-fast-track.md`](done/21-fix-xs-s-solo-disengagement-fast-track.md)

- **[Issue: #20] `#20` — Lock Model Gate Template** (2026-09-14) 🔵 — Verrouillage déterministe des templates upgrade/downgrade de la gate modèle (`⛔ VERBATIM` + `⛔ TOKEN = ALIAS`), support multi-fournisseur Anthropic + OpenAI/Codex (`sol`/`luna`/`terra`). 6/6 tests PASS.
  [`20-lock-model-gate-template.md`](done/20-lock-model-gate-template.md)

### Plans livrés (2026-09-14)

- **[Issue: #19] `#19` — Levier L2 : Élimination des tours superflus / Fast-path** (2026-09-14) 🔵 — Gate modèle Cas 1 silencieuse, Phase 1.5 sans arrêt (Cas 1), Phase 6 fusionnée dans Phase 5 pour plans XS/S/M. −2 tours plans simples, ~29 200 tokens économisés. Version 3.1.0 → 3.2.0. 8/8 tests PASS.
  [`19-roadmap-tracking-optimisation-tokens-elimination-tours-superflus-fast-path.md`](done/19-roadmap-tracking-optimisation-tokens-elimination-tours-superflus-fast-path.md)

- **[Issue: #18] `#18` — Compression sémantique noyau SKILL.md (L3)** (2026-09-14) 🔵 — Densification sémantique du noyau post-scission P1 : 274 → 209 lignes (−23,7 %), ~820 tokens/tour économisés. Version 3.0.0 → 3.1.0. 7/7 tests PASS.
  [`18-roadmap-tracking-optimisation-tokens-architecture-compression-semantique.md`](done/18-roadmap-tracking-optimisation-tokens-architecture-compression-semantique.md)

- **[Issue: #17] `#17` — Scission modulaire SKILL.md (L1)** (2026-09-14) 🔵 — SKILL.md monolithique (1 590 lignes) scindé en noyau (274 lignes) + 4 modules à chargement conditionnel. −48 % tokens skill sur 18 tours. Version 2.8.0 → 3.0.0. 10/10 tests PASS. Note: L'implémentation réelle aboutit à
**4 modules** : `modules/templates.md` a été créé puis supprimé.
  [`17-roadmap-tracking-optimisation-tokens-architecture-scission-modulaire.md`](done/17-roadmap-tracking-optimisation-tokens-architecture-scission-modulaire.md)

### Plans livrés (2026-09-13)

- **[Issue: #8] `#8` — Grilling adaptatif phases 2/4/6** (2026-09-12) 🔵 — Intégration du grilling (design tree, rounds pré-amorcés, frontier réduite) pour les plans complexes L/XL. Validé.
  [`8-roadmap-tracking-grilling.md`](done/8-roadmap-tracking-grilling.md)

- **[Issue: #16] `#16` — Robustesse hooks mécaniques anti-bypass** (2026-09-13) 🔵 — Garde mécanique (`UserPromptSubmit` + `PreToolUse` one-shot/session) contre le court-circuit du skill par les modes système. 8/8 tests PASS. Version 2.8.0.
  [`16-robustesse-hooks-mecaniques-anti-bypass.md`](done/16-robustesse-hooks-mecaniques-anti-bypass.md)

- **[Issue: #15] `#15` — Bug : hook cold-start inactif + guardrail de désengagement bypassé** (2026-09-13) 🔵 — Correction hook `SessionStart` (suppression précondition `test -d ./doc/roadmap`) + guardrail de désengagement S-solo durci (règle `⛔ Garde dure`).
  [`15-bug-hook-cold-start-et-guardrail-desengagement.md`](done/15-bug-hook-cold-start-et-guardrail-desengagement.md)

- **[Issue: #14] `#14` — Analyse et proposition d'amélioration du skill roadmap-tracking** (2026-09-13) 🔵 — Analyse post-création du skill : 5 axes diagnostiqués (désengagement prototypage, modes système, optimisation tokens, architecture modulaire, aide) + décisions confirmées (Axe D, Axe E).
  [`14-analyse-axes-amélioration.md`](done/14-analyse-axes-amélioration.md)

### Plans livrés (2026-09-12)

- **[Issue: #13] `#13` — SKILL.md Compression P1** (2026-09-12) 🔵 — gabarits commit fusionnés en section canonique + 2 renvois ; version 2.5.7 → 2.6.0. (-29 lignes, ~2 %).
  [`13-skill-compression-p1.md`](done/13-skill-compression-p1.md)

- **[Issue: #11] `#11` — Harden applicability rules and startup rule** (2026-09-12) 🔵 — Critère objectif fichier-touché, traçabilité post-fix urgences, suppression one-shot, principe directeur avant exclusions, re-proposition doc/roadmap/ adaptative.
  [`11-applicabilite-regle-demarrage-hardening.md`](done/11-applicabilite-regle-demarrage-hardening.md)

- **[Issue: #10] `#10` — Invocation guard pour les fichiers du skill** (2026-09-12) 🔵 — Règle « Interdit avant ce checkpoint » + entrée bypass tacite couvrant la lecture directe des fichiers du skill ; détection obligatoire de `issues.mode` en Phase 5.
  [`10-roadmap-tracking-invocation-guard.md`](done/10-roadmap-tracking-invocation-guard.md)

- **[Issue: #9] `#9` — One-shot implementation option + complexity in breakpoints** (2026-09-12) 🔵 — Ajout `📊 Complexity :` en Phase 5 et reprise ; option `⚡ one-shot` qui enchaîne toutes les étapes sans tests intermédiaires ; note Phase 7 step 0.
  [`9-roadmap-tracking-one-shot-complexity.md`](done/9-roadmap-tracking-one-shot-complexity.md)

### Plans livrés (2026-09-11)

- **[Issue: #4] `#4` — Format tableau obligatoire pour tous les rapports** (2026-09-11) 🔵 — Règle absolue « format des rapports » + instruction de listing renforcée (interdiction du format clé-valeur).
  [`4-roadmap-tracking-rapport-format-tableau.md`](done/4-roadmap-tracking-rapport-format-tableau.md)

- **[Issue: #7] `#7` — Résolution tests.mode non-sautable dans la garde d'entrée** (2026-09-11) 🔵 — Nouvel item 4 dans la checklist pré-action ; table anti-court-circuit mise à jour.
  [`7-roadmap-tracking-tests-mode-garde-entree.md`](done/7-roadmap-tracking-tests-mode-garde-entree.md)

- **[Issue: #6] `#6` — Proposition du mode de tests axée sur l'accessibilité de l'environnement** (2026-09-11) 🔵 — Question Phase 7 recentrée sur « l'env de test est-il accessible à l'agent ? » + message de reset post-persistance + version `2.2.0`.
  [`6-roadmap-tracking-tests-mode-accessibilite.md`](done/6-roadmap-tracking-tests-mode-accessibilite.md)

- **[Issue: #5] `#5` — Proposition autonomous + re-jeu gate modèle** (2026-09-11) 🔵 — Proposition `manual`/`autonomous` à l'entrée Phase 7 avec persistance `.skill-config.yml` ; re-jeu de la gate modèle au changement de modèle en cours de session.
  [`5-roadmap-tracking-autonomous-proposal-model-gate-replay.md`](done/5-roadmap-tracking-autonomous-proposal-model-gate-replay.md)

- **[Issue: #3] `#3` — Correction des findings e2e** (2026-09-11) 🔵 — F1 listing tolérant, F2 branche reprise non conforme, F3 numérotation union, F4 limite github documentée.
  [`3-roadmap-tracking-corrections-findings-e2e.md`](done/3-roadmap-tracking-corrections-findings-e2e.md)

- **[Issue: #1] `#1` — roadmap-tracking : agnostique IDE/modèles + autonomie + plugin (axes A→E)** (2026-09-11) 🔵 — Généralisation du skill (5 axes), packaging plugin v2.0.0.
  [`1-roadmap-tracking-agnostic-autonomy-plugin.md`](done/1-roadmap-tracking-agnostic-autonomy-plugin.md)

- **[Issue: #2] `#2` — roadmap-tracking : tests e2e d'installation fraîche (black-box)** (2026-09-11) 🔵 — Campagne e2e 18/24 ✅ PASS, 6 ⚠️ PARTIAL, 0 ❌ FAIL ; 4 findings → plan #3.
  [`2-roadmap-tracking-tests-e2e-autonomes.md`](done/2-roadmap-tracking-tests-e2e-autonomes.md)
