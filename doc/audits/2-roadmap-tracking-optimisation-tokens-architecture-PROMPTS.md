# Implémentation 2-roadmap-tracking-optimisation-tokens-architecture.md

## 📌 Stratégie d'exécution recommandée

- L'ordre chronologique doit être respecté : P1 doit impérativement être exécuté et validé en premier, car P2 (compression du noyau) et P3 (règles de tours dans les modules) dépendent directement de la nouvelle arborescence créée par P1.
- Le prompt doit pointer explicitement vers le document d'audit de référence (doc/audits/2-roadmap-tracking-optimisation-tokens-architecture.md) présent sur le disque, qui contient déjà l'intégralité des spécifications techniques, contrats d'interface et analyses de risque.

Ci-dessous les 3 prompts complets, auto-suffisants (« zero-shot context ») et prêts à l'emploi.

## 🥇 Prompt pour P1 — Scission modulaire (L1)

> Modèle recommandé dans le menu : Claude Opus 4.6 (Thinking) (ou Claude Sonnet 4.6 (Thinking))

### Pourquoi Claude Opus 4.6 (Thinking) ?

- La scission modulaire est une tâche d'architecture système one-shot. L'échec précédent du patch P1 a prouvé que des règles implicites ou des garde-fous disparaissent facilement si le modèle n'a pas une vision globale et profonde des interactions entre phases.
- Opus 4.6 dispose de la profondeur de raisonnement nécessaire pour isoler proprement le noyau minimal (~3 500 tokens) et distribuer les ~12 000 tokens restants dans les 5 sous-fichiers sans introduire de rupture de contrat ni d'incohérence de nommage.
- Investissement rentable : C'est une opération que l'on ne fait qu'une seule fois.

```xml
<role>
Tu es un Architecte IA Senior et Expert en Prompt Engineering. Tu interviens sur le repository local pour exécuter le chantier prioritaire P1 d'optimisation de la skill `roadmap-tracking`.
</role>
<mission>
Implémenter la scission modulaire (Levier L1) de la skill `roadmap-tracking` conformément à l'audit architectural validé.
Objectif : Transformer le fichier monolithique `SKILL.md` en une architecture noyau + 5 modules à chargement différé, sans perdre aucun invariant fonctionnel ni dégrader la qualité opérationnelle (tolérance zéro régression).
</mission>
<reference_spec>
Lis attentivement et applique STRICTEMENT les spécifications du document :
`doc/audits/2-roadmap-tracking-optimisation-tokens-architecture.md`
En particulier :
- Section « B. Levier 1 — Architecture modulaire à chargement différé » (découpage cible, inventaire des 5 modules, règles de routage)
- Section « A. Post-mortem analytique du rollback P1 » (erreurs à ne pas reproduire : ne pas supprimer de garde-fous sémantiques)
- Section « C. Synthèse des gains et roadmap d'implémentation »
</reference_spec>
<instructions_executoires>
1. Crée le répertoire `modules/` à la racine de la skill.
2. Extrais et crée les 5 modules autonomes en Markdown :
   - `modules/init-scan.md` (Phases 1 & 2 : scan, indexation, initialisation)
   - `modules/plan.md` (Phase 3 : rédaction de plans, validation, dimensionnement)
   - `modules/execute.md` (Phase 4 : boucle d'exécution, gates de sécurité, step tracking)
   - `modules/wrapup.md` (Phases 5 & 6 : revue, complétion, roadmap update)
   - `modules/templates.md` (Format de plan, conventions, tableaux de métriques)
3. Réfracte le fichier `SKILL.md` pour n'en faire que le **noyau d'aiguillage** (~3 500 tokens) contenant :
   - Le frontmatter YAML
   - La vision, principes directeurs et règles universelles
   - La table de routage / index des modules
   - La directive de chargement conditionnel (lecture du module correspondant à la phase active via l'outil de lecture de fichier)
4. Assure la parfaite continuité des références de fichiers, balises de décision et règles de sécurité.
5. Vérifie le travail :
   - Décompte des mots/lignes avant vs après (SKILL.md noyau vs modules)
   - Vérification qu'aucune directive critique n'a été tronquée ou omise
   - Rapport clair des modifications apportées
</instructions_executoires>
```

---

## 🥈 Prompt pour P2 — Compression sémantique du noyau (L3)

> Modèle recommandé dans le menu : Claude Sonnet 4.6 (Thinking)

### Pourquoi Claude Sonnet 4.6 (Thinking) ?

- Une fois le noyau isolé, il s'agit d'une tâche de micro-chirurgie textuelle (suppression du passif, densification des listes, tables compactes).
- Sonnet 4.6 avec le mode Thinking actif est parfait ici : il réfléchit explicitement à la portée sémantique de chaque suppression avant d'éditer, évitant de supprimer par erreur un garde-fou opérationnel.
- Opus n'est pas nécessaire pour ce volume réduit (~3 500 tokens) et Flash risquerait de tronquer trop agressivement.

