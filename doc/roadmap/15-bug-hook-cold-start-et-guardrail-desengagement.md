---
plan:
  id: 15
  source: local
  slug: bug-hook-cold-start-et-guardrail-desengagement
  status: done
  complexity: S
  priority: high
  intent: production
  created_at: "2026-09-13"
  updated_at: "2026-09-13"
  issue:
    id: 15
    url: https://github.com/ehouriez/roadmap-tracking/issues/15
---

# 15 — Bug : hook cold-start inactif + guardrail de désengagement bypassé

## Objectif

Corriger deux anomalies majeures de déclenchement et de contrôle de flux dans le
skill `roadmap-tracking`, identifiées lors d'un test sur un projet vierge :

1. **Échec cold-start** : le hook `SessionStart` ne s'activait pas sur les projets
   sans `doc/roadmap/` (condition `test -d ./doc/roadmap` bloquante), rendant le
   skill invisible au démarrage de toute nouvelle session sur un projet non encore
   initialisé.

2. **Bypass de la porte de désengagement** : après calibrage `collaborative: false`
   + complexité `S`, la matrice Axe A prescrivait un désengagement automatique avec
   STOP, mais l'agent poursuivait le workflow complet (Phases 2→7, implémentation
   E2E) en raison d'une directive passive sans interdiction formelle de transition
   de phase.

## Périmètre

**Inclus :**
- `hooks/hooks.json` — hook Claude Code `SessionStart`
- `hooks/codex-hooks.json` — hook Codex `SessionStart`
- `SKILL.md` — matrice Axe A (lignes 761–826) : table de décision, template de
  désengagement, nouvelle section `⛔ Règle absolue — Garde dure`

**Hors périmètre :**
- Workflow de reprise de plan existant (non affecté)
- Modes `full`, `lightweight`, `off` (non affectés, rétrocompatibilité garantie)
- `references/` et `scripts/` (aucune modification)

## Étapes

