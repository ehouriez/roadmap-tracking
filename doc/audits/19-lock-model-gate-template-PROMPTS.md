Tu es un ingénieur logiciel expert en développement d'agents et de skills CLI.

### CONTEXTE DU PROBLÈME
Le skill "roadmap-tracking" a généré ce message erroné lors d'une transition de modèle :
```txt
⏸️ Continue sur Sonnet 4.6 ou switch de modèle ?
- Tape `bypass` pour continuer sur le modèle actif
- Tape `/model claude-opus-5` puis `continue` pour switcher
```
**Causes identifiées :**
1. L'agent a inventé un format de message non standardisé.
2. L'agent a halluciné des versions explicites (`Sonnet 4.6`, `claude-opus-5`) au lieu d'utiliser des alias génériques.
3. Il n'existe pas de template strict et déterministe dans le skill imposant la structure textuelle exacte du prompt de switch.

---

### OBJECTIF GLOBAL
Verrouiller de manière déterministe l'affichage des messages d'upgrade/downgrade de modèle, généraliser les identifiants de modèles (sans numéro de version), intégrer le support multi-fournisseur (Anthropic/Claude Code vs OpenAI/Codex), et synchroniser la documentation interne du skill.

---

### PLAN D'EXÉCUTION OBLIGATOIRE (À suivre étape par étape)

#### ÉTAPE 1 : Analyse de la fuite (Diagnostic)
Identifie précisément dans le code et les fichiers d'instructions du skill comment l'agent a pu générer le message ci-dessus. Vérifie s'il s'agit d'un manque de template explicite, d'une instruction floue ("proposer à l'utilisateur de changer de modèle") ou d'une mauvaise extraction des métadonnées du runtime.

#### ÉTAPE 2 : Mise à jour de `references/environment.md`
1. **Renommage de section :**
   - Renomme la section `[L21-41]` actuellement dédiée au mapping des modèles vers un nom explicite et agnostique : `## Model Tier & Environment Mapping`.
2. **Refonte de la matrice (Tableau) :**
   - Remplace le tableau existant par le format suivant (ajout impératif de la colonne `OpenAI default` et suppression des numéros de version) :

| Tier | Role | Anthropic default | OpenAI default | Override key |
|---|---|---|---|---|
| `standard` | General work — scoping, plan writing, step implementation | **sonnet** (current) | **luna** (current) | `models.map` |
| `reasoning` | Complex analysis, architecture, multi-file planning | **opus** | **sol** | `models.map` |
| `light` | Out of scope for planning (never recommended) | **haiku** | — | `models.map` |

3. **Exemples de configuration `.skill-config.yml` :**
   - Documente sous le tableau les exemples de mapping pour chaque contexte :
   ```yaml
   # Contexte Anthropic / Claude Code
   models:
     map:
       - { name: opus,   tier: reasoning }
       - { name: sonnet, tier: standard }

   # Contexte OpenAI / Codex
   models:
     map:
       - { name: sol,    tier: reasoning }
       - { name: luna,   tier: standard }
   ```
4. **Commandes de switch CLI (Lignes 56-67) :**
   - Modifie la section pour documenter formellement que la commande `/model <name>` utilise **exclusivement** les alias génériques (`opus`, `sonnet`, `sol`, `luna`).
   - Interdiction formelle d'inclure des versions (`3.5`, `4.6`, `5`, `o1`, etc.) dans les commandes suggérées.

#### ÉTAPE 3 : Synchronisation dans `modules/plan.md`
- Localise la référence croisée pointant vers `references/environment.md` (lignes 110-118).
- Mets à jour l'ancre et le nom de la section pour refléter le nouveau nom `## Model Tier & Environment Mapping`.
- Assure-toi que les instructions dans `plan.md` imposent le respect strict des alias définis dans cette table.

#### ÉTAPE 4 : Verrouillage strict du template de notification (Code / Prompts)
Définis et implémente dans les fichiers de templates/prompts du skill un schéma de message immuable.

**Règles strictes de formatage :**
- Aucun numéro de version.
- Le nom du modèle cible et du modèle actuel doivent impérativement être en **gras** (`**nom**`).
- Phrases directes et claires.

**Template obligatoire pour un Upgrade :**
```text
⏸️ Transition recommandée vers un modèle supérieur

Modèle actif : **{current_model}**
Modèle requis : **{target_model}**

Choix disponibles :
- Tape `/model {target_model}` puis `continue` pour basculer sur le modèle recommandé
- Tape `bypass` pour forcer l'exécution sur **{current_model}** (possible dégradation de l'efficacité)
```

**Template obligatoire pour un Downgrade :**
```text
⏸️ Retour recommandé vers un modèle standard

Modèle actif : **{current_model}**
Modèle requis : **{target_model}**

Choix disponibles :
- Tape `/model {target_model}` puis `continue` pour optimiser vos coûts/performances (recommandé)
- Tape `bypass` pour rester sur **{current_model}**
```

---

### CONTRAINTES DE VALIDATION
1. Montre les `diff` précis pour chaque fichier modifié (`references/environment.md`, `modules/plan.md`, et tout fichier de code/prompt impacté).
2. Vérifie qu'aucun fichier ne contient de résidu de chaîne en dur comme `claude-opus-5` ou `Sonnet 4.6`.
3. Si une meilleure alternative d'implémentation existe pour éviter que le modèle LLM sous-jacent ne dévie du template (ex: guardrail par regex ou choix interactif CLI natif), propose-la à la fin en justification technique concise.