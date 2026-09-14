# Rapport d'analyse — Implémentation Plan #129
## Comparaison Sonnet 4.8 vs Opus 4.8 en contexte agentique (Claude Code)
**Date** : 2026-09-14
**Auteur** : Emmanuel Houriez
**Destinataires** : Thomas, Mathieu
**Projet** : Auxitum — Moteur d'exécution durci

---

## 1 — Résumé exécutif

Le [plan #129](https://github.com/ehouriez/auxitum/blob/main/doc/roadmap/129-hardened-execution-engine.md) — moteur d'exécution durci corrigeant 4 failles JARVIS (état volatil, process unique, RBAC hors moteur, injection shell) — a été **livré en une demi-journée** (10h51 → 14h21) pour un coût total de **$28,61** réparti sur 10 sessions Claude Code. La répartition modèle est de 6 sessions 🟦 Sonnet ($9,39 — 33%) et 4 sessions 🟧 Opus ($19,22 — 67%). L'ensemble du cycle de vie a été piloté par le **skill `/roadmap-tracking`**, qui assure la persistance du contexte entre sessions via le fichier de plan (`doc/roadmap/129-hardened-execution-engine.md`) et l'[issue GitHub #129](https://github.com/ehouriez/auxitum/issues/129) — chaque session dispose donc de l'historique complet des décisions, résultats et diagnostics précédents.

Malgré ce contexte partagé, **la phase de debug du test de réconciliation boot a révélé un écart critique entre les deux modèles** : 🟦 Sonnet a consommé 4 sessions et $6,76 en 43m20s sans identifier la root cause (un tag d'image Docker `:latest` au lieu de `:dev`), alors même que le plan consignait l'historique de chaque tentative. 🟧 Opus l'a trouvée et prouvée en 1 session ($8,19), en exploitant le même plan comme contexte. Le surcoût de l'errance Sonnet — $6,76 de sessions non productives — représente **24% du budget total du plan**. Le skill `/roadmap-tracking` avait d'ailleurs correctement recommandé Opus pour l'implémentation complexe (étapes 2-4, complexité L), recommandation validée par les résultats.

---

## 2 — Chronologie complète

### 2.1 Tableau des sessions

| # | Modèle | Heure début | Durée | Coût ($) | Tokens (in → out / Σ) | Phase skill | Résultat | Description | Lien Langfuse |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 🟦 Sonnet | 10:51:34 | 12m 05s | 2,05 | 2 829k → 24k (Σ 2 746k) | Implémentation | ✅ | Étape 1 : migration 005 + couche persistance | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/80ad1169-642b-42d9-834b-275fd568feb2) |
| 2 | 🟦 Sonnet | 11:20:01 | 0m 55s | 0,58 | 514k → 2k (Σ 436k) | Tests | ✅ | Tests étape 1 — tous verts | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/3d355f15-3d4a-4c85-8b03-51788b89cacf) |
| 3 | 🟧 Opus | 11:22:40 | 21m 22s | 6,55 | 5 818k → 39k (Σ 5 545k) | Implémentation | ✅ | Étapes 2+3+4 one-shot (complexité L, recommandation skill) | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/49992ca1-c314-4263-a42b-f7d5f5e2a8cd) |
| 4 | 🟧 Opus | 11:57:25 | 5m 56s | 2,16 | 1 219k → 14k (Σ 1 116k) | Tests | ⚠️ | Tests étapes 2-4 : A ✅, B ✅, C ❌ | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/027fdfb2-f09b-4e40-8f3a-616ffe0699fa) |
| 5 | 🟦 Sonnet | 12:16:38 | 7m 15s | 1,68 | 2 395k → 16k (Σ 2 314k) | Tests/Debug | ❌ | Diagnostic « décalage image » — ne tranche pas la root cause | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/64651671-fbcb-4ca7-84d5-ff638e56a355) |
| 6 | 🟦 Sonnet | 12:30:07 | 2m 40s | 1,09 | 1 283k → 9k (Σ 1 198k) | Tests/Fix | ⚠️ | Post-reset : C vert (faux positif¹), A échoue → mock fixé | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/28025e67-6c95-4ed2-812f-6caf25a32768) |
| 7 | 🟦 Sonnet | 12:48:54 | 7m 58s | 1,11 | 1 421k → 8k (Σ 1 336k) | Tests | ❌ | A ✅, C ❌ (container non recréé) | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/cf3fdfe7-7bc2-4b60-89b8-e72368ba3d18) |
| 8 | 🟦 Sonnet | 13:02:09 | 25m 27s | 2,88 | 2 520k → 37k (Σ 2 281k) | Tests/Debug | ❌ | --force-recreate, C ❌ encore. ⚠️ Blocage >12min | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/8a430b5f-5036-4e77-9576-e2a6e9b77d55) |
| 9 | 🟧 Opus | 13:41:22 | 26m 01s | 8,19 | 6 492k → 47k (Σ 6 081k) | Tests/Fix | ✅ | **Root cause trouvée** : tag `:latest` ≠ `:dev` → VERDICT PASS | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/940feac2-b083-495f-84ad-bb8962f864bb) |
| 10 | 🟧 Opus | 14:11:14 | 10m 25s | 2,32 | 1 660k → 12k (Σ 1 561k) | Validation/Fix | ✅ | Durcissement `AUXITUM_IMAGE_TAG` dans env.template | [session](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/a51e62cd-7bc4-478d-90b6-ddcdd753205d) |

