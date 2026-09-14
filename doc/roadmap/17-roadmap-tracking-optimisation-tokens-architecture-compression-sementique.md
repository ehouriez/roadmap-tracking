---
plan:
  id: '17'
  name: 17-roadmap-tracking-optimisation-tokens-architecture-compression-sementique.md
  link: doc/roadmap/17-roadmap-tracking-optimisation-tokens-architecture-compression-sementique.md
  source: local
status: done
date: 2026-09-14
updated_at: 2026-09-14
description: >
  Compression sémantique (Levier L3) du noyau SKILL.md post-scission P1 (plan #16).
  Densification des formulations discursives en syntaxe impérative concise sans
  altérer aucune règle logique, invariant de sécurité ou balise opérationnelle.
priority: medium
complexity: S
scope:
  modules:
    - SKILL.md
issue:
  id: null
  url: null
---

# [⚡] Plan #17 - Compression sémantique du noyau SKILL.md (L3)

## Objectif

Appliquer la **densification sémantique** (Levier L3 de l'audit
`doc/audits/2-roadmap-tracking-optimisation-tokens-architecture.md`) sur le
noyau `SKILL.md` résiduel après la scission modulaire P1 (plan #16), en
éliminant le remplissage narratif et les formulations passives sans supprimer
aucune règle logique ni garde-fou comportemental.

Cible : réduire de ≥ 15 % les tokens du noyau pour économiser ~12 000 tokens
sur une session de 18 tours (objectif audit L3 : ~11 240 tokens).

## Contexte

- **Plan #16** (scission modulaire L1) : SKILL.md monolithique → noyau + 4
  modules. Noyau résiduel : 274 lignes, ~3 500 tokens.
- **Audit §4 Levier 3** : compression ciblée sur les sections permanentes du
  noyau — aucune règle supprimée, uniquement reformulation concise.
- **Post-mortem P1 (plan #12)** : leçon clé — ne jamais supprimer de
  contraintes négatives positionnelles (blocs `❌`). L3 ne touche que la forme,
  jamais le fond.

## Périmètre

### Inclus

- `SKILL.md` — densification sémantique de toutes les sections narratives
- Version bump `3.0.0` → `3.1.0`

### Hors scope

- `modules/*.md` — non touchés
- `references/*.md` — non touchés
- Levier L2 (élimination des tours inutiles) — livré dans le **plan #18**
- Toute suppression de règle logique, condition, balise ou contrainte

## Étapes

- [x] Étape 1 — Analyser le contenu de `SKILL.md` section par section et identifier les suppressions à tolérance zéro (blocs `⛔`, exemples `❌`/`✅`, tables de routage) `(S · standard → Sonnet)`
- [x] Étape 2 — Appliquer la densification sémantique : supprimer le remplissage narratif, condenser les règles en syntaxe impérative, compacter les introductions de section `(S · standard → Sonnet)`
- [x] 🧪 Tests — Vérifier l'intégrité : comptage lignes, présence des invariants critiques, absence de fuite de contenu modulaire
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|---|---|---|
| Exemples `❌` format des rapports | Conservés intégralement | Contraintes négatives positionnelles (leçon P1) — efficacité liée à la proximité avec l'instruction protégée |
| Blocs `⛔` (5 règles absolues) | Conservés intégralement | Garde-fous permanents — présence à chaque tour obligatoire |
| Paragraphe "Cadre, suit et trace..." | Supprimé | Redondant avec la description du frontmatter |
| Intro "Ce workflow s'applique au travail..." | Supprimé | Redondant avec le heading de section |
| Intro 2 lignes "La création d'un plan..." (⛔ séparation) | Supprimé | Redondant avec le heading et la liste "Ne JAMAIS" |
| Phrase "GABARITS CONTRAIGNANTS, pas des suggestions" | Supprimée | Redondante avec le `⛔ Interdit` qui précède |
| Correction proactive — intro 5 lignes → 1 | Condensé | Toutes les conditions (démarrage, reprise, fin d'étape, MAJ statut) couvertes par "À chaque interaction" |
| Urgences — blockquote séparé → inline dans la puce | Fusionné | Contenu identique, un seul point d'entrée |

## Tests

### Procédure de test

```bash
echo "=== Count Lines ==="
wc -l SKILL.md

echo "=== Five Absolute Rules Present ==="
grep -c "^## ⛔ Règle absolue" SKILL.md

echo "=== Bootstrap Block Present ==="
grep -c "⛔ Bootstrap" SKILL.md

echo "=== Version Bumped to 3.1.0 ==="
grep "version:" SKILL.md

echo "=== Correction Proactive Present ==="
grep -c "Correction proactive" SKILL.md

echo "=== Module Routing Table Intact ==="
grep -c "init-scan.md\|plan.md\|execute.md\|wrapup.md" SKILL.md

echo "=== No Phase Content Leaked into Core ==="
grep -c "^## Phase 1" SKILL.md && echo "FAIL" || echo "OK"
```

**Résultats attendus :** ≤ 235 lignes, 5 blocs `⛔ Règle absolue`, 1 bootstrap,
version `3.1.0`, 1 occurrence "Correction proactive", ≥ 4 références modules, 0
heading `## Phase 1` dans le noyau.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|---|---|---|---|---|
| 2026-09-14 | Comptage lignes | ≤ 235 | **209** (−65 lignes, −23,7 %) | ✅ PASS |
| 2026-09-14 | Blocs `⛔ Règle absolue` | 5 | **5** | ✅ PASS |
| 2026-09-14 | Bootstrap ⛔ présent | 1 | **1** | ✅ PASS |
| 2026-09-14 | Version `3.1.0` | `3.1.0` | **`3.1.0`** | ✅ PASS |
| 2026-09-14 | Correction proactive présente | 1 | **1** | ✅ PASS |
| 2026-09-14 | Table de routage modules intacte | ≥ 4 refs | **16 refs** | ✅ PASS |
| 2026-09-14 | Aucune fuite de contenu modulaire | 0 | **0** | ✅ PASS |

## Impact mesuré

| Métrique | Avant (v3.0.0) | Après (v3.1.0) | Réduction |
|---|---|---|---|
| Lignes | 274 | **209** | **−65 (−23,7 %)** |
| Tokens estimés | ~3 500 | ~2 680 | **~−820 tokens/tour** |
| Économie 18 tours | — | ~14 760 tokens | **−5,3 % total session** |

## Sections condensées

| Section | Transformation | Tokens économisés |
|---|---|---|
| Frontmatter `description` | 10 lignes → 4 (narratif → résumé direct) | ~80 |
| Intro `# Roadmap Tracking` | 8 lignes → 1 (paragraphe redondant supprimé) | ~90 |
| `Prerequisites` | 7 lignes → 2 (reformulation impérative) | ~60 |
| `Applicabilité` | 27 lignes → 13 (listes denses, blockquotes fusionnés) | ~180 |
| Modules workflow intro | 3 lignes → 1 | ~25 |
| `⛔ format des rapports` | Suppression phrase "GABARITS CONTRAIGNANTS" | ~20 |
| `⛔ séparation` | Suppression intro 2 lignes redondante | ~30 |
| `⛔ traçabilité tests` | Retrait clause parenthétique superflue | ~15 |
| `⛔ pas de ⏸️ sans 📦` | Reformulation compacte −2 lignes | ~30 |
| `Correction proactive` | Intro 5→1 ligne, bullets dé-wrappés, exécution condensée | ~290 |

## Journal de session

### Session 2026-09-14

- ✅ Analysé : audit L3 + post-mortem plan #12 pour identifier les invariants intouchables
- ✅ Fait : densification sémantique de `SKILL.md` v3.0.0 → v3.1.0
- ✅ Fait : 274 → 209 lignes (−65 lignes, −23,7 %) ; ~820 tokens/tour économisés
- ✅ Vérifié : 7/7 tests PASS — tous les invariants critiques présents et intacts
- 📊 Résultat : objectif L3 (~11 240 tokens sur 18 tours) dépassé (~14 760 tokens)
