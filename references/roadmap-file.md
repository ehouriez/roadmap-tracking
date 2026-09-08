# Fichier roadmap.md

`./doc/roadmap/roadmap.md` liste tous les plans (numéro, titre, statut,
priorité, description, issue liée).

## Quand le mettre à jour

- Création d'un nouveau plan.
- Changement de statut d'un plan.
- Modification significative d'un plan.
- Archivage (déplacer le fichier dans `_archives/` + mettre à jour le statut).

## Icônes de statut

| Statut | Icône | Usage |
|---|---|---|
| `active` | 🟢 | En cours de travail |
| `done` | 🔵 | Terminé et validé |
| `blocked` | 🔴 | Bloqué (dépendance / décision en attente) |
| `archived` | ⚪ | Archivé (dans `_archives/`) |

## Tri de la section « À faire »

Par priorité : `critical` → `high` → `medium` → `low`. À priorité égale, par
numéro de plan croissant.

## Structure

```markdown
# Roadmap [NOM DU PROJET]

> Backlog actif. L'historique détaillé est archivé dans `_archives/`.
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

### [Issue: #34] Titre du plan [PRIORITÉ: MOYENNE] [Complexité: S] 🔴

Plan : [`34-nom-du-plan.md`](34-nom-du-plan.md)

Description succincte. **Bloqué par** : [raison].

---

## Fait

### Plans livrés (YYYY-MM-DD → YYYY-MM-DD)

- **[Issue: #8] `#8` — Titre** (YYYY-MM-DD) 🔵 — Ce qui a été livré.
  [`8-nom-du-plan.md`](8-nom-du-plan.md)

---

## Archivé

- ⚪ `#12` — Titre — Archivé le YYYY-MM-DD — Raison.
  [`_archives/12-nom-du-plan.md`](_archives/12-nom-du-plan.md)
```

> Le `#` reste réservé au **texte** (`#27`) ; les cibles de liens et les noms de
> fichiers n'utilisent que le numéro nu (`27-nom-du-plan.md`).