> ¹ Le C vert de la session 6 était un faux positif : le `reset_dev` avait temporairement exporté `AUXITUM_IMAGE_TAG=dev`, masquant le problème de tag. Dès la session suivante sans ce contexte shell, C échouait à nouveau.

### 2.2 Timeline visuelle

```
10:51  11:00  11:10  11:20  11:30  11:40  11:50  12:00  12:10  12:20  12:30  12:40  12:50  13:00  13:10  13:20  13:30  13:40  13:50  14:00  14:10  14:20
  │      │      │      │      │      │      │      │      │      │      │      │      │      │      │      │      │      │      │      │      │      │
  ├──── 🟦 #1 ────┤    ├🟦#2┤                                                                                                                       
  │  Étape 1 impl │    │test│                                                                                                                       
  │    \$2,05  ✅  │    │\$0,58│                                                                                                                       
                        ├────────── 🟧 #3 ──────────┤         ├─ 🟧 #4 ─┤                                                                          
                        │   Étapes 2-4 one-shot      │         │ Tests   │                                                                          
                        │       \$6,55  ✅             │         │ \$2,16 ⚠️│                                                                          
                                                                          ├── 🟦 #5 ──┤├ 🟦#6 ┤         ├── 🟦 #7 ──┤├────────── 🟦 #8 ──────────┤
                                                                          │  Diag ❌   ││Fix ⚠️│         │  Test ❌   ││   Diag ❌  ⚠️ blocage      │
                                                                          │   \$1,68    ││\$1,09 │         │   \$1,11   ││       \$2,88                │
                                                                                                                      ├──────────── 🟧 #9 ────────────┤├──── 🟧 #10 ────┤
                                                                                                                      │  ROOT CAUSE TROUVÉE  ✅       ││ Fix définitif ✅│
                                                                                                                      │        \$8,19                  ││     \$2,32       │
  │◄─────────── IMPLÉMENTATION ──────────────►│◄──── TESTS ────►│◄────────────── BOUCLE DEBUG ─────────────────────────────────────────────────────────►│◄── HARDENING ──►│
  │          Sonnet + Opus : \$11,18            │  Opus : \$2,16   │     Sonnet : \$6,76 (perdu)     │      Opus : \$8,19 (résolu)                         │   Opus : \$2,32  │
```

### 2.3 Phases du skill `/roadmap-tracking` et correspondance sessions

Le skill `/roadmap-tracking` structure le cycle de vie d'un plan en 7 phases. Voici leur correspondance avec les sessions observées :

| Phase du skill | Sessions | Modèle(s) | Coût | Statut |
|---|---|---|---|---|
| ① Analyse & cadrage | Pré-session (2026-09-10) | — | — | Plan créé, 4 failles documentées, arbitrage réécriture tranché |
| ② Planification (étapes) | Pré-session | — | — | 4 étapes définies, complexité L |
| ③ Implémentation étape 1 | Sessions 1-2 | 🟦 Sonnet | \$2,63 | ✅ Migration 005 + persistance + tests verts |
| ④ Implémentation étapes 2-4 | Sessions 3-4 | 🟧 Opus (recommandation skill) | \$8,71 | ✅ Moteur complet livré, A+B verts, C ❌ |
| ⑤ Tests (boucle tests/fix) | Sessions 5-8 | 🟦 Sonnet | \$6,76 | ❌ 4 sessions sans root cause |
| ⑤ Tests (résolution) | Session 9 | 🟧 Opus | \$8,19 | ✅ Root cause trouvée, C vert |
| ⑥ Validation | Session 10 | 🟧 Opus | \$2,32 | ✅ Fix définitif, plan clôturé `done` |
| ⑦ Clôture | Session 10 | 🟧 Opus | (inclus) | ✅ Post-mortem rédigé dans le plan |

**Point clé** : le skill `/roadmap-tracking` assure que **chaque session dispose du plan complet comme contexte** — incluant le journal de session, les résultats des tests (attendus vs observés), les diagnostics précédents et les hypothèses éliminées. Ce contexte persisté entre sessions signifie que l'échec de Sonnet en phase ⑤ **n'est pas imputable à une perte de contexte** : Sonnet avait accès à l'historique complet de l'errance via le plan. C'est sa **capacité de raisonnement** qui est en cause, pas son contexte.

---

## 3 — Analyse comparative Sonnet vs Opus

### 3.1 Synthèse chiffrée

| Métrique | 🟦 Sonnet 4.8 | 🟧 Opus 4.8 | Ratio Opus/Sonnet |
|---|---|---|---|
| Nombre de sessions | 6 | 4 | — |
| Durée cumulée | 56m 20s | 63m 44s | ×1,13 |
| Coût cumulé ($) | \$9,39 | \$19,22 | ×2,05 |
| Tokens input cumulés | 10 962k | 15 189k | ×1,39 |
| Tokens output cumulés | 96k | 112k | ×1,17 |
| Tokens total (Σ) | 10 311k | 14 303k | ×1,39 |
| Coût moyen / session | \$1,57 | \$4,81 | ×3,06 |
| Coût moyen / minute | \$0,17 | \$0,30 | ×1,79 |
| Sessions avec résultat définitif² | 2 / 6 (33%) | 4 / 4 (100%) | ×3,0 |

> ² **Résultat définitif** = session ayant produit un avancement irréversible (code livré, test concluant, root cause identifiée, fix appliqué). Les sessions 5, 6, 7, 8 (Sonnet debug) n'ont produit aucun résultat définitif sur le problème principal (bloc C), malgré un accès complet au contexte du plan via le skill `/roadmap-tracking`.