```xml
<role>
Tu es un Expert Senior en Prompt Engineering et Densification Textuelle. Tu interviens sur le repository local pour exécuter le chantier P2 d'optimisation de la skill `roadmap-tracking`.
</role>

<contexte>
Le chantier P1 (scission de `SKILL.md` en un noyau + 5 modules dans `modules/`) a été complété avec succès. Le fichier `SKILL.md` actuel ne contient désormais que le noyau central d'orchestration.
</contexte>

<mission>
Exécuter la compression sémantique (Levier L3) sur le fichier `SKILL.md` résiduel, sans altérer aucune règle logique, invariant de sécurité ou balise opérationnelle.
</mission>

<reference_spec>
Lis attentivement :
- `doc/audits/2-roadmap-tracking-optimisation-tokens-architecture.md` (Section « B. Levier 3 — Compression sémantique du noyau résiduel » et « A. Post-mortem analytique du rollback P1 »).
- Le fichier `doc/roadmap/12-skill-compression-p1.md` pour comprendre les pièges du rollback passé.
</reference_spec>

<regles_inviolables>
1. Tolérance zéro régression : chaque suppression doit porter sur la forme (verbiage, tournures passives, répétitions phraséologiques) et JAMAIS sur le fond.
2. Ne PAS supprimer de consignes de sécurité, de formats de balises ou de conditions logiques.
3. Remplacer les formulations discursives par des puces denses, des tables compactes ou des syntaxes impératives directes.
</regles_inviolables>

<instructions_executoires>
1. Analyse le contenu actuel de `SKILL.md`.
2. Applique une densification systématique :
   - Élimine le remplissage narratif et les explications pédagogiques redondantes.
   - Condense les règles en syntaxe impérative concise (sujet + verbe d'action + contrainte).
   - Optimise la table de routage des modules.
3. Quantifie précisément l'impact :
   - Nombre de lignes et estimation de tokens avant vs après.
   - Liste des sections condensées avec justification de conservation sémantique.
</instructions_executoires>
```

---

## 🥉 Prompt pour P3 — Élimination des tours inutiles (L2)

> Modèle recommandé dans le menu : Claude Sonnet 4.6 (Thinking) ou Gemini 3.8 Flash

### Pourquoi Claude Sonnet 4.6 (Thinking) ou Gemini 3.8 Flash ?

- Les modifications sont très circonscrites : modifier les conditions de passage de tour dans les directives de execute.md et plan.md pour permettre le fast-path sur les plans simples.
- Claude Sonnet 4.6 offre une garantie absolue de fluidité du protocole.
- Si la consigne est déjà rédigée sous forme de patch précis, Gemini 3.8 Flash (Medium ou High) est parfaitement capable d'exécuter ces modifications ciblées avec une grande rapidité.

```xml
<role>
Tu es un Architecte IA Senior spécialisé dans l'optimisation des flux conversationnels multi-tours et des protocoles d'agents autonomes.
</role>

<contexte>
L'architecture modulaire de `roadmap-tracking` est en place (`SKILL.md` et dossier `modules/`). L'audit architectural a identifié que 15,1 % des tokens consommés proviennent de tours d'API superflus sur les plans de complexité simple (S et M).
</contexte>

<mission>
Implémenter le Levier L2 (Élimination des tours superflus / Fast-path) dans les modules concernés, conformément aux spécifications d'audit.
</mission>

<reference_spec>
Consulte :
- `doc/audits/2-roadmap-tracking-optimisation-tokens-architecture.md` (Section « B. Levier 2 — Élimination des tours superflus » et matrice de complexité XS/S/M/L/XL).
- `modules/plan.md`, `modules/execute.md` et `SKILL.md`.
</reference_spec>

<instructions_executoires>
1. Dans `modules/plan.md` :
   - Introduire la règle de **fast-path pour les plans XS et S** : si un plan ne comporte aucun breaking change ni impact architectural critique, autoriser la présentation du plan et la demande de validation en réduisant les étapes d'itération préliminaires.
2. Dans `modules/execute.md` :
   - Autoriser l'enchaînement fluide des étapes (steps) élémentaires au sein du même tour si elles sont vérifiables de manière déterministe et sans ambiguïté.
   - Conserver impérativement les gates de validation humaine pour les points d'arrêt critiques (breaking changes, actions irréversibles).
3. Ajuster dans `SKILL.md` la règle universelle d'orchestration des tours pour refléter ce fast-path sans ambiguïté.
4. Rédige un compte-rendu démontrant comment le protocole évite les allers-retours vides tout en maintenant les barrières de sécurité.
</instructions_executoires>
```

## 💡 Stratégie d'exécution recommandée

- Lancer P1 avec Claude Opus 4.6 (Thinking) pour créer l'architecture modulaire et valider l'arbre de fichiers.
- Basculer sur Claude Sonnet 4.6 (Thinking) pour compresser le noyau (P2) et injecter les règles de fluidification des tours (P3).