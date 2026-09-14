# Scission modulaire (L1) — roadmap-tracking SKILL.md

Transformer le fichier monolithique `SKILL.md` (1 590 lignes, ~11 880 mots, ~80 Ko) en une architecture **noyau d'aiguillage + 5 modules à chargement différé**, conformément à l'audit [2-roadmap-tracking-optimisation-tokens-architecture.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/doc/audits/2-roadmap-tracking-optimisation-tokens-architecture.md).

## Contexte post-mortem

Leçon du rollback P1 (§1 de l'audit) : **ne jamais supprimer de garde-fous sémantiques**. Ici aucune règle n'est supprimée — elles sont déplacées dans des modules chargés au moment pertinent. Les 4 blocs `⛔` restent dans le noyau permanent.

## User Review Required

> [!IMPORTANT]
> **Découpage des modules** — L'audit proposait 6 fichiers dans `references/workflow-*.md`. Votre instruction demande 5 fichiers dans `modules/` avec des noms différents. Le plan ci-dessous suit **votre instruction** (noms : `init-scan.md`, `plan.md`, `execute.md`, `wrapup.md`, `templates.md`), en redistribuant le contenu pour couvrir intégralement le SKILL.md.

> [!IMPORTANT]
> **Contenu du module `templates.md`** — Votre instruction le décrit comme « Format de plan, conventions, tableaux de métriques ». Ce module ne dupliquera pas `references/templates.md` existant ; il contiendra les templates de chat (⏸️, 📦, 🚀, signaux de mode, tag d'étape, gate modèle) et les conventions de format internes au workflow, distinctes du template de fichier plan.

## Proposed Changes

### Découpage détaillé — contenu source → module cible

| Module | Sections SKILL.md actuelles (lignes) | Tokens est. |
|---|---|---|
| **SKILL.md (noyau)** | Frontmatter (L1–26), Description (L28–38), Prerequisites (L39–47), Fichiers de référence (L48–61), Applicabilité (L62–89), 4 blocs ⛔ (L307–385), Correction proactive (L387–434), Signaux de mode (L436–445), Table de routage modules, Résumé compact des phases | ~3 500 |
| **`modules/init-scan.md`** | Système d'aide Axe E (L90–143), Règle de démarrage (L146–238), Détection ID/Migration (L240–306), Garde d'entrée ⛔ (L653–757, **copie de renforcement**, le ⛔ canonique reste dans le noyau), Règle anti-court-circuit, Phase 1 (L760–812), Matrice Axe A (L775–812), Garde dure désengagement (L814–874), Phase 1.5 gate modèle (L876–893) | ~4 850 |
| **`modules/plan.md`** | Phase 2 cadrage + Axe B (L895–972), Éval complexité + grille sizing + gate modèle (L446–580), Grilling adaptatif (L582–651), Phase 3 proposition (L974–1022), Phase 4 validation + grilling (L1024–1061) | ~4 100 |
| **`modules/execute.md`** | Phase 5 Act limité (L1063–1119), Phase 6 validation pré-implémentation (L1121–1143), Phase 7 implémentation (L1145–1326), Tests intermédiaires (L1328–1383), Étape 🧪 Tests (L1385–1444), Étape ✅ Validation (L1446–1473), Commit référence format (L1474–1502) | ~4 300 |
| **`modules/wrapup.md`** | Reprise plan existant (L1504–1590), Clôture plan (extraite de L1299–1326, référencée en Phase 7), Gate modèle sur reprise | ~1 100 |
| ~~`modules/templates.md`~~ | ~~Templates de chat (⏸️, 📦, 🚀, désengagement, surcout Axe D)~~ | **Supprimé** — voir écart ci-dessous |

---

### Noyau — SKILL.md (~3 500 tokens)

#### [MODIFY] [SKILL.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/SKILL.md)

Réfacter en conservant **uniquement** :

1. **Frontmatter YAML** — inchangé (version bump → `3.0.0`)
2. **Description** — inchangée
3. **Prerequisites** — inchangé
4. **Fichiers de référence** — table existante + ajout de la table des modules
5. **Applicabilité** — inchangée
6. **4 blocs ⛔ Règles absolues** — inchangés, mot pour mot
7. **Correction proactive** — inchangée
8. **Signaux de mode** — inchangé (compact, ~10 lignes)
9. **Table de routage des modules** — NOUVELLE section :
   ```markdown
   ## Modules de workflow (chargement conditionnel)
   
   Charge le module correspondant à la phase active via l'outil de lecture
   de fichier. Ne charge **jamais** plus d'un module à la fois sauf en
   Phase 1 (init-scan + plan).
   
   | Module | Fichier | Quand le charger |
   |---|---|---|
   | Initialisation & scan | `modules/init-scan.md` | **Tour 1** — démarrage, aide, reprise |
   | Planification | `modules/plan.md` | **Phases 1–4** — cadrage, sizing, proposition |
   | Exécution | `modules/execute.md` | **Phases 5–7** — création plan, implémentation, tests |
   | Clôture & reprise | `modules/wrapup.md` | **Reprise d'un plan** ou **clôture** |
   | Templates & conventions | `modules/templates.md` | **À la demande** — formats de chat, commits, métriques |
   ```
10. **Résumé compact des phases** — NOUVELLE section (~15 lignes) résumant les 7 phases en 1 ligne chacune pour que l'agent sache qu'elles existent sans les avoir en contexte.

---

### Modules

#### [NEW] [init-scan.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/init-scan.md)

Contenu extrait mot pour mot des sections L90–306 + L653–874 + L876–893 du SKILL.md actuel.

#### [NEW] [plan.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/plan.md)

Contenu extrait des sections L446–651 + L895–1061.

#### [NEW] [execute.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/execute.md)

Contenu extrait des sections L1063–1502.

#### [NEW] [wrapup.md](file:///c:/Users/pou_x/Documents/Antigravity/Projects/roadmap-tracking/modules/wrapup.md)

Contenu extrait des sections L1504–1590 + bloc clôture (L1299–1326).

#### ~~[NEW] modules/templates.md~~ — **ÉCART D'IMPLÉMENTATION (supprimé)**

> **Décision post-implémentation** : `modules/templates.md` a été créé puis
> supprimé. Seule la ligne de routing dans SKILL.md a été retirée.
>
> **Raison** : le module était orphelin (1 seule référence — sa propre entrée
> de routing) et dupliquait intégralement du contenu déjà présent inline dans
> les modules de phase (`execute.md`, `wrapup.md`, `init-scan.md`). Le garder
> aurait introduit de la maintenance (deux endroits à synchroniser) sans gain
> fonctionnel ni gain tokens. Conforme au principe YAGNI et à la leçon du
> rollback P1 : ne pas ajouter de surface sans usage prouvé.
>
> **Impact** : l'architecture finale compte **4 modules** au lieu de 5. Aucun
> contenu perdu — les templates de chat vivent inline dans leurs modules de
> phase respectifs.

---

## Invariants de sécurité (tolérance zéro régression)

Les éléments suivants doivent être présents **inchangés** dans le résultat final :

| Invariant | Localisation cible |
|---|---|
| 4 blocs `⛔ Règle absolue` | **Noyau** (SKILL.md) — jamais déplacés |
| Garde d'entrée (checkpoint universel) | `modules/init-scan.md` — intégral |
| Règle anti-court-circuit (table complète) | `modules/init-scan.md` — intégral |
| Garde dure de désengagement | `modules/init-scan.md` — intégral |
| Points d'arrêt `⏸️` (tous) | Modules respectifs — aucun supprimé |
| Correction proactive | **Noyau** (SKILL.md) — toujours visible |
| Templates ❌/✅ formats | `modules/templates.md` — intégraux |

## Verification Plan

### Automated Verification
```powershell
# 1. Décompte lignes/mots du noyau vs modules
Get-Content SKILL.md | Measure-Object -Line -Word
Get-ChildItem modules/*.md | ForEach-Object { 
    $m = Get-Content $_.FullName | Measure-Object -Line -Word
    "$($_.Name): Lines=$($m.Lines) Words=$($m.Words)" 
}

# 2. Vérifier que les 4 blocs ⛔ sont dans le noyau
(Select-String -Path SKILL.md -Pattern "^## ⛔" | Measure-Object).Count  # → 4

# 3. Vérifier qu'aucune directive critique n'est tronquée
# Chercher les balises clés dans l'ensemble {SKILL.md + modules/}
@("⛔ Garde d'entrée", "anti-court-circuit", "Garde dure", "⏸️ POINT D'ARRÊT", "📦 Commit", "🧪 Tests") | ForEach-Object {
    $found = Select-String -Path SKILL.md, modules/*.md -Pattern $_ | Measure-Object
    "$_`: $($found.Count) occurrence(s)"
}
```

### Manual Verification
- Relecture diff du SKILL.md avant/après
- Validation qu'aucun contenu n'a été perdu (somme des mots modules ≈ baseline)
- Test fonctionnel : invocation du skill sur un projet test
