# Explication — skill-core

> Voir aussi : [Référence skill-core](reference-skill-core.md)

---

## Le problème que résout le workflow

Implémenter avant de planifier est le schéma d'échec le plus courant en développement assisté par IA : le modèle se lance dans le code, découvre des ambiguïtés à mi-parcours, produit quelque chose de partiellement juste, et l'utilisateur débogue un changement dont les objectifs n'avaient pas été clarifiés. Le skill roadmap-tracking impose un **point de non-retour entre la planification et l'exécution** : rien n'est écrit avant que le plan soit explicitement validé.

---

## Architecture en phases et ses raisons

```
Tour 1 de session
  │
  ├─ 1. Analyse silencieuse (complexité, périmètre, dépendances)
  ├─ 1.5 Gate modèle → ⏸️ si mismatch
  │    ↓ modules/init-scan.md
  │
  ├─ 2. Cadrage interactif (grilling frontier illimitée)
  ├─ 3. Proposition verbale du plan    ← rien n'est écrit
  │      ⏸️ STOP 1
  ├─ 4. Validation de la proposition
  │      ⏸️ ExitPlanMode
  │    ↓ modules/plan.md
  │
  ├─ 5. Création plan file + issue + roadmap.md
  │      ⏸️ STOP 2
  ├─ 6. Validation avant impl. (L/XL uniquement)
  │      ⏸️
  ├─ 7. Implémentation étape par étape + 🧪 Tests + ✅ Validation
  │    ↓ modules/execute.md
  │
  └─ Clôture ← modules/wrapup.md
```

Les `⏸️` sont des verrous d'alignement, pas de la friction : ils garantissent que l'utilisateur et le modèle ont la même image du travail avant le premier commit.

---

## Pourquoi le chargement conditionnel des modules

Un skill monolithique chargé en totalité représentait un coût fixe de ~50–70 K tokens mesuré sur un portfolio réel de 285 plans (plan #17, audit §4.3). La scission en 4 modules chargés selon la phase réduit ce coût à ~15 K tokens au démarrage.

Trade-off : la lisibilité transversale est sacrifiée — les modules se référencent mutuellement. L'invariant tenu : jamais plus d'un module simultanément, sauf Phase 1 (init-scan + plan ensemble pour la gate modèle).

---

## Pourquoi la séparation création/implémentation est une règle absolue

La tentation de créer le plan ET d'enchaîner l'implémentation dans la même réponse est forte : le modèle connaît déjà le contenu du plan, pourquoi s'arrêter ?

La raison est comportementale : le `⏸️` STOP 2 entre Phase 5 et Phase 7 est le seul moment où l'utilisateur peut recalibrer les priorités, ajuster le périmètre, ou décider de ne pas implémenter maintenant. Supprimer ce point revient à retirer à l'utilisateur son seul moment d'inflexion naturel.

---

## Pourquoi le plan file est la source de vérité des tests

Une session IA se réinitialise à chaque conversation. Sans trace persistante, les résultats de tests d'une session précédente sont invisibles à la suivante — ouvrant la voie à des régressions silencieuses ou à des escalades manquées ("2 strikes" entre sessions).

En écrivant la procédure et les résultats dans `## Tests` du plan, on crée une mémoire inter-sessions indépendante du contexte de la conversation.

---

## Pourquoi le CONTEXT.md est borné à 200 lignes / 15 Ko

Un `CONTEXT.md` non borné grossit session après session, et son coût de relecture — payé à chaque démarrage — devient le goulet d'étranglement. Le budget de 200 lignes / 15 Ko avec basculement automatique vers `context/<thème>.md` permet de ne charger que ce qui est pertinent à la tâche en cours.

---

## Pourquoi l'auto-calibrage

Le workflow complet a du sens pour un plan L/XL complexe. Pour un bugfix XS ou une feature S en solo, il représente une friction disproportionnée. La matrice `complexité × collaborative` dérive automatiquement le mode adapté — restant overridable à tout moment via verbal trigger ou `.skill-config.yml`.
