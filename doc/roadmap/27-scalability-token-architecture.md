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

> **⚠️ PRÉREQUIS DE REPRISE — lire avant toute implémentation** :
> `doc/rapports/rapport-ameliorations-2026-10-17.md` (rapport d'audit complet,
> mesures tokens, contre-propositions, décisions). Ce rapport est la source de
> vérité pour le *pourquoi* de chaque étape. Sans lui, les choix d'implémentation
> manquent de contexte (ex. : pourquoi pas de dossiers par statut §4.2, pourquoi
> mapper et non officialiser les statuts §Q1, estimation gains −82 % §8).
>
> Décisions utilisateur actées : statuts hors-enum **mappés** (`in-progress`→`active`,
> `cancelled`→`archived`) ; `/impeccable` **non utilisé**.
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
- [x] Étape 1 — Borner la lecture de `roadmap.md` dans `modules/init-scan.md` : head 50 + tail 30 + `grep` statistique, jamais de lecture intégrale ; documenter la règle (S · standard → Sonnet)
- [x] Étape 2 — Mapping du vocabulaire de statut : `in-progress`→`active`, `cancelled`→`archived` ; ajouter une **garde de validation** (statut ∈ enum) dans `references/roadmap-file.md` + `references/templates.md` ; documenter le mapping (S · standard → Sonnet)

### Lot 2 — Index généré (cœur de la scalabilité)
- [x] Étape 3 — `scripts/build_roadmap.py` : scanne le front matter (racine + `done/`) → génère `.index.json` compact (`{id,status,priority,complexity,title,deps,path}`), `roadmap.md` (backlog actif trié priorité→ID) et `done/INDEX.md` ; modes `--dry-run` (défaut) / `--write` / `--check` (écarts index↔réel) (L · reasoning → Opus)
- [x] Étape 4 — Adapter `modules/init-scan.md` : listing depuis l'index (fallback lecture directe si index absent = rétrocompat) ; régénération de l'index à la clôture d'un plan (hook dans `modules/wrapup.md`) (M · reasoning → Opus)
- [x] Étape 5 — Listing paresseux : par défaut actifs + bloqués triés par priorité + compteur « + N done » ; filtres `plans high` / `plans blocked` / `plans #250-300` (S · standard → Sonnet)

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
SKILL_REPO=/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking
INIT_SCAN=$SKILL_REPO/modules/init-scan.md
ROADMAP_FILE=$SKILL_REPO/references/roadmap-file.md
TEMPLATES=$SKILL_REPO/references/templates.md
```

### Procédure de test

```bash
echo "=== Étape 1 — Règle de lecture bornée dans init-scan.md ==="
grep -n "Lecture bornée de" $INIT_SCAN

echo "=== Étape 1 — Présence head-50, tail-30, grep ==="
grep -n "head -50\|tail -30\|grep" $INIT_SCAN | grep -v "^Binary"

echo "=== Étape 1 — Mention toutes phases ==="
grep -n "toutes phases" $INIT_SCAN

echo "=== Étape 1 — Placement correct (après bloc A.0, avant listing) ==="
grep -n "help.welcomed: true\|Lecture bornée\|Si l'utilisateur ne référence" $INIT_SCAN | head -5

echo "=== Étape 2 — Vocabulaire de statut dans roadmap-file.md ==="
grep -n "Vocabulaire de statut\|Valeurs canoniques\|Mapping des valeurs\|Garde de validation" $ROADMAP_FILE

echo "=== Étape 2 — Mapping in-progress et cancelled ==="
grep -n "in-progress\|cancelled" $ROADMAP_FILE

echo "=== Étape 2 — Status field mis à jour dans templates.md ==="
grep -n "status.*Mapping automatique\|in-progress.*active" $TEMPLATES
```

**Résultats attendus :**
- Étape 1 : règle `⛔ Lecture bornée de roadmap.md` présente à la ligne ~108, avec `head -50`, `tail -30`, `grep`, mention `toutes phases` ; placée entre `help.welcomed: true` et `Si l'utilisateur ne référence pas`.
- Étape 2 : section `## Vocabulaire de statut` présente dans `roadmap-file.md` avec sous-sections `Valeurs canoniques` (4 entrées) et `Mapping des valeurs hors-enum` (`in-progress`→`active`, `cancelled`→`archived`) + garde `⛔` ; champ `status` de `templates.md` référence `Mapping automatique`.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-10-19 | Étape 1 — règle bornée init-scan.md | Présente, head-50/tail-30/grep, toutes phases, placement correct | Ligne 108, toutes assertions positives | ✅ |
| 2026-10-19 | Étape 2 — mapping + garde roadmap-file.md + templates.md | Section Vocabulaire, 4 canoniques, mapping, garde, templates ref | Toutes assertions grep positives | ✅ |

