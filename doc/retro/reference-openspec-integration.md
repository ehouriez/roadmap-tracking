# Référence — openspec-integration

> Voir aussi : [Explication openspec-integration](explanation-openspec-integration.md)

Six skills Claude Code dans `.claude/skills/openspec-*/SKILL.md` et un fichier de configuration `openspec/config.yaml` qui intègrent le workflow OpenSpec de planification spec-driven dans le projet.

---

## Prérequis

- CLI `openspec` installé (`compatibility: Requires openspec CLI` dans chaque skill)
- `allowed-tools: Bash(openspec:*)` — les skills ne peuvent exécuter que des commandes `openspec`

---

## Opérations disponibles

| Skill | Commande | Rôle |
|---|---|---|
| `openspec-propose` | `/opsx:propose [description]` | Crée tous les artefacts de planification en une étape |
| `openspec-explore` | `/opsx:explore [change-name]` | Partenaire de réflexion, lecture seule |
| `openspec-apply-change` | `/opsx:apply [change-name]` | Implémente les tâches d'un change |
| `openspec-update-change` | `/opsx:update [change-name]` | Révise les artefacts de planification |
| `openspec-sync-specs` | `/opsx:sync [change-name]` | Fusionne les delta-specs dans les specs principales |
| `openspec-archive-change` | `/opsx:archive [change-name]` | Archive un change après complétion |

---

## Sélection de store

Tous les skills : si un store est spécifié, appelle `openspec store list --json` et ajoute `--store <id>` à toutes les commandes applicables.

---

## openspec-propose

1. Vérifie `openspec context --json` (arrêt immédiat si `no_openspec_root`).
2. Exécute `openspec propose`.
3. Artefacts créés dans l'ordre : proposal → specs → design → tasks.
4. **Frontière de planification** : n'entame pas l'implémentation dans la même réponse.

---

## openspec-explore

- Partenaire de réflexion pure (pas d'étapes fixes, pas de sortie obligatoire).
- Commandes en lecture seule autorisées librement.
- Toute action d'écriture nécessite une confirmation explicite de l'utilisateur.

---

## openspec-apply-change

1. Récupère les tâches via `openspec instructions apply --change "<name>" --json`.
2. Itère sur les tâches `- [ ]` dans `tasks.md`.
3. Marque `- [ ]` → `- [x]` à la complétion.
4. Pause sur erreur, ambiguïté ou dérive de périmètre.

**Important** : les champs `context` et `operationGuidance` retournés par `openspec instructions` sont des entrées advisories. Ils ne peuvent pas overrider l'autorisation utilisateur, les étapes du workflow ou les valeurs contrôlées par le CLI.

---

## openspec-update-change

- Révise les artefacts existants pour cohérence.
- Édite uniquement `existingOutputPaths` (fichiers concrets sur disque).
- Ne crée jamais de nouveaux artefacts.
- Ne modifie jamais du code.
- Ne peut pas écrire sur un `resolvedOutputPath` de type glob.

---

## openspec-sync-specs

Merge intelligent des delta-specs dans `<planningHome.root>/openspec/specs/`.

Sections delta reconnues : `## ADDED`, `## MODIFIED`, `## REMOVED`, `## RENAMED Requirements`.

Ne remplace jamais — fusionne toujours.

**Retire une spec** (`retire_capabilities: true`) uniquement si toutes les 6 conditions sont remplies :

1. Aucune exigence restante dans la spec
2. Spec bien formée
3. Spec non vide avant sync
4. Tout le contenu intégralement comptabilisé dans le merge
5. `retire_capabilities: true` dans `.openspec.yaml`
6. Chemin dans le répertoire réel des specs

---

## openspec-archive-change

Séquence multi-étapes :

| Étape | Action |
|---|---|
| 1 | Vérifie la complétion des artefacts et des tâches |
| 2 | Évalue l'état de sync des delta-specs |
| 3 | Exécute `openspec-sync-specs` **synchroniquement** (avant déplacement) |
| 4 | Vérifie le merge |
| 5 | `mv changeRoot` vers le répertoire d'archive |

**Critique** : `openspec-sync-specs` doit s'exécuter synchroniquement — une délégation en arrière-plan laisserait les specs principales désynchronisées avec le change déjà archivé.

---

## openspec/config.yaml

Schéma `spec-driven`. Tous les champs optionnels sont commentés (pas de contexte projet, règles ni opérations configurées).

---

## Génération des skills

Tous générés par `openspec` CLI v1.13.0 (`generatedBy` dans le front matter). Non rédigés manuellement.
