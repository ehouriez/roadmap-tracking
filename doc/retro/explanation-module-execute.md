# Explication — module-execute

> Voir aussi : [Référence module-execute](reference-module-execute.md)

---

## Pourquoi Phase 5 est strictement limitée

La Phase 5 ne crée que le fichier plan, l'issue et `roadmap.md`. Pourquoi ne pas commencer à lire le code ou analyser les dépendances à ce stade ?

Quand le modèle commence à analyser le code pendant la création du plan, il "pré-implémente" mentalement et franchit le `⏸️` STOP 2 sans attendre la validation. L'interdiction stricte de lire du code applicatif en Phase 5 garantit que le STOP est un vrai arrêt.

---

## Pourquoi la zero-lookup rule pour les prérequis de tests

Les procédures de test écrites sans chemins absolus, variables d'environnement et commandes de setup se retrouvent inutilisables à la reprise (session suivante, autre environnement). L'"épingle" au moment de l'écriture résout ces prérequis une fois pour toutes, rendant la procédure autonome.

---

## Pourquoi le "2 strikes" plutôt qu'un budget tokens

L'audit §6.3.3 avait proposé une règle basée sur le budget tokens. Problème : le modèle n'a pas accès aux données de coût/tokens sans intégration Langfuse ou visibility sur l'API `usage`. Le proxy comportemental "2 ❌ consécutifs sur le même bloc en sessions distinctes" est observable directement depuis le fichier plan — pas de dépendance externe.

---

## Pourquoi le mode one-shot (⚡) garde 🧪 et ✅

Le one-shot supprime la friction des `⏸️` intermédiaires pour les utilisateurs qui ne veulent pas valider étape par étape. Mais les tests finals sont une garantie de qualité non négociable — supprimer les `⏸️` intermédiaires est une accélération valide ; supprimer les tests finaux est une régression.

---

## Pourquoi tests.mode est persisté dans .skill-config.yml

La question "l'environnement de test est-il accessible ?" est une propriété du projet, pas de la session. La persister évite de la reposer à chaque conversation, et garantit que la réponse est cohérente entre toutes les sessions sur le même projet.

---

## Pourquoi la gate modèle de Phase 7 couvre la séquence entière

Évaluer la gate par étape créerait une "gate fatigue" : l'utilisateur verrait la recommandation de modèle répétée pour chaque étape complexe. Une seule évaluation en début de Phase 7, sur le tier le plus élevé requis parmi toutes les étapes, couvre l'ensemble sans redondance.