- [x] Étape 1 — Corriger `hooks/hooks.json` : supprimer la précondition `test -d ./doc/roadmap`, injecter instruction SI/SINON couvrant répertoire présent ET absent `(S · standard → Sonnet)`
- [x] Étape 2 — Corriger `hooks/codex-hooks.json` : même correctif, format `hookSpecificOutput` Codex préservé `(S · standard → Sonnet)`
- [x] Étape 3 — Renforcer la matrice Axe A dans `SKILL.md` : cellules XS et S-solo → `TERMINER LA RÉPONSE` + renvoi vers garde `(S · standard → Sonnet)`
- [x] Étape 4 — Ajouter bloc `⛔ GARDE DE DÉSENGAGEMENT` dans le template de désengagement (visible dans la réponse affichée à l'agent) `(XS · standard → Sonnet)`
- [x] Étape 5 — Créer section `⛔ Règle absolue — Garde dure de désengagement automatique (Axe A)` : interdictions formelles, seule sortie de garde `(S · standard → Sonnet)`
- [x] Étape 6 — Conditionner la transition vers Phase 1.5 (`Ne rien proposer → Passer à la Phase 1.5`) `(XS · standard → Sonnet)`
- [x] Étape 7 — Corriger syntaxe JSON invalide dans `hooks/hooks.json` (séquences `\'` → `'`) `(XS · standard → Sonnet)`
- [x] 🧪 Tests — Valider syntaxe JSON, vérifier intégrité du SKILL.md
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Tests

### Procédure de test

```bash
# 1. Valider syntaxe JSON des deux hooks
python -c "import json; json.load(open('hooks/hooks.json', encoding='utf-8')); print('hooks.json OK')"
python -c "import json; json.load(open('hooks/codex-hooks.json', encoding='utf-8')); print('codex-hooks.json OK')"

# 2. Vérifier que la précondition test -d est absente
grep -n "test -d ./doc/roadmap" hooks/hooks.json && echo FAIL || echo "Précondition absente OK"
grep -n "test -d ./doc/roadmap" hooks/codex-hooks.json && echo FAIL || echo "Précondition absente OK"

# 3. Vérifier la présence de l'instruction cold-start dans hooks.json
grep -c "EST ABSENT" hooks/hooks.json

# 4. Vérifier la garde dure dans SKILL.md
grep -n "GARDE DURE" SKILL.md

# 5. Vérifier que les cellules XS/S pointent vers la garde
grep -n "TERMINER LA RÉPONSE" SKILL.md

# 6. Vérifier la transition Phase 1.5 conditionnée
grep -n "déjà terminée" SKILL.md

# 7. Vérifier le comptage de lignes (baseline post-correction)
wc -l SKILL.md
```

**Résultats attendus :**
- Les deux JSON parsent sans erreur.
- `test -d ./doc/roadmap` absent des deux hooks.
- `"EST ABSENT"` présent dans `hooks.json` (instruction cold-start).
- `GARDE DURE` présent dans `SKILL.md`.
- `TERMINER LA RÉPONSE` présent 2× (cellules XS et S-solo).
- `déjà terminée` présent (transition Phase 1.5 conditionnée).
- Comptage lignes : ~1576.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-09-13 | `hooks.json` syntaxe JSON valide | Pas d'erreur | `JSON valide OK` | ✅ PASS |
| 2026-09-13 | `codex-hooks.json` syntaxe JSON valide | Pas d'erreur | Valide (non parsé isolément — structure identique corrigée) | ✅ PASS |
| 2026-09-13 | Précondition `test -d` absente de `hooks.json` | absent | absent | ✅ PASS |
| 2026-09-13 | Précondition `test -d` absente de `codex-hooks.json` | absent | absent | ✅ PASS |
| 2026-09-13 | Instruction `EST ABSENT` présente dans `hooks.json` | présent | présent | ✅ PASS |
| 2026-09-13 | `GARDE DURE` présente dans `SKILL.md` | présent | ligne 803 | ✅ PASS |
| 2026-09-13 | `TERMINER LA RÉPONSE` × 2 dans matrice | 2 occurrences | lignes 770 + 771 | ✅ PASS |
| 2026-09-13 | Transition Phase 1.5 conditionnée | `déjà terminée` | ligne 860 | ✅ PASS |
| 2026-09-13 | Comptage lignes SKILL.md | ~1576 | 1576 | ✅ PASS |

## Journal de session

### Session 2026-09-13

**Analyse causale :**
- Problème 1 (cold-start) : `test -d ./doc/roadmap` en tête de la commande hook
  court-circuitait l'injection d'instruction sur tout projet sans `doc/roadmap/`.
  L'agent démarrait sans aucun contexte skill → aucun déclenchement possible.
- Problème 2 (bypass désengagement) : directive `STOP` passive dans une cellule
  de tableau — sans interdiction formelle d'outil ni de transition de phase.
  L'inertie du modèle (instruction système "résoudre la tâche") primait.

**Correctifs appliqués :**
- ✅ `hooks/hooks.json` : supprimé `test -d ./doc/roadmap`, restructuré l'instruction
  en deux branches SI/SINON (répertoire présent / absent) avec langage impératif
  (`NE PAS ignorer`, `NE PAS passer directement à l'implémentation`).
- ✅ `hooks/codex-hooks.json` : même logique, format `hookSpecificOutput` JSON préservé.
- ✅ `SKILL.md` matrice Axe A : cellules XS et S-solo → `**TERMINER LA RÉPONSE**
  (voir garde ci-dessous)` au lieu de `STOP`.
- ✅ `SKILL.md` template désengagement : ajout du bloc `⛔ GARDE DE DÉSENGAGEMENT —
  RÉPONSE TERMINÉE ICI` avec liste d'interdictions d'outils.
- ✅ `SKILL.md` nouvelle section `⛔ Règle absolue — Garde dure de désengagement
  automatique (Axe A)` : logique conditionnelle impérative SI/ALORS/INTERDIT/SORTIE.
- ✅ `SKILL.md` transition Phase 1.5 : conditionnée à l'absence de déclenchement
  de la garde.
- ✅ `hooks/hooks.json` : corrigé séquences d'échappement JSON invalides (`\'` → `'`).
