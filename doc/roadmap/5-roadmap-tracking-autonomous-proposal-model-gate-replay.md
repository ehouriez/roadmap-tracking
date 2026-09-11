---
plan:
  id: '5'
  name: 5-roadmap-tracking-autonomous-proposal-model-gate-replay.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/5-roadmap-tracking-autonomous-proposal-model-gate-replay.md
status: done
date: 2026-09-11
description: >
  Corriger deux déclenchements manquants du workflow : (a) proposer le mode
  autonomous à l'entrée Phase 7 quand tests.mode n'est pas fixé, et persister le
  choix dans .skill-config.yml ; (b) rejouer la gate de recommandation de modèle
  quand le modèle actif change en cours de session.
priority: medium
complexity: M
scope:
  modules:
    - SKILL.md
    - references/environment.md
    - references/autonomous-tests.md
issue:
  id: 5
  url: https://github.com/ehouriez/roadmap-tracking/issues/5
---

# [🔀] Plan #5 - roadmap-tracking : proposition autonomous + re-jeu gate modèle

## Objectif

Corriger deux déclenchements manquants du workflow, repérés en session :

- **(a)** Le mode `manual` est imposé par défaut même quand l'agent tourne dans
  l'environnement d'exécution et peut lancer les tests lui-même. Le mode
  `autonomous` existe mais n'est jamais proposé — `autonomous-tests.md:6` promet
  une « détection qui propose » qui n'est implémentée nulle part.
- **(b)** La gate de recommandation de modèle n'est pas rejouée quand le modèle
  actif change en cours de session (ex. `/model opus`), laissant passer un
  mismatch (sur/sous-dimensionnement) sans le signaler.

## Périmètre

### Inclus
- `SKILL.md` : proposition autonomous (Phase 7), règle de re-jeu de gate
- `references/environment.md` : schéma `.skill-config.yml`, procédure de détection
- `references/autonomous-tests.md` : réconcilier la note « detection proposes »
  (ligne 6) désormais implémentée

### Hors scope
- Format des rapports (plan #4)
- Autres modes de tests, mécanique interne de la boucle Exécuteur/Vérificateur

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| (a) Signal de proposition | Proposer si `tests.mode` non fixé dans `.skill-config.yml` | L'accès Bash étant quasi toujours présent en Claude Code, « accès shell détecté » proposerait à chaque session ; le signal « config non fixée » est stable et non redondant |
| (a) Placement de la proposition | À l'entrée Phase 7, avant l'étape 0 | Proposer quand on sait que des tests vont tourner, pas au démarrage d'une simple consultation |
| (a) Mémorisation du choix | Écrire `tests.mode` dans `.skill-config.yml` (créé si absent) | Persistant entre sessions, l'opérateur n'est plus resollicité |
| (b) Détection du changement de modèle | Comparer, à chaque entrée de gate, le modèle actif au dernier modèle évalué | Règle simple, sans état externe ; couvre Phase 1.5, entrée Phase 7 et reprise |

## Étapes

- [x] Étape 1 — (b) Règle « changement de modèle = re-jeu de la gate » : mémoriser le dernier modèle évalué, comparer à chaque entrée de gate (Phase 1.5, entrée Phase 7, reprise), rejouer si différent — dans `SKILL.md` (S · standard → Sonnet)
- [x] Étape 2 — (a) Proposition autonomous à l'entrée Phase 7 : si `tests.mode` non fixé → `AskUserQuestion` manual/autonomous → écrire le choix dans `.skill-config.yml` ; réconcilier `autonomous-tests.md:6` et le schéma de `environment.md` (M · standard → Sonnet)
- [x] 🧪 Tests — Rédiger et exécuter la procédure de test
- [x] ✅ Validation — Vérifier les résultats et clôturer

## Procédure de tests finaux

```bash
echo "=== Go To Project Root ==="
cd /mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking

echo "=== Verify Step 1 - Model-Change Replay Section Exists ==="
grep -n "Re-jeu de la gate sur changement de modèle" SKILL.md

echo "=== Verify Step 1 - Referenced At Phase 1.5 ==="
grep -n "Mémoriser le modèle évalué" SKILL.md

echo "=== Verify Step 1 - Referenced At Phase 7 Entry Gate ==="
grep -n "Exception — changement de modèle" SKILL.md

echo "=== Verify Step 1 - Referenced At Resume Gate ==="
grep -n "Rejouer aussi la gate" SKILL.md

echo "=== Verify Step 2 - Test-Mode Proposal Section Exists ==="
grep -n "Proposition du mode de tests" SKILL.md

echo "=== Verify Step 2 - Proposal Persists To Config ==="
grep -n "Persister le choix" SKILL.md

echo "=== Verify Step 2 - autonomous-tests.md Reconciled ==="
grep -n "Where the proposal happens" references/autonomous-tests.md

echo "=== Verify Step 2 - environment.md Schema Reconciled ==="
grep -n "unset → proposed at Phase 7" references/environment.md

echo "=== Verify Step 2 - environment.md Detection Procedure Reconciled ==="
grep -n "SKILL.md.*Phase 7 proposes" references/environment.md
```

**Résultats attendus :** chaque `grep` renvoie **au moins une ligne** (numéro + texte). Aucun `grep` ne doit sortir vide (code retour 1). Les 10 vérifications confirment que les deux règles sont bien câblées à leurs points d'ancrage et que les deux fichiers de référence sont réconciliés.

## Journal de session

### Session 2026-09-11
- ✅ Étape 1 — règle de re-jeu de gate sur changement de modèle ajoutée dans `SKILL.md` (section canonique + 3 points d'ancrage).
- ✅ Étape 2 — proposition `manual`/`autonomous` à l'entrée Phase 7 + persistance `.skill-config.yml` ; `autonomous-tests.md` et `environment.md` réconciliés.
- 📋 Prochain : exécution de la procédure de tests finaux, puis validation/clôture.
