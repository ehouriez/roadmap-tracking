# Fichier roadmap.md

`./doc/roadmap/roadmap.md` liste tous les plans (numéro, titre, statut,
priorité, description, issue liée).

## Quand le mettre à jour

- Création d'un nouveau plan.
- Changement de statut d'un plan.
- Modification significative d'un plan.
- Clôture d'un plan (déplacement vers `done/` + mise à jour du lien vers `done/NNN-slug.md`).
- Archivage (déplacer le fichier dans `archived/` + mettre à jour le statut).

## Vocabulaire de statut

### Valeurs canoniques (enum)

| Statut | Icône | Usage |
|---|---|---|
| `active` | 🟢 | En cours de travail |
| `blocked` | 🔴 | Bloqué (dépendance / décision en attente) |
| `done` | 🔵 | Terminé et validé |
| `archived` | ⚪ | Archivé (dans `archived/`) |

Ces quatre valeurs sont les **seules valeurs canoniques** du champ `status` dans le front matter d'un plan.

### Mapping des valeurs hors-enum

Certains plans antérieurs à cette convention peuvent contenir des statuts non canoniques. Le skill les mappe automatiquement :

| Valeur rencontrée | Valeur canonique | Motif |
|---|---|---|
| `in-progress` | `active` | Variante historique |
| `cancelled` | `archived` | Variante historique |

> ⛔ **Garde de validation** — Lors de toute lecture ou écriture d'un champ
> `status` de plan (front matter, listing, clôture, mise à jour), vérifier que
> la valeur ∈ `{active, blocked, done, archived}`. Si la valeur figure dans le
> tableau de mapping ci-dessus, l'appliquer silencieusement et notifier via
> le tableau de correction proactive (voir SKILL.md §
> « Correction proactive des incohérences de plan »). Si la valeur est hors-enum
> ET hors-mapping, signaler et ne pas créer/mettre à jour le plan sans correction.

## Sous-répertoire `done/`

Les plans clôturés (`status: done`) sont stockés dans `./doc/roadmap/done/`.
Les liens dans la section « Fait » de `roadmap.md` pointent vers `done/NNN-slug.md`
(chemin relatif depuis `doc/roadmap/`).

Les plans archivés (`status: archived`) restent dans `archived/` — concept distinct.

## Tri de la section « À faire »

Par priorité : `critical` → `high` → `medium` → `low`. À priorité égale, par
numéro de plan croissant.

## Structure

```markdown
# Roadmap [NOM DU PROJET]

> Backlog actif. L'historique détaillé est archivé dans `archived/`.
> Dernière mise à jour : YYYY-MM-DD.

## Contexte

Backlog consolidé : plans nommés d'après leur issue GitHub (voir `doc/roadmap/`).
- « À faire » : travaux restants, triés par priorité.
- « Fait » : ce qui a été livré et validé.

---

## À faire

### [Issue: #27] Titre du plan [PRIORITÉ: HAUTE] [Complexité: M] 🟢

Plan : [`27-nom-du-plan.md`](27-nom-du-plan.md)

Description succincte de ce qui reste à faire.

---

### [Plan: 5] Titre du plan [PRIORITÉ: MOYENNE] [Complexité: S] 🟢

Plan : [`5-nom-du-plan.md`](5-nom-du-plan.md)

> Utiliser `[Plan: {id}]` en mode `local` (pas d'issue GitHub) au lieu de
> `[Issue: #NN]`. L'en-tête reste identique sinon.

Description succincte de ce qui reste à faire.

---

### [Issue: #34] Titre du plan [PRIORITÉ: MOYENNE] [Complexité: S] 🔴

Plan : [`34-nom-du-plan.md`](34-nom-du-plan.md)

Description succincte. **Bloqué par** : [raison].

---

## Fait

### Plans livrés (YYYY-MM-DD → YYYY-MM-DD)

- **[Issue: #8] `#8` — Titre** (YYYY-MM-DD) 🔵 — Ce qui a été livré.
  [`8-nom-du-plan.md`](done/8-nom-du-plan.md)

---

## Archivé

- ⚪ `#12` — Titre — Archivé le YYYY-MM-DD — Raison.
  [`archived/12-nom-du-plan.md`](archived/12-nom-du-plan.md)
```

> Le `#` reste réservé au **texte** (`#27`) ; les cibles de liens et les noms de
> fichiers n'utilisent que le numéro nu (`27-nom-du-plan.md`).
