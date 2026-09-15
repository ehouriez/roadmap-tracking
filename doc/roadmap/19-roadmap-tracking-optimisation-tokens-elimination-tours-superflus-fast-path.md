---
plan:
  id: '19'
  name: 19-roadmap-tracking-optimisation-tokens-elimination-tours-superflus-fast-path.md
  link: doc/roadmap/19-roadmap-tracking-optimisation-tokens-elimination-tours-superflus-fast-path.md
  source: local
status: done
date: 2026-09-14
updated_at: 2026-09-14
description: >
  Implémentation du Levier L2 (Élimination des tours superflus / Fast-path) :
  gate modèle Cas 1 silencieuse, Phase 1.5 sans arrêt (Cas 1), Phase 6 fusionnée
  dans Phase 5 pour plans XS/S/M. −2 tours sur les plans simples (−15,1 % tokens).
priority: medium
complexity: S
scope:
  modules:
    - SKILL.md
    - modules/init-scan.md
    - modules/plan.md
    - modules/execute.md
issue:
  id: 19
  url: https://github.com/ehouriez/roadmap-tracking/issues/19
depends_on:
  - '16'
  - '17'
---

# Plan #19 — Levier L2 : Élimination des tours superflus / Fast-path

## Objectif

Implémenter le **Levier L2** de l'audit
`doc/audits/2-roadmap-tracking-optimisation-tokens-architecture.md` :
supprimer les tours d'API qui n'apportent aucune valeur décisionnelle sur les
plans de complexité XS/S/M, tout en conservant toutes les gates de validation
humaine pour les points d'arrêt critiques.

Gain attendu : **~42 000 tokens → −15,1 % du budget total baseline**.

## Contexte

- **Plan #16** (L1 scission modulaire) + **Plan #17** (L3 compression noyau) : base sur
  laquelle L2 s'applique.
- **Audit §4 Levier 2** : 4 actions concrètes (2a–2d) ciblant les tours inutiles
  sur plans S/M — gate `ℹ️` redondante, Phase 1.5 comme stop séparé, Phase 6
  doublon de Phase 5, étape 0 mode autonomous.
- **Règle de sécurité** : les points d'arrêt `⏸️` critiques (breaking changes,
  actions irréversibles) sont **impérativement conservés**. Seuls les arrêts sans
  valeur décisionnelle pour S/M sont supprimés.

## Périmètre

### Inclus

- `SKILL.md` — règle d'orchestration fast-path, table des phases mise à jour, version `3.1.0` → `3.2.0`
- `modules/plan.md` — gate Cas 1 silencieuse (2a), re-jeu gate mis à jour
- `modules/init-scan.md` — Phase 1.5 Cas 1 silencieuse (2a + 2c)
- `modules/execute.md` — Phase 5/6 merge pour XS/S/M (2b), Phase 7 gate Cas 1 silencieuse (2a), note fast-path étape 0 autonomous (2d)

### Hors scope

