## Prompt utilisé pour implémentation sans skill

A partir du fichier d'audit @doc/audits/0-roadmap-tracking-estimation-couts-tokens.md :

1. Crée un plan doc/audits/0-rationalisation-tokens-without-skill.md avec les étapes d'implémentation de la section "Priorité d'action suggérée"
2. Implémente toutes les étapes du plan
3. Une fois toutes les étapes implémentées :
   - Écris la procédure de tests E2E dans le plan
   - Exécute les tests E2E
   - Mets à jour le plan avec les résultats
4. Tests OK → consigne le succès dans le plan
5. Tests NOK → consigne l'échec dans le plan et arrête-toi

---

## Suivi tokens de la session :

claude --resume 7fd7b163-48db-422c-ac3d-362fc15412d8

https://obs.agentic-hub.inetum.network/project/cmqhrg3rk00111y0752kdsnjc/sessions/7fd7b163-48db-422c-ac3d-362fc15412d8

| Implementation | ID | Created At | Duration | Environment | Scores | User IDs | Traces | Total Cost | Usage |
|---|---|---|---|---|---|---|---|---|---|
| No skill | 7fd7b163-48db-422c-ac3d-362fc15412d8 | 2026-09-12 22:55:47 | 4m 52s | default | | emmanuel.houriez@inetum.com | 1 | $2.382006 | 2,995,656 → 20,748 (Σ 2,827,976) |

---

## Remarques d'un agent indépendant sur la conception du prompt (coût en token non comptabilisé)

### Ce qui est bon

| Point | Détail |
|---|---|
| Concis | 10 lignes, lisible d'un coup d'œil |
| Logique linéaire | Pas de branchement complexe — flux séquentiel clair |
| Stop-on-failure | L'agent sait qu'il doit s'arrêter en cas d'échec |
| Ton naturel | Ça sonne humain, pas spec |

### Points d'attention

| # | Passage | Remarque |
|---|---|---|
| 1 | « Implémente toutes les étapes du plan » | Sans le skill, l'agent risque de tout implémenter en un seul tour sans checkpoint intermédiaire. Si une étape casse la suivante, tu ne le sauras qu'aux tests E2E. C'est acceptable dans un contexte de comparaison de coûts — mais à noter |
| 2 | « Écris la procédure de tests E2E dans le plan » | L'agent doit inventer la procédure de tests. Sans indication de ce qui constitue un test valide pour une rationalisation de tokens, les tests risquent d'être superficiels (« le fichier a bien été modifié ») plutôt que probants (« le nombre de tokens a baissé de X% ») |
| 3 | Pas de mention du step 4 en cas de succès | Step 4 consigne le succès mais ne dit pas de s'arrêter — contrairement au step 5 qui dit explicitement « arrête-toi ». Mineur mais asymétrique |
| 4 | Pas d'instruction sur les commits | L'agent commit-il au fur et à mesure ? À la fin ? Jamais ? Sans skill, ce comportement n'est pas cadré |

---

## Comparaison

| Implementation | ID | Created At | Duration | Environment | Scores | User IDs | Traces | Total Cost | Usage |
|---|---|---|---|---|---|---|---|---|---|
| With /roadmap-tracking skill | 79424181-aff2-43ab-9be0-c6a5805e7b4a | 2026-09-12 23:17:03 | 12m 42s | default | | emmanuel.houriez@inetum.com | 1 | $4.10835 | 4,181,087 → 48,570 (Σ 3,872,586) |
| No skill | 7fd7b163-48db-422c-ac3d-362fc15412d8 | 2026-09-12 22:55:47 | 4m 52s | default | | emmanuel.houriez@inetum.com | 1 | $2.382006 | 2,995,656 → 20,748 (Σ 2,827,976) |