# Explication — hooks-system

> Voir aussi : [Référence hooks-system](reference-hooks-system.md)

---

## Le problème : les directives textuelles perdent contre les directives concurrentes

Les directives de style "avant toute implémentation, invoque le skill" perdent systématiquement contre des modes concurrents ("shortest path", "don't stop") ou contre un prompt impératif bien formulé. Les plans #15 et #16 avaient documenté des régressions systématiques.

---

## Pourquoi trois hooks distincts

Chaque hook adresse un vecteur de bypass différent :

| Hook | Vecteur couvert |
|---|---|
| `SessionStart` | Prompt immédiat avant que la directive soit visible |
| `UserPromptSubmit` | Directive "oubliée" au bout de quelques échanges avec des modes de style actifs |
| `PreToolUse` | Bypass au moment exact où l'implémentation commence — observable mécaniquement |

---

## Pourquoi la garde PreToolUse est un script Python

Une directive textuelle dans `PreToolUse` peut être ignorée par un modèle avec des instructions concurrentes. Un script Python qui retourne un JSON de refus est une contrainte hard — le harness l'applique sans que le modèle puisse la contourner textuellement.

---

## Pourquoi deux fichiers JSON (hooks.json / codex-hooks.json)

Claude Code et Codex ont des formats de hook incompatibles et des conventions de découverte différentes. Un fichier unique ne peut pas être valide pour les deux IDEs. La duplication est le prix de la compatibilité multi-IDE depuis un seul package.

---

## Pourquoi hooks.json est en français et codex-hooks.json en anglais

SKILL.md et les interactions utilisateur sont en français. Claude Code (multilingue) traite les hooks en français nativement. Codex (OpenAI) montre une meilleure fiabilité d'instruction-following en anglais sur les messages de système — comportement empirique documenté dans les retours du projet.

---

## Pourquoi le refus à l'outil plutôt qu'à la session

Un refus à l'initialisation de session bloquerait toutes les sessions sur un projet adopté, même celles qui ont déjà invoqué le skill. Le refus à l'outil (premier outil mutant) cible exactement le moment où le bypass se produit, avec granularité suffisante pour s'auto-désarmer après.
