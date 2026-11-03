# Explication — module-wrapup

> Voir aussi : [Référence module-wrapup](reference-module-wrapup.md)

---

## Pourquoi un résumé de reprise avant le STOP

Le `⏸️` de reprise n'est pas de la friction — c'est la lecture du tableau de bord avant de reprendre la route. Sans ce résumé, l'utilisateur ne sait pas où en est le plan, et le modèle risque de repartir dans la mauvaise direction (étape déjà faite, wrong model tier, test déjà en échec).

---

## Pourquoi les 4 supports de clôture sont atomiques

`status: done` dans le front matter implique l'issue fermée et le fichier dans `done/`. Laisser l'un des 4 supports ouverts crée un état incohérent : une issue GitHub ouverte pour un plan done, ou un plan done toujours visible dans le listing actif.

---

## Pourquoi intent: null à la clôture

Le champ `intent` (Axe B) encode si le plan ciblait un prototype ou une production. C'est une métadonnée de workflow, pas une propriété permanente du plan. La resetter à `null` à la clôture évite qu'un intent "prototype" survive et fausse un futur plan qui reprendrait les mêmes fichiers.

---

## Pourquoi plan.link est mis à jour vers done/ à la clôture

Le champ `plan.link` sert de pointeur canonique vers le fichier plan. Après le `git mv` en `done/`, l'ancienne valeur du lien pointe vers un fichier inexistant. Le mettre à jour à la clôture garantit que le lien reste valide et exploitable par les outils (notamment `migrate_plan_ids.py`).

---

## Pourquoi la purge CONTEXT.md est toujours opt-in

Un `CONTEXT.md` accumule des entrées de plusieurs plans. Supprimer une entrée à la clôture d'un plan peut supprimer un piège qui est encore pertinent pour un autre plan actif. La proposition OUI/NON donne à l'utilisateur le contrôle sans automatiser une suppression potentiellement destructive.

---

## Pourquoi archived/ est distinct de done/

`done/` = plans terminés avec succès. `archived/` = plans abandonnés ou annulés. La distinction permet de différencier le succès de l'abandon dans les statistiques et le listing. `archived/roadmap_done.md` est un fichier hérité d'une ancienne convention — il est gelé et ne doit plus recevoir de plans.
