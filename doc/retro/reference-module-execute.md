# Référence — module-execute

> Voir aussi : [Explication module-execute](explanation-module-execute.md)

`modules/execute.md` — Phases 5 à 7. Création du fichier plan et de l'issue GitHub (Phase 5), validation avant implémentation pour plans L/XL (Phase 6), et implémentation étape par étape avec tests (Phase 7).

---

## Phase 5 — Act limité

Mode : `🔨 MODE ACT (PLAN)`. Opérations autorisées uniquement : fichier plan, issue GitHub, `roadmap.md`. Aucune lecture de code applicatif.

### Détection du mode `issues`

| Priorité | Condition | Mode |
|---|---|---|
| 1 | `.skill-config.yml` → `issues.mode` | Valeur lue |
| 2 | `.git/` + remote GitHub + `gh auth status` OK | `github` |
| 3 | Sinon | `local` |

### Mode `github`

1. Créer l'issue GitHub via `gh issue create`
2. Créer `./doc/roadmap/{ISSUE}-slug.md` avec front matter complet
3. Mettre à jour le corps de l'issue avec le chemin vers le plan
4. Mettre à jour `roadmap.md`

### Mode `local`

1. Calculer ID = max(préfixes numériques des fichiers ∪ valeurs `plan.id` en front matter) + 1
2. Créer `./doc/roadmap/{ID}-slug.md`
3. Mettre à jour `roadmap.md`

Collision possible en mode collaboratif : résolution par git au merge (documenté, non masqué).

### `⏸️ STOP POINT 2` — 4 options

1. Implémentation étape par étape
2. Mode one-shot (⚡) — supprime les `⏸️` intermédiaires (garde 🧪 et ✅)
3. Modifier le plan
4. Stopper

---

## Phase 6 — Validation avant implémentation (L/XL uniquement)

XS/S/M : sautée — `⏸️ STOP POINT 2` de la Phase 5 double comme gate.

Pour L/XL : grilling sur risques d'implémentation, couverture de tests, rollback, impact features existantes.

Gate binaire en fin :
- Continuer → Phase 7
- Retour → Phase 3 (modifier le plan)

---

## Phase 7 — Implémentation

Mode : `🔨 MODE ACT (IMPLÉMENTATION)`.

### Auto-vérification avant démarrage

Checklist obligatoire :
- Plan ouvert et sections `## Étapes` et `## Tests` présentes
- `tests.mode` résolu et persisté
- Étape 0 jouée (mode `manual` uniquement)

**Fast-track** (XS ou S+solo en `mode: auto`) : step 0 supprimé, aucun `⏸️` intermédiaire.

### Gate modèle en début de Phase 7

Évalue le tier le plus élevé requis parmi toutes les étapes du plan (pas par étape). Section canonique dans `modules/plan.md`.

### Étape 0 — Sélection des tests intermédiaires (mode `manual`)

AskUserQuestion multiSelect, toutes options décochées par défaut.

Mode `autonomous` : étape 0 sautée.

---

## Tests unitaires intermédiaires

Procédure **écrite dans `## Tests` du plan** (Edit/Write en PREMIER) avant affichage dans le chat.

Structure obligatoire :

```
### Prérequis pour les tests
### Procédure de test
### Résultats joués et vérifiés
```

**Zero-lookup rule** : tous les chemins absolus, variables d'environnement et commandes de setup résolus à l'écriture.

`⏸️` + `📦 Commit proposé` après chaque bloc de test validé.

---

## Étape 🧪 Tests (obligatoire, avant-dernière)

Procédure complète écrite dans `## Tests` du plan.

Prérequis + procédure résolus au moment de l'écriture (zero-lookup).

Si aucun fichier modifié depuis le dernier commit : `📦 Aucun commit nécessaire`.

---

## Étape ✅ Validation (obligatoire, dernière)

- **Succès** → déclenche le workflow de clôture (`modules/wrapup.md`)
- **Échec** → crée ou met à jour `## Diagnostic en cours` dans le plan

Structure de `## Diagnostic en cours` (créée à la première failure, supprimée à la résolution) :
- Bloc(s) en échec
- Hypothèses éliminées
- Pistes ouvertes
- Vérifications à jouer

---

## Commits d'implémentation

Format Conventional Commits avec référence à l'issue et numéro d'étape.

Jamais auto-exécutés — toujours des propositions `📦`.

---

## Règle d'escalade « 2 strikes »

**Déclencheur** : ≥ 2 verdicts ❌ consécutifs sur le même bloc de test dans des sessions distinctes, tier `standard`.

**Action** : recommande passage au tier `reasoning` + option bypass.

**Non applicable** : si modèle déjà au tier `reasoning`.

**Deux ❌ dans la même session autonome** : ne comptent pas comme 2 strikes (`max_iterations` gère ce cas).

### Critères d'escalade immédiate (1 seul strike)

- Interaction infra+code sans preuve matérielle
- Diagnostic sans pistes restantes dans `## Diagnostic en cours`
- Session bloquée > 10 min
