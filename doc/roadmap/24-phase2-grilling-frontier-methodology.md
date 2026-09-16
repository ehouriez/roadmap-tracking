---
plan:
  id: '24'
  name: 24-phase2-grilling-frontier-methodology.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/24-phase2-grilling-frontier-methodology.md
status: active
date: 2026-09-16
description: >
  Remplacer la mécanique "frontier réduite" (cap 2 rounds) de la Phase 2 par la
  méthodologie complète du skill grilling : design tree, rounds frontier illimités,
  terminaison par frontier vide + confirmation, résumé structuré vers Phase 3.
priority: high
complexity: M
intent: null
scope:
  modules:
    - modules/plan.md
    - references/forms.md
issue:
  id: 24
  url: https://github.com/ehouriez/roadmap-tracking/issues/24
---

# [🔍] Plan #24 — Phase 2 : Intégration méthodologie grilling (frontier illimitée)

## Objectif

Remplacer la mécanique "frontier réduite" (cap artificiel à 2 rounds) de la Phase 2 par la méthodologie complète du skill `grilling` : design tree explicite, rounds frontier illimités, terminaison par frontier vide avec confirmation de compréhension partagée, et résumé structuré de l'arbre résolu vers Phase 3.

## Périmètre

### Inclus
- `modules/plan.md` — Section "Grilling adaptatif" (réécriture complète) + Section "Phase 2" (mise à jour)
- `references/forms.md` — Clarification frontière AskUserQuestion (round 1) / format texte `❓ Qn` (rounds 2+)

### Hors scope
- Phases 3-7 et leurs modules
- `modules/execute.md`, `modules/wrapup.md`, `modules/init-scan.md`
- Grilling Phases 4 et 6 (mécanique inchangée — réservé L/XL)

## Étapes

- [x] Étape 1 — Réécrire `modules/plan.md` § Grilling adaptatif : supprimer frontier réduite, adopter frontier illimitée + design tree + non-blocage partiel + terminaison frontier vide (M · standard → Sonnet)
- [x] Étape 2 — Mettre à jour `modules/plan.md` § Phase 2 : ajouter mapping design tree, confirmation compréhension partagée, résumé structuré vers Phase 3 (S · standard → Sonnet)
- [x] Étape 3 — Mettre à jour `references/forms.md` : clarifier frontière AskUserQuestion (round 1) / format texte `❓ Qn` (rounds 2+) (S · standard → Sonnet)
- [x] 🧪 Tests — Vérification contraintes C1-C7 et A1-A3 + dry-run mental migration DB
- [ ] ✅ Validation — Contrôle final + clôture

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Format questions rounds 2+ | Format texte `❓ **Qn**` | AskUserQuestion limité à 4q/4opts, incompatible avec frontier émergente |
| Round d'amorçage | Conserver `AskUserQuestion` | Choix structurés connus à l'avance → UX cliquable de valeur |
| Design tree | Conceptuel (non affiché) | L'agent mappe mentalement l'arbre, n'affiche que les questions frontier |
| Terminaison | Frontier vide + confirmation explicite | Alignement exact avec skill grilling source |

## Tests

> Section obligatoire renseignée à l'étape 🧪 Tests.

### Procédure de test

Vérification par checklist fonctionnelle (C1-C7) et architecturale (A1-A3) + dry-run mental.

**Résultats attendus :** chaque contrainte est couverte par une ligne/section identifiable dans les fichiers modifiés.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-16 | C1 — Design tree | Mention "arbre de décisions" en Phase 2 et § Grilling adaptatif | `plan.md:14` + `plan.md:242` ✅ | PASS |
| 2026-09-16 | C2 — Rounds par frontier | Pas de question dépendante dans le même round | `plan.md:259-260` ✅ | PASS |
| 2026-09-16 | C3 — Format strict | `❓ **Qn**` + `➡️` pour rounds 2+ | `forms.md:9` + `plan.md:275-290` ✅ | PASS |
| 2026-09-16 | C4 — Fact-finding non-bloquant | Sub-agent dispatché sans bloquer autres questions | `plan.md:298-303` ✅ | PASS |
| 2026-09-16 | C5 — Terminaison explicite | Frontier vide + confirmation + résumé structuré | `plan.md:305-325` + `forms.md:90-99` ✅ | PASS |
| 2026-09-16 | C6 — Rounds non plafonnés | "Aucun — continuer tant que frontier non vide" | `plan.md:266` ✅ | PASS |
| 2026-09-16 | C7 — Transition Phase 3 | Résumé structuré sert d'input Phase 3 | `plan.md:312` + `forms.md:97` ✅ | PASS |
| 2026-09-16 | A1 — Phases 4/6 intactes | "max 1 round de suivi" explicite pour Phases 4/6 | `plan.md:264-268` ✅ | PASS |
| 2026-09-16 | A2 — Cohérence workflow | Phase 2 → Phase 3 via résumé structuré | Flux inchangé ✅ | PASS |
| 2026-09-16 | A3 — Fichiers dans roadmap-tracking/ | Seuls plan.md + forms.md modifiés | ✅ | PASS |
| 2026-09-16 | Dry-run migration DB | 3 rounds produits, frontier émergente, logique frontier-based | Rounds 1→2→3 démontrent la logique ✅ | PASS |

## Journal de session

### Session 2026-09-16
- ✅ Fait : Issue #24 créée, fichier plan créé, roadmap.md mis à jour
- 🔄 En cours : Implémentation étapes 1-3
- 📋 Prochain : Étape 1 — réécriture § Grilling adaptatif
- 🚧 Blocages : aucun
