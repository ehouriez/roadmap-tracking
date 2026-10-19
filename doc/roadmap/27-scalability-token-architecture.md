---
plan:
  id: '27'
  name: 27-scalability-token-architecture.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/27-scalability-token-architecture.md
status: active
date: 2026-10-19
description: >
  Rendre roadmap-tracking scalable à 350/500/1000+ plans en supprimant le coût
  fixe d'hydratation de session : roadmap.md et index générés depuis le front
  matter, listing paresseux, validation d'intégrité, CONTEXT.md segmenté et
  borné, capitalisation auto encadrée. Issue des recommandations du rapport
  doc/rapports/rapport-ameliorations-2026-10-17.md.
priority: high
complexity: XL
intent: null
scope:
  modules:
    - modules/init-scan.md
    - references/roadmap-file.md
    - references/templates.md
    - references/environment.md
    - scripts/
    - SKILL.md
    - README.md
  patterns:
    - "modules/**/*.md"
    - "references/**/*.md"
    - "scripts/**/*.py"
issue:
  id: 27
  url: https://github.com/ehouriez/roadmap-tracking/issues/27
---

# [🏗️] Plan #27 - Scalability & Token Architecture

> **Origine** : rapport d'audit `doc/rapports/rapport-ameliorations-2026-10-17.md`
> (projet de référence Auxitum, 287 plans). Décisions utilisateur actées :
> statuts hors-enum **mappés** (pas officialisés) ; `/impeccable` **non utilisé**.
>
> **Mode `github`** : issue [#27](https://github.com/ehouriez/roadmap-tracking/issues/27) créée le 2026-10-19.

## Objectif

Supprimer le coût fixe d'amorçage de session (~70 K tokens mesurés sur Auxitum :
`roadmap.md` ~49,6 K + `CONTEXT.md` ~20,8 K), proportionnel au volume et
intenable à 500/1000 plans. Principe directeur : **le skill lit un index compact
(~3-5 Ko), jamais le narratif complet** ; `roadmap.md` devient un artefact
**généré** depuis le front matter (source de vérité unique → zéro dérive).

## Périmètre

### Inclus
- Borne de lecture de `roadmap.md` (quick win immédiat).
- Mapping du vocabulaire de statut (`in-progress`→`active`, `cancelled`→`archived`).
- Génération `roadmap.md` + index machine-lisible + `done/INDEX.md` depuis le front matter.
- Listing paresseux / pagination / filtres.
- Validation d'intégrité (`doctor`) + observabilité portfolio (`stats`).
- Segmentation + budget dur de `CONTEXT.md` ; capitalisation auto encadrée.
- Scripts de migration idempotents + onboarding (README, `aide migration`).

### Hors scope
- Officialisation de nouveaux statuts (décision : mapping, pas extension).
- Toute passe `/impeccable` (décision utilisateur).
- Réorganisation en dossiers par statut (déconseillée dans le rapport, §4.2).
- Migration applicative du dépôt Auxitum lui-même (les scripts sont fournis ;
  leur exécution sur Auxitum est un acte séparé, piloté par l'utilisateur).

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Source de vérité du suivi | Front matter des plans | `roadmap.md` hand-maintenu dérive (F1/F3/F4 du rapport) |
| Lecture par le skill | Index compact généré | ~3-5 Ko vs ~275 Ko de narratif → −82 % d'amorçage |
| Organisation fichiers | Statut = donnée (front matter), pas localisation | Évite le churn `git mv` + liens cassés (§4.2) |
| Statuts hors-enum | Mapping `in-progress`→`active`, `cancelled`→`archived` | 3 plans/287 ne justifient pas +2 statuts à vie (§Q1) |
| CONTEXT.md | Noyau borné + `context/` thématique à la demande | Déjà 81 Ko lu en entier/session → gouffre amorcé |
| Langage scripts | Python 3, réutilise le parseur de `migrate_plan_ids.py` | Précédent existant, pas de dépendance nouvelle |
| Rétrocompat | Index optionnel, fallback lecture directe si absent | Ne jamais casser un projet sans index |

## Étapes

### Lot 1 — Quick wins (gains immédiats, zéro dépendance)
- [ ] Étape 1 — Borner la lecture de `roadmap.md` dans `modules/init-scan.md` : head 50 + tail 30 + `grep` statistique, jamais de lecture intégrale ; documenter la règle (S · standard → Sonnet)
- [ ] Étape 2 — Mapping du vocabulaire de statut : `in-progress`→`active`, `cancelled`→`archived` ; ajouter une **garde de validation** (statut ∈ enum) dans `references/roadmap-file.md` + `references/templates.md` ; documenter le mapping (S · standard → Sonnet)

### Lot 2 — Index généré (cœur de la scalabilité)
- [ ] Étape 3 — `scripts/build_roadmap.py` : scanne le front matter (racine + `done/`) → génère `.index.json` compact (`{id,status,priority,complexity,title,deps,path}`), `roadmap.md` (backlog actif trié priorité→ID) et `done/INDEX.md` ; modes `--dry-run` (défaut) / `--write` / `--check` (écarts index↔réel) (L · reasoning → Opus)
- [ ] Étape 4 — Adapter `modules/init-scan.md` : listing depuis l'index (fallback lecture directe si index absent = rétrocompat) ; régénération de l'index à la clôture d'un plan (hook dans `modules/wrapup.md`) (M · reasoning → Opus)
- [ ] Étape 5 — Listing paresseux : par défaut actifs + bloqués triés par priorité + compteur « + N done » ; filtres `plans high` / `plans blocked` / `plans #250-300` (S · standard → Sonnet)

### Lot 3 — Intégrité, réconciliation & observabilité
- [ ] Étape 6 — `scripts/doctor.py` : audit statut vs dossier, statut ∈ enum, dépendances réciproques, liens `done/` orphelins, index à jour ; rapport tableau + corrections **proposées** (jamais auto-destructrices) ; `--dry-run` par défaut (M · reasoning → Opus)
- [ ] Étape 7 — **Réconciliation au démarrage (garde d'intégrité légère)** : câbler dans `modules/init-scan.md` (règle de démarrage, après la garde d'entrée) une détection **à bas coût** d'écart entre l'état réel (arborescence `doc/roadmap/` + `roadmap.md`) et les conventions #27 — index périmé (comparaison mtime index ↔ fichiers plan), plans mal placés (statut terminal en racine), statut hors-enum, `roadmap.md` désynchronisé de l'index. Si écart → **PROPOSER** la réconciliation (`build_roadmap --write`, `normalize_status`, déplacements) via OUI/NON/instructions ; **jamais d'application silencieuse**. ⚠️ Contrainte dure : staleness check léger uniquement — **pas de `doctor` complet systématique au démarrage** (sinon on re-crée le coût fixe qu'on supprime) ; le `doctor` complet reste sur demande (`aide doctor`). Marqueur de snooze/refus réutilisant le pattern `.migration-declined` (M · reasoning → Opus)
- [ ] Étape 8 — Catégories d'aide `aide doctor` et `aide stats` (observabilité portfolio depuis l'index, sans lire les plans) dans `modules/init-scan.md` (S · standard → Sonnet)

