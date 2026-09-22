---
plan:
  id: '11'
  name: 11-applicabilite-regle-demarrage-hardening.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/11-applicabilite-regle-demarrage-hardening.md
status: done
date: 2026-09-12
description: >
  Harden the Applicabilité and Règle de démarrage sections of SKILL.md to
  eliminate subjective bypass vectors with objective file-touch criterion,
  mandatory post-fix traceability for emergencies, and adaptive re-proposal
  on doc/roadmap/ refusal.
priority: high
complexity: S
scope:
  modules:
    - SKILL.md
issue:
  id: 11
  url: https://github.com/ehouriez/roadmap-tracking/issues/11
---

# [🛡️] Plan #11 - Harden Applicability Rules and Startup Rule

## Objectif

Éliminer les vecteurs de bypass subjectifs dans les sections `Applicabilité`
et `Règle de démarrage` du SKILL.md en remplaçant les critères d'exclusion
flous par des règles objectives, en imposant une traçabilité post-fix pour les
urgences, et en rendant le refus de `doc/roadmap/` adaptatif plutôt que définitif.

## Périmètre

### Inclus
- Section `## Applicabilité` du `SKILL.md`
- Section `## Règle de démarrage` du `SKILL.md`

### Hors scope
- Toutes les autres sections du `SKILL.md`
- `references/`, `scripts/`
- Logique d'implémentation du skill

## Étapes

- [x] Étape 1 — Lire les sections cibles et préparer les patches (XS · standard → Sonnet)
- [x] Étape 2 — Appliquer les modifications 1, 2, 3, 4 dans `Applicabilité` (XS · standard → Sonnet)
- [x] Étape 3 — Appliquer la modification 5 dans `Règle de démarrage` (XS · standard → Sonnet)
- [x] 🧪 Tests — Vérifier la cohérence interne et l'absence de régression
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Modifications détaillées

| # | Section | Action |
|---|---------|--------|
| 1 | Applicabilité | Remplacer les 2 bullets subjectifs par critère objectif : « aucun fichier du projet touché » |
| 2 | Applicabilité | Reformuler bullet urgences + ajouter bloc dédié imposant post-fix traceability |
| 3 | Applicabilité | Supprimer bullet `one-shot` |
| 4 | Applicabilité | Ajouter blockquote gras avant `Il ne s'applique PAS`, supprimer ligne de fin |
| 5 | Règle de démarrage | Branche `Non` : re-proposition unique si fichier projet impliqué ; avertissement + continuation au 2e refus |

## Tests

### Procédure de test

```bash
echo "=== Check 1: 'sans impact projet' removed ==="
grep -n "sans impact projet" SKILL.md && echo "FAIL" || echo "PASS"

echo "=== Check 2: 'sans impact codebase' removed ==="
grep -n "sans impact codebase" SKILL.md && echo "FAIL" || echo "PASS"

echo "=== Check 3: 'one-shot' exclusion bullet removed ==="
grep -n "demandes one-shot" SKILL.md && echo "FAIL" || echo "PASS"

echo "=== Check 4: 'En cas de doute' blockquote BEFORE exclusion list ==="
line_doute=$(grep -n "En cas de doute" SKILL.md | head -1 | cut -d: -f1)
line_list=$(grep -n "ne s'applique PAS" SKILL.md | head -1 | cut -d: -f1)
[ "$line_doute" -lt "$line_list" ] && echo "PASS" || echo "FAIL"

echo "=== Check 5: Urgences post-fix block present ==="
grep -n "traçabilité post-fix obligatoire" SKILL.md && echo "PASS" || echo "FAIL"

echo "=== Check 6: Re-proposal logic in 'Non' branch ==="
grep -n "re-propose" SKILL.md | head -3

echo "=== Check 7: 'aucun fichier du projet' objective criterion ==="
grep -n "aucun fichier du projet" SKILL.md | head -3

echo "=== Check 8: Warning message in 'Non' branch ==="
grep -n "suivi par roadmap-tracking" SKILL.md
```

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-12 | Check 1 : `sans impact projet` absent | Absent | Absent | ✅ PASS |
| 2026-09-12 | Check 2 : `sans impact codebase` absent | Absent | Absent | ✅ PASS |
| 2026-09-12 | Check 3 : bullet `one-shot` absent | Absent | Absent | ✅ PASS |
| 2026-09-12 | Check 4 : `En cas de doute` avant la liste | Ligne doute < ligne liste | L.67 < L.69 | ✅ PASS |
| 2026-09-12 | Check 5 : bloc urgences post-fix présent | Présent | L.73 | ✅ PASS |
| 2026-09-12 | Check 6 : logique re-proposition dans branche `Non` | Présent | L.82 + L.98 | ✅ PASS |
| 2026-09-12 | Check 7 : critère objectif `aucun fichier du projet` | Présent | L.70 | ✅ PASS |
| 2026-09-12 | Check 8 : message d'avertissement 2e refus | Présent | L.101-102 | ✅ PASS |

## Journal de session

| Date | Action |
|------|--------|
| 2026-09-12 | Plan créé — issue #11 ouverte |
| 2026-09-12 | Implémentation one-shot — 5 modifications appliquées, 8/8 tests PASS, plan clôturé |
