# Module : Clôture & reprise

> **Chargé lors de la reprise d'un plan existant ou de la clôture d'un plan.**
> Contient le workflow de reprise (avec gate modèle sur reprise) et la
> checklist de clôture référencée par la Phase 7 (`modules/execute.md`).

---

# Workflow : reprise d'un plan existant

> ⚠️ **Même si le prompt de l'utilisateur demande explicitement de « démarrer »,
> « implémenter » ou « tout lancer », ce workflow s'applique intégralement.**
> Un prompt d'action directe (« Démarre les étapes de #109 ») n'est PAS un
> raccourci : il signifie « je veux travailler sur ce plan », pas « saute tous
> les checkpoints ». Voir la **règle anti-court-circuit** dans la garde d'entrée.

> **Plan non conforme (branche dédiée — jamais de reprise silencieuse).** Avant
> d'afficher le résumé, vérifier que le plan respecte `references/templates.md`
> (front matter présent et exploitable : `plan.id`, `status`, `complexity` ;
> structure d'étapes reconnaissable). **Si le plan est malformé** (pas de front
> matter, front matter partiel, ou étapes non standard), ne pas reprendre en
> aveugle : présenter le constat puis proposer explicitement, via l'action
> « poser une question » (`AskUserQuestion` — voir `references/environment.md §
> Generic Action Mapping`), **3 options** :
>
> | Choix | Action |
> |---|---|
> | **Mettre en conformité** | Compléter le plan selon `references/templates.md` (Option 1 : dériver les champs calculables, demander à l'utilisateur les champs de jugement — `description`, `priority`, `complexity`), puis reprendre normalement. |
> | **Mode dégradé** | Reprendre malgré tout, en documentant explicitement les limites (progression/tags/gate non fiables si absents). Aucune donnée n'est inventée : les champs manquants restent `⚠️`. |
> | **Annuler** | Ne pas reprendre ce plan ; laisser l'utilisateur choisir un autre plan ou en créer un. |
>
> Ne jamais afficher un résumé « propre » avec des valeurs inventées à partir
> d'un plan malformé. Le choix « Mode dégradé » est le seul qui reprend un plan
> non conforme, et il est **explicitement documenté** à l'utilisateur.

1. 🧠 MODE PLAN — lis le fichier plan, affiche l'état. Reprendre les tags
   `(taille · modèle)` déjà présents dans le plan pour les étapes restantes :

```
### 📋 Résumé du plan #{ISSUE}
**Statut** : 🟢 active | **complexité** : {taille} · {tier} → {modèle} | **Dernière session** : YYYY-MM-DD | **Progression** : 3/7
**Étapes restantes** : 4. [ ] Migrer le schéma (L · reasoning → Opus)  5. [ ] … (M · standard → Sonnet)

---
⏸️ Que souhaites-tu faire ?
1. 🚀 Continuer l'implémentation — reprendre à l'étape 4
2. ⚡ Continuer l'implémentation — reprendre à l'étape 4, puis enchaîner toutes les étapes suivantes en one-shot
3. 🔍 Clarifier / recadrer
4. 📝 Modifier le plan
5. 📋 Voir le journal

---

💾 Tout le contexte du plan courant est sauvegardé dans {INTRO_FICHIERS} :
- `{PLAN_COURANT}` (plan courant)
{PLANS_LIES}
ℹ️ Tu peux exécuter `/clear`, puis coller le message ci-dessous dans la nouvelle
   conversation pour repartir sur une session neuve — rien ne sera perdu.

> Reprends le plan `{PLAN_COURANT}`.
```

> **Gate modèle sur reprise.** Si le modèle actif est détectable et son tier
> ne correspond pas aux **étapes restantes** (ex. étape `L`/`XL` restante alors
> que le tier actif est `standard`, ou l'inverse), afficher la gate de
> recommandation (voir « Évaluation de complexité et recommandation de modèle »
> dans `modules/plan.md`)
> avant le point d'arrêt. Si le plan est antérieur à cette convention et ne
> porte pas de tags, ne pas afficher de gate par étape. Rejouer aussi la gate
> si le modèle actif a changé depuis la dernière évaluation (voir « Re-jeu de la
> gate sur changement de modèle »).

> **Vérification "2 strikes" sur reprise.** Après la gate modèle et avant
> d'afficher le point d'arrêt de reprise, inspecter le tableau « Résultats
> joués et vérifiés » de la section `## Tests` du plan. Si la règle
> "2 strikes" est déclenchée (≥ 2 ❌ consécutifs sur le même bloc, modèle
> actif = tier `standard`), afficher la recommandation d'escalade (voir
> « Règle d'escalade "2 strikes" » dans `modules/execute.md`) **avant** le
> `⏸️` de reprise. L'opérateur voit la recommandation dans le même résumé
> que l'état du plan — pas de tour supplémentaire. Vérifier aussi les
> critères d'escalade immédiate si un seul ❌ est présent.

2. **STOP.** Attendre la validation. Ne rien implémenter, ne lire aucun code
   source applicatif, ne lancer aucune commande tant que l'utilisateur n'a pas
   choisi une option.

3. Si option 2 → phase de clarification (format `references/forms.md`) ciblée sur
   les étapes restantes.

4. **Transition vers Phase 7** — Si l'utilisateur choisit d'implémenter
   (option 1) :
   - **Mode `manual`** (défaut) : basculer en Phase 7 **en commençant
     impérativement par l'étape 0** (sélection des tests intermédiaires via
     `AskUserQuestion`). Ne JAMAIS sauter l'étape 0, même si l'utilisateur a
     dit « démarre tout » dans son prompt initial ou dans sa réponse au point
     d'arrêt.
   - **Mode `autonomous`** : l'étape 0 est supprimée — basculer directement
     à l'étape 1 de la Phase 7. La boucle Exécuteur/Vérificateur prend le
     relais (voir `references/autonomous-tests.md`).

5. 🔨 MODE ACT — exécuter étape par étape, puis dérouler **obligatoirement** les
   étapes `🧪 Tests` et `✅ Validation` (voir Phase 7) avant de clôturer, et
   mettre à jour journal, issue et `roadmap.md`.

> Si un plan repris ne contient pas encore les étapes `🧪 Tests` / `✅ Validation`
> (plan antérieur à cette convention), **les ajouter** comme deux dernières
> étapes avant de poursuivre.

> Si un plan repris ne contient pas encore de section `## Tests` (plan antérieur
> à cette convention), **la créer à la volée** — vide — dès la première étape de
> tests jouée (voir `references/templates.md` pour sa structure), puis y
> consigner procédure, résultats attendus et résultats vérifiés comme l'exige la
> règle « ⛔ traçabilité des tests dans le fichier plan ». Ne pas éditer
> rétroactivement les plans déjà `done` : la section n'est créée que sur un plan
> effectivement repris et travaillé.

---

## Clôture d'un plan validé

> **Clôture d'un plan validé — checklist COMPLÈTE (ne rien omettre).** Dès que
> toutes les étapes sont livrées **et** validées, la clôture consiste à mettre à
> jour **les quatre supports** de suivi, dans cet ordre :
>
> 1. **Fichier de plan** : passer le front matter à `status: done`, cocher la
>    dernière étape et consigner la validation dans le journal de session.
>    **Remettre `intent: null`** si le champ `intent` est présent dans le front
>    matter (Axe B — reset automatique à la clôture). Mettre à jour `plan.link`
>    pour refléter le nouveau chemin dans `done/` *(mode `github` : URL GitHub
>    vers `doc/roadmap/done/NNN-slug.md` ; mode `local` : chemin relatif
>    `doc/roadmap/done/NNN-slug.md`)*.
> 2. **Déplacement vers `done/`** : déplacer le fichier plan dans
>    `doc/roadmap/done/` via `git mv` (créer le répertoire si absent) :
>    ```bash
>    mkdir -p ./doc/roadmap/done
>    git mv ./doc/roadmap/{NNN}-slug.md ./doc/roadmap/done/{NNN}-slug.md
>    ```
> 3. **`roadmap.md`** : déplacer l'entrée de la section « À faire » vers
>    **« Fait »** (statut `done` 🔵) et mettre à jour le lien vers
>    `done/{NNN}-slug.md` (voir `references/roadmap-file.md`).
> 4. **Issue GitHub rattachée** *(mode `github` uniquement)* : la **fermer**
>    (`gh issue close <issue.id>`), idéalement précédée d'un commentaire de
>    clôture récapitulant ce qui a été livré et validé (`gh issue comment
>    <issue.id> --body "…"`). Voir `references/github-issues.md`. Si le plan n'a
>    pas d'issue rattachée (`issue.id` absent / fallback `draft-`), sauter et
>    signaler.
>    **Mode `local`** : cette étape n'existe pas — `status: done` + déplacement
>    + `roadmap.md` suffisent. Le signaler explicitement à l'utilisateur.
>
> Ces quatre actions vont **ensemble** en mode `github` : `status: done` dans le
> plan implique un déplacement dans `done/`, une entrée en « Fait » **et** une
> issue fermée. Ne jamais laisser une issue ouverte alors que son plan est `done`.
>
> **Ne jamais** déplacer un plan validé vers `_archives/roadmap_done.md` : ce
> fichier est un historique figé qui n'est plus utilisé. L'archivage physique
> dans `_archives/` (statut `archived` ⚪) est une opération distincte et rare
> (voir `references/roadmap-file.md`), pas la clôture normale d'un plan.