### 3.2 Analyse par phase

#### Phase Implémentation

| Aspect | Détail |
|---|---|
| **🟦 Sonnet (session 1)** | Étape 1 — migration 005 + `operationStore.js`. Tâche bien cadrée par le plan (schéma SQL + CRUD, périmètre défini). Livré en 12m05s pour \$2,05. **Résultat parfait**, tous tests verts dès la première exécution. |
| **🟧 Opus (session 3)** | Étapes 2+3+4 en one-shot — moteur durci complet, SSE, réconciliation boot, variableSchema, tests unitaires + smoke E2E. **Recommandation du skill `/roadmap-tracking`** qui avait estimé la complexité cumulée à L et préconisé Opus. Livré en 21m22s pour \$6,55. **Résultat parfait** : 154/154 tests unitaires verts, architecture complète (EventEmitter, RBAC intra-moteur, quoting sûr, buffers bornés). |
| **Coût phase** | \$8,60 (Sonnet \$2,05 + \$0,58 / Opus \$6,55) |
| **Analyse** | Sonnet est efficace sur une tâche isolée de complexité modérée. Opus a été choisi sur recommandation du skill pour le lot complexe (3 étapes L en one-shot) et a livré sans erreur. **La recommandation du skill est validée** : le rapport complexité/coût d'Opus est excellent quand la tâche est large et cohérente. |

#### Phase Tests

| Aspect | Détail |
|---|---|
| **🟦 Sonnet (session 2)** | Tests étape 1 — exécution de la procédure documentée dans le plan. 55s, \$0,58. Parfait. |
| **🟧 Opus (session 4)** | Tests étapes 2-4 — blocs A+B verts, C échoue (race condition procédure puis tag image). Opus a identifié la race condition immédiatement et corrigé la procédure (ajout health-check wait). Résultats consignés dans le plan. \$2,16. |
| **Coût phase** | \$2,74 |
| **Analyse** | Les deux modèles exécutent correctement des procédures de test documentées dans le plan. L'échec du bloc C n'est imputable à aucun des deux — c'est un problème d'environnement (tag image). |

#### Phase Debug/Fix (boucle tests/fix du skill)

