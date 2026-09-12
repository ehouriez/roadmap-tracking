## Demande

Estime le coût en tokens de cette conversation selon deux scénarios.
Exclure de l'estimation les tokens de ce prompt-ci et de ta réponse.

### Scénario A — Réel (avec le skill /roadmap-tracking chargé et utilisé)

Comptabiliser :
- Tokens d'entrée (input) : system prompt, skill chargé, messages utilisateur,
  contexte fichiers lus
- Tokens de sortie (output) : toutes les réponses de l'agent
- Tokens de raisonnement (thinking) si applicable

### Scénario B — Contrefactuel (implémentation directe sans le skill)

Estimer ce qu'aurait coûté la même conversation si l'agent avait implémenté
directement sans charger ni dérouler le workflow du skill. Expliciter les
hypothèses retenues pour cette estimation.

### Format de sortie

| Catégorie | Scénario A (avec skill) | Scénario B (sans skill) | Delta |
|---|---|---|---|
| Tokens input | | | |
| Tokens output | | | |
| Tokens thinking | | | |
| **Total** | | | |

Ajouter une ligne de coût monétaire estimé si les tarifs du modèle sont connus.

---

## Résultats

> ⚠️ Estimations par comptage manuel et extrapolation — pas de métriques réelles accessibles.

### Plan de complexité S — session du 2026-09-12 (plan #11, hardening Applicabilité + Règle de démarrage)

#### Méthodologie

**Scénario A — composants estimés :**
- Skill text (SKILL.md chargé via `Skill()`) : ~10 000 tokens, présent à chaque tour d'entrée
- System prompts + reminders (ponytail, concise, auto, env, rules) : ~5 000 tokens/tour
- Lectures de fichiers (SKILL.md complet, templates.md, roadmap.md, bash outputs) : ~20 000 tokens cumulés
- Messages utilisateur + réponses agent cumulés : ~13 000 tokens
- Nombre de tours API estimé : ~18

**Scénario B — hypothèses :**
1. Pas de skill chargé → pas de workflow overhead
2. 4 tours : prompt → lecture sections cibles → 2 édits → confirmation
3. Lecture : ~1 500 tokens (sections Applicabilité + Règle de démarrage uniquement)
4. Pas d'AskUserQuestion (2 rounds supprimés), pas de création plan/issue/roadmap
5. System prompt baseline identique (~5 000/tour) — seul le skill text est absent

#### Tableau

| Catégorie | Scénario A (avec skill) | Scénario B (sans skill) | Ratio A/B |
|---|---|---|---|
| Complexité du plan | S | S | — |
| Tokens input | ~265 000 | ~24 000 | ×11 |
| Tokens output | ~10 500 | ~1 500 | ×7 |
| Tokens thinking | ~2 500 | ~400 | ×6 |
| **Total** | **~278 000** | **~25 900** | **×10.7** |

#### Lecture

Le ratio ×10 est presque entièrement porté par la **répétition du skill text** (~10 000 tokens × 18 tours = ~180 000 tokens), soit ~65 % du coût total du scénario A. C'est le prix d'un workflow formalisé sur un plan S. Sur un plan L/XL — où le skill apporte le plus de valeur — le ratio serait moindre, car le numérateur (B) croît aussi avec la complexité.
