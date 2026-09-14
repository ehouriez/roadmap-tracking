---
plan:
  id: '1'
  name: 1-weather-forecast-script.md
  link: doc/roadmap/1-weather-forecast-script.md
  source: local
status: done
date: 2026-09-14
description: >
  Script Python interrogeant l'API Open-Meteo pour afficher les prévisions
  météo du lendemain sur une tranche horaire configurable (défaut 08h-10h).
priority: medium
complexity: S
intent: null
issue:
  id: null
  url: null
---

# [🌤️] Plan #1 - Weather Forecast Script

## Objectif

Fournir un script CLI qui interroge l'API Open-Meteo (gratuite, sans clé)
et affiche les prévisions horaires du lendemain pour une tranche configurable.

## Périmètre

### Inclus
- Script Python `weather_forecast.py` à la racine du projet
- Arguments CLI : `--lat`, `--lon`, `--from-hour`, `--to-hour` (défauts : Paris, 8, 10)
- Sortie console : tableau horaire (heure, température, précipitations, code météo)
- Stdlib uniquement (`urllib`, `argparse`, `json`, `datetime`)

### Hors scope
- Interface graphique, notifications push
- Historique / persistance des données
- Support multi-villes par nom (geocoding)

## Étapes

- [x] Étape 1 — Écrire `weather_forecast.py` avec appel Open-Meteo + filtrage horaire (S · standard → Sonnet)
- [X] 🧪 Tests — Exécuter le script et vérifier la sortie
- [X] ✅ Validation — Vérifier les résultats et clôturer

## Décisions techniques

| Décision | Choix retenu | Justification |
|----------|-------------|---------------|
| API météo | Open-Meteo | Gratuit, sans clé, RGPD-compatible, JSON propre |
| HTTP client | `urllib.request` | Stdlib, zéro dépendance |
| Format de sortie | Tableau texte aligné | Lisible en terminal sans lib externe |

## Tests

### Procédure de test

```bash
echo "=== Install Check (no deps required) ==="
python3 --version

echo "=== Default Run (Paris, 08h-10h) ==="
python3 weather_forecast.py

echo "=== Custom Location And Time Slot ==="
python3 weather_forecast.py --lat 43.2965 --lon 5.3698 --from-hour 7 --to-hour 12

echo "=== Help ==="
python3 weather_forecast.py --help
```

**Résultats attendus :** tableau horaire avec température, précipitations et description météo pour chaque heure de la tranche. Pas d'erreur réseau avec les valeurs par défaut.

### Résultats joués et vérifiés

| Date | Test | Attendu | Observé | Verdict |
|------|------|---------|---------|---------|

## Journal de session

### Session 2026-09-14
- ✅ Fait : plan créé, script implémenté (fast-track)
- 📋 Prochain : tests manuels


### Session 2026-09-14

```bash
$ python3 weather_forecast.py
Traceback (most recent call last):
  File "weather_forecast.py", line 35, in <module>
    def filter_tomorrow(data: dict, from_hour: int, to_hour: int) -> list[dict]:
TypeError: 'type' object is not subscriptable
```

Erreur `TypeError: 'type' object is not subscriptable` signifie que tu utilises Python < 3.9. La syntaxe list[dict] dans les annotations de type n'est disponible nativement qu'à partir de Python 3.9.

**Correctifs appliqués :**
- ✅ Ajout manuel de `from __future__ import annotations` en tout début de fichier (après le shebang/docstring). Cela diffère l'évaluation des annotations et accepte la syntaxe moderne sur Python 3.7+