| Aspect | Détail |
|---|---|
| **🟦 Sonnet (sessions 5-8)** | 4 sessions dans la boucle tests/fix du skill. Le plan était mis à jour entre chaque session avec les résultats observés, les hypothèses testées et les pistes éliminées. Malgré ce contexte riche, Sonnet a produit des diagnostics partiels (« décalage image », stale rows, container non recréé) et des fix de surface (`--force-recreate`, mock `playbooks.js`), mais **n'a jamais inspecté le contenu réel de l'image Docker**. Session 8 bloquée >12min. |
| **🟧 Opus (sessions 9-10)** | 2 sessions. Session 9 : diagnostic systématique en lisant le plan (qui contenait l'historique complet des 4 échecs Sonnet) — grep du `server.js` et `operationStore.js` **dans le conteneur**, preuve que l'image `:latest` v1.1.1 (pré-#129) ne contient pas le code de réconciliation → root cause tranchée, pull `:dev` → PASS immédiat. Session 10 : correctif définitif (`env.template`) + post-mortem. |
| **Coût phase** | \$17,27 (dont \$6,76 perdus en errance Sonnet) |
| **Analyse** | Le plan consigné par le skill `/roadmap-tracking` fournissait à chaque session le **même contexte riche** : diagnostics précédents, hypothèses éliminées, résultats observés. L'écart entre Sonnet et Opus n'est donc **pas** un problème de contexte — c'est un écart de **capacité de raisonnement transversal**. Opus a su exploiter le plan et les indices accumulés pour formuler l'hypothèse décisive (inspecter l'artefact runtime). Sonnet a relu les mêmes informations 4 fois sans franchir ce cap. |

### 3.3 Le point de bascule : la boucle debug

C'est **l'événement central** de cette implémentation et le principal enseignement pour l'arbitrage Sonnet/Opus.

#### Le rôle du skill `/roadmap-tracking` dans la boucle

Le skill `/roadmap-tracking` maintient dans le plan un **journal de session** et un **tableau de résultats de tests** mis à jour après chaque session. Concrètement, à l'entrée de chaque session de debug, le modèle avait accès à :

- La procédure de test complète (blocs A, B, C) avec résultats attendus
- Le tableau des résultats observés (✅/❌) pour chaque rejeu
- L'analyse cumulative documentant les causes 1 et 2
- Les hypothèses explicitement éliminées (race condition, stale rows)
- Les entrées du journal décrivant chaque session précédente

**Ce contexte annule l'argument de l'amnésie inter-sessions.** Le skill est conçu précisément pour cela : permettre à n'importe quel modèle, à n'importe quelle session, de reprendre le travail là où la session précédente l'a laissé.

#### Chronologie de l'errance Sonnet (sessions 5-8) — avec contexte plan disponible

| Session | Contexte disponible dans le plan | Hypothèse explorée par Sonnet | Action | Root cause ? |
|---|---|---|---|---|
| 5 | Journal session 4 : A ✅, B ✅, C ❌, race condition identifiée | « Décalage image » (intuition correcte mais non prouvée) | Relance tests unitaires (qui passent déjà) | ❌ Intuition abandonnée |
| 6 | + Journal session 5 : diagnostic « décalage image » sans preuve | Reset from scratch, rejeu complet | C vert (faux positif), A ❌ (mock) → fix mock | ❌ Faux positif masque le problème |
| 7 | + Journal session 6 : C vert (après reset), A fixé | Rejeu post-fix mock | A ✅, C ❌ (container non recréé) | ❌ |
| 8 | + Journal session 7 : C ❌ « container non recréé » | `--force-recreate` | C ❌ encore. Blocage >12min | ❌ 4ème tentative |

**Coût cumulé de l'errance** : \$6,76 / 43m20s / 0 résultat sur le problème principal.

**Fait aggravant** : la session 5 a effleuré la bonne piste (« décalage image »), et cette piste était **consignée dans le plan** pour les sessions suivantes. Sonnet l'a lue à chaque session sans jamais la transformer en diagnostic prouvé. Il aurait suffi d'exécuter `docker exec auxitum-orchestrator grep reconcileOrphanedRuns /app/server.js` pour trancher — cette commande n'a été jouée dans aucune des 4 sessions.

#### Résolution Opus (session 9) — avec le même contexte plan

| Étape du diagnostic Opus | Action | Résultat |
|---|---|---|
| 1 | Lecture du plan : 4 échecs documentés, piste « décalage image » effleurée mais non prouvée | Formulation de l'hypothèse décisive : le conteneur ne contient peut-être pas le code |
| 2 | Inspection de l'image dans le conteneur : version, révision, contenu `server.js` | Image `:latest` v1.1.1 rév `164ecf10` (2026-09-10, **pré-#129**) |
| 3 | Grep `reconcileOrphanedRuns` dans `/app/server.js` | **Absent** |
| 4 | Vérification existence `/app/lib/operations/operationStore.js` | **Inexistant** |
| 5 | Vérification nombre de migrations | 4 (pas 5) — migration 005 absente de l'image |
| 6 | Pull explicite de `:dev` + restart | **VERDICT PASS immédiat** |

**Coût de la résolution** : \$8,19 / 26m01s / root cause identifiée, prouvée et résolue.

**Observation clé** : Opus a exploité le contexte du plan (les 4 échecs documentés, la piste « décalage image ») pour formuler directement l'hypothèse que Sonnet n'a pas su transformer en action. Le skill `/roadmap-tracking` a donc **servi Opus mais pas Sonnet** — le contexte persisté est un accélérateur pour un modèle capable de l'exploiter, mais pas un substitut à la capacité de raisonnement.

#### Calcul du surcoût de l'errance Sonnet

| Métrique | Valeur |
|---|---|
| Coût des sessions Sonnet debug (5-8) | \$6,76 |
| Temps passé en sessions Sonnet debug | 43m 20s |
| Temps humain perdu (attente + supervision + relances) | ~1h25 (12:16 → 13:41) |
| Résultats produits sur le problème C | 0 |
| **Surcoût net si Opus avait été utilisé dès la session 5** | **\$6,76 évités** |

### 3.4 Forces et faiblesses observées

| Dimension | 🟦 Sonnet 4.8 | 🟧 Opus 4.8 |
|---|---|---|
| **Implémentation simple** (étape 1 : migration + CRUD) | ✅ Excellent — rapide, bon marché (\$2,05), résultat parfait | Non testé sur ce type de tâche (capable a fortiori) |
| **Implémentation complexe** (étapes 2-4 one-shot, complexité L) | Non testé (jugé inadapté par le skill `/roadmap-tracking`) | ✅ Excellent — 3 étapes en 1 session, architecture complète, 154 tests verts |
| **Tests de validation** (exécution de procédures du plan) | ✅ Correct — exécute fidèlement les procédures | ✅ Correct — exécute et adapte la procédure en cas d'échec |
| **Diagnostic de root cause** (problème transverse code/infra, avec contexte plan complet) | ❌ **Échec** — 4 sessions malgré le contexte plan, diagnostics superficiels, aucune inspection d'artefact runtime | ✅ **Succès** — 1 session, exploite le contexte plan pour formuler l'hypothèse décisive, diagnostic par preuve matérielle |
| **Exploitation du contexte plan** (skill `/roadmap-tracking`) | ⚠️ Lit le plan mais ne capitalise pas sur les pistes documentées — la piste « décalage image » effleurée en session 5 n'est jamais approfondie malgré sa présence dans le journal | ✅ Lit le plan et en extrait les informations critiques — les 4 échecs documentés orientent directement le diagnostic |
| **Fix correctif + durcissement** | ⚠️ Fix collatéraux corrects (mock, --force-recreate) | ✅ Root cause corrigée + durcissement préventif (env.template) + post-mortem |
| **Stabilité de session** | ⚠️ Session 8 bloquée >12min, exit+resume nécessaire | Pas de blocage observé (signalé comme pouvant arriver aussi) |
| **Rapport coût/efficacité** | ⚠️ Excellent sur tâches cadrées (\$0,17/min) ; **catastrophique en debug non trivial** (\$6,76 pour 0 résultat) | Coût unitaire plus élevé (\$0,30/min) mais **100% de taux de résolution** → meilleur ROI net |

---

## 4 — Analyse des coûts

### 4.1 Ventilation détaillée

| Poste | Coût ($) | % du total |
|---|---|---|
| **Coût total plan #129** | **\$28,61** | 100% |
| ├─ 🟦 Sonnet (6 sessions) | \$9,39 | 32,8% |
| │  ├─ Implémentation + tests étape 1 (sessions 1-2) | \$2,63 | 9,2% |
| │  └─ **Boucle debug infructueuse (sessions 5-8)** | **\$6,76** | **23,6%** |
| ├─ 🟧 Opus (4 sessions) | \$19,22 | 67,2% |
| │  ├─ Implémentation étapes 2-4 (session 3) | \$6,55 | 22,9% |
| │  ├─ Tests initiaux (session 4) | \$2,16 | 7,5% |
| │  ├─ Résolution root cause (session 9) | \$8,19 | 28,6% |
| │  └─ Fix définitif + validation (session 10) | \$2,32 | 8,1% |

**Fait saillant** : les \$6,76 de la boucle debug Sonnet représentent presque un quart du budget total. Ces sessions n'ont produit aucun résultat sur le problème principal, alors même que le skill `/roadmap-tracking` fournissait un contexte complet. En comparaison, Opus a résolu le problème + implémenté un fix préventif pour \$10,51 (sessions 9+10).

### 4.2 Scénarios contrefactuels

#### Scénario A — « Tout Sonnet » (Opus jamais utilisé)

| Hypothèse | Estimation |
|---|---|
| Implémentation étapes 2-4 avec Sonnet | Sonnet aurait probablement nécessité 3 sessions distinctes au lieu de 1 Opus. Estimation : 3 × ~$2,00 = ~$6,00 (vs $6,55 Opus — coût comparable). Risque : qualité architecturale potentiellement inférieure sur un lot L one-shot, et le skill `/roadmap-tracking` aurait dû séquencer en 3 sessions distinctes plutôt qu'un one-shot, ajoutant du temps humain. |
| Debug bloc C | Sonnet n'a montré aucune progression vers la root cause en 4 sessions, malgré un contexte plan complet et des diagnostics accumulés. Le problème (tag image) est un problème d'infrastructure que Sonnet ne sait pas diagnostiquer par preuve. **Estimation conservatrice : 4 à 8 sessions supplémentaires**, soit $6 à $12 de plus, sans garantie de résolution. Scénario probable : intervention humaine manuelle pour trancher après épuisement du budget de patience. |
| **Coût estimé scénario A** | **$22 à $28+** (sans certitude de livraison du bloc C). Le budget aurait pu dépasser celui observé, **avec un risque significatif de non-livraison**. |

#### Scénario B — « Opus dès le debug » (escalade immédiate après session 4)

| Élément | Coût réel | Coût scénario B | Économie |
|---|---|---|---|
| Sessions 1-4 (identiques) | $11,34 | $11,34 | — |
| Sessions 5-8 (Sonnet debug) | $6,76 | **$0,00** (supprimées) | **+$6,76** |
| Session 9 (Opus debug) | $8,19 | $8,19 | — |
| Session 10 (Opus fix) | $2,32 | $2,32 | — |
| **Total** | **$28,61** | **$21,85** | **$6,76 économisés (−23,6%)** |
| **Temps humain économisé** | — | — | **~1h25** (12:16 → 13:41) |

> **Scénario B est le scénario optimal observé.** Il suppose qu'Opus aurait trouvé la root cause même sans les informations collectées par Sonnet — hypothèse raisonnable : Opus a diagnostiqué par inspection directe de l'artefact, sans exploiter les résultats Sonnet autrement que via le plan (qui aurait contenu les résultats de la session 4 de toute façon).

#### Scénario C — « Tout Opus » (Opus pour toutes les sessions)

| Élément | Estimation |
|---|---|
| Sessions 1-2 (étape 1, Sonnet → Opus) | Ratio coût Opus/Sonnet observé sur implémentation : ×3,19 ($6,55 / 21m vs $2,05 / 12m). Estimation : ~$4,00 à $5,00 pour l'étape 1 en Opus (tâche simple, surcoût principalement lié au prix/token). Tests : ~$1,50. |
| Sessions 3-4 (déjà Opus) | $8,71 (inchangé) |
| Sessions 5-8 (n'auraient pas eu lieu) | $0,00 |
| Sessions 9-10 (déjà Opus) | $10,51 (inchangé) |
| **Coût estimé scénario C** | **~$24,72 à $25,72** |

#### Synthèse des scénarios

| Scénario | Coût estimé | Durée humaine estimée | Risque | Commentaire |
|---|---|---|---|---|
| **Réel** (mixte, escalade tardive) | $28,61 | ~3h30 (10:51 → 14:21) | Aucun (livré) | Surcoût dû à 4 sessions Sonnet improductives |
| **A — Tout Sonnet** | $22 à $28+ | >4h | **Élevé** : root cause possiblement jamais trouvée | Le skill aurait accumulé les échecs dans le plan sans que Sonnet progresse |
| **B — Opus dès le debug** | **$21,85** | **~2h05** | Faible | **Scénario optimal** — le skill `/roadmap-tracking` aurait dû recommander Opus pour le debug |
| **C — Tout Opus** | ~$25,00 | ~2h05 | Faible | Surcoût modéré sur tâches simples, mais pas d'errance |

**Conclusion coûts** : le scénario B (mixte avec escalade immédiate) est le plus efficient. Le scénario C (tout Opus) est acceptable et élimine tout risque d'errance. Le scénario A (tout Sonnet) est le pire en termes de risque. **Le skill `/roadmap-tracking` devrait intégrer une règle d'escalade automatique vers Opus dans sa phase tests/fix.**

### 4.3 Ratio coût/résolution

| Catégorie | Sessions | Coût | Résultats produits | Coût / résultat |
|---|---|---|---|---|
| Sessions productives (1, 2, 3, 4, 9, 10) | 6 | $21,85 | 6 (impl. étape 1, tests étape 1, impl. étapes 2-4, tests initiaux, root cause, fix définitif) | **$3,64 / résultat** |
| Sessions d'errance (5, 6, 7, 8) | 4 | $6,76 | 0 sur le problème principal³ | **∞** (investissement perdu) |
| **Toutes sessions** | **10** | **$28,61** | **6** | **$4,77 / résultat** |

> ³ La session 6 a produit un fix collatéral utile (mock `playbooks.js`), mais ce fix aurait aussi été identifié et résolu dans une session Opus.

**Lecture directe** : chaque dollar investi dans Opus a produit un résultat. Près d'un quart des dollars investis dans Sonnet (hors implémentation initiale) n'a rien produit — et ce malgré un contexte plan complet fourni par le skill.

---

## 5 — Problèmes opérationnels observés

### 5.1 Sessions bloquées

| Incident | Session | Modèle | Durée du blocage | Impact | Workaround |
|---|---|---|---|---|---|
| Session ne rend pas la main | #8 (🟦 Sonnet) | Sonnet 4.8 | >12min | Temps humain perdu en attente, incertitude sur l'état de la session | `exit` + relance Claude Code + `resume` + saisie manuelle `"continue"` → reprise après 3m56s supplémentaires |

**Fréquence observée** : 1 occurrence sur 10 sessions (10%). L'opérateur signale que « cela arrive souvent que ce soit avec Sonnet ou Opus » — le problème n'est donc pas spécifique à un modèle mais constitue un risque opérationnel récurrent de Claude Code en mode agentique.

**Impact** : la session 8 a duré 25m27s au total dont >12min de blocage improductif. Sans le blocage, la durée utile aurait été ~10min. Le blocage a donc **plus que doublé** la durée de la session et retardé d'autant l'escalade vers Opus.

**Recommandation** : mettre en place un timeout de supervision (e.g. 8-10min sans output) au-delà duquel l'opérateur interrompt systématiquement la session. Le coût d'un `exit` + `resume` est négligeable comparé au coût d'attente passive.

### 5.2 Le skill `/roadmap-tracking` comme mécanisme de persistance inter-sessions

Contrairement à un usage « brut » de Claude Code où le `/clear` provoque une perte totale de contexte, le workflow piloté par le skill `/roadmap-tracking` assure une **continuité structurée** entre sessions :

| Mécanisme du skill | Ce qui est persisté | Où |
|---|---|---|
| Journal de session | Résumé de chaque session (fait / prochain) | `doc/roadmap/129-hardened-execution-engine.md` § Journal |
| Tableau de résultats de tests | Résultats attendus vs observés, verdict par test | `doc/roadmap/129-hardened-execution-engine.md` § Tests |
| Analyse cumulative | Causes identifiées, hypothèses éliminées, diagnostic en cours | `doc/roadmap/129-hardened-execution-engine.md` § Tests (bloc ⚠️) |
| Issue GitHub | Statut, commentaires de progression | [Issue #129](https://github.com/ehouriez/auxitum/issues/129) |

**Ce que le `/clear` détruit** : uniquement la mémoire conversationnelle intra-session (le « chat »). Le skill compense intégralement cette perte par le plan fichier.

**Ce que le skill ne compense pas** : la capacité intrinsèque du modèle à exploiter les informations persistées. C'est là que l'écart Sonnet/Opus se manifeste le plus clairement — avec le même plan, Opus extrait et agit sur les informations critiques, Sonnet les lit sans les transformer en action décisive.

### 5.3 Capitalisation inter-sessions : Sonnet vs Opus face au même plan

| Comportement observé | 🟦 Sonnet | 🟧 Opus |
|---|---|---|
| Lecture du plan et du journal de session | ✅ Oui | ✅ Oui |
| Reprise de la bonne phase du workflow | ✅ Oui (rejeu des tests) | ✅ Oui |
| Identification des hypothèses déjà éliminées | ⚠️ Partielle — re-explore des pistes déjà infirmées | ✅ Complète — élimine les pistes documentées comme écartées |
| Synthèse transversale du plan (lier les indices entre eux) | ❌ Non — traite chaque indice isolément | ✅ Oui — relie « décalage image » (session 5) + « `:latest` par défaut » (docker-compose) + « smoke B passe mais C non » |
| Formulation d'hypothèse nouvelle à partir du contexte accumulé | ❌ Non — reste dans le même cadre (code source) | ✅ Oui — sort du cadre pour inspecter l'artefact runtime |

**Enseignement pour le skill** : le contexte persisté par `/roadmap-tracking` est une condition nécessaire mais non suffisante. Le skill devrait intégrer une **règle d'escalade modèle** dans sa phase tests/fix, basée sur le nombre d'échecs consécutifs consignés dans le plan.

### 5.4 Nature du problème : au-delà du code

Le problème de tag image est un **problème d'infrastructure transversal** impliquant l'interaction entre :
- `docker-compose.yml` (variable `${AUXITUM_IMAGE_TAG:-latest}`)
- `update.sh` (chaîne de résolution `shell env > .env > défaut`)
- `env.template.*` (absence de déclaration de la variable)
- Le registre d'images (`ghcr.io`, tags `:dev` vs `:latest`)
- Le comportement de `docker compose --force-recreate` (ne pull pas)

Ce type de problème **traverse les couches** (code applicatif, configuration, CI/CD, runtime Docker). Il nécessite de :
1. Remettre en question l'hypothèse implicite « le code déployé = le code committé »
2. Inspecter l'artefact réel en cours d'exécution
3. Comprendre la chaîne de résolution des variables d'environnement Docker

Sonnet a raisonné exclusivement dans le périmètre du code source (analyse statique, hypothèses de bugs de code, corrections de procédure). Opus a raisonné sur l'ensemble de la chaîne de déploiement. **Le plan documentait pourtant le fait que le code n'est pas bind-monté** (`docker-compose.yml:123-129`, noté dans le journal de la session 8) — mais Sonnet n'a pas tiré la conclusion qui s'imposait.

---

## 6 — Recommandations

### 6.1 Stratégie de sélection de modèle

| Type de tâche | Modèle recommandé | Justification (observée sur #129) |
|---|---|---|
| **Implémentation simple** (1 étape, complexité S/M, périmètre bien défini) | 🟦 **Sonnet** | Session 1 : résultat parfait pour $2,05. Le skill `/roadmap-tracking` cadre la tâche, Sonnet l'exécute. |
| **Implémentation complexe** (multi-étapes, complexité L, architecture transverse) | 🟧 **Opus** | Session 3 : 3 étapes en 1 session. La recommandation du skill était correcte. |
| **Exécution de tests** (procédures documentées dans le plan) | 🟦 **Sonnet** | Session 2 : exécution fidèle pour $0,58. Sonnet suit les procédures du plan. |
| **Debug trivial** (erreur de syntaxe, import manquant, fix local) | 🟦 **Sonnet** | Session 6 : fix du mock correct. |
| **Debug non trivial** (root cause non évidente, problème transverse code/infra/CI) | 🟧 **Opus** | Sessions 5-8 vs 9 : Sonnet échoue sur 4 sessions malgré le contexte plan, Opus résout en 1. |
| **Durcissement / fix préventif** (correction structurelle) | 🟧 **Opus** | Session 10 : correctif `env.template` propre, post-mortem documenté. |

### 6.2 Règle d'escalade — intégration au skill `/roadmap-tracking`

**Règle proposée : « 2 strikes and escalate »**

```
SI   la phase tests/fix du skill enregistre un échec sur le même bloc de test
ET   la session suivante (même modèle) échoue à nouveau sur le même bloc
ALORS  le skill recommande une escalade vers Opus pour la session suivante.
```

**Implémentation dans le skill** : le journal de session du plan contient déjà les verdicts par bloc de test. Le skill pourrait détecter automatiquement 2 ❌ consécutifs sur le même bloc et insérer une recommandation d'escalade dans la section « Prochain » du journal.

**Justification chiffrée sur #129** :

| Moment d'escalade | Sessions Sonnet perdues | Coût perdu | Temps perdu |
|---|---|---|---|
| Après session 5 (1 strike) | 1 | $1,68 | 7m 15s |
| **Après session 6 (2 strikes)** — seuil proposé | **2** | **$2,77** | **9m 55s** |
| Après session 7 (3 strikes) | 3 | $3,88 | 17m 53s |
| Après session 8 (4 strikes) — réel | 4 | $6,76 | 43m 20s |

Avec la règle « 2 strikes », l'économie sur #129 aurait été de **$3,99** et **~33min** de temps humain.

**Critères d'escalade immédiate (bypass de la règle 2 strikes)** :
- Le problème implique l'interaction entre code et infrastructure (Docker, CI/CD, registre d'images)
- La session Sonnet produit un diagnostic sans preuve matérielle (hypothèse non vérifiée)
- La session Sonnet bloque >10min sans output
- Le plan consigne une piste pertinente non exploitée par les sessions précédentes

### 6.3 Optimisations possibles

#### 6.3.1 Enrichir le skill `/roadmap-tracking` avec une section « diagnostic structuré »

**Problème observé** : le journal de session est un log libre. Les hypothèses éliminées, les pistes ouvertes et les vérifications manquantes ne sont pas structurées de manière à guider le modèle suivant.

**Solution** : ajouter dans le plan une section dédiée lors de la phase tests/fix :

```markdown
## Diagnostic en cours — bloc C
### Hypothèses éliminées
- [ ] Race condition procédure → fixée (health-check wait)
- [ ] Stale rows en DB → infirmée (pre-cleanup = 0/0)
### Piste ouverte (non vérifiée)
- [ ] ⚠️ L'image Docker en cours contient-elle le code de réconciliation ?
### Vérification à jouer
- `docker exec auxitum-orchestrator grep reconcileOrphanedRuns /app/server.js`
```

Ce format structuré aide même Sonnet à identifier les vérifications manquantes et réduit le risque de re-explorer des pistes éliminées.

#### 6.3.2 Automatiser la détection de dérive d'artefact

Le problème de tag image est systémique. Le correctif `env.template` (session 10) le résout pour `AUXITUM_IMAGE_TAG`, mais d'autres variables pourraient présenter le même pattern.

**Recommandation** : ajouter au démarrage de l'orchestrateur un log structuré indiquant la version, la révision Git et le tag d'image — vérifiable automatiquement par les procédures de test du skill.

#### 6.3.3 Budget prévisionnel par complexité de plan

Basé sur l'expérience #129, proposition de grille budgétaire intégrable au skill `/roadmap-tracking` :

| Complexité plan | Budget implémentation | Budget tests | Budget debug (provision) | Budget total estimé |
|---|---|---|---|---|
| S (Small) | $2-4 (🟦 Sonnet) | $1-2 (🟦 Sonnet) | $2-4 (🟦 Sonnet) | **$5-10** |
| M (Medium) | $4-8 (🟦 Sonnet) | $2-3 (🟦 Sonnet) | $4-8 (🟦, escalade 🟧 si 2 strikes) | **$10-19** |
| L (Large) | $6-10 (🟧 Opus) | $2-4 (mixte) | $8-12 (🟧 Opus direct si infra) | **$16-26** |
| XL (Extra-Large) | $10-20 (🟧 Opus) | $4-8 (mixte) | $10-16 (🟧 Opus) | **$24-44** |

Le plan #129 (L) a coûté $28,61, légèrement au-dessus de la fourchette haute — la différence ($2,61) correspond précisément à l'excédent de la boucle d'errance Sonnet. Avec la règle « 2 strikes », le coût aurait été ~$24,62 — dans la fourchette.

---

## 7 — Annexes

### 7.1 Sessions Langfuse (tableau cliquable)

| # | Session ID | Modèle | Phase | Coût ($) | Lien |
|---|---|---|---|---|---|
| 1 | `80ad1169` | 🟦 Sonnet | Implémentation | 2,05 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/80ad1169-642b-42d9-834b-275fd568feb2) |
| 2 | `3d355f15` | 🟦 Sonnet | Tests | 0,58 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/3d355f15-3d4a-4c85-8b03-51788b89cacf) |
| 3 | `49992ca1` | 🟧 Opus | Implémentation | 6,55 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/49992ca1-c314-4263-a42b-f7d5f5e2a8cd) |
| 4 | `027fdfb2` | 🟧 Opus | Tests | 2,16 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/027fdfb2-f09b-4e40-8f3a-616ffe0699fa) |
| 5 | `64651671` | 🟦 Sonnet | Debug | 1,68 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/64651671-fbcb-4ca7-84d5-ff638e56a355) |
| 6 | `28025e67` | 🟦 Sonnet | Debug/Fix | 1,09 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/28025e67-6c95-4ed2-812f-6caf25a32768) |
| 7 | `cf3fdfe7` | 🟦 Sonnet | Tests | 1,11 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/cf3fdfe7-7bc2-4b60-89b8-e72368ba3d18) |
| 8 | `8a430b5f` | 🟦 Sonnet | Debug | 2,88 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/8a430b5f-5036-4e77-9576-e2a6e9b77d55) |
| 9 | `940feac2` | 🟧 Opus | Debug/Fix | 8,19 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/940feac2-b083-495f-84ad-bb8962f864bb) |
| 10 | `a51e62cd` | 🟧 Opus | Fix définitif | 2,32 | [Ouvrir](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/a51e62cd-7bc4-478d-90b6-ddcdd753205d) |

