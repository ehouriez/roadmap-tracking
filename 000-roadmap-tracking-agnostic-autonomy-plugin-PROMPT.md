## Contexte

Je poursuis la généralisation du skill `/roadmap-tracking` entamée dans cette conversation. Tu as produit un **plan d'architecture** (voir ton précédent message)
pour rendre le skill agnostique IDE + fournisseur de modèles. Ce plan est
**validé** — ne le remettre en question que si un conflit apparaît avec les
nouvelles exigences ci-dessous.

Cette session ajoute **4 axes d'évolution supplémentaires** à intégrer dans
le même chantier.

---

## Nouveaux axes d'évolution

### Axe A — Zéro dépendance aux règles externes

**Problème** : le skill exige aujourd'hui la présence de
`operator-commands-formatting.md` dans `rules/` du dossier personnel
`.claude/`. C'est un prérequis fragile et non portable — un collègue qui
clone le projet et utilise le skill sans avoir cette règle obtient un
comportement dégradé silencieux.

**Exigence** :
- **Aucune règle** présente dans `rules/` (ou équivalent IDE) ne doit être
  un prérequis pour la bonne exécution du skill.
- Embarquer le contenu de `operator-commands-formatting.md` **directement
  dans le skill**, dans `references/` (ex. `references/commands-formatting.md`
  ou intégré dans le futur `references/environment.md` du plan validé —
  à toi de décider le meilleur emplacement).
- Le `## Prerequisites` du SKILL.md doit être réécrit pour pointer vers
  cette référence interne au lieu d'une règle externe.
- Le skill doit être **auto-suffisant** : cloner le dossier
  `skills/roadmap-tracking/` suffit pour l'utiliser, quel que soit l'IDE.

### Axe B — Gestion des issues GitHub optionnelle

**Problème** : le skill suppose aujourd'hui que le projet est sur GitHub et
que l'utilisateur veut créer/gérer des issues. Ce n'est pas toujours le cas.

**Exigence** : supporter 4 modes de gestion des issues, mutuellement
exclusifs :

| Mode | Condition | Comportement |
|---|---|---|
| **a. GitHub privé** | Projet privé hébergé sur GitHub | Fonctionnement actuel (issues automatiques via `gh`) |
| **b. GitHub public** | Projet public hébergé sur GitHub | Fonctionnement actuel (même workflow) |
| **c. Hors GitHub** | Projet non hébergé sur GitHub | Pas d'issues GitHub. Plans uniquement sous `./doc/roadmap/`. Le numéro de plan est auto-incrémenté localement |
| **d. GitHub opt-out** | Projet sur GitHub mais l'utilisateur refuse les issues | Même comportement que (c) : plans locaux uniquement |

**Points de conception à trancher** :

1. **Détection et choix du mode** — Comment l'utilisateur configure-t-il son
   mode ? Propose un mécanisme basé sur :
   - Détection automatique au premier lancement (présence de `.git/`,
     remote GitHub, `gh auth status`) + confirmation utilisateur.
   - Question posée via l'action générique « poser une question »
     (`AskUserQuestion` / TUI / texte selon l'IDE).
   - Persistance du choix dans `.skill-config.yml` (le fichier de config
     optionnel du plan validé — réutiliser le même fichier).
   - Possibilité de **changer de mode** à tout moment (commande explicite
     ou modification de la config).

2. **Numérotation des plans en mode (c)/(d)** — Sans issue GitHub, il n'y a
   plus de numéro externe. Définir une stratégie d'auto-incrémentation
   locale robuste (scan du dossier `./doc/roadmap/`, max+1, gestion des
   conflits si plusieurs personnes travaillent en parallèle).

3. **Impact sur le workflow** — Identifier et documenter **chaque point du
   workflow** (phases 1→7, reprise, clôture, migration) qui est affecté par
   le mode choisi. Les phases qui touchent aux issues doivent avoir une
   branche conditionnelle propre (pas un `if` caché dans une phrase).

4. **Impact sur les fichiers de référence** — `references/github-issues.md`
   devient conditionnel. `references/templates.md` (front matter `issue.id`,
   `issue.url`) doit supporter les champs à `null` proprement.
   `references/roadmap-file.md` doit fonctionner sans références d'issues.

### Axe C — Exécution des tests par l'agent (accès direct à l'environnement)

**Problème** : le skill suppose aujourd'hui que l'agent n'a **pas** accès
à l'environnement de test — il rédige une procédure, la présente à
l'opérateur, et attend les résultats. Or certains IDE (Claude Code avec
accès shell, Codex avec sandbox) permettent à l'agent d'exécuter les tests
lui-même.

