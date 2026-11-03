# Explication — scripts-python

> Voir aussi : [Référence scripts-python](reference-scripts-python.md)

---

## Le problème : roadmap.md maintenu manuellement

Avant le plan #27, `roadmap.md` était maintenu manuellement : chaque changement de statut, chaque nouveau plan nécessitait une écriture cohérente. Sur un portfolio de 285 plans, ce fichier avait grossi à ~275 Ko et était devenu la source principale de dérive (statuts incorrects, liens cassés, ordre de priorité manquant).

---

## Pourquoi migrate_plan_ids.py est la bibliothèque commune

Quatre des cinq scripts ont besoin de lire le front matter YAML des plans. Dupliquer le parser dans chaque script créerait 4 implémentations qui divergeraient progressivement. `migrate_plan_ids.py` est devenu le parser canonique par opportunité : c'était le premier script à implémenter le parsing, les autres ont naturellement importé depuis lui.

---

## Pourquoi doctor.py est strictement read-only

La tentation de faire "fix + audit" en un seul script est forte. L'argument contre : `doctor.py` est exécuté en démarrage de session et en CI. Lui permettre d'écrire introduirait des mutations non prévues dans ces contextes. La séparation read-only → propose / write-enabled → normalize est délibérée.

---

## Pourquoi le défaut --dry-run

Sur un portfolio de 30+ plans, une mutation accidentelle (`normalize_status.py` sans `--write` prévu) peut déplacer des dizaines de fichiers. Le défaut dry-run exige une intention explicite de mutation — même principe que `git checkout --` vs `git reset --hard`.

---

## Pourquoi build_roadmap.py dérive le nom de projet depuis roadmap.md existant

Sur un projet adopté, `roadmap.md` existe avec un H1 choisi par l'équipe. Inventer un nom à la régénération écraserait ce choix. Lire l'H1 existant préserve la stabilité du document à travers les régénérations.

---

## Pourquoi split_context.py fail-open sur collision

Si le fichier thématique cible existe déjà (`context/deploiement.md` par exemple), écraser silencieusement détruirait du contenu existant. L'exit 1 avant toute écriture est un garde-fou de non-destruction qui force l'opérateur à résoudre la collision manuellement.

---

## Pourquoi --self-check sur chaque script

Les scripts sont exécutés par le skill en session active. Un bug régressif dans un script introduirait une erreur difficilement diagnostiquable. `--self-check` offre un test de santé rapide sans dépendance externe, exécutable en CI ou au moment d'une mise à jour du plugin.