### Lot 4 — CONTEXT.md maîtrisé
- [ ] Étape 9 — Segmentation : noyau `CONTEXT.md` (RÈGLES ABSOLUES, budget dur ~200 l./15 Ko, toujours chargé) + dossier `context/*.md` thématique chargé à la demande ; mettre à jour la section « Hydratation » de `SKILL.md` (M · reasoning → Opus)
- [ ] Étape 10 — Capitalisation auto encadrée : capture gatée OUI/NON/instructions, catégorisation obligatoire (⚠️🔗📌💡) + réf. plan d'origine, garde-fou de budget (refus d'ajout si seuil dépassé → bascule thématique), purge proposée à la clôture de plan (M · reasoning → Opus)

### Lot 5 — Migration & onboarding
- [ ] Étape 11 — `scripts/normalize_status.py` (applique le mapping) + procédure de déplacement des plans mal placés (`done`→`done/`, `archived`→`_archives/`, créer `_archives/`) ; idempotent, `--dry-run`, rollback git (M · standard → Sonnet)
- [ ] Étape 12 — Onboarding : README « Quickstart 5 min » + catégorie `aide migration` (adoption sur projet existant non suivi) (S · standard → Sonnet)
- [ ] Étape 13 — Documentation : aligner `references/{roadmap-file,templates,environment}.md` sur index/statuts/CONTEXT/réconciliation ; bump de version `SKILL.md` (S · standard → Sonnet)

- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test (E2E fresh-install + génération/validation index + mapping statut + réconciliation au démarrage sur arborescence dérivée)
- [ ] ✅ Validation — Vérifier les résultats des tests et clôturer

> Lots séquencés par dépendance : Lot 2 (index) est prérequis du Lot 3. L'étape 7
> (réconciliation au démarrage) dépend de l'étape 3 (`build_roadmap`), de la logique
> de l'étape 6 (`doctor`) et des scripts de l'étape 11 (`normalize`/déplacements) —
> à implémenter donc **après** le Lot 5, ou en limitant d'abord la réconciliation à
> la régénération d'index puis en étendant. Lot 1 est indépendant et livrable
> immédiatement. Lot 4 (CONTEXT) est indépendant des autres.

## Tests

> Section renseignée aux étapes de tests (mode `autonomous` : boucle
> Exécuteur/Vérificateur). Source de vérité traçable.

### Prérequis pour les tests

```bash
(à renseigner en Phase 7 — chemins absolus du repo skill, fixtures de plans
 synthétiques pour build_roadmap/doctor, invocation de scripts/e2e_fresh_install_setup.sh)
```

### Procédure de test

```bash
(à renseigner en Phase 7)
```

**Résultats attendus :** à définir par étape (index conforme au front matter,
`doctor` détecte les dérives injectées, mapping idempotent, listing paresseux
affiche le bon sous-ensemble, budget CONTEXT respecté).

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|

## Journal de session

### Session 2026-10-19
- ✅ Fait : plan créé depuis le rapport d'audit du 2026-10-17 ; décisions actées (mapping statut, pas d'impeccable). Ajout de l'étape 7 — **réconciliation au démarrage** (détection d'écart arborescence/`roadmap.md` vs conventions #27, avec proposition OUI/NON et garde de coût) — suite à une question de cadrage. 13 étapes d'implémentation.
- 📋 Prochain : créer l'issue GitHub #27, réaligner le fichier, puis démarrer le Lot 1 (quick wins).
- 🚧 Blocages : issue GitHub non créée (gérée par l'utilisateur).
