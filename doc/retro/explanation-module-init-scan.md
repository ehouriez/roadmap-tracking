# Explication — module-init-scan

> Voir aussi : [Référence module-init-scan](reference-module-init-scan.md)

---

## Le problème : les directives textuelles ne suffisent pas

La garde d'entrée existait dès les premières versions comme règle textuelle. Les tests e2e montraient que des formulations impératives (`Démarre`, `Go`, `Fais tout`) ou des prompts visuellement structurés (spec bien rédigée) créaient systématiquement un bypass tacite : le modèle interprétait le prompt comme "tout est déjà planifié, lancez-vous". Le plan #16 (hooks mécaniques anti-bypass) a matérialisé la garde en trois hooks, réduisant le bypass à un problème de configuration.

---

## Pourquoi la garde PreToolUse est one-shot

Si la garde refusait toutes les écritures de la session, le skill serait impossible à utiliser une fois déclenché — même pour écrire le fichier plan. Le design one-shot résout ce paradoxe :

1. Le premier appel d'outil mutant déclenche le refus et force l'invocation du skill.
2. Le modèle invoque le skill (ou se désengage sur tâche XS).
3. La garde s'auto-désarme via le fichier marqueur.
4. Toutes les écritures suivantes passent librement.

Le kill-switch `ROADMAP_TRACKING_AUTOSTART=off` permet de contourner l'ensemble pour les projets qui n'ont pas adopté le skill.

---

## Pourquoi l'index .index.json plutôt que roadmap.md

Sur un portfolio de 285 plans, `roadmap.md` représentait ~275 Ko (~49 K tokens). Le relire à chaque démarrage était le poste de coût dominant (plan #27). `.index.json` encode les 7 champs nécessaires au listing sous quelques Ko — réduction de ~82 % du coût de startup.

Trade-off : deux artefacts à maintenir en synchronisation. La réconciliation légère au démarrage (mtime uniquement) détecte la désynchronisation sans recréer un coût fixe.

---

## Pourquoi la réconciliation est low-cost uniquement

Le plan #27 avait mesuré que lancer `doctor.py` à chaque démarrage recréait exactement le coût fixe qu'il cherchait à supprimer. Décision explicite : la réconciliation de startup se limite à 3 signaux `stat` (mtime). L'audit complet reste sur demande (`aide doctor`).

---

## Pourquoi ${PY} et ${SKILL_DIR}

**`${SKILL_DIR}`** : le skill peut être installé en scope projet, utilisateur ou cache global. Assumer `scripts/` = CWD du projet causerait des erreurs `ModuleNotFoundError` silencieuses dès que le projet ne contient pas les scripts. La valeur injectée par le harness est la seule source fiable.

**`${PY}`** : sur Windows, `python3.exe` dans `WindowsApps` est un stub Microsoft Store détecté par `command -v` mais qui échoue à l'exécution. La résolution via `import sys` identifie le stub (l'import échoue) et passe automatiquement au suivant.

---

## Pourquoi les marqueurs snooze/decline

Sans marqueur, la proposition de migration, de réconciliation ou de découpe CONTEXT.md réapparaîtrait à chaque session — friction source d'abandon ou de skip forcé. Avec le marqueur, l'utilisateur reprend le contrôle (snooze 2/8/30j ou refus définitif) sans modifier sa configuration de skill.

---

## Pourquoi l'aide est générée à la volée

Maintenir un fichier d'aide séparé signifie deux sources de vérité à synchroniser. L'aide générée depuis SKILL.md et les références est toujours exactement synchrone avec la version installée — pas de dérive possible entre le comportement réel et la documentation d'aide.
