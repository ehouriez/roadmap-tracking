# Référence — module-plan

> Voir aussi : [Explication module-plan](explanation-module-plan.md)

`modules/plan.md` — Phases 2 à 4. Cadrage interactif, évaluation de complexité, gate de recommandation de modèle, et proposition du plan. Toujours en lecture seule — aucun fichier écrit avant Phase 5.

---

## Phase 2 — Cadrage interactif

Mode : `🔍 MODE CADRAGE`. Aucune écriture, aucune commande.

Structure :
1. Affichage de la compréhension en 2-3 phrases avant le premier round.
2. Rounds de grilling successifs jusqu'à frontier vide.
3. Clôture : confirmation de compréhension partagée + résumé structuré des décisions.

| Round | Format |
|---|---|
| Round 1 | `AskUserQuestion` (Claude Code/Codex) |
| Rounds suivants | Texte `❓ **Qn** [Catégorie]` |

Invocation de `impeccable:impeccable` si demande UX/UI : réflexion et cadrage uniquement (pas pipeline de production).

---

## Grilling adaptatif (section canonique)

**Trigger** : systématique en Phase 2 (indépendant de `grilling.enabled`). Actif en Phases 4 et 6 pour complexité L/XL (respecte `grilling.enabled`).

**Frontier** : liste des questions dont la réponse changerait matériellement le plan. Recompute après chaque round. Vide → termination.

**Format d'un round** :
```
❓ **Q1** [Périmètre] Question...
❓ **Q2** [Dépendances] Question...
```

**Contraintes AskUserQuestion** (round 1) :
- Max 4 questions par appel
- Max 4 options par question
- `header` ≤ 12 chars
- Option recommandée en première position

**Batching** : ~3–4 questions par appel, prochain appel après réception des réponses.

**Rounds suivants** : toutes les questions de la frontier en une fois.

**Sub-agents** : utilisables pendant le grilling pour résoudre des questions factuelles sans bloquer les autres.

**Termination** : frontier vide → résumé structuré → confirmation de compréhension partagée → Phase 3.

---

## Grille de sizing

| Taille | Nb d'étapes | Effort estimé | Exemple |
|---|---|---|---|
| XS | 1 | < 30 min | Bugfix trivial |
| S | 2–4 | < 2 h | Petite feature |
| M | 5–9 | 2–6 h | Module modéré |
| L | 10–19 | 1–3 j | Fonctionnalité majeure |
| XL | 20+ | > 3 j | Refactoring complet |

---

## Matrice tier de modèle

| Tier | Alias Anthropic | Alias OpenAI |
|---|---|---|
| `standard` | sonnet | luna |
| `reasoning` | opus | sol |
| `light` (toujours mismatch) | haiku | terra |

**Résolution** : `models.map` en premier (`.skill-config.yml`), puis defaults case-insensitive.

Règle `/model` : toujours passer l'alias générique (`sonnet`, `opus`), jamais la version runtime (`Sonnet 4.6`).

---

## Gate de recommandation de modèle (section canonique)

Évaluée en Phase 1.5 (init-scan), Phase 4 (plan) et Phase 7 (execute).

| Cas | Condition | Action |
|---|---|---|
| Cas 1 | Tier actif ≥ tier requis | Continuer silencieusement — aucun affichage |
| Cas 2 | Tier actif < tier requis | Bloc `⚠️` + `⏸️` bypass stop |

Si modèle non détectable : gate silencieusement sautée.

Re-jeu : à chaque changement de modèle détecté en session.

---

## Tags d'étape

Format : `(taille · tier → modèle)`. Exemples :
- `(M · reasoning → opus)`
- `(S · standard → sonnet)`

`🧪 Tests` et `✅ Validation` ne portent jamais de tags.

---

## Phase 3 — Proposition du plan

Mode : `🧠 MODE PLAN`. Rien n'est écrit.

Contenu de la proposition :
- Objectif, périmètre (inclus / hors scope)
- Étapes avec tags `(taille · tier → modèle)`
- Décisions techniques
- Plan de tests

`⏸️ STOP POINT 1` en fin de Phase 3 — attend validation explicite avant Phase 4.

---

## Phase 4 — Validation de la proposition

| Complexité | Grilling | Gate |
|---|---|---|
| L/XL | Oui (si `grilling.enabled: true`) | Après grilling |
| XS/S/M | Non | Directe |

Résolution :
- Claude Code : `ExitPlanMode` + validation
- Autres : réponse texte explicite

Phase 5 commence uniquement sur validation explicite. `⏸️` bloquant.

---

## Estimation du surcoût skill

Affichée pour plans S/M en mode `lightweight`, `collaborative: true` :

| Complexité | Mode | Tokens Δ | Coût Δ (ref. Sonnet) | Durée Δ |
|---|---|---|---|---|
| S | lightweight | ~1 000 000 | ~$1,70 | ~2 min |
| M | lightweight | ~1 700 000 | ~$2,80 | ~4 min |
| L | full | ~2 800 000 | ~$4,80 | ~7 min |
| XL | full | ~4 500 000 | ~$7,50 | ~11 min |
