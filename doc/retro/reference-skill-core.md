# Référence — skill-core

> Voir aussi : [Explication skill-core](explanation-skill-core.md)

`SKILL.md` — Point d'entrée du skill `roadmap-tracking:roadmap-tracking`. Orchestre un workflow à 7 phases pour encadrer, planifier, suivre et tracer des demandes de développement, configuration et architecture via des fichiers plan, `roadmap.md` et des issues GitHub.

---

## Point d'entrée et déclencheurs

- **Skill id** : `roadmap-tracking:roadmap-tracking`
- **Fichier** : `SKILL.md`
- **Déclencheurs automatiques** : `plan`, `cadrage`, `roadmap`, `issue`, `backlog`, `sprint`, `ticket`, `#[0-9]+`, `suivi de tâche`, `implémente`, `reprends`, `continue`, `enchaîne`, etc. (SKILL.md:16–19)

---

## Prérequis

| Prérequis | Obligatoire |
|---|---|
| `doc/roadmap/` présent | Oui |
| Python 3 (`python3 / python / py`) | Oui |
| `git` | Oui |
| `gh` CLI | Non (mode `github` uniquement) |

---

## Les 7 phases

| Phase | Rôle | Module | Point d'arrêt |
|---|---|---|---|
| 1 | Analyse silencieuse + complexité + auto-calibrage (Axe A) | `init-scan.md` | Non |
| 1.5 | Gate modèle (Cas 2 uniquement) | `init-scan.md` | `⏸️` si Cas 2 |
| 2 | Cadrage interactif / grilling frontier illimitée | `plan.md` | Non |
| 3 | Proposition verbale du plan (rien n'est écrit) | `plan.md` | `⏸️` STOP 1 |
| 4 | Validation de la proposition | `plan.md` | `⏸️` (ExitPlanMode) |
| 5 | Act limité — création plan/issue/roadmap | `execute.md` | `⏸️` STOP 2 |
| 6 | Validation avant implémentation (L/XL uniquement) | `execute.md` | `⏸️` |
| 7 | Implémentation étape par étape + 🧪 Tests + ✅ Validation | `execute.md` | `⏸️` post-🧪 |

**Fast-path** : XS/S solo (`collaborative: false`) → Phases 1.5 (Cas 1) et 6 supprimées. Mode `lightweight` → aucun `⏸️` intermédiaire.

---

## Modules de workflow

| Module | Fichier | Phases / déclencheur |
|---|---|---|
| Initialisation & scan | `modules/init-scan.md` | Tour 1, Phases 1–1.5 |
| Planification | `modules/plan.md` | Phases 2–4 |
| Exécution | `modules/execute.md` | Phases 5–7 |
| Clôture & reprise | `modules/wrapup.md` | Reprise d'un plan existant + clôture |

Règle : jamais plus d'un module simultanément sauf Phase 1 (init-scan + plan ensemble).

---

## Hydratation du contexte

```
CONTEXT.md (noyau) — ≤ 200 lignes / ≤ 15 Ko — lu au démarrage si non vide
context/*.md (thématiques) — chargés à la demande selon la pertinence
```

Écriture via capitalisation encadrée uniquement (AskUserQuestion → OUI / NON / Instructions). Jamais silencieuse.

Catégories d'entrées :

| Préfixe | Catégorie |
|---|---|
| ⚠️ | Piège / régression évitée |
| 🔗 | Dépendance entre features/plans |
| 📌 | Contrainte durable |
| 💡 | Insight / décision structurante |

---

## Auto-calibrage (Axe A)

| Complexité | `collaborative` | Mode effectif |
|---|---|---|
| XS | any | `lightweight` |
| S | false | `lightweight` |
| S | true | `lightweight` |
| M | any | `lightweight` |
| L, XL | any | `full` |

Override : `.skill-config.yml` → `roadmap-tracking.mode: full | lightweight | off`.

Triggers verbaux : `mode workflow complet`, `mode lightweight`, `désactive le skill`, `remets le mode auto`, `projet collaboratif`, `projet solo`.

---

## Règles absolues

1. **Format des rapports** : tout listing de plans = tableau markdown. Formats `clé: valeur` et listes à puces en remplacement d'un tableau : interdits.
2. **Séparation création/implémentation** : jamais créer un plan ET implémenter dans le même passage.
3. **Tests obligatoires avant clôture** : `status: done` impossible sans 🧪 Tests et ✅ Validation complétés.
4. **Traçabilité tests dans le fichier plan** : procédure et résultats écrits dans `## Tests` du plan file (Edit/Write en PREMIER, chat = pointeur uniquement).
5. **⏸️ sans 📦 = invalide** : tout point d'arrêt post-tests nécessite un bloc `📦 Commit proposé` (ou `📦 Aucun commit nécessaire`).

---

## Signaux de mode

| Signal | Sens |
|---|---|
| `🧠 MODE PLAN` | Réflexion, rien n'est exécuté |
| `🔍 MODE CADRAGE` | Questions, rien n'est exécuté |
| `🔨 MODE ACT (PLAN)` | Création plan/issue/roadmap uniquement |
| `🔨 MODE ACT (IMPLÉMENTATION)` | Implémentation de l'étape N |
| `⏸️ POINT D'ARRÊT` | En attente de validation |

---

## Applicabilité

Ne s'applique **pas** :
- Questions de culture générale sans modification de fichier
- Urgences (`URGENT`, `PROD DOWN`) — fix immédiat autorisé ; traçabilité post-fix **obligatoire**
- Demandes d'aide (`aide`, `aide workflow`, `aide config`, …, `help`)

---

## Correction proactive des incohérences

À chaque interaction avec un fichier plan : corrige silencieusement les métadonnées structurelles incohérentes (`status`, `updated_at`, dépendances réciproques manquantes, fichiers mal placés). Notifie via tableau récapitulatif après chaque série de corrections.

---

## Fichiers de référence chargés à la demande

| Fichier | Quand charger |
|---|---|
| `references/environment.md` | **Toujours au démarrage** |
| `references/forms.md` | Phase 2 (cadrage) |
| `references/templates.md` | Phase 5 + changements de statut |
| `references/roadmap-file.md` | Phase 5 + changements de statut |
| `references/github-issues.md` | Mode `github` uniquement |
| `references/migration.md` | Mode `github`, migration IDs |
| `references/autonomous-tests.md` | Phase 7, `tests.mode: autonomous` |
