# Plan — Rationalisation tokens SKILL.md (P1)

> Issu de la section « Priorité d'action suggérée » de
> `doc/audits/0-roadmap-tracking-estimation-couts-tokens.md`.
>
> Objectif : réduire SKILL.md d'environ 35 % en tokens via compression P1 —
> sans modifier aucune règle, aucun comportement.

## Contexte

Session analysée : plan #11, complexité S, ~18 tours, ~278 000 tokens.
Levier dominant identifié : répétition du skill text (~10 000 tokens/tour × 18 tours = 180 000 tokens).
P1 vise 10 000 → 6 500 tokens/tour (−35 %), ce qui ramène le ratio A/B de ×10,7 à ×8,3.

## Cibles concrètes (P1)

1. **Bloc ❌ redondant** — `❌ **Formats INTERDITS**` (lignes 127-137 de SKILL.md) :
   exemple de format interdit présent deux fois — dans la « Règle de démarrage » ET
   dans `⛔ Règle absolue — format des rapports`. La section ⛔ est la référence
   canonique ; supprimer le doublon de la Règle de démarrage.

2. **3 gabarits de commit dupliqués** — sections « Tests unitaires intermédiaires »
   (lignes ~1114-1139), « Étape 🧪 Tests » (lignes ~1191-1221) et
   « Commit d'implémentation pré-tests » (lignes 1254-1281) :
   les deux premières reproduisent quasi à l'identique la troisième.
   Supprimer les gabarits inline, remplacer par une référence à la section canonique.

## Étapes

- [x] **Étape 1** — Supprimer le bloc `❌ **Formats INTERDITS**` en doublon
      (lignes 127-137 de SKILL.md, dans la section « Règle de démarrage »).

- [x] **Étape 2** — Remplacer le gabarit `📦 Commit proposé` inline de la section
      « Tests unitaires intermédiaires » (lignes ~1123-1138) par une référence à la
      section canonique « Commit d'implémentation pré-tests ».

- [x] **Étape 3** — Remplacer le gabarit `📦 Commit proposé` inline de la section
      « Étape 🧪 Tests » (lignes ~1200-1221) par la même référence.

- [x] **Étape 4** — Mesurer la réduction effective (wc -l avant/après).
      Avant : 1369 lignes. Après : 1326 lignes. Réduction : −43 lignes (−3,1 %).

## Tests E2E

> Procédure de vérification comportementale — grep sur SKILL.md.

```bash
echo "=== T1 — Taille réduite ==="
[ $(wc -l < SKILL.md) -lt 1369 ] && echo "PASS: $(wc -l < SKILL.md) < 1369" || echo "FAIL"

echo "=== T2 — Bloc ❌ FORMATS INTERDITS supprimé dans Règle de démarrage ==="
# Le bloc supprimé était AVANT la note Mode local. Il ne doit plus y avoir de
# "❌ **Formats INTERDITS**" dans les 140 premières lignes.
! grep -n "❌ \*\*Formats INTERDITS\*\*" SKILL.md | awk -F: '$1 < 141' | grep -q . \
  && echo "PASS: bloc doublon absent avant ligne 141" || echo "FAIL"

echo "=== T3 — Exemple ❌ canonique toujours présent dans ⛔ Règle absolue ==="
grep -q "❌ Exemple exact du format INTERDIT" SKILL.md \
  && echo "PASS" || echo "FAIL"

echo "=== T4 — Section canonique commit toujours présente ==="
grep -q "## Commit d'implémentation pré-tests (référence de format)" SKILL.md \
  && echo "PASS" || echo "FAIL"

echo "=== T5 — Gabarits inline supprimés (📦 Commit proposé — Étape X/N absent) ==="
! grep -q "### 📦 Commit proposé — Étape X/N" SKILL.md \
  && echo "PASS: gabarit inline étape absent" || echo "FAIL"

echo "=== T6 — Gabarits inline supprimés (📦 Commit proposé — Pré-tests finaux absent) ==="
! grep -q "### 📦 Commit proposé — Pré-tests finaux" SKILL.md \
  && echo "PASS: gabarit inline tests finaux absent" || echo "FAIL"

echo "=== T7 — Référence à la section canonique présente (tests intermédiaires) ==="
grep -q "Commit d'implémentation pré-tests.*référence de format" SKILL.md \
  && echo "PASS" || echo "FAIL"

echo "=== T8 — Phase 7 et règles clés toujours présentes ==="
grep -q "## Phase 7 — Implémentation" SKILL.md \
  && grep -q "⛔ Règle absolue — séparation création / implémentation" SKILL.md \
  && grep -q "⛔ Garde d'entrée" SKILL.md \
  && echo "PASS: sections critiques présentes" || echo "FAIL"
```

## Résultats

**Date** : 2026-09-12 — **Verdict global : ✅ PASS (8/8)**

| Test | Résultat |
|---|---|
| T1 — Taille réduite | ✅ PASS — 1326 < 1369 |
| T2 — Bloc ❌ doublon supprimé avant ligne 141 | ✅ PASS |
| T3 — Exemple ❌ canonique toujours présent | ✅ PASS |
| T4 — Section canonique commit présente | ✅ PASS |
| T5 — Gabarit inline Étape X/N absent | ✅ PASS |
| T6 — Gabarit inline Pré-tests finaux absent | ✅ PASS |
| T7 — Référence section canonique présente | ✅ PASS |
| T8 — Sections critiques Phase 7 / ⛔ présentes | ✅ PASS |

### Mesure effective

| Métrique | Avant | Après | Réduction |
|---|---|---|---|
| Lignes SKILL.md | 1 369 | 1 326 | −43 (−3,1 %) |
| Tokens estimés/tour | ~10 000 | ~9 700 | ~−300 (−3 %) |

### Écart vs estimation audit

L'audit estimait −35 % (10 000 → 6 500 tokens). La compression P1 telle qu'identifiée
n'atteint que −3 % : les 3 suppressions concrètes (1 bloc doublon + 2 gabarits inline)
représentent 43 lignes, pas ~479.

**Cause de l'écart** : la cible « 13 blocs ❌ redondants » dans l'audit était une
estimation par extrapolation depuis les sections visibles lors de l'analyse, sans
recensement exhaustif ligne à ligne. Sur le SKILL.md v2.5.7 actuel, seul 1 bloc
❌ est réellement un doublon exact (le gabarit format interdit dans la Règle de
démarrage). Les 2 gabarits de commit remplacés par des références économisent
~30 lignes supplémentaires.

Pour atteindre −35 %, il faudrait implémenter P2 (scission skill lite / implémentation)
qui coupe le texte chargé à chaque tour — levier structurel, hors périmètre P1.
