# Index de la documentation — roadmap-tracking

> Généré par retro-doc v2 · Langue : français · Base : `doc/retro/`

---

## Tableau des entités

| Statut | Identifiant | Description | Référence | Explication |
|--------|-------------|-------------|-----------|-------------|
| ✅ | `skill-core` | Skill principal — workflow à 7 phases, règles absolues, matrice d'applicabilité, signaux de mode et capitalisation du contexte inter-sessions | [→](reference-skill-core.md) | [→](explanation-skill-core.md) |
| ✅ | `module-init-scan` | Module d'initialisation et de scan — garde d'entrée universelle, création de `doc/roadmap/` et matrice d'auto-calibrage Axe A | [→](reference-module-init-scan.md) | [→](explanation-module-init-scan.md) |
| ✅ | `module-plan` | Module de planification (phases 2-4) — cadrage interactif, grilling adaptatif à frontier illimitée, proposition de plan et gate de recommandation modèle | [→](reference-module-plan.md) | [→](explanation-module-plan.md) |
| ✅ | `module-execute` | Module d'exécution (phases 5-7) — création du fichier plan et de l'issue GitHub, implémentation étape par étape, tests et validation | [→](reference-module-execute.md) | [→](explanation-module-execute.md) |
| ✅ | `module-wrapup` | Module de clôture et de reprise — clôture d'un plan validé, workflow de reprise d'un plan existant et capitalisation encadrée vers `CONTEXT.md` | [→](reference-module-wrapup.md) | [→](explanation-module-wrapup.md) |
| ✅ | `scripts-python` | Cinq scripts Python autonomes (`build_roadmap`, `doctor`, `normalize_status`, `split_context`, `migrate_plan_ids`) — génération de l'index et du roadmap, audit d'intégrité, normalisation et migration | [→](reference-scripts-python.md) | [→](explanation-scripts-python.md) |
| ✅ | `hooks-system` | Hooks `SessionStart`/`UserPromptSubmit`/`PreToolUse` pour Claude Code et Codex — déclenchement automatique du skill et garde anti-bypass en écriture | [→](reference-hooks-system.md) | [→](explanation-hooks-system.md) |
| ✅ | `references` | Sept fichiers de référence chargés à la demande (`environment`, `forms`, `templates`, `roadmap-file`, `github-issues`, `migration`, `autonomous-tests`) — contrats et formats du workflow | [→](reference-references.md) | [→](explanation-references.md) |
| ✅ | `plugin-config` | Manifestes de publication du plugin (`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`) — métadonnées et déclaration des hooks pour les marketplaces Claude Code et Codex | [→](reference-plugin-config.md) | — |
| ✅ | `openspec-integration` | Intégration du workflow OpenSpec (`.claude/skills/openspec-*/`, `openspec/`) — propose, apply, archive, explore, sync et update pour la gestion structurée des changements | [→](reference-openspec-integration.md) | [→](explanation-openspec-integration.md) |
| ✅ | `tests-e2e` | Projet de test isolé (`tests/my-project--s-solo/`) et script de setup (`scripts/e2e_fresh_install_setup.sh`) — 6 fixtures couvrant tous les scénarios d'usage | [→](reference-tests-e2e.md) | [→](explanation-tests-e2e.md) |

**Légende** : ✅ docs générées · ⬜ inventorié, docs non encore générées
