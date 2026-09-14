# Audit #2 — Architecture d'optimisation tokens pour roadmap-tracking

> **Objectif** : réduire de **≥ 35 %** la consommation tokens (input + output)
> du skill `roadmap-tracking` sans dégradation mesurable de la qualité des
> outputs.
>
> **Date** : 2026-09-14 · **Auteur** : Agent architecte (Opus 4.6)
> **Baseline** : SKILL.md v2.8.0 — 1 590 lignes, ~11 880 mots, ~80 138 octets
> **Référence coût** : session S plan #11 → 278 000 tokens totaux (18 tours)

---

## Table des matières

1. [Post-mortem P1 (rollback)](#1-post-mortem-p1-rollback)
2. [Réévaluation des phases existantes](#2-réévaluation-des-phases-existantes)
3. [Cartographie des coûts — baseline détaillée](#3-cartographie-des-coûts--baseline-détaillée)
4. [Stratégie d'optimisation — 3 leviers retenus](#4-stratégie-doptimisation--3-leviers-retenus)
5. [Matrice risques / gains](#5-matrice-risques--gains)
6. [Projection chiffrée consolidée](#6-projection-chiffrée-consolidée)
7. [Plan de validation qualité](#7-plan-de-validation-qualité)
8. [Annexes](#8-annexes)

---

## 1. Post-mortem P1 (rollback)

### Contexte

Le plan #12 (`doc/roadmap/12-skill-compression-p1.md`) visait une réduction de
~35 % de SKILL.md via deux actions :

| Action | Cible audit | Résultat réel | Écart |
|---|---|---|---|
| Suppression de 13 blocs `❌` redondants | −63 000 tokens cumulés | **1 seul bloc `❌` réellement redondant** dans v2.5.7 | **×13 surestimation** |
| Fusion de 3 gabarits de commit | −27 lignes | −22 lignes (fusion effective) | Conforme |

Résultat net : 1 369 → 1 340 lignes (**−2,1 %** au lieu de −35 %).

### Causes racines de l'échec

| # | Cause | Catégorie | Détail |
|---|---|---|---|
| **C1** | Surestimation du nombre de blocs `❌` redondants | Estimation erronée | L'audit initial comptait 13 blocs `❌`. En réalité, 12/13 sont des **contraintes positives nécessaires** (exemples interdits servant de garde-fou comportemental). Seul le bloc `❌ Formats INTERDITS` de la section « Démarrage standard » dupliquait le bloc de la section `⛔ Règle absolue — format des rapports`. |
| **C2** | Le bloc `❌` supprimé a été réintroduit manuellement | Rollback volontaire | Le gain de sa suppression (~6 lignes, ~50 tokens/tour) n'était pas établi comme suffisant face au risque de régression comportementale. L'utilisateur a jugé que la contrainte négative sert de renforcement positionnel et l'a restaurée. |
| **C3** | Confusion entre **redondance textuelle** et **redondance sémantique** | Erreur d'analyse | Un bloc qui répète un contenu n'est redondant que si sa suppression ne modifie pas le comportement du modèle. Les blocs `❌` sont des **contraintes négatives positionnelles** : leur efficacité dépend de leur proximité avec l'instruction qu'ils protègent, pas seulement de leur unicité dans le fichier. |
| **C4** | Le levier P1 (compression textuelle brute) cible le mauvais multiplicateur | Architecture | Le coût dominant n'est pas la verbosité du texte, c'est la **répétition du texte complet à chaque tour** (~11 000 tokens × 18 tours = ~198 000 tokens, soit **71 % du coût total**). Comprimer de 35 % le texte ne réduit que 35 % × 71 % = ~25 % du total — et les 35 % de compression textuelle ne sont pas atteignables sans altérer les garde-fous. |

### Leçon architecturale

> **La compression textuelle du prompt est un levier à rendement
> décroissant.** Au-delà de ~10-15 % de compression (élimination des vraies
> duplications), chaque réduction supplémentaire attaque les formulations de
> garde-fou et dégrade la fiabilité. Le levier structurellement efficace est
> la **réduction du nombre de tokens présentés à chaque tour**, pas la
> réduction du nombre total de tokens dans le fichier.

---

## 2. Réévaluation des phases existantes

L'audit initial (`0-roadmap-tracking-estimation-couts-tokens.md`) proposait 6
pistes (P1 à P6). Réévaluation post-mortem P1 :

| Piste | Libellé | Verdict | Justification |
|---|---|---|---|
| **P1** | Compression SKILL.md −35 % | ❌ **Écartée** | Post-mortem : gain réel ~2 %, non ~35 %. Les blocs `❌` ne sont pas redondants (C1/C3). La fusion des gabarits commit est faite (v2.6.0→v2.8.0). Le gisement restant de compression textuelle pure est ≤ 5 %. |
| **P2** | Scission planning / implémentation | ✅ **Retenue — recalibrée** | Le principe est sain (charger moins de texte pendant les tours de planning). Mais le mécanisme proposé (deux fichiers skill chargés séquentiellement via `Skill()`) dépend d'une capacité plateforme non garantie. Recalibré en **Levier 1** ci-dessous (scission par sections conditionnelles avec directives de chargement). |
| **P3** | Prompt caching plateforme | ⚠️ **Hors scope skill** | Dépend de l'infrastructure IDE (Claude Code `cache_control`, Antigravity caching). Impossible à implémenter dans le skill seul. Mentionné comme amplificateur externe. |
| **P4** | Fusion ⏸️2 + gate Phase 6 pour S/M | ✅ **Retenue — intégrée** | Intégrée dans le **Levier 2** (élimination des tours inutiles). Gain modéré mais sans risque. |
| **P5** | Silence gate ℹ️ Cas 1 | ✅ **Retenue — intégrée** | Intégrée dans le **Levier 2**. La gate ℹ️ (modèle adapté) n'ajoute aucune valeur décisionnelle ; la supprimer économise ~200 tokens output × propagation. |
| **P6** | Garde « référence déjà en contexte » | ✅ **Retenue** | Impact marginal (~1 700 tokens) mais risque nul. Intégrée dans le **Levier 3**. |

---

## 3. Cartographie des coûts — baseline détaillée

### 3.1 Distribution des tokens par section de SKILL.md

Mesure sur SKILL.md v2.8.0 (1 590 lignes, ~11 880 mots). Estimation : 1 mot ≈ 1,3 tokens pour du markdown français/anglais mixte → **~15 450 tokens** pour le fichier complet.

| Section | Lignes | Mots | Tokens est. | % du skill | Phase d'utilisation |
|---|---|---|---|---|---|
| Header + Metadata | L1–38 | 201 | ~260 | 1,7 % | Toujours |
| Prerequisites | L39–47 | 41 | ~55 | 0,4 % | Toujours |
| Fichiers de référence | L48–61 | 133 | ~175 | 1,1 % | Toujours |
| Applicabilité | L62–89 | 252 | ~330 | 2,1 % | Toujours |
| Système d'aide (Axe E) | L90–143 | 342 | ~445 | 2,9 % | Aide uniquement |
| Règle de démarrage | L146–238 | 631 | ~820 | 5,3 % | Tour 1 uniquement |
| Détection ID / Migration | L240–306 | 467 | ~610 | 3,9 % | Tour 1 (mode github) |
| Règles absolues (4 blocs ⛔) | L307–385 | 496 | ~645 | 4,2 % | Toujours |
| Correction proactive | L387–434 | 327 | ~425 | 2,8 % | Toujours |
| Signaux de mode | L436–445 | 71 | ~90 | 0,6 % | Toujours |
| Évaluation complexité + Gate | L446–580 | 988 | ~1 285 | 8,3 % | Phase 1–1.5, Phase 7 |
| Grilling adaptatif | L582–651 | 425 | ~555 | 3,6 % | L/XL uniquement |
| ⛔ Garde d'entrée | L653–757 | 1 102 | ~1 435 | 9,3 % | Tour 1 (puis rappel) |
| Phase 1 + Matrice A | L760–812 | 358 | ~465 | 3,0 % | Phase 1 |
| Garde dure désengagement | L814–874 | 515 | ~670 | 4,3 % | Phase 1 (XS/S) |
| Phase 1.5 | L876–893 | 177 | ~230 | 1,5 % | Phase 1.5 |
| Phase 2 + Axe B | L895–972 | 551 | ~715 | 4,6 % | Phase 2 |
| Phase 3 | L974–1022 | 353 | ~460 | 3,0 % | Phase 3 |
| Phase 4 | L1024–1061 | 299 | ~390 | 2,5 % | Phase 4 |
| Phase 5 | L1063–1119 | 483 | ~630 | 4,1 % | Phase 5 |
| Phase 6 | L1121–1143 | 166 | ~215 | 1,4 % | Phase 6 |
| Phase 7 (cœur) | L1145–1326 | 1 501 | ~1 950 | 12,6 % | Phase 7 |
| Tests intermédiaires | L1328–1383 | 354 | ~460 | 3,0 % | Phase 7 |
| Tests finaux (🧪) | L1385–1444 | 410 | ~535 | 3,5 % | Phase 7 |
| Validation (✅) | L1446–1473 | 231 | ~300 | 1,9 % | Phase 7 |
| Commit (référence format) | L1474–1502 | 194 | ~250 | 1,6 % | Phase 7 |
| Reprise plan existant | L1504–1590 | 812 | ~1 055 | 6,8 % | Reprise |
| **TOTAL** | **1 590** | **11 880** | **~15 450** | **100 %** | — |

### 3.2 Modèle de coût par tour (session S, 18 tours)

| Composant | Tokens/tour | × 18 tours | % total |
|---|---|---|---|
| SKILL.md complet | ~15 450 | ~278 100 | **71 %** |
| System prompts (IDE, rules) | ~5 000 | ~90 000 | 23 % |
| Contexte conversationnel (croissant) | ~0 → 2 000 | ~18 000 | 5 % |
| Lectures fichiers (cumulées) | — | ~20 000 | 5 % |
| **Tokens output** | — | ~10 500 | — |
| **TOTAL** | — | **~278 000** | — |

> **Constat clé** : 71 % du budget est la re-présentation de SKILL.md à chaque
> tour. C'est **le seul levier à fort rendement**. Les references sont chargées
> à la demande et ne pèsent pas sur chaque tour.

### 3.3 Analyse phase par phase — utilisation réelle des sections

Sur une session S typique (18 tours) :

| Section | Utilisée aux tours | Tokens × tours utiles | Tokens × tours inutiles |
|---|---|---|---|
| Règle de démarrage (820 tk) | Tour 1 | 820 | 820 × 17 = **13 940** |
| Détection ID / Migration (610 tk) | Tour 1 (github) | 610 | 610 × 17 = **10 370** |
| Système d'aide (445 tk) | Jamais (sauf commande aide) | 0 | 445 × 18 = **8 010** |
| Grilling (555 tk) | Jamais (S < L) | 0 | 555 × 18 = **9 990** |
| Phase 1–5 (2 890 tk) | Tours 1–6 (~6 tours) | 17 340 | 2 890 × 12 = **34 680** |
| Phase 6–7 + tests (3 710 tk) | Tours 7–18 (~12 tours) | 44 520 | 3 710 × 6 = **22 260** |
| Garde d'entrée (1 435 tk) | Tour 1 (critique) | 1 435 | 1 435 × 17 = **24 395** |
| Garde dure (670 tk) | Jamais (S+collab) | 0 | 670 × 18 = **12 060** |
| Reprise (1 055 tk) | Jamais (nouveau plan) | 0 | 1 055 × 18 = **18 990** |
| **Total tokens gaspillés** | — | — | **~154 700** |

> **154 700 tokens gaspillés sur 278 000 = 55,6 % du budget total.** Ce sont
> des sections présentées au modèle mais jamais utilisées dans le contexte de
> la session en cours.

---

## 4. Stratégie d'optimisation — 3 leviers retenus

### Principe directeur

> Ne pas comprimer le texte. **Réduire le texte présenté à chaque tour** en
> ne chargeant que les sections pertinentes pour la phase en cours.

### Levier 1 — Scission en modules conditionnels (chargement sélectif)

#### Concept

Découper SKILL.md en un **noyau** (toujours chargé) et des **modules
conditionnels** (chargés uniquement quand la phase l'exige), en utilisant le
même mécanisme que les `references/*.md` actuels : directives « charge ce
fichier quand tu en as besoin ».

#### Découpage proposé

| Module | Contenu | Tokens | Chargé quand |
|---|---|---|---|
| **SKILL.md** (noyau) | Header, Metadata, Prérequis, Fichiers de ref, Applicabilité, Signaux de mode, Règles absolues (4 ⛔), Correction proactive, Table des modules, Résumé des phases | ~3 500 | **Toujours** (chaque tour) |
| **`references/workflow-startup.md`** | Règle de démarrage, Bloc A.0, Détection ID, Migration, Garde d'entrée (complète), Garde dure, Anti-court-circuit | ~4 850 | **Tour 1** (démarrage ou reprise) |
| **`references/workflow-planning.md`** | Phase 1 + Matrice A, Phase 1.5, Phase 2 + Axe B, Phase 3, Phase 4, Éval complexité + Gate (complet), Grilling adaptatif | ~4 100 | **Phases 1–4** (planning) |
| **`references/workflow-implementation.md`** | Phase 5, Phase 6, Phase 7 (complet), Tests intermédiaires, Tests finaux, Validation, Commit référence, Clôture | ~4 300 | **Phases 5–7** (implémentation) |
| **`references/workflow-resume.md`** | Reprise plan existant, Gate modèle sur reprise | ~1 100 | **Reprise uniquement** |
| **`references/aide.md`** | Système d'aide (Axe E), Note de bienvenue | ~445 | **Commande aide uniquement** |

#### Impact sur une session S (18 tours)

| Tour | Modules chargés | Tokens chargés | vs baseline |
|---|---|---|---|
| Tour 1 | noyau + startup + planning | 3 500 + 4 850 + 4 100 = **12 450** | 15 450 (−19 %) |
| Tours 2–6 (planning) | noyau + planning | 3 500 + 4 100 = **7 600** | 15 450 (−51 %) |
| Tours 7–12 (implémentation) | noyau + implementation | 3 500 + 4 300 = **7 800** | 15 450 (−49 %) |
| Tours 13–18 (implémentation) | noyau + implementation | 3 500 + 4 300 = **7 800** | 15 450 (−49 %) |

**Calcul du gain** :

```
Baseline  : 15 450 × 18 = 278 100 tokens (skill seul)
Optimisé  : 12 450 × 1 + 7 600 × 5 + 7 800 × 12 = 12 450 + 38 000 + 93 600
          = 144 050 tokens
Économie  : 278 100 − 144 050 = 134 050 tokens
Réduction : −48,2 % sur le poste skill (71 % du total)
Réduction totale : 134 050 / 278 000 = −48,2 % × 0,71 = −34,2 % du total
```

> **Ce seul levier atteint déjà ~34 % d'économie** — à la frontière de
> l'objectif de 35 %.

#### Risque qualité : **FAIBLE**

- Aucune règle n'est supprimée : elles sont déplacées dans des fichiers
  chargés au moment pertinent.
- Le noyau conserve les 4 règles absolues `⛔` (qui doivent être présentes à
  chaque tour pour servir de garde-fous permanents).
- Le mécanisme de chargement conditionnel est déjà prouvé par
  `references/forms.md`, `references/templates.md`, etc.

#### Prérequis de mise en œuvre

- Le noyau doit contenir une **table de chargement** (similaire à la table
  « Fichiers de référence » existante L48–61) indiquant explicitement à
  l'agent quel module charger et quand.
- Les directives de chargement doivent être **positives** (« charge X quand
  tu fais Y ») et non conditionnelles complexes.
- Un **résumé compact de chaque phase** (~1 ligne) doit rester dans le noyau
  pour que l'agent sache que les phases existent sans les avoir en contexte.

---

### Levier 2 — Élimination des tours inutiles (réduction du multiplicateur)

#### Concept

Réduire le nombre de tours API pour une session S de 18 à ~14 en éliminant
les interactions qui n'apportent pas de valeur sur les petites complexités.

#### Actions concrètes

| # | Action | Tours économisés | Tokens économisés (post-Levier 1) |
|---|---|---|---|
| **2a** | Supprimer la gate `ℹ️` (Cas 1 — modèle adapté) en Phase 1.5 et Phase 7 : n'afficher la gate que si mismatch (Cas 2) | 0 tour (pas de round-trip) mais −200 tokens output × 2 gates, propagés sur ~16 tours input | ~3 600 |
| **2b** | Fusionner ⏸️2 (Phase 5) et Phase 6 pour plans S/M : la confirmation de création du plan inclut directement l'autorisation d'implémenter via une option « 🚀 Créer et implémenter » | **1 tour complet** | ~12 800 (1 × noyau+impl + system + output) |
| **2c** | Supprimer la Phase 1.5 comme point d'arrêt séparé pour plans S/M : intégrer le check gate dans le résumé Phase 3 (sans arrêt si Cas 1) | **1 tour complet** (si Cas 1) | ~12 800 |
| **2d** | Mode `autonomous` + S : supprimer l'étape 0 (sélection tests intermédiaires) — déjà prévu mais renforcer la directive | **1 tour** | ~12 800 |

**Gain total Levier 2** : ~42 000 tokens → **−15,1 %** du total baseline.

> Applicable seulement aux plans S/M. Les plans L/XL conservent l'intégralité
> des points d'arrêt (le grilling et les gates sont justifiés).

#### Risque qualité : **FAIBLE**

- Les points d'arrêt critiques (⏸️1 plan, ⏸️ pre-implémentation) sont
  conservés.
- Seuls les points d'arrêt dont la valeur ajoutée est nulle sur S/M sont
  supprimés.
- La gate modèle reste active en cas de mismatch (Cas 2).

---

### Levier 3 — Compression ciblée du noyau (densification sémantique)

#### Concept

Appliquer une compression **sémantique** (pas textuelle brute) sur les
sections qui restent dans le noyau permanent, en éliminant les redondances
inter-sections et en densifiant les formulations sans supprimer de règle.

#### Actions concrètes

| # | Action | Tokens économisés/tour | Impact 18 tours |
|---|---|---|---|
| **3a** | Fusionner les 2 blocs `❌ Formats INTERDITS` (L207–217 et L320–333) en un seul, positionné dans la section `⛔ Règle absolue — format des rapports`. Le bloc dans « Démarrage standard » devient un renvoi d'une ligne | ~100 tokens/tour | ~1 800 |
| **3b** | Densifier la table « Règle anti-court-circuit » (L719–757) : la table de 12 lignes des « cas à risque élevé » partage ~60 % de contenu avec le paragraphe qui la précède. Fusionner en une table unique sans texte narratif dupliqué | ~200 tokens/tour | ~3 600 |
| **3c** | Compacter les templates de chat (`⏸️`, `📦`, `🚀 Implémentation`) : remplacer les blocs multi-lignes par des templates sur 2-3 lignes avec variables. Les templates actuels sont des exemples verbeux ; une forme compacte + directive « adapter au contexte » est suffisante | ~150 tokens/tour | ~2 700 |
| **3d** | Garde « référence déjà en contexte » (P6 de l'audit initial) : ajouter une directive dans le noyau pour ne pas relire `environment.md` si déjà en contexte | ~95/occurrence (1 relecture évitée/session) | ~1 700 |
| **3e** | Supprimer les blocs de renforcement « ⚠️ rappel » dans les phases d'implémentation qui répètent les règles absolues déjà présentes dans le noyau permanent. Les sections `> ⚠️ Même si le prompt...` dans la Reprise (L1506–1510) et similaires renvoient au noyau au lieu de répéter | ~80 tokens/tour | ~1 440 |

**Gain total Levier 3** : ~11 240 tokens → **−4,0 %** du total baseline.

#### Risque qualité : **TRÈS FAIBLE**

- Aucune règle supprimée.
- Densification = reformulation plus concise à contenu identique.
- Les blocs `❌` sont conservés, simplement dé-dupliqués.
- Les templates sont conservés, simplement compactés.

---

## 5. Matrice risques / gains

| Levier | Gain tokens | Gain % total | Risque qualité | Risque technique | Effort impl. | Réversibilité |
|---|---|---|---|---|---|---|
| **L1** — Scission modules | −134 050 | −34,2 % (poste skill) | Faible | Moyen (dépend du mécanisme de chargement conditionnel) | **M** — refactoring structurel | Totale (reconstitution du fichier unique) |
| **L2** — Élimination tours | −42 000 | −15,1 % | Faible | Faible (modifications de directives) | **S** — éditions locales | Totale |
| **L3** — Compression noyau | −11 240 | −4,0 % | Très faible | Très faible | **S** — éditions mineures | Totale |
| **L1+L2+L3** | **−187 290** | **−53,3 %** (brut) | Faible | Moyen | **M** | Totale |

> **Note sur le cumul** : L1 et L2 ne sont pas strictement additifs car L2
> réduit le nombre de tours, ce qui réduit aussi le bénéfice marginal de L1
> (moins de tours = moins de répétitions économisées). Le calcul corrigé est
> en section 6.

---

## 6. Projection chiffrée consolidée

### Scénario conservateur (L1 + L3 seuls) — sans modifier le workflow

```
Baseline              : 278 000 tokens (18 tours)

L1 — Scission modules : −134 050  (noyau 3 500/tour + modules à la demande)
L3 — Compression noyau: −11 240   (noyau réduit de ~15 450 → ~14 500 → 
                                    effet sur les tours post-scission)
                         ─────────
Total                  : −145 290 tokens
                       = −52,3 % (brut, non ajusté)
```

Ajustement : la compression L3 s'applique au noyau (3 500 → ~3 050 tokens),
ce qui réduit tous les tours. Impact corrigé sur 18 tours :

```
L1 corrigé (noyau 3 050) : 
  Tour 1  : 3 050 + 4 850 + 4 100 = 12 000
  Tours 2-6  : 3 050 + 4 100 = 7 150 × 5 = 35 750
  Tours 7-18 : 3 050 + 4 300 = 7 350 × 12 = 88 200
  Total skill : 135 950

Baseline skill : 278 100
Économie skill : 278 100 − 135 950 = 142 150 tokens
En % du total  : 142 150 / 278 000 = −51,1 % sur le poste skill

Poste skill = 71 % du total → impact total = −51,1 % × 0,71 = −36,3 %
```

> ✅ **Objectif de 35 % atteint** avec L1 + L3 seuls (scénario conservateur).

### Scénario nominal (L1 + L2 + L3) — avec optimisation du workflow S/M

```
Réduction des tours : 18 → 14 (L2)

L1+L3 corrigé (14 tours) :
  Tour 1  : 12 000
  Tours 2-5  : 7 150 × 4 = 28 600
  Tours 6-14 : 7 350 × 9 = 66 150
  Total skill : 106 750

L2 — tours éliminés :
  System prompt économisé : 5 000 × 4 = 20 000
  Output économisé        : ~500 × 4 = 2 000
  Total L2                : 22 000

Économie totale : (278 100 − 106 750) + 22 000 = 193 350
En % du total   : 193 350 / 278 000 = −69,5 % (poste skill + tours)

Ajusté au total session (incl. system prompts constants) :
  Baseline totale : ~390 000 tokens (skill + system + contexte + reads)
  Économie nette  : ~193 000 tokens
  Impact total    : −49,5 %
```

> ✅ **Scénario nominal : −49,5 % d'économie totale** — largement au-dessus
> de l'objectif de 35 %.

### Tableau récapitulatif

| Scénario | Leviers | Tours | Tokens skill | Éco. skill | Éco. totale |
|---|---|---|---|---|---|
| **Baseline** | — | 18 | 278 100 | — | — |
| **Conservateur** | L1 + L3 | 18 | 135 950 | −51,1 % | **−36,3 %** |
| **Nominal** | L1 + L2 + L3 | 14 | 106 750 | −61,6 % | **−49,5 %** |

---

## 7. Plan de validation qualité

### 7.1 Critères de non-régression (seuil 0 %)

Aucune optimisation ne peut être déployée si elle provoque une régression sur
l'un des critères suivants :

| # | Critère | Méthode de vérification | Seuil |
|---|---|---|---|
| **Q1** | Format des rapports : listing des plans toujours en tableau markdown | Prompt de test : « liste les plans existants » → vérifier format `\| # \| Fichier \| Statut \|` | 100 % des cas |
| **Q2** | Points d'arrêt `⏸️` respectés : aucune implémentation sans validation utilisateur | Prompt de test : « implémente tout » → vérifier que le workflow s'arrête aux `⏸️` | 100 % des cas |
| **Q3** | Gate modèle fonctionnelle : détection de mismatch, bloc `⚠️`, point d'arrêt bypass | Prompt de test sur modèle standard avec plan L → vérifier gate `⚠️` | 100 % des cas |
| **Q4** | Tests obligatoires : 🧪 et ✅ jamais sautés | Prompt de test : plan S complet → vérifier que 🧪 et ✅ sont proposés | 100 % des cas |
| **Q5** | Commit format correct : `📦` présent, Conventional Commits respecté | Vérifier format commit sur étape d'implémentation | 100 % des cas |
| **Q6** | Désengagement XS/S solo fonctionnel | Prompt de test : tâche XS → vérifier template de désengagement | 100 % des cas |
| **Q7** | Reprise de plan existant : résumé + point d'arrêt avant implémentation | Prompt de test : « continue #X » → vérifier résumé + ⏸️ | 100 % des cas |
| **Q8** | Anti-court-circuit : « go » / « fais tout » ne saute pas les checkpoints | Prompt de test : « fais tout sur #X » → vérifier checkpoints maintenus | 100 % des cas |
| **Q9** | Chargement des modules : les sections déplacées sont bien chargées quand nécessaires | Vérifier que l'agent lit le fichier reference au bon moment | 100 % des cas |
| **Q10** | Traçabilité tests : résultats écrits dans le fichier plan (pas seulement dans le chat) | Vérifier section `## Tests` du plan après une étape de test | 100 % des cas |

### 7.2 Protocole de test

1. **Test A/B structurel** : exécuter le même prompt de plan S avec la version
   actuelle (baseline) et la version optimisée. Comparer :
   - Qualité du plan produit (structure, étapes, front matter).
   - Respect des points d'arrêt.
   - Format des outputs (tableaux, commits, gates).
   - Nombre de tokens consommés (mesure réelle via observabilité).

2. **Test de non-régression par critère** : pour chaque Q1–Q10, exécuter le
   prompt de test et vérifier le seuil.

3. **Test de charge** : exécuter un plan L complet pour vérifier que les
   modules sont bien chargés séquentiellement et que le grilling, les gates
   multiples, et les tests autonomes fonctionnent correctement.

### 7.3 Métriques de succès

| Métrique | Baseline | Cible | Seuil d'échec |
|---|---|---|---|
| Tokens totaux (plan S) | ~278 000 | ≤ 180 700 (−35 %) | > 195 000 |
| Critères qualité Q1–Q10 | 10/10 pass | 10/10 pass | < 10/10 |
| Temps d'exécution | 12m42s | ≤ 12m42s | > 15m00s |

---

## 8. Annexes

### A. Glossaire des termes

| Terme | Définition |
|---|---|
| **Noyau** | Sous-ensemble de SKILL.md chargé à chaque tour d'API |
| **Module conditionnel** | Fichier `references/workflow-*.md` chargé uniquement pendant certaines phases |
| **Tour** | Un aller-retour complet API (input → output) |
| **Contrainte négative positionnelle** | Bloc `❌` dont l'efficacité dépend de sa position dans le prompt (proximité avec l'instruction protégée) |
| **Compression sémantique** | Reformulation plus concise préservant 100 % du contenu sémantique |

### B. Relation avec les audits précédents

| Document | Relation |
|---|---|
| `0-roadmap-tracking-estimation-couts-tokens.md` | Audit initial — source des pistes P1–P6, dont ce document est le successeur |
| `0-rationalisation-tokens-SYNTHESE.md` | Synthèse comparative avec/sans skill — source des axes A–D, déjà implémentés |
| `12-skill-compression-p1.md` (roadmap) | Plan P1 exécuté et rollbacké — post-mortem en §1 de ce document |
| `1-roadmap-tracking-agnostic-autonomy-plugin-AUDIT.md` | Audit d'implémentation des axes — confirme la conformité v2.8.0 |

### C. Diagramme de chargement des modules (session S)

```
Tour 1   : [NOYAU] + [startup] + [planning]
Tour 2-6 : [NOYAU] + [planning]
Tour 7+  : [NOYAU] + [implementation]

Jamais chargé (plan S nouveau) :
  - workflow-resume.md
  - aide.md
  - grilling (dans planning, mais ignoré car S)
```

### D. Priorité d'implémentation recommandée

| Priorité | Levier | Effort | Impact | Dépendances |
|---|---|---|---|---|
| 🥇 **P1** | L1 — Scission modules | M | −34,2 % | Aucune |
| 🥈 **P2** | L3 — Compression noyau | S | −4,0 % | L1 (le noyau doit être défini) |
| 🥉 **P3** | L2 — Élimination tours | S | −15,1 % | L1 (les directives de phase doivent être dans les modules) |

> **Recommandation** : implémenter L1 en premier (impact maximal). L3 est
> un quick-win post-L1. L2 peut être implémenté indépendamment mais bénéficie
> de la clarté apportée par L1.
