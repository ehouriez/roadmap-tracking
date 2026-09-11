---
plan:
  id: '3'
  name: 3-roadmap-tracking-corrections-findings-e2e.md
  link: https://github.com/ehouriez/roadmap-tracking/blob/main/doc/roadmap/3-roadmap-tracking-corrections-findings-e2e.md
status: active
date: 2026-09-11
description: >
  Corriger les 4 findings relevés par la campagne de tests e2e (plan #2) :
  signalement des plans malformés au listing, branche de reprise dédiée aux
  plans non conformes, réconciliation de la numérotation locale, et couverture
  du chemin github end-to-end.
priority: medium
complexity: M
scope:
  modules:
    - SKILL.md
    - references/templates.md
    - references/roadmap-file.md
issue:
  id: 3
  url: https://github.com/ehouriez/roadmap-tracking/issues/3
---

# [🛠️] Plan #3 - roadmap-tracking : correction des findings e2e

## Objectif

Traiter les 4 écarts documentés par la campagne de tests e2e du plan #2
(issue #2), sans régression du comportement v2.0.0. Chaque finding devient une
étape corrective ciblée.

## Périmètre

### Inclus
- `SKILL.md § Règle de démarrage` : signalement d'anomalie au listing.
- `SKILL.md § Reprise d'un plan existant` : branche « plan malformé ».
- `SKILL.md` Phase 5 mode `local` + `references/templates.md` : réconciliation
  de la numérotation locale avec les `plan.id` déclarés.
- Décision de couverture pour le chemin github end-to-end (finding 4).

### Hors scope
- Refonte du workflow 7 phases.
- Toute modification du mode autonome (non impliqué par les findings).

## Findings à corriger (source : plan #2, issue #2)

| # | Finding | Test d'origine |
|---|---|---|
| F1 | Listing des plans malformés sous-spécifié (pas de colonne d'anomalie / `⚠️`) | 7.1 |
| F2 | Reprise sans branche dédiée aux plans malformés | 7.2a-d |
| F3 | Numérotation locale par préfixe de fichier ignorant les `plan.id` du front matter | 7.3 |
| F4 | Chaîne github end-to-end non éprouvée (simulation zéro-API) | 4.2 |

## Étapes

- [ ] Étape 1 — F1 : ajouter au `§ Règle de démarrage` une consigne de listing
      tolérant — pour un plan sans front matter (ou partiel), afficher `⚠️` /
      valeur par défaut dans les colonnes manquantes du tableau, sans crash, et
      lister quand même le fichier (S · standard → Sonnet)
- [ ] Étape 2 — F2 : ajouter au workflow de reprise une branche « plan
      malformé » — à la lecture d'un plan sans front matter conforme, proposer
      explicitement l'un de : mise en conformité (Option 1 / script), mode
      dégradé documenté, ou refus explicite. Jamais de reprise silencieuse
      (M · standard → Sonnet)
- [ ] Étape 3 — F3 : réconcilier la numérotation locale (Phase 5 mode `local` +
      `templates.md`) — l'ID local doit être `max(préfixes de fichier ∪ plan.id
      déclarés en front matter) + 1` pour éviter la collision logique
      (M · standard → Sonnet)
- [ ] Étape 4 — F4 : trancher la couverture github e2e — soit ajouter un test
      e2e github réel sur repo jetable **opt-in** (hors CI par défaut), soit
      documenter explicitement la limite comme hors-scope dans le plan #2
      (S · standard → Sonnet)
- [ ] 🧪 Tests — Rédiger et exécuter la procédure de test (rejouer les tests e2e
      concernés du plan #2 : 7.1, 7.2a-d, 7.3, et 4.2 si option retenue)
- [ ] ✅ Validation — Vérifier les résultats et clôturer

> Chaque étape d'implémentation porte son tag `(taille · tier → modèle)`. Les
> étapes `🧪 Tests` et `✅ Validation` sont obligatoires et non sizées.

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| Réconciliation d'ID (F3) | `max(préfixes ∪ plan.id) + 1` | Évite la collision logique sans casser la rétrocompat |
| Couverture github (F4) | À trancher en Étape 4 | Éviter les effets de bord sur le compte GitHub réel |

## Journal de session

### Session 2026-09-11 — Création du plan
- ✅ Fait : plan de correction créé à partir des 4 findings du plan #2 (issue #2).
- 📋 Prochain : implémenter l'Étape 1 (F1) après validation du point d'arrêt.
- 🚧 Blocages : aucun.
