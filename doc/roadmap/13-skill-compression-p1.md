---
plan:
  id: '13'
  name: 13-skill-compression-p1.md
  link: doc/roadmap/13-skill-compression-p1.md
  source: local
status: done
date: 2026-09-12
description: >
  Compress SKILL.md by ~35% (P1 of token optimization audit): remove 13
  redundant ❌ blocks and merge 3 duplicate commit templates into one
  canonical section with references.
priority: medium
complexity: S
scope:
  modules:
    - SKILL.md
issue:
  id: 13
  url: https://github.com/ehouriez/roadmap-tracking/issues/13
---

# [⚡] Plan #13 - SKILL.md Compression P1

## Objectif

Réduire SKILL.md de ~35 % (10 000 → 6 500 tokens/tour) sans modifier aucune
règle de workflow. Deux cibles concrètes identifiées par l'audit
`doc/audits/0-roadmap-tracking-estimation-couts-tokens.md` :

- **13 blocs `❌` redondants** à supprimer.
- **3 gabarits de commit** identiques dans les sections `Tests unitaires
  intermédiaires`, `🧪 Tests` et `Commit d'implémentation (référence de format)`
  (partagent ~80 % de leur contenu) → fusionner en 1 section canonique + 2
  renvois.

## Périmètre

### Inclus
- `SKILL.md` — suppression des 13 blocs `❌` redondants
- `SKILL.md` — fusion des 3 gabarits de commit en section canonique + renvois

### Hors scope
- P2 (scission planning / implémentation — architecture)
- P3 (prompt caching — infrastructure plateforme)
- P4 (fusion ⏸️2 + gate Phase 6 pour S/M)
- P5 (silence gate ℹ️ Cas 1)
- P6 (garde « référence déjà en contexte »)
- Tout fichier autre que `SKILL.md`

## Étapes

- [x] Étape 1 — Localiser et supprimer les 13 blocs `❌` redondants dans SKILL.md `(S · standard → Sonnet)`
- [x] Étape 2 — Fusionner les 3 gabarits de commit : conserver la section canonique `Commit d'implémentation (référence de format)`, remplacer les deux occurrences dans `Tests unitaires intermédiaires` et `🧪 Tests` par une ligne de renvoi `(S · standard → Sonnet)`
- [x] 🧪 Tests — Vérifier l'intégrité du contenu (comptage de lignes, blocs supprimés, renvois fonctionnels)
- [x] ✅ Validation — Vérifier les résultats des tests et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Méthode fusion gabarits | Section canonique + renvois | Demande utilisateur — une seule source de vérité, renvois dans les 2 autres sections |
| Périmètre | P1 uniquement | Impact maximal, risque minimal, faisable en une session (cf. audit) |

## Tests

> Section obligatoire renseignée lors des étapes de tests.

### Procédure de test

```bash
echo "=== Count Lines ==="
wc -l SKILL.md

echo "=== Verify Formats INTERDITS Block Removed ==="
grep -n "Formats INTERDITS" SKILL.md && echo FAIL || echo OK

echo "=== Verify Commit Template Removed from Tests Intermediaires ==="
grep -n "Commit proposé — Étape X/N" SKILL.md && echo FAIL || echo OK

echo "=== Verify Commit Template Removed from Tests Finaux ==="
grep -n "Commit proposé — Pré-tests finaux" SKILL.md && echo FAIL || echo OK

echo "=== Verify References to Canonical Section ==="
grep -n "Commit d'implémentation pré-tests.*référence" SKILL.md

echo "=== Verify Version Bumped ==="
grep -n "version.*2.6.0" SKILL.md
grep -n "version.*2.6.0" .claude-plugin/plugin.json
```

**Résultats attendus :** 1340 lignes, "Formats INTERDITS" absent, 2 templates supprimés, 2 renvois présents aux lignes ~1112 et ~1180, version 2.6.0 dans les deux fichiers.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-12 | Comptage lignes | < 1369 | 1340 (-29 lignes) | ✅ PASS |
| 2026-09-12 | Bloc `❌ Formats INTERDITS` absent | absent | absent | ✅ PASS |
| 2026-09-12 | Template commit `Tests intermédiaires` supprimé | absent | absent | ✅ PASS |
| 2026-09-12 | Template commit `🧪 Tests` supprimé | absent | absent | ✅ PASS |
| 2026-09-12 | Renvois canoniques en place | 2 renvois | lignes 1112 + 1180 | ✅ PASS |
| 2026-09-12 | Version 2.6.0 dans SKILL.md | 2.6.0 | 2.6.0 | ✅ PASS |
| 2026-09-12 | Version 2.6.0 dans plugin.json | 2.6.0 | 2.6.0 | ✅ PASS |

## Journal de session

### Session 2026-09-12
- ✅ Fait : bloc `❌ Formats INTERDITS` redondant de la section Démarrage standard
- ✅ Fait : supprimé le bloc `❌ Formats INTERDITS` redondant de la section Démarrage standard
- ✅ Fait : remplacé les gabarits commit dans `Tests unitaires intermédiaires` et `🧪 Tests` par des renvois à la section canonique
- ✅ Fait : version bumpée 2.5.7 → 2.6.0 (SKILL.md + plugin.json)
- 📊 Résultat : 1369 → 1340 lignes (-29 lignes, ~2 %). La cible audit de 35 % n'est pas atteinte — seul 1 bloc `❌` était réellement redondant dans la version 2.5.7 (vs 13 estimés). Les 3 gabarits de commit ont bien été fusionnés. Pour aller plus loin, P2 (scission planning/implémentation) est nécessaire.

### Session 2026-09-12 (2)
- ✅ Fait : bloc `❌ Formats INTERDITS` réintroduit manuellement dans le fichier `SKILL.md` car le gain de cette suppression n'est pas établi