### Lot 2 — procédure (étape 5)

```bash
SKILL_REPO=/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking
IS=$SKILL_REPO/modules/init-scan.md

echo "=== E5.1 Listing paresseux — titre updated ==="
grep -n "Listing paresseux" $IS

echo "=== E5.2 Contenu par défaut : active + blocked ==="
grep -n "status: active.*blocked\|status: blocked" $IS | head -5

echo "=== E5.3 Tri priorité critical → high → medium → low ==="
grep -n "critical → high → medium → low" $IS

echo "=== E5.4 Compteur + N done ==="
grep -n "+ N done" $IS

echo "=== E5.5 Filtres verbaux présents ==="
grep -n "Filtres verbaux\|plans high\|plans blocked\|plans #N-M" $IS
```

**Résultats attendus :**
- E5.1 : « Listing paresseux (défaut) » présent dans la règle de démarrage.
- E5.2 : `status: active` et `status: blocked` documentés comme contenu par défaut.
- E5.3 : ordre de tri `critical → high → medium → low` présent.
- E5.4 : compteur `+ N done` documenté.
- E5.5 : section « Filtres verbaux » avec `plans high`, `plans blocked`, `plans #N-M`.

### Résultats joués et vérifiés — Lot 2 (étape 5)

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-10-19 | E5.1 listing paresseux titre | « Listing paresseux (défaut) » présent | Ligne 136, présent | ✅ |
| 2026-10-19 | E5.2 contenu active + blocked | status active + blocked documentés | Lignes 145, 202, présents | ✅ |
| 2026-10-19 | E5.3 tri priorité | critical → high → medium → low | Ligne 146, présent | ✅ |
| 2026-10-19 | E5.4 compteur N done | `+ N done` documenté | Ligne 147, présent | ✅ |
| 2026-10-19 | E5.5 filtres verbaux | plans high / blocked / #N-M présents | Lignes 196-203, présents | ✅ |

### Lot 2 — procédure (étapes 3-4)

```bash
SKILL_REPO=/mnt/c/INETUM/AGV/agv-adm/GIT_GITHUB/skills/roadmap-tracking
RM=$SKILL_REPO/doc/roadmap

echo "=== E3.1 Script self-check ==="
python3 $SKILL_REPO/scripts/build_roadmap.py --self-check

echo "=== E3.2 Generation (write) + check up-to-date (exit 0) ==="
python3 $SKILL_REPO/scripts/build_roadmap.py --roadmap-dir $RM --write
python3 $SKILL_REPO/scripts/build_roadmap.py --roadmap-dir $RM --check

echo "=== E3.3 Drift detection returns exit 1 ==="
python3 -c "import json;p='$RM/.index.json';d=json.load(open(p));d.append({'id':'999','status':'active','priority':'low','complexity':'S','title':'x','deps':[],'path':'999-x.md'});json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)"
python3 $SKILL_REPO/scripts/build_roadmap.py --roadmap-dir $RM --check; echo "exit=$?"
python3 $SKILL_REPO/scripts/build_roadmap.py --roadmap-dir $RM --write

echo "=== E3.4 Done excluded from backlog, present in done index ==="
grep -c "Issue: #" $RM/roadmap.md
grep -c "| #" $RM/done/INDEX.md

echo "=== E4.1 init-scan reads .index.json with fallback ==="
grep -n "\.index\.json\|Index absent\|fallback" $SKILL_REPO/modules/init-scan.md

echo "=== E4.2 wrapup regenerates index at closure ==="
grep -n "build_roadmap.py --roadmap-dir doc/roadmap --write" $SKILL_REPO/modules/wrapup.md
```

**Résultats attendus :**
- Étape 3 : `self-check passed` ; `--write` crée `.index.json` + `roadmap.md` + `done/INDEX.md` ; `--check` exit 0 quand à jour, exit 1 + diff (`- plan 999`) quand périmé ; `roadmap.md` ne liste que le backlog actif (1 entrée `#27`), les 24 `done` sont dans `done/INDEX.md`.
- Étape 4 : `init-scan.md` instruit de lire `.index.json` d'abord avec fallback lecture bornée si absent ; `wrapup.md` régénère les vues via `build_roadmap.py --write` à la clôture.

