# Explication — openspec-integration

> Voir aussi : [Référence openspec-integration](reference-openspec-integration.md)

---

## Le rôle dans le projet

Le projet roadmap-tracking utilise lui-même les skills openspec pour ses propres évolutions structurées. Les 6 skills dans `.claude/skills/openspec-*/` sont les outils de planification de l'équipe de développement du skill — pas des artefacts du skill lui-même.

---

## Pourquoi les specs restent en delta jusqu'au sync

Modifier les specs principales directement à chaque feature rendrait le diff des specs illisible et mélangerait les concerns de plusieurs changes simultanés. Les delta-specs isolent les exigences de chaque change dans son propre répertoire jusqu'au moment de la fusion (sync), préservant une traçabilité propre.

---

## Pourquoi archive est synchrone avec sync

Le workflow intuitif serait d'archiver puis de syncer en arrière-plan. Mais une fois le `changeRoot` déplacé en archive, la référence au change est perdue. Si le sync échoue ou est ignoré, les specs principales restent désynchronisées sans que personne ne le sache. Forcer le sync synchroniquement avant le déplacement garantit la cohérence : pas d'archive sans sync réussi.

---

## Pourquoi allowed-tools restreint à openspec:*

Les skills openspec touchent des fichiers de spécification et de planification. Les restreindre à `Bash(openspec:*)` empêche les dérives — exécution de commandes arbitraires depuis un skill de planification. Principe de moindre privilège appliqué au niveau du skill.

---

## Pourquoi les skills sont générés par le CLI

La cohérence entre les skills (sélection de store, gestion de `context`/`operationGuidance`, sécurité des chemins) est difficile à maintenir à la main sur 6 fichiers. La génération depuis le CLI `openspec` garantit que tous les skills partagent les mêmes patterns et bénéficient automatiquement des mises à jour du CLI.
