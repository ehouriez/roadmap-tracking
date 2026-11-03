# Explication — fichiers de référence

> Voir aussi : [Référence references](reference-references.md)

---

## Le problème du skill monolithique

Un skill monolithique embarquant tous les formats, templates et règles dans un seul fichier a un coût de chargement fixe proportionnel à sa taille. Avant le plan #17, la section templates à elle seule représentait ~8 K tokens chargés même quand aucun plan n'allait être créé.

---

## Pourquoi le chargement conditionnel

Les 7 fichiers de référence couvrent des besoins très différents. En Phase 2, seule `forms.md` est pertinente. En Phase 5 mode local, `github-issues.md` et `migration.md` ne le sont pas du tout.

Le chargement conditionnel réduit le coût de contexte moyen à ~5–8 K tokens par phase, contre ~40 K tokens si tout était chargé au démarrage.

Trade-off : le skill doit mémoriser quel fichier charger et quand. Un agent qui répond sans charger le bon fichier produit des réponses incomplètes. La table "Quand charger" dans SKILL.md est la réponse à ce risque.

---

## Pourquoi les règles de formatage des commandes sont dans environment.md

Les règles de formatage operator commands (`echo "=== ... ==="`, pas de `\` de continuation) s'appliquent dès qu'une commande shell est présentée — ce qui peut arriver dès le démarrage (commandes de migration, de réconciliation). Les co-localiser avec `environment.md` (chargé toujours au démarrage) garantit leur disponibilité constante.

---

## Pourquoi autonomous-tests.md est opt-in uniquement

La détection de la présence d'un shell (Bash disponible dans Claude Code) activerait le mode autonomous presque systématiquement. Or le mode autonomous a un coût en sous-agents et peut donner une fausse impression d'isolation (sub-agent = isolation totale, alors que l'inline fallback est la dégradation gracieuse). L'activation opt-in par `.skill-config.yml` force une décision explicite par projet.

---

## Pourquoi le Verifier doit être un fresh Agent (pas un fork)

Un fork hérite du contexte complet du parent. Le Verifier doit recevoir uniquement les résultats de test bruts et rendre un verdict indépendant — sans avoir vu le code, les tentatives précédentes, ni les biais de la session parent. L'isolation est la valeur ajoutée du mode autonomous ; un fork l'annule.

---

## Pourquoi .migration-declined est dans .gitignore

La décision de migrer ou non les IDs de plans est personnelle à chaque développeur sur le projet. La mettre en `.gitignore` empêche qu'un développeur "refuse" la migration pour l'ensemble de l'équipe en committant son fichier marqueur.
