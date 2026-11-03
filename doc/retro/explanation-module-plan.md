# Explication — module-plan

> Voir aussi : [Référence module-plan](reference-module-plan.md)

---

## Le problème du cadrage à questions fixes

Les premières versions de Phase 2 posaient une liste prédéfinie de questions. Deux écueils en pratique : soit les questions couvraient des domaines non pertinents pour la demande (bruit), soit elles ne révélaient pas des dépendances cachées qui émergent seulement dans les réponses aux premières questions.

---

## Pourquoi la frontier illimitée

Le plan #24 a introduit la "frontier illimitée". L'idée centrale : une question dont la réponse dépend d'une autre question ouverte n'a pas encore de sens à poser. La frontier recompute après chaque round, émergence par émergence, jusqu'à ce qu'il n'y ait plus rien à clarifier.

Trade-off : le nombre de rounds est théoriquement illimité (d'où la contrainte de chargement conditionnel). En pratique, la frontier vide est atteinte en 2–3 rounds pour la plupart des demandes.

---

## Pourquoi Phase 2 ignore grilling.enabled

`grilling.enabled: false` supprime le grilling en Phases 4 et 6 — pas en Phase 2.

Phases 4 et 6 valident un plan déjà rédigé (grilling sur des risques connus). Phase 2 établit la compréhension de la demande. Sauter Phase 2 revient à rédiger un plan sans avoir compris la demande — c'est le schéma d'échec qu'on cherche à éviter.

---

## Pourquoi la gate modèle est canonical dans plan.md

La gate modèle est évaluée en Phase 1.5 (init-scan), Phase 4 (plan) et Phase 7 (execute). Dupliquer les templates de message dans chaque module créerait de la dérive de formulation entre versions. `plan.md` héberge la section canonique unique, référencée par les autres.

---

## Pourquoi les alias génériques, pas les versions runtime

Un template de gate qui cite `claude-opus-5` sera cassé à la sortie de `claude-opus-6`. Un alias (`opus`) est résolu dynamiquement par le harness et reste valide à travers les versions de modèle.

---

## Pourquoi Phase 3 propose verbalement sans écrire

Avant Phase 3, l'utilisateur n'a pas encore approuvé le plan. Créer le fichier à ce stade forcerait soit une suppression si l'utilisateur rejette, soit une accumulation de fichiers orphelins. La proposition verbale de Phase 3 est un investissement zéro-risk pour les deux parties.

---

## Pourquoi le mode one-shot (⚡) est proposé en Phase 5

Certains utilisateurs font confiance à l'implémentation et ne souhaitent pas valider étape par étape. Le one-shot supprime les `⏸️` intermédiaires mais conserve impérativement `🧪 Tests` et `✅ Validation` — accélération valide, régression de qualité refusée.
