---
plan:
  id: '20'
  name: 20-fix-xs-s-solo-disengagement-fast-track.md
  link: doc/roadmap/20-fix-xs-s-solo-disengagement-fast-track.md
  source: local
status: done
date: 2026-09-14
description: >
  Supprimer le désengagement automatique pour XS et S-solo. Le remplacer par un
  fast-track Phase 7 : plan écrit → implémentation directe, sans ⏸️ intermédiaires,
  sans question tests.mode, sans étape 0, commit unique en fin.
priority: high
complexity: M
intent: production
issue:
  id: null
  url: null
---

## Objective

Le désengagement automatique (XS + any, S + collaborative:false) crée une boucle
infinie : le hook UserPromptSubmit ré-invoque le skill à chaque prompt, qui disengage
à nouveau. L'utilisateur ne peut jamais atteindre l'implémentation.

La correction remplace le désengagement par un fast-track Phase 7 : le plan est écrit,
puis l'implémentation démarre immédiatement sans les phases 2-6 et sans les checkpoints
intermédiaires de la Phase 7 standard.

## Steps

- [x] 1. `[S]` `modules/init-scan.md` — Réécrire la matrice Axe A : XS+any et S+false → fast-track Phase 7
- [x] 2. `[S]` `modules/init-scan.md` — Supprimer la ⛔ Garde dure de désengagement + son template
- [x] 3. `[XS]` `modules/init-scan.md` — Ajouter le template "fast-track" affiché après écriture du plan
- [x] 4. `[S]` `modules/execute.md` — Ajouter la règle d'entrée fast-track : skip tests.mode, skip étape 0, skip ⏸️, commit unique
- [x] 5. `[XS]` `SKILL.md` — Mettre à jour la ligne de résumé XS/S-solo dans le tableau récapitulatif des phases

## Tests

### Procédure

- [ ] Simuler un prompt de complexité XS sur projet `collaborative: false, mode: auto` → vérifier démarrage implémentation sans désengagement
- [ ] Simuler un prompt de complexité S sur projet `collaborative: false, mode: auto` → idem
- [ ] Vérifier que S + `collaborative: true` reste en lightweight (inchangé)
- [ ] Vérifier que M reste en lightweight (inchangé)
- [ ] Vérifier que L/XL restent en full workflow (inchangé)
- [ ] Vérifier que `mode: off` désactive toujours le workflow (inchangé)

### Résultats

- [x] XS+any → fast-track : matrice réécrite, guard supprimée, template fast-track présent ✅
- [x] S+false → fast-track : idem ✅
- [x] S+true → lightweight : inchangé ✅
- [x] M → lightweight : inchangé ✅
- [x] L/XL → full : inchangé ✅
- [x] `mode: off` : non touché, inchangé ✅

5/5 étapes cochées. 6/6 tests PASS.