**Exigence** : supporter 2 modes d'exécution des tests, mutuellement
exclusifs :

| Mode | Condition | Comportement |
|---|---|---|
| **a. Manuel** (actuel) | L'agent n'a pas accès à l'env de test | Workflow actuel inchangé : procédure écrite → `⏸️` → opérateur exécute → transmet résultats |
| **b. Autonome** | L'agent a accès à l'env de test | L'agent exécute les tests lui-même via une boucle vérificateur/exécuteur |

**Spécifications du mode autonome (b)** :

- **L'étape 0 de la Phase 7 est supprimée** (pas de question sur les tests
  intermédiaires — tous sont exécutés automatiquement après chaque étape).
- **Les procédures de tests sont toujours écrites dans le plan** (traçabilité
  documentaire, même si l'agent les exécute lui-même).

#### Architecture à deux rôles : Vérificateur ≠ Exécuteur

La boucle test→fix→retest repose sur une **séparation stricte des rôles** :
l'agent qui implémente (Exécuteur) n'est **jamais** celui qui juge les
résultats (Vérificateur). Principe : **« L'agent ne note pas sa propre
copie. »**

**Cycle des personas** :

```
Exécuteur (implémente l'étape)
    │
    ▼ fin d'étape → switch persona
Vérificateur (prompt système dédié)
    │
    ├─ ✅ Done → switch retour Exécuteur
    │            → continuer le workflow
    │
    └─ ❌ Fail → switch retour Exécuteur
                 → steps iii-v (analyser, corriger, MAJ tests)
                 → switch Vérificateur (retour en i)
```

**Contrat du Vérificateur** (à formaliser dans un prompt système dédié) :

| Aspect | Règle |
|---|---|
| **Rôle** | Exécuter les tests et comparer résultats vs résultats attendus |
| **Accès** | Résultats des tests **uniquement**. Aucun accès au code source d'implémentation (aveugle au code) |
| **Interdit** | Ne jamais corriger. Ne jamais suggérer de fix. Ne jamais modifier le code ou les tests |
| **Output** | Verdict `PASS` ou `FAIL` + diagnostic factuel (ce qui est observé vs ce qui est attendu) |
| **État** | Sans mémoire entre itérations — chaque invocation repart du prompt système + résultats, rien d'autre |
| **Durée de vie** | N'existe que le temps des steps i+ii. Le retour au persona Exécuteur est immédiat après le verdict |

**Contrat de l'Exécuteur** (persona par défaut de l'agent) :

| Aspect | Règle |
|---|---|
| **Rôle** | Implémenter, analyser les root causes, corriger, mettre à jour les tests |
| **Accès** | Accès complet au code et aux tests |
| **Interdit** | Ne jamais juger ses propres résultats de test. Ne jamais déclarer un test `PASS` — seul le Vérificateur le peut |
| **Gate "Done"** | Seul un verdict `PASS` du Vérificateur autorise la sortie de boucle |

**Boucle de vérification** :

```
┌──────────────────────────────────────────────────────────────────────┐
│                    [SWITCH → Vérificateur]                          │
│  i.   Exécuter les tests unitaires du plan                         │
│  ii.  Comparer résultats vs résultats attendus                     │
│       ├─ ✅ PASS (Gate "Done")                                     │
│       │   → Afficher résultats vs attendus                         │
│       │   → [SWITCH → Exécuteur]                                   │
│       │   → Sortir de la boucle, continuer le workflow             │
│       └─ ❌ FAIL                                                   │
│           → Afficher diagnostic factuel (observé vs attendu)       │
│           → [SWITCH → Exécuteur]                                   │
│  iii. Analyser les root causes (à partir du diagnostic)            │
│  iv.  Corriger l'implémentation                                    │
│  v.   Mettre à jour les tests dans le plan                         │
│  vi.  → Retour à (i)                                               │
└──────────────────────────────────────────────────────────────────────┘
```

**Implémentation du switch de persona selon l'IDE** :

Le skill décrit le **contrat** (ci-dessus). Le **mécanisme** d'implémentation
varie selon l'IDE et doit être documenté dans `references/environment.md` :

| Mécanisme | IDE | Description |
|---|---|---|
| Sub-agent réel | Claude Code (si supporté) | Process séparé avec prompt système distinct. Isolation maximale |
| Changement de rôle structuré | Universel (fallback) | L'agent switch son persona via un prompt interne structuré dans le même contexte. Moins d'isolation mais portable |
| Appel externe | Futur / sur mesure | Webhook vers un service de vérification (hors scope initial) |

