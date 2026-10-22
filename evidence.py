"""Recipe evidence for pairs: how much more (or less) often two toppings share a sandwich recipe than chance.

Reads recipe_counts.json (made by recipes.py). Each Dutch recipe counts DUTCH_WEIGHT times, because
RecipeNLG hardly knows Dutch toppings. Returns {(i, j): (pmi, weight)} for pairs with enough evidence.
"""
import json
import math
from pathlib import Path

DUTCH_WEIGHT = 30
# In RecipeNLG these are mostly cooking ingredients (sauce sugar, butter for the pan), not toppings.
COOKING = {"Kristalsuiker", "Bruine basterdsuiker", "Poedersuiker", "Schenkstroop", "Roomboter", "Margarine"}
# "Never together" only counts for toppings the recipes clearly know (eggs are listed as plain "eggs").
WELL_COVERED = 150


def recipe_evidence(items, path="recipe_counts.json"):
    C = json.loads(Path(path).read_text())
    names = [it["name"] for it in items]
    ix = {n: i for i, n in enumerate(names)}
    single, pair = {}, {}
    for k, v in C["single"].items():
        if k not in COOKING:
            single[k] = v
    for k, v in C["pair"].items():
        a, b = k.split("|")
        if a not in COOKING and b not in COOKING:
            pair[(a, b)] = v
    n_rec = C["recipes_used"]
    for r in C["dutch"]:
        n_rec += DUTCH_WEIGHT
        for x in r:
            single[x] = single.get(x, 0) + DUTCH_WEIGHT
        for x in range(len(r)):
            for y in range(x + 1, len(r)):
                k = tuple(sorted((r[x], r[y])))
                pair[k] = pair.get(k, 0) + DUTCH_WEIGHT
    out = {}
    known = sorted(single)
    for x in range(len(known)):
        for y in range(x + 1, len(known)):
            a, b = known[x], known[y]
            na, nb = single[a], single[b]
            n = pair.get((a, b), 0)
            expected = na * nb / n_rec
            if n == 0 and (expected < 5 or min(na, nb) < WELL_COVERED):
                continue  # absence only means something when the pair had every chance
            if n > 0 and n < 3 and expected < 3:
                continue  # too rare either way
            pmi = math.log((n + 0.5) / (expected + 0.5))
            weight = min(1.0, (n + expected) / 40)  # more recipes, more trust
            i, j = sorted((ix[a], ix[b]))
            out[(i, j)] = (pmi, weight)
    return out