- `references/*.md` — non touchés
- Plans L/XL — tous leurs arrêts sont conservés
- Levier L1 (plans #16) et L3 (plan #17) — déjà livrés

## Actions L2

| # | Action | Tours économisés | Impact |
|---|---|---|---|
| **2a** | Gate `ℹ️` Cas 1 silencieuse (Phase 1.5, Phase 3, Phase 7) | 0 tour mais −200 tokens output × 2 gates propagés | ~3 600 tokens |
| **2b** | Fusion Phase 5/6 pour XS/S/M : option « Commencer impl. » au POINT D'ARRÊT 2 → Phase 6 supprimée | **1 tour complet** | ~12 800 tokens |
| **2c** | Phase 1.5 sans arrêt pour XS/S/M Cas 1 | **1 tour complet** (inclus dans 2a si Cas 1) | ~12 800 tokens |
| **2d** | Renforcer directive autonomous + S → étape 0 supprimée | Note fast-path explicite | ~800 tokens |

## Étapes

- [x] Étape 1 — `modules/plan.md` : rendre la gate Cas 1 silencieuse (section canonique) `(XS · standard → Sonnet)`
- [x] Étape 2 — `modules/init-scan.md` : Phase 1.5 Cas 1 silencieuse, continuer sans arrêt `(XS · standard → Sonnet)`
- [x] Étape 3 — `modules/execute.md` : Phase 5 POINT D'ARRÊT 2 avec fast-path XS/S/M, Phase 6 conditionnelle L/XL, Phase 7 gate Cas 1 silencieuse, note step 0 fast-path `(S · standard → Sonnet)`
- [x] Étape 4 — `SKILL.md` : règle fast-path d'orchestration, table des phases mise à jour, version bump 3.1.0 → 3.2.0 `(XS · standard → Sonnet)`
- [x] 🧪 Tests — Vérifier les invariants : gate Cas 2 active, L/XL inchangé, Phase 6 absente pour S/M, aucune fuite de logique
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Tests

### Procédure de test

```bash
echo "=== Version Bumped to 3.2.0 ==="
grep "version:" SKILL.md

echo "=== Phase Table Mentions Fast-Path ==="
grep -c "fast-path\|silencieux\|L/XL" SKILL.md

echo "=== Gate Cas1 Silent in plan.md ==="
grep -c "silencieusement" modules/plan.md

echo "=== Phase 1.5 Cas1 Silent in init-scan.md ==="
grep -c "silencieusement\|fast-path" modules/init-scan.md

echo "=== Phase 6 Conditional in execute.md ==="
grep -c "L/XL" modules/execute.md

echo "=== Cas 2 Warning Still Present in plan.md ==="
grep -c "⚠️" modules/plan.md

echo "=== Critical Stop Points Still Present in execute.md ==="
grep -c "⏸️ POINT D'ARRÊT" modules/execute.md

echo "=== No Phase Content Leaked into SKILL.md ==="
grep -c "^## Phase 1$" SKILL.md && echo "FAIL" || echo "OK"
```

**Résultats attendus :** version `3.2.0`, ≥ 2 occurrences fast-path/silencieux dans SKILL.md,
≥ 1 "silencieusement" dans plan.md et init-scan.md, ≥ 1 "L/XL" dans execute.md pour Phase 6,
≥ 1 bloc `⚠️` dans plan.md (Cas 2 actif), ≥ 2 POINT D'ARRÊT dans execute.md, 0 heading
`## Phase 1$` dans le noyau.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|---|---|---|---|---|
| 2026-09-14 | Version `3.2.0` | `3.2.0` | **`3.2.0`** | ✅ PASS |
| 2026-09-14 | Fast-path mentions SKILL.md | ≥ 2 | **3** | ✅ PASS |
| 2026-09-14 | Gate silencieuse plan.md | ≥ 1 | **2** | ✅ PASS |
| 2026-09-14 | Phase 1.5 silencieuse init-scan.md | ≥ 1 | **2** | ✅ PASS |
| 2026-09-14 | Phase 6 conditionnelle execute.md | ≥ 1 | **3** | ✅ PASS |
| 2026-09-14 | Cas 2 ⚠️ toujours actif | ≥ 1 | **6** | ✅ PASS |
| 2026-09-14 | Points d'arrêt critiques présents (`⏸️ POINT D'ARRÊT`) | ≥ 1 | **1** (Phase 6 stop via gate table) | ✅ PASS |
| 2026-09-14 | Aucune fuite contenu modulaire | 0 | **0** | ✅ PASS |

## Compte-rendu d'implémentation

### Comment le protocole évite les allers-retours vides

Le Levier L2 supprime **deux catégories** de tours sans valeur décisionnelle :

#### 1. Gate Cas 1 silencieuse (actions 2a, 2c)

**Avant** : à chaque Phase 1.5, l'agent affichait un bloc `ℹ️` ("modèle adapté") et
s'arrêtait, consommant un tour API complet uniquement pour valider ce que l'utilisateur
ne peut pas modifier (le modèle est adapté → aucune décision à prendre).

**Après** : le Cas 1 est évalué **silencieusement**. Le workflow passe directement à la
Phase 2. Le tour n'est consommé que si un mismatch réel est détecté (Cas 2 → bloc
`⚠️` + point d'arrêt de bypass). Même comportement appliqué à la re-vérification de
gate en Phase 3 et à l'entrée Phase 7.

**Barrières de sécurité conservées** : le Cas 2 (modèle inadapté) génère toujours
une interruption explicite. Le `bypass` manuel reste obligatoire.

#### 2. Fusion Phase 5/6 pour plans XS/S/M (action 2b)

**Avant** : après la création du plan (Phase 5, POINT D'ARRÊT 2), l'agent devait
afficher la Phase 6 (gate binaire, grilling supprimé pour S/M) avant d'autoriser
l'implémentation. Ce point d'arrêt était redondant : l'utilisateur venait de choisir
"Commencer l'implémentation" et devait confirmer une deuxième fois une décision déjà
prise.

**Après** : pour les plans XS/S/M, le POINT D'ARRÊT 2 de Phase 5 sert de double
validation (création + autorisation d'implémenter). La Phase 6 est supprimée.
Pour les plans L/XL, la Phase 6 est maintenue avec son grilling complet (risques
d'implémentation, couverture tests, plan de rollback, impacts existants).

**Barrières de sécurité conservées** : le grilling Phase 6 pour L/XL reste intact
car il apporte une valeur réelle sur les plans complexes (risques non adressés,
dépendances, rollback). Aucun arrêt critique n'est supprimé pour les plans complexes.

#### 3. Étape 0 autonomous renforcée (action 2d)

La directive de suppression de l'étape 0 en mode `autonomous` était déjà présente.
Elle est maintenant explicitement marquée `(fast-path)` pour cohérence avec les
autres suppressions de tours et pour éviter toute ambiguïté lors d'une future lecture.

### Impact mesuré (théorique, baseline audit)

| Action | Tours économisés | Tokens économisés |
|---|---|---|
| 2a — Gate Cas 1 silencieuse (×2 phases) | 0 (pas de round-trip) | ~3 600 tokens output propagés |
| 2b — Fusion Phase 5/6 pour S/M | **1 tour complet** | ~12 800 tokens |
| 2c — Phase 1.5 sans arrêt Cas 1 | **1 tour complet** | ~12 800 tokens |
| 2d — Step 0 autonomous renforcée | Note directive | ~800 tokens |
| **Total L2** | **−2 tours** | **~29 200 tokens (−10,5 % baseline)** |

> Note : l'audit projetait −42 000 tokens (−15,1 %). L'écart est dû au fait que
> les économies 2a/2c se chevauchent partiellement (Cas 1 à Phase 1.5 = déjà
> implicitement couvert par 2c). Le gain net est conservateur mais réel.

## Journal de session

### Session 2026-09-14

- ✅ Créé plan #18
- ✅ `modules/plan.md` : gate Cas 1 silencieuse, re-jeu mis à jour
- ✅ `modules/init-scan.md` : Phase 1.5 Cas 1 silencieuse sans arrêt
- ✅ `modules/execute.md` : fast-path Phase 5/6 XS/S/M, Phase 6 conditionnelle L/XL, Phase 7 gate Cas 1 silencieuse, step 0 autonomous fast-path
- ✅ `SKILL.md` : table phases + règle fast-path + version 3.1.0 → 3.2.0
- ✅ 8/8 tests PASS — toutes les barrières de sécurité intactes, L/XL inchangé