Le choix du mécanisme peut être documenté dans `.skill-config.yml` ou
détecté automatiquement selon l'IDE.

**Garde-fou obligatoire** : si la boucle dépasse **N itérations** (à
définir — propose une valeur par défaut raisonnable), l'agent **s'arrête**,
affiche un diagnostic (tentatives, erreurs persistantes, hypothèses) et
**demande à l'utilisateur** s'il veut continuer, ajuster, ou abandonner
cette étape. L'utilisateur peut aussi interrompre la boucle à tout moment
avec un signal explicite (« stop », « arrête »).

**Même boucle pour les tests finaux (`🧪 Tests`)** : la boucle
vérificateur/exécuteur s'applique identiquement aux tests finaux
(avant-dernière étape). Le `⏸️` de clôture reste mais se déplace : il vient
**après** les tests passés (verdict `PASS` du Vérificateur), pas avant
leur exécution.

**Points de conception à trancher** :

1. **Détection du mode** — Comment déterminer si l'agent a accès à l'env de
   test ? Propose un mécanisme (détection auto + config + confirmation).
   Persistance dans `.skill-config.yml`.

2. **Affichage des résultats** — En mode autonome, l'agent doit quand même
   **afficher clairement** les résultats à chaque itération (transparence).
   Propose un format compact de reporting par itération qui distingue
   visuellement les outputs du Vérificateur et de l'Exécuteur.

3. **Interaction avec le bloc `📦 Commit proposé`** — En mode autonome, la
   boucle tourne avant le commit. Le commit n'est proposé qu'une fois le
   verdict `PASS` obtenu du Vérificateur. Adapter le template en
   conséquence.

4. **Valeur par défaut du garde-fou** — Propose un nombre max d'itérations
   raisonnable avec justification.

5. **Prompt système du Vérificateur** — Rédige une proposition de prompt
   système complet pour le persona Vérificateur, respectant le contrat
   ci-dessus.

### Axe D — Cohérence avec le plan validé

Les axes A, B et C s'ajoutent au plan d'architecture validé (agnostique
IDE + modèles). Vérifie et documente les **interactions** :

- L'axe A impacte `references/environment.md` (nouveau fichier du plan) :
  y intégrer le fallback de formatage des commandes ?
- L'axe B impacte `.skill-config.yml` (config optionnelle du plan) : y
  ajouter le mode issues ?
- L'axe C impacte `.skill-config.yml` : y ajouter le mode tests + le
  mécanisme de persona switch ?
- Les 3 axes ensemble rendent `.skill-config.yml` plus riche — reste-t-il
  optionnel et non bloquant ?

---

## Contraintes transverses

- **Rétrocompatibilité stricte** : un utilisateur Claude Code, sans
  `.skill-config.yml`, sur un projet GitHub, doit retrouver **exactement**
  le comportement actuel (v1.3.0) sans rien configurer.
- **Pas de sur-ingénierie** : la config reste optionnelle. Chaque mode a
  un fallback raisonnable basé sur la détection automatique.
- **Workflow inchangé** : les 7 phases, les points d'arrêt, les règles
  absolues restent. Ce sont les **mécanismes sous-jacents** (issues, tests,
  commandes IDE, persona switch) qui deviennent adaptatifs.
- **Un seul fichier de config** : ne pas multiplier les fichiers de
  configuration. `.skill-config.yml` centralise tout (IDE, modèles, mode
  issues, mode tests, mécanisme persona).
- **Maintenabilité** : chaque point de variabilité (IDE, modèle, issues,
  tests, persona) doit être modifiable à un seul endroit.

## Livrable attendu

**Ne pas écrire le contenu final.** Produire d'abord un **plan
d'architecture mis à jour** qui :

1. **Intègre les 4 nouveaux axes** dans le plan existant (validé).
2. **Liste chaque fichier impacté** avec les sections à ajouter, modifier
   ou supprimer.
3. **Tranche les points de conception** listés dans chaque axe (avec
   justification).
4. **Documente les interactions entre axes** (axe D).
5. **Propose le schéma complet de `.skill-config.yml`** (tous les champs,
   toutes les valeurs possibles, les défauts).
6. **Propose le prompt système du Vérificateur** (complet, prêt à
   l'emploi).
7. **Identifie les risques** de régression ou de complexité excessive.

J'approuve ce plan avant que tu rédiges les fichiers.

## Ordre de lecture recommandé

1. Lire les fichiers actuels du skill (comprendre l'existant).
2. Lire le plan d'architecture validé (comprendre les changements déjà
   décidés).
3. Lire les 4 axes ci-dessus (comprendre ce qui s'ajoute).
4. Produire le plan mis à jour.