# Référence — module-wrapup

> Voir aussi : [Explication module-wrapup](explanation-module-wrapup.md)

`modules/wrapup.md` — Workflow de reprise d'un plan existant et checklist de clôture d'un plan validé.

---

## Workflow de reprise

### 1. Validation du plan avant reprise

Vérifier la présence de `plan.id`, `status`, `complexity` et la structure des étapes.

Si plan non conforme, 3 options via AskUserQuestion :

| Option | Action |
|---|---|
| Conformer le plan | Appliquer `references/templates.md` |
| Mode dégradé | Reprendre en affichant `⚠️` pour les champs manquants |
| Annuler | Stopper |

Jamais inventer de valeurs pour les champs manquants.

### 2. Résumé de reprise

Affiche : statut, complexité, tier modèle recommandé, date de dernière session, compteur d'étapes (terminées / total), étapes restantes avec tags.

### 3. Vérifications avant `⏸️` (dans l'ordre)

1. **Gate modèle** : si tier requis par les étapes restantes > tier actif → recommandation de modèle.
2. **Vérification "2 strikes"** : si ≥ 2 ❌ consécutifs dans `## Tests` sur le même bloc avec tier `standard` → recommandation d'escalade.

### 4. `⏸️ STOP POINT` de reprise

Obligatoire après le résumé. Jamais de lecture de code source ni d'exécution de commande avant ce point.

### 5. Dispatch post-arrêt

| Mode | Action |
|---|---|
| `manual` | Étape 0 : AskUserQuestion sélection tests intermédiaires → Phase 7 |
| `autonomous` | Phase 7 directement (étape 0 sautée) |

### Rétrocompatibilité

| Situation | Action |
|---|---|
| Plan sans `🧪 Tests` / `✅ Validation` | Ajouter à la reprise |
| Plan sans `## Tests` | Créer à la première exécution de test |
| Plan sans tags d'étape | Sauter la gate modèle par étape |

---

## Checklist de clôture

### Prérequis

`🧪 Tests` et `✅ Validation` doivent être explicitement complétés et cochés avant clôture.

### 4 étapes de clôture (dans l'ordre)

| Étape | Action |
|---|---|
| 1 | `status: done` + `intent: null` dans le front matter ; `updated_at` rafraîchi ; `plan.link` → chemin `done/` |
| 2 | `git mv doc/roadmap/NNN-slug.md doc/roadmap/done/NNN-slug.md` |
| 3 | `${PY} ${SKILL_DIR}/scripts/build_roadmap.py --roadmap-dir doc/roadmap --write` |
| 4 | Fermer l'issue GitHub avec commentaire de clôture (mode `github` uniquement) |

**Cas particuliers** :

| Situation | Action |
|---|---|
| `issue.id` absent | Sauter étape 4, signaler à l'utilisateur |
| `build_roadmap.py` absent | Édition manuelle de `roadmap.md` |
| Mode `local` | Étapes 1–3 uniquement |

Les 4 étapes sont atomiques en mode `github` : laisser l'une ouverte = état d'erreur explicite.

### Purge CONTEXT.md

À la clôture, proposer (OUI/NON, jamais silencieux) de purger les entrées `CONTEXT.md` / `context/*.md` devenues obsolètes.

### Archivage

`archived/` (`status: archived`) = opération rare, distincte de `done/`.

`archived/roadmap_done.md` = fichier gelé déprécié. Ne jamais y déplacer un plan validé.