### 7.2 Références projet

| Ressource | Lien |
|---|---|
| Plan #129 (fichier roadmap) | [129-hardened-execution-engine.md](https://github.com/ehouriez/auxitum/blob/main/doc/roadmap/129-hardened-execution-engine.md) |
| Issue GitHub #129 | [github.com/ehouriez/auxitum/issues/129](https://github.com/ehouriez/auxitum/issues/129) |
| Plateforme d'observabilité (Langfuse) | [obs.agentic-hub.inetum.network](https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc) |

### 7.3 Glossaire

| Terme | Définition |
|---|---|
| **Skill `/roadmap-tracking`** | Skill Claude Code qui structure le cycle de vie d'un plan en 7 phases (analyse, cadrage, planification, implémentation, tests, validation, clôture). Maintient un contexte persisté dans le fichier de plan (`doc/roadmap/{issue}-slug.md`) et l'issue GitHub, permettant la continuité entre sessions réinitialisées par `/clear`. Recommande le modèle adapté (Sonnet/Opus) selon la complexité estimée. |
| **`/clear`** | Commande Claude Code qui réinitialise la mémoire conversationnelle de la session. N'affecte pas les fichiers (plan, code, tests). Utilisé entre chaque session pour garantir un contexte propre. Le skill `/roadmap-tracking` compense cette réinitialisation via le plan fichier. |
| **Langfuse** | Plateforme d'observabilité des LLM utilisée pour tracer chaque session Claude Code (durée, coût, tokens, modèle). |
| **Plan** | Fichier Markdown structuré (`doc/roadmap/129-*.md`) servant de spécification, de journal de session et de rapport de tests. Source de vérité partagée entre toutes les sessions d'un même plan. |
| **Complexité L** | Complexité « Large » dans l'échelle du skill (S/M/L/XL). Indique un plan nécessitant plusieurs étapes d'implémentation, une architecture transverse et des tests multi-blocs. Le skill recommande Opus pour les implémentations de complexité ≥ L. |
| **One-shot** | Mode d'implémentation où plusieurs étapes sont livrées en une seule session Claude Code. Recommandé par le skill pour Opus quand les étapes sont cohérentes et que la complexité le justifie. |
| **Root cause** | Cause racine d'un problème. Sur #129 : la variable `AUXITUM_IMAGE_TAG` n'était pas persistée dans `.env`, provoquant l'utilisation silencieuse de l'image `:latest` (prod, pré-#129) au lieu de `:dev`. |
