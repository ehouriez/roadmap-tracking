## Objectif

Ajouter une **nouvelle étape d'implémentation** dans le plan
`@000-roadmap-tracking-agnostic-autonomy-plugin.md` : une suite de tests
end-to-end du skill `/roadmap-tracking` installé depuis le dépôt public
GitHub `https://github.com/ehouriez/roadmap-tracking`, simulant une
**installation fraîche dans Claude Code**.

## Contexte

Le skill est désormais publié. Il faut valider que l'expérience
d'installation et d'utilisation fonctionne de bout en bout pour un
utilisateur qui découvre le skill — sans configuration préalable, sans
fichiers existants, sans historique.

## Spécifications de la nouvelle étape

### Environnement de test

- **Racine** : `/tmp/roadmap-tracking/tests/`
- **Projets fictifs** : créer un jeu de projets de référence couvrant les
  cas d'usage du skill. Chaque projet est un dossier autonome sous la
  racine, initialisé comme un repo Git local.

Exemples de projets fictifs (à compléter selon ta couverture) :

| Projet fictif | Simule | Particularités |
|---|---|---|
| `project-github-private` | Projet privé GitHub avec issues | Remote GitHub, `gh` authentifié |
| `project-github-optout` | Projet GitHub mais opt-out issues | Remote GitHub, mode issues désactivé |
| `project-no-github` | Projet hors GitHub | Pas de remote GitHub, numérotation locale |
| `project-existing-plans` | Projet avec plans existants | Plans pré-créés dans `doc/roadmap/` |
| `project-fresh` | Projet vierge, aucun historique | Rien dans `doc/roadmap/` |

### Ce que les tests doivent couvrir

Pour chaque projet fictif pertinent, tester **au minimum** :

1. **Installation du skill** depuis le repo public
   (vérifier que le skill est chargé et fonctionnel)
2. **Détection d'environnement** : IDE, modèle actif, mode issues, mode
   tests — selon la config (ou absence de config) du projet fictif
3. **Premier lancement** : règle de démarrage, listing des plans, détection
   `.skill-config.yml`
4. **Création d'un plan** : phases 1→6 (analyse, cadrage, proposition,
   validation, création du plan/issue/roadmap)
5. **Reprise d'un plan existant** : résumé, point d'arrêt, choix
6. **Gate de complexité** : suggestion de modèle adaptée au contexte
7. **Mode issues GitHub vs local** : numérotation, front matter, roadmap.md
8. **Mode tests manuel vs autonome** (si testable dans l'environnement)
9. **Fichiers générés** : vérifier structure, front matter YAML, contenu
   du plan, roadmap.md, cohérence des liens

### Exigences techniques

- **Rejouabilité** : tous les tests doivent pouvoir être relancés à la
  demande. Prévoir un mécanisme de setup/teardown qui recrée les projets
  fictifs de référence à l'identique avant chaque exécution.
- **Autonomie** : tu exécutes toi-même les tests (mode autonome). Pas de
  procédure manuelle à transmettre à l'opérateur.
- **Idempotence** : relancer les tests N fois donne les mêmes résultats
  (pas d'effets de bord cumulatifs).

### Format de reporting

Après chaque test, afficher :

```
### Test X.Y — Nom du test
**Projet** : project-xxx
**Attendu** :
> Description de ce qui doit se produire

**Résultat** :
> Description de ce qui s'est produit

**Verdict** : ✅ PASS | ❌ FAIL | ⚠️ PARTIAL
**Détail** (si FAIL/PARTIAL) : explication de l'écart
```

En fin d'exécution, afficher un **tableau récapitulatif** :

```
### 📊 Récapitulatif des tests

| # | Test | Projet | Attendu (résumé) | Résultat (résumé) | Verdict |
|---|------|--------|-------------------|--------------------|---------| 
| 1.1 | Installation skill | project-fresh | Skill chargé | Skill chargé | ✅ |
| 1.2 | Détection env | project-fresh | IDE=claude-code | IDE=claude-code | ✅ |
| 2.1 | Création plan sans GitHub | project-no-github | Plan local #1 | Plan local #1 | ✅ |
| ... | ... | ... | ... | ... | ... |

**Total** : XX/YY tests passés (ZZ% de couverture)
**Échecs** : [liste des tests en échec si applicable]
```

## Contraintes

- **Écrire la nouvelle étape dans le plan** avant de l'exécuter — le plan
  reste la source de vérité documentaire.
- **Ne pas modifier les étapes existantes** du plan sauf si la nouvelle
  étape crée une dépendance (auquel cas, documenter).
- **Nettoyer `/tmp/roadmap-tracking/tests/`** en début de chaque run
  (teardown + setup propre).
- **Ne pas toucher au code du skill** dans cette étape — c'est un test
  black-box de l'existant. Si un test échoue, le documenter comme écart,
  ne pas corriger.

## Livrable

1. La nouvelle étape ajoutée dans le plan (description, procédure, tests
   de référence)
2. L'exécution complète des tests avec reporting détaillé + tableau
   récapitulatif