### Résultats joués et vérifiés — Lot 2 (étapes 3-4)

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|
| 2026-10-19 | E3.1 self-check | `self-check passed` | `✅ self-check passed` | ✅ |
| 2026-10-19 | E3.2 write + check | write 3 fichiers, check exit 0 | 3 fichiers écrits, `up to date (27 plans)` exit 0 | ✅ |
| 2026-10-19 | E3.3 drift exit 1 | exit 1 + `- plan 999` | `stale`, `- plan 999`, exit 1 | ✅ |
| 2026-10-19 | E3.4 backlog/done split | backlog 1 actif, 24 done indexés | roadmap.md 1 `#27`, index actif=1 done=24 | ✅ |
| 2026-10-19 | E4.1 init-scan index-first | ref `.index.json` + fallback | 5 occurrences `.index.json`, fallback présent | ✅ |
| 2026-10-19 | E4.2 wrapup regen hook | hook `build_roadmap --write` | 1 occurrence | ✅ |

## Journal de session

### Session 2026-10-19 (création)
- ✅ Fait : plan créé depuis le rapport d'audit du 2026-10-17 ; décisions actées (mapping statut, pas d'impeccable). Ajout de l'étape 7 — **réconciliation au démarrage** (détection d'écart arborescence/`roadmap.md` vs conventions #27, avec proposition OUI/NON et garde de coût) — suite à une question de cadrage. 13 étapes d'implémentation.
- 📋 Prochain : créer l'issue GitHub #27, réaligner le fichier, puis démarrer le Lot 1 (quick wins).
- 🚧 Blocages : issue GitHub non créée (gérée par l'utilisateur).

### Session 2026-10-19 (implémentation Lot 1 — étapes 1-2)
- ✅ Fait : Étape 1 — règle `⛔ Lecture bornée de roadmap.md` ajoutée dans `modules/init-scan.md` (head-50/tail-30/grep, règle globale toutes phases). Étape 2 — section `## Vocabulaire de statut` avec enum + mapping (`in-progress`→`active`, `cancelled`→`archived`) + garde de validation ajoutés dans `references/roadmap-file.md` ; champ `status` mis à jour dans `references/templates.md`.
- 📋 Prochain : Lot 2 — étape 3 (`scripts/build_roadmap.py`).
- 🚧 Blocages : aucun.

### Session 2026-10-19 (implémentation Lot 2 — étape 5)
- ✅ Fait : Étape 5 — Listing paresseux dans `modules/init-scan.md`. Défaut : `status: active` + `status: blocked`, tri priorité (critical→high→medium→low) puis `id`, compteur `+ N done`. Filtres verbaux : `plans high` (critical+high), `plans blocked`, `plans #N-M` (intervalle d'id).
- 📋 Prochain : Lot 3 — étape 6 (`scripts/doctor.py`).
- 🚧 Blocages : aucun.

### Session 2026-10-19 (implémentation Lot 2 — étapes 3-4)
- ✅ Fait : Étape 3 — `scripts/build_roadmap.py` créé (réutilise le parseur de front matter de `migrate_plan_ids.py`, zéro dépendance). Scanne racine + `done/`, applique le mapping de statut, génère `.index.json` (JSON, fichier caché sous `doc/roadmap/`, consommé par le skill), `roadmap.md` (backlog actif trié priorité→ID, généré tel quel) et `done/INDEX.md` ; modes `--dry-run`/`--write`/`--check`/`--self-check`. Étape 4 — `modules/init-scan.md` : listing index-first (`.index.json`) avec fallback lecture bornée si absent (rétrocompat) ; `modules/wrapup.md` : la clôture régénère les vues via `build_roadmap.py --write` (support 3 n'est plus un édit manuel de `roadmap.md`). Décisions utilisateur : index = JSON ; `roadmap.md` généré tel quel. Index généré pour 27 plans (1 actif / 24 done / 2 archived). Tests autonomes → voir section `## Tests`.
- 📋 Prochain : Lot 2 — étape 5 (listing paresseux / filtres), puis Lot 3.
- 🚧 Blocages : aucun. ⚠️ `build_roadmap.py` et les vues générées sont versionnés dans le repo du skill mais le skill s'exécute depuis le cache plugin : la copie cache ne contiendra le script qu'après publication/sync de la nouvelle version.
