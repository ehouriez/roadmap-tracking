# Explication — tests-e2e

> Voir aussi : [Référence tests-e2e](reference-tests-e2e.md)

---

## La nature particulière du "code" à tester

Le skill roadmap-tracking est un fichier Markdown avec des instructions comportementales. Ses "tests unitaires" sont des tests comportementaux : est-ce que le modèle suit les instructions dans des scénarios variés ? Les fixtures e2e matérialisent ces scénarios en projets git réels sur lesquels le modèle peut être évalué.

---

## Pourquoi 6 fixtures et pas une seule

Les 6 scénarios couvrent les dimensions orthogonales du comportement attendu :

```
GitHub présent/absent   × Plans existants/inexistants
× Plans conformes/non-conformes × doc/roadmap/ présent/absent
```

Un seul fixture "canonique" laisserait les cas dégradés non testés — et c'est précisément sur les cas dégradés (plan sans front matter, projet sans GitHub) que le skill régresse le plus souvent.

---

## Pourquoi la simulation GitHub sans appel API

Les tests e2e exécutés en CI ne doivent pas dépendre de la disponibilité d'une API externe ni de credentials. La simulation via remote `https://github.com/...` trompe la détection de mode du skill (qui vérifie la présence d'un remote GitHub) sans déclencher d'appel réseau.

Trade-off : les tests ne couvrent pas les erreurs d'API GitHub (rate limiting, authentification expirée). Ces cas restent testés uniquement manuellement.

---

## Pourquoi le teardown rm -rf

L'idempotence des tests e2e est critique : un test qui échoue partiellement ne doit pas laisser un état corrompu qui ferait échouer le test suivant. `rm -rf TEST_ROOT` avant chaque run garantit un état vierge. L'alternative (détection d'état existant + correctif) est beaucoup plus fragile.

---

## Pourquoi le plan test.md est à la racine du repo fixture

`tests/my-project--s-solo/test.md` représente un plan en cours (non encore dans `doc/roadmap/`), simulant l'état "avant" que le skill ne crée le fichier plan dans le sous-répertoire correct. C'est une entrée de test, pas un plan géré par le skill — d'où sa position hors de `doc/roadmap/`.
