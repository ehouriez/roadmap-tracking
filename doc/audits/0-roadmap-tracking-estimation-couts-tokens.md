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

---

## Pistes de rationalisation de la consommation tokens

> Analyse réalisée le 2026-09-12 sur la base du scénario A ci-dessus (plan S, 18 tours, ~278 000 tokens).

### Hypothèses de découpage interne du skill

SKILL.md mesuré : 10 144 mots (~10 000 tokens/tour), 1 369 lignes réparties ainsi :

| Section | Lignes | Tokens estimés | % du skill |
|---|---|---|---|
| Header + préambule (applicabilité, garde, gates, grilling) | 665 | ~4 850 | 48 % |
| Phases 1-5 — Planning | 220 | ~1 600 | 16 % |
| Phases 6-7 + tests + reprise — Implémentation | 484 | ~3 550 | 35 % |

Répartition session S : ~12 tours en phase planning, ~6 tours en phase implémentation.

### Tableau des pistes

| # | Piste | Type | Mécanisme | Impact estimé (tokens) | Impact ratio A/B | Risque fiabilité |
|---|---|---|---|---|---|---|
| 1 | **Compression SKILL.md −35%** (supprimer 13 blocs ❌ redondants, fusionner gabarits dupliqués planning/reprise, compresser descriptions de tables répétées) | Actionnable | 10 000 → 6 500 tokens/tour × 18 = −63 000 input | −63 000 | ×10.7 → ×8.3 | **Faible** — règles inchangées, formulation seule compressée |
| 2 | **Scission planning / implémentation** (skill "lite" chargé au démarrage avec header+phases 1-5 ; phases 6-7+reprise chargées uniquement à l'entrée Phase 7 via `Skill()`) | Actionnable | Post-P1 : tours 1-12 à 4 200 au lieu de 6 500 → −2 300/tour × 12 = −27 500 incrémental vs P1 seul | −27 500 (après P1) | ×8.3 → ×7.1 | **Moyen** — la section « reprise » doit rester accessible dès la règle de démarrage ; le résumé de reprise (~200 tokens) doit être dupliqué dans le skill lite, la procédure complète restant dans le skill implémentation |
| 3 | **Prompt caching côté plateforme** (marquer le skill text avec `cache_control: ephemeral` — Claude API/Claude Code ; skill reads cost ≈10 % sur tours 2-N) | Plateforme | Post-P1+P2 : tours 2-12 à 420 (planning caché) + tours 14-18 à 650 (full caché) → −75 000 coût-équivalent | −75 000 coût-équiv. | ratio coût ×7.1 → **×4.2** | **Nul** (transparent) |
| 4 | **Fusion ⏸️2 + gate Phase 6 pour S/M** (⏸️2 option « 1-Start » = autorisation d'implémenter ; supprimer le redirect vers une Phase 6 séparée — tables sémantiquement identiques pour S/M) | Actionnable | 1 tour complet économisé × (6 500 post-P1 skill + 5 000 system) + ~500 output = −12 000 | −12 000 | ×7.1 → ×6.6 | **Faible** — Pour L/XL (grilling Phase 4 et Phase 6 distincts) : garder les deux étapes |
| 5 | **Silence gate ℹ️ Cas 1** (tier match = ne rien afficher ; bloquer uniquement en Cas 2 mismatch → ⏸️ bypass) | Actionnable | ~200 tokens output × 2 gates (Phase 1.5 + Phase 7) propagés sur ~16 tours input = −3 400 + −400 output | −3 800 | ×6.6 → ×6.5 | **Très faible** — ℹ️ est informationnel, aucun checkpoint bloquant |
| 6 | **Garde « référence déjà en contexte »** (instruction dans le skill : ne pas relire `environment.md` si déjà chargé dans la session) | Actionnable | −1 700 tokens (environment.md ≈ 1 600 mots × 1 re-lecture évitée) | −1 700 | marginal | **Très faible** |
| — | **Total cumulé actionnable (P1+P2+P4+P5+P6)** | — | — | **−108 000 tokens** | **×10.7 → ×6.5** | — |
| — | **+ Plateforme (P3)** | — | — | **−183 000 coût-équiv.** | **ratio coût ~×4.0** | — |

### Lecture

Le levier dominant est P1 (compression textuelle) — seul levier applicable sur la totalité des 18 tours sans contrainte d'architecture. P2 (scission) est le deuxième levier ; sa contrainte principale est que la section « reprise d'un plan existant » doit rester accessible dès la règle de démarrage. P4 (fusion stops) est **non applicable à L/XL** : la Phase 4 grilling et la Phase 6 grilling sont des étapes de réflexion distinctes pour les plans complexes. P3 est hors portée du skill — c'est une décision d'infrastructure Claude Code (annotation des skill injections comme breakpoints de cache).

### Priorité d'action suggérée

P1 en premier : impact maximal, risque minimal, faisable en une session. Cible concrète : les 13 blocs `❌` redondants + les 3 gabarits de commit répétés identiquement dans les sections « tests intermédiaires », « 🧪 Tests » et « Commit d'implémentation » (ces 3 sections partagent ~80 % de leur contenu).
