# Gestion des issues GitHub

Chaque plan est rattaché à une issue GitHub, et **le numéro de cette issue est
l'identifiant du plan** (nom de fichier `{ISSUE}-slug.md`). L'issue se crée donc
**avant** le fichier plan. L'intégration est **configurable** : elle utilise
`gh` si disponible, sinon bascule en mode manuel.

## Détection (à faire avant toute action GitHub)

```bash
command -v gh && gh auth status
```

- **`gh` présent et authentifié** → mode automatique (créer/mettre à jour via `gh`).
- **Sinon** → mode manuel : fournir à l'utilisateur le titre, les labels et le
  corps de l'issue à copier-coller, puis **lui demander le numéro d'issue en
  retour** — ce numéro conditionne le nom du fichier plan (`{ISSUE}-slug.md`) et
  son `plan.id`. En attendant, utiliser le fallback `draft-slug.md`.

Ne jamais supposer l'état de l'authentification : le vérifier.

## Récupérer le numéro d'issue (mode automatique)

`gh issue create` renvoie l'URL de l'issue ; en extraire le numéro, ou le
demander explicitement en JSON :

```bash
URL=$(gh issue create --title "Plan — Titre" --label "plan" --body "$BODY")
ISSUE=$(basename "$URL")   # ex. 27
```

## Rattachement d'un plan

- Plan avec **issue déjà rattachée** → mettre à jour cette issue à la fin de
  chaque étape significative.
- Plan **sans issue** → demander avant de commencer :

> Aucune issue GitHub n'est rattachée à ce plan. Souhaites-tu rattacher une
> issue existante (indique `#XX`) ou en créer une nouvelle ?

- **Création d'un nouveau plan** → même vérification : quelle issue rattacher,
  ou en créer une.

## Mode automatique — commandes

Créer une issue (le numéro n'existe qu'après création) :

```bash
gh issue create --title "Titre du plan" --label "plan,priority:high" --body "$BODY"
```

Mettre à jour (commentaire d'avancement) :

```bash
gh issue comment <ID> --body "$BODY"
```

Récupérer `owner/repo` pour renseigner `plan.link` / `issue.url` :

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

## Référencer le plan dans l'issue

L'issue est créée **avant** le fichier plan (son numéro = ID du plan). Dès que
le nom du fichier est décidé, ajouter au **début** du corps de l'issue une ligne
de référence vers le plan :

```
Plan: doc/roadmap/{ISSUE}-slug.md
```

En mode automatique, relire le corps puis le réécrire (préserver l'existant) :

```bash
BODY=$(gh issue view <ID> --json body -q .body)
gh issue edit <ID> --body "Plan: doc/roadmap/<ID>-slug.md

$BODY"
```

En mode manuel : demander à l'utilisateur d'ajouter cette ligne en tête du corps
de l'issue.

## Format de mise à jour d'issue

Inclure au minimum :

- ✅ Tâches complétées durant la session
- 🔄 Tâches en cours
- 📋 Prochaines étapes
- 🚧 Blocages éventuels

Après création/rattachement, renseigner `issue.id` et `issue.url` dans le front
matter du plan et référencer l'issue dans `roadmap.md`.

## Clôture de l'issue (plan `status: done`)

Quand le plan passe à `status: done` (toutes les étapes livrées **et** validées),
**fermer l'issue rattachée** — c'est un des trois supports de la clôture (plan +
`roadmap.md` + issue, voir SKILL.md « Clôture d'un plan validé »).

Commenter (récapitulatif de clôture) puis fermer :

```bash
gh issue comment <ID> --body "$BODY"   # ce qui a été livré + validé (E2E, tests)
gh issue close <ID>
```

Ne jamais laisser une issue ouverte alors que son plan est `done`. Si le plan n'a
pas d'issue (`issue.id` absent / fallback `draft-`), il n'y a rien à fermer — le
signaler.
