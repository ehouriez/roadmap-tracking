---
plan:
  id: '19'
  name: 19-lock-model-gate-template.md
  link: doc/roadmap/19-lock-model-gate-template.md
  source: local
status: done
date: 2026-09-14
description: >
  Verrouiller le format des messages de gate modèle (upgrade/downgrade) de manière
  déterministe — templates verbatim, alias génériques uniquement (jamais les versions
  runtime), support multi-fournisseur Anthropic + OpenAI/Codex.
priority: high
complexity: M
intent: production
issue:
  id: null
  url: null
---

# [🔒] Plan #19 - Lock Model Gate Template

## Objectif

Le skill a produit un message de gate modèle erroné (`⏸️ Continue sur Sonnet 4.6 ou switch de modèle ?` avec `/model claude-opus-5`) par absence de template verbatim et de règle interdisant les versions runtime. Ce plan verrouille les templates upgrade/downgrade de la gate modèle, généralise vers les alias génériques, et ajoute le support OpenAI/Codex (`sol`/`luna`/`terra`).

## Périmètre

### Inclus

- `references/environment.md` — renommage section, ajout colonne OpenAI (`sol`/`luna`/`terra`), exemple config Codex, règle `/model alias uniquement`
- `modules/plan.md` — anchor MAJ, règle verbatim, règle token = alias (pas version runtime), templates upgrade/downgrade distincts
- `README.md` — exemple config : `gpt-5`/`gpt-5-mini` → `sol`/`luna`

### Hors scope

- `modules/execute.md` (aucune référence à des noms de modèles versionnés)
- `references/templates.md` (tags `→ Sonnet`/`→ Opus` déjà génériques)
- `modules/init-scan.md` (aucun template de gate)

## Étapes

- [x] Étape 1 — `environment.md` : renommer section + ajouter colonne OpenAI + exemple config Codex `(XS · standard → sonnet)`
- [x] Étape 2 — `environment.md` : règle alias `/model` dans Generic Action Mapping `(XS · standard → sonnet)`
- [x] Étape 3 — `plan.md` : anchor MAJ + règle verbatim + règle token = alias + templates upgrade/downgrade `(S · standard → sonnet)`
- [x] Étape 4 — `README.md` : MAJ exemple config `gpt-5`/`gpt-5-mini` → `sol`/`luna` `(XS · standard → sonnet)`
- [x] 🧪 Tests — Vérifier grep résidus versionnés + relire templates gate rendus
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|---|---|---|
| Alias OpenAI | `sol`/`luna`/`terra` | Modèles Codex réels (oct. 2026), confirmés par l'utilisateur |
| Tier `light` OpenAI | `terra` | Mapping `low` → `light` tier ; cohérent avec la convention |
| Templates gate | Deux blocs distincts upgrade/downgrade | Clarté du message utilisateur ; fusionne `⚠️` + `⏸️` en un seul template verbatim |
| Règle verbatim | Mention explicite `⛔ VERBATIM` dans plan.md | Seul guard déterministe contre la paraphrase LLM |
| Token modèle affiché | Alias tier uniquement (`sonnet`/`opus`/…), jamais la version runtime | Évite l'hallucination de versions comme `Sonnet 4.6`, `claude-opus-5` |

## Tests

### Procédure de test

```bash
echo "=== Check No Versioned Model Strings In Skill Files ==="
grep -rnE "Sonnet [0-9]|Opus [0-9]|Haiku [0-9]|claude-opus-[0-9]|claude-sonnet-[0-9]|sol [0-9]|luna [0-9]" --include="*.md" . | grep -vE "^\./doc/"

echo "=== Check Section Rename In environment.md ==="
grep -n "Model Tier & Environment Mapping" references/environment.md

echo "=== Check OpenAI Column In environment.md ==="
grep -n "sol\|luna\|terra" references/environment.md

echo "=== Check Verbatim Rule In plan.md ==="
grep -n "VERBATIM\|verbatim" modules/plan.md

echo "=== Check Upgrade Template In plan.md ==="
grep -n "Transition recommandée\|Retour recommandé" modules/plan.md

echo "=== Check README Config Example ==="
grep -n "sol\|luna" README.md
```

**Résultats attendus :**
- Grep versioned strings → aucune sortie (zéro résidu hors `doc/`)
- Section rename → `## Model Tier & Environment Mapping` trouvée dans `environment.md`
- OpenAI column → `sol`, `luna`, `terra` présents dans `environment.md`
- Verbatim rule → mention `VERBATIM` présente dans `plan.md`
- Upgrade template → `Transition recommandée` et `Retour recommandé` présents dans `plan.md`
- README → `sol` et `luna` présents

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|---|---|---|---|---|
| 2026-09-14 | Versioned strings hors `doc/` | Aucun résidu | `modules/plan.md:155` — exemple négatif intentionnel dans `⛔ TOKEN = ALIAS` | ✅ PASS |
| 2026-09-14 | Section rename `environment.md` | `## Model Tier & Environment Mapping` | Trouvé à L22 | ✅ PASS |
| 2026-09-14 | Colonne OpenAI `environment.md` | `sol`/`luna`/`terra` présents | 7 occurrences dont table + exemples config | ✅ PASS |
| 2026-09-14 | Règle verbatim `plan.md` | `⛔ **VERBATIM**` | Trouvé à L148 | ✅ PASS |
| 2026-09-14 | Templates upgrade/downgrade | `Transition recommandée` + `Retour recommandé` | Trouvés à L162 et L175 | ✅ PASS |
| 2026-09-14 | README config example | `sol`/`luna` | Trouvés à L116-117 | ✅ PASS |

## Journal de session

### Session 2026-09-14

- ✅ Fait : Étapes 1-4 implémentées, 6/6 tests PASS
- 📋 Prochain : ✅ Validation et clôture
