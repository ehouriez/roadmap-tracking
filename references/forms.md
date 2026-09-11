# Formulaire de cadrage interactif (Phase 2)

Le cadrage se fait avec l'outil **`AskUserQuestion`** — des choix cliquables,
pas un formulaire texte où l'utilisateur répond « 1a, 2c, 3ab ».

## Contraintes de l'outil et batching

| Contrainte | Conséquence |
|---|---|
| Max **4 questions** par appel | Découper le cadrage en plusieurs appels successifs |
| Max **4 options** par question | Garder les options les plus pertinentes ; l'option « Autre » est ajoutée nativement |
| Réponses multiples | Mettre `multiSelect: true` (ex. « hors scope explicite ») |
| Champ libre | Inutile de prévoir une option « Autre : ___ » : l'outil la fournit |
| `header` | Label court (≤ 12 caractères), ex. « Périmètre », « Objectifs » |
| Recommandation | Placer l'option recommandée en premier avec « (Recommandé) » |

**Stratégie de découpage** : regroupe par thème, ~3-4 questions par appel.
Un plan simple (XS/S) → **3-4 questions** (1 appel). Un plan complexe (M/L/XL)
→ **5-10 questions** (2-3 appels). N'enchaîne un appel qu'après les réponses du
précédent, pour adapter les questions suivantes aux réponses reçues.

## Avant le premier appel

Affiche ta compréhension en 2-3 phrases :

```
### 🔍 Cadrage du plan (🧠 MODE PLAN — rien n'est encore écrit)

**Ma compréhension** :
> Résumé de ce que j'ai compris de ta demande.

Je vais te poser quelques questions ciblées pour te proposer un plan précis.
```

Puis lance les appels `AskUserQuestion`.

## Matière des questions (guide, pas une limite)

Adapte chaque question à l'analyse du prompt (options concrètes, pré-remplies
avec ta meilleure suggestion — pas des questions ouvertes génériques). Ne pose
que des questions dont la réponse **impacte la structure du plan**. Ne demande
pas ce qui est déjà explicite.

**📐 Périmètre**
- Modules / fichiers concernés ? (proposer les modules détectés)
- Hors scope explicite ? (`multiSelect`)

**🎯 Objectifs et critères de succès**
- Comment sait-on que c'est « terminé » ? (tests passent, feature en UI, déployé staging…)
- Contraintes non fonctionnelles ? (perf, rétro-compat, pas de nouvelle dépendance…)

**🔗 Dépendances et contexte**
- Lien avec un plan existant ? (lequel ?)
- État actuel du code ? (existant à modifier / from scratch / refacto / à analyser)

**⚙️ Choix techniques**
- Approche d'implémentation préférée ? (proposer 2 options concrètes A/B)
- Libs/outils à utiliser ou éviter ?

**📦 Découpage** (obligatoire si complexité pressentie ≥ M)
- Découpage en lots proposé ? (proposer un découpage concret)
- Lot à livrer en priorité ?

**🎨 UX/UI** (si la demande touche à l'interface)
Quand la demande porte sur l'UX/UI et que `impeccable:impeccable` est disponible,
invoque-le d'abord (voir SKILL.md § « Assistance design ») pour formuler des
questions ciblées : hiérarchie visuelle, charge cognitive, états (vide, erreur,
chargement), accessibilité, responsive, cohérence avec le design system existant.
Reste en **référence de réflexion** — ne lance pas son pipeline de production.

**💡 Suggestions et points d'attention** (créativité encouragée)
Ajoute toute question hors catégorie utile : challenge une incohérence ou un
risque technique, propose une alternative, anticipe les cas limites, suggère une
simplification si la demande semble sur-ingénierée. Formule-la comme un choix
(d'accord / pas pertinent / à discuter).

## Après les réponses

Les questions restées sans réponse sont traitées selon ton meilleur jugement.
Enchaîne sur la **Phase 3 — Proposition du plan**.
