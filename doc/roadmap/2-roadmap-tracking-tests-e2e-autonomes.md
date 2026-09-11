---
plan:
  id: '2'
  name: 2-roadmap-tracking-tests-e2e-autonomes.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/2-roadmap-tracking-tests-e2e-autonomes.md
status: done
date: 2026-09-11
enriched: 2026-09-11
description: >
  Suite de tests end-to-end « installation fraîche » du skill roadmap-tracking
  publié : black-box, exécuté en autonomie (« Moi comme exécuteur »), GitHub
  simulé (zéro appel API), sur 6 projets fictifs rejouables.
priority: high
complexity: L
scope:
  modules:
    - scripts/e2e_fresh_install_setup.sh
    - doc/roadmap/
issue:
  id: 2
  url: https://github.com/ehouriez/roadmap-tracking/issues/2
---

# [🧪] Plan #2 - roadmap-tracking : tests e2e d'installation fraîche (black-box)

## Objectif

Valider l'expérience *end-to-end* du skill publié
(`github.com/ehouriez/roadmap-tracking`) pour un utilisateur qui le découvre,
sans configuration ni historique. Test **black-box** : on ne modifie **pas** le
code du skill ; tout écart est **documenté**, jamais corrigé ici (les
corrections font l'objet du plan #3).

## Périmètre

### Inclus
- Installation depuis le dépôt public + `claude plugin validate`.
- Détection d'environnement (IDE, modèle/tier, mode issues, mode tests).
- Règle de démarrage, listing des plans, `.skill-config.yml`.
- Création de plan (phases 1→6), reprise, gate de complexité.
- Mode issues `github` vs `local` (numérotation, front matter, roadmap.md).
- Robustesse face aux plans non conformes.

### Hors scope
- Chaîne GitHub end-to-end sur l'API réelle (issue simulée, zéro appel).
- Sessions Claude Code headless réelles (gates interactifs non automatisables).
- Correction des écarts (→ plan #3).

## Modèle d'exécution retenu (« Moi comme exécuteur »)

Le skill est un `SKILL.md` d'instructions qu'un agent *suit* ; il ne « tourne »
pas. L'agent (1) installe le plugin pour de vrai depuis GitHub, (2) crée les
projets fictifs, (3) lit le `SKILL.md` **installé** et déroule sa procédure
contre chaque projet en tranchant les gates interactifs par des **choix
documentés et fixes**, (4) vérifie les artefacts déterministes.

> **Limite assumée** : l'agent est à la fois exécuteur et vérificateur → une
> instruction ambiguë qu'il comblerait intuitivement peut passer inaperçue. La
> fidélité maximale exigerait un test manuel humain, hors périmètre.

**GitHub simulé (zéro appel API)** : les fixtures « github » reçoivent un remote
`https://github.com/ehouriez/<slug>.git` pour que la détection de mode résolve
`github`, mais aucune issue/repo n'est créé. Justification : idempotence, aucun
effet de bord sur le compte GitHub réel.

## Environnement de fixtures

- **Racine** : `/tmp/roadmap-tracking/tests/`
- **Setup/teardown rejouable** : `scripts/e2e_fresh_install_setup.sh`
  (teardown `rm -rf` puis recréation à l'identique → **idempotent**). Chaque
  projet est un repo git local autonome.

| Projet fictif | Simule | Particularités |
|---|---|---|
| `project-github-private` | GitHub avec issues | Remote github, `gh` authentifié, mode auto→github, `doc/roadmap/` vide |
| `project-github-optout` | GitHub mais opt-out issues | Remote github + `.skill-config.yml` `issues.mode: local` |
| `project-no-github` | Hors GitHub | Pas de remote github, 1 plan local existant (`2-existing-local.md`) |
| `project-existing-plans` | Plans conformes | `7-conformant-active.md`, `9-conformant-done.md` + roadmap.md |
| `project-existing-plans-unexpected-format` | Plans non conformes | 4 fichiers obligatoires + roadmap.md les référençant |
| `project-fresh` | Vierge | Pas de `doc/roadmap/` du tout |

**4 fichiers obligatoires de `project-existing-plans-unexpected-format`** :

| Fichier | Non-conformité |
|---|---|
| `plan-no-frontmatter.md` | Aucun front matter YAML (markdown brut) |
| `plan-frontmatter-no-issue.md` | Front matter valide mais bloc `issue` absent |
| `plan-frontmatter-partial.md` | Front matter incomplet (`plan.name`, `status`, `complexity` manquants) |
| `plan-no-frontmatter-no-issue.md` | Ni front matter ni issue, structure d'étapes non standard |

## Choix documentés pour les gates interactifs (rejouabilité)

| Gate | Réponse fixe retenue |
|---|---|
| `doc/roadmap/` absent → créer ? | **oui** |
| Nouveau plan ou reprise ? | **nouveau plan** (sauf tests de reprise → plan désigné) |
| Cadrage (`AskUserQuestion` Phase 2) | Réponses par défaut minimales cohérentes |
| Gate modèle (Cas 2 `⚠️`) | **`bypass`** |
| Point d'arrêt Phase 4 / Phase 6 | **valide / implémenter** (tests de création) ; **stop** avant code applicatif |
| Étape 0 Phase 7 | **Aucun test intermédiaire** |

## Grille de tests de référence (E-series)

24 tests. Format de reporting imposé : `### Test X.Y`, blocs **Attendu /
Résultat / Verdict** (`✅ PASS` / `❌ FAIL` / `⚠️ PARTIAL`) + tableau final.

| # | Test | Projet | Verdict |
|---|------|--------|---------|
| 1.1 | Installation depuis GitHub public | (global) | ✅ |
| 1.2 | Détection d'environnement | project-fresh | ✅ |
| 2.1 | `doc/roadmap/` absent → offre de création | project-fresh | ✅ |
| 2.2 | Listing vide + question | project-fresh | ✅ |
| 3.1 | Détection mode local | project-no-github | ✅ |
| 3.2 | Numérotation locale max+1 | project-no-github | ✅ |
| 3.3 | Création plan local — artefacts | project-no-github | ✅ |
| 3.4 | Gate de complexité | project-no-github | ✅ |
| 4.1 | Détection mode github | project-github-private | ✅ |
| 4.2 | Création plan github — artefacts (simulé) | project-github-private | ⚠️ |
| 4.3 | Contrôle ID github-only | project-github-private | ✅ |
| 5.1 | Opt-out respecté | project-github-optout | ✅ |
| 5.2 | Création plan local malgré remote github | project-github-optout | ✅ |
| 6.1 | Listing de plans conformes | project-existing-plans | ✅ |
| 6.2 | Reprise d'un plan conforme | project-existing-plans | ✅ |
| 6.3 | Lecture roadmap.md | project-existing-plans | ✅ |
| 7.1 | Listing de 4 plans non conformes sans crash | project-…-unexpected | ⚠️ |
| 7.2a | Reprise `plan-no-frontmatter.md` | project-…-unexpected | ⚠️ |
| 7.2b | Reprise `plan-frontmatter-no-issue.md` | project-…-unexpected | ⚠️ |
| 7.2c | Reprise `plan-frontmatter-partial.md` | project-…-unexpected | ⚠️ |
| 7.2d | Reprise `plan-no-frontmatter-no-issue.md` | project-…-unexpected | ⚠️ |
| 7.3 | Création d'un plan conforme malgré coexistence | project-…-unexpected | ✅ |
| 7.4 | Robustesse roadmap.md non conforme | project-…-unexpected | ✅ |
| 8.1 | Mode tests manuel vs autonome | (config) | ✅ |

**Résultat de campagne** : **18/24 ✅ PASS**, **6 ⚠️ PARTIAL**, **0 ❌ FAIL**
(100 % sans crash silencieux).

## Étapes

- [x] Étape 1 — Script de setup/teardown idempotent des 6 fixtures (M · standard → Sonnet)
- [x] Étape 2 — Installation depuis GitHub + validation du plugin (S · standard → Sonnet)
- [x] Étape 3 — Exécution de la grille E-series contre chaque fixture (L · reasoning → Opus)
- [x] 🧪 Tests — Grille E-series exécutée (24 tests, reporting Attendu/Résultat/Verdict)
- [x] ✅ Validation — Résultats consolidés, findings consignés, fixtures restaurées

## Findings (black-box, non corrigés — voir plan #3)

1. **Listing des plans malformés sous-spécifié (7.1).** La « Règle de démarrage »
   de `SKILL.md` ne prescrit pas de colonne d'anomalie / `⚠️` ni de valeur par
   défaut pour un plan sans front matter. Le signalement d'anomalie n'existe
   **que** dans le script de migration (mode github + déclenchement explicite).
2. **Reprise sans branche « plan malformé » (7.2a-d).** Le workflow de reprise
   lit `front matter ou ligne Description` en fallback mais n'a **aucune branche
   dédiée** proposant activement conformité / mode dégradé / refus.
3. **Numérotation locale vs `plan.id` du front matter (7.3).** L'ID local =
   `max(préfixes de nom de fichier) + 1` **ignore** les `plan.id` déclarés dans
   le front matter de fichiers sans préfixe → collision logique possible (ici,
   prochain ID local = 1 alors que `plan.id` 3 et 4 existent en front matter).
4. **Chaîne github end-to-end non éprouvée (4.2).** Par choix (zéro-API), la
   création réelle d'issue n'est pas testée → couverture partielle.

**Points forts confirmés** : installation propre + `validate` sans warning ;
détection de mode robuste (opt-out via config prioritaire) ; artefacts locaux
100 % conformes à `templates.md` ; script `migrate_plan_ids.py` **résilient**
aux 4 malformations (exit 0, remédiation guidée) ; aucun crash sur aucun cas.

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Modèle d'exécution | « Moi comme exécuteur » | Rejouable/idempotent ; gates interactifs non automatisables autrement |
| GitHub | Simulé, zéro appel API | Idempotence ; aucun effet de bord sur le compte réel |
| Fixtures | Script de setup/teardown versionné | Rejouabilité + idempotence garanties |

## Journal de session

### Session 2026-09-11 — Campagne e2e

**Modèle actif** : Claude Opus 4.8 (1M context) — tier `reasoning`.

**✅ Fait** : campagne complète exécutée. Plugin cloné depuis GitHub public,
`claude plugin validate` → `Validation passed` sans warning ; publié identique à
la copie locale. 6 fixtures créées via `scripts/e2e_fresh_install_setup.sh`
(idempotence vérifiée par double run). Grille E-series : **18/24 ✅ PASS,
6 ⚠️ PARTIAL, 0 ❌ FAIL**.

**🔎 Findings consignés (4)** — reportés ci-dessus (section « Findings ») et en
commentaire de l'issue #2 :

1. Listing des plans malformés sous-spécifié dans `SKILL.md § Règle de démarrage`.
2. Reprise sans branche dédiée aux plans malformés.
3. Numérotation locale par préfixe de fichier ignorant les `plan.id` du front matter.
4. Chaîne github end-to-end non éprouvée (simulation zéro-API assumée).

**📋 Prochain** : corrections traitées dans le plan #3
(`3-roadmap-tracking-corrections-findings-e2e.md`, issue #3).

**🚧 Blocages** : aucun.
