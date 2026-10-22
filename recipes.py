"""Count how often toppings appear together in real sandwich recipes (RecipeNLG) plus Dutch classics.

Run: python3 recipes.py /path/to/recipenlg/   (a folder with the RecipeNLG parquet or full_dataset.csv files)
Writes recipe_counts.json: per-topping and per-pair recipe counts. Only these counts are kept in the repo,
not the recipes themselves (RecipeNLG is for non-commercial research use).
"""
import json
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import pyarrow.parquet as pq

from build import ITEMS
from flavours import ALIASES, DUTCH_RECIPES

# A recipe counts as a sandwich when its title says so.
SANDWICH = re.compile(
    r"\b(sandwich(es)?|sammie|toast(ie|ies|s)?|panini|sub|subs|hoagie|hero|grinder|po'? ?boy|wrap|wraps|burger|burgers|slider|sliders|"
    r"bagel|bagels|bruschetta|crostini|tartine|smorrebrod|open[- ]face[d]?|club|blt|melt|croque|monte cristo|reuben|muffuletta|"
    r"banh mi|cuban|roll[- ]?ups?|on rye|on a bun|bun|buns|baguette|ciabatta|focaccia sandwich)\b",
    re.I,
)


# ...but not when it is a bake, a dessert or a breakfast dish that merely mentions one.
NOT_SANDWICH = re.compile(
    r"\b(french toast|cinnamon|sticky|sweet rolls?|dinner rolls?|hot cross|bread pudding|pudding|casserole|cake|cookies?|bars|pie|"
    r"dough|muffins?|biscuits?|scones?|crackers|cheesecake|egg rolls?|spring rolls?|sushi|cabbage rolls?|lasagna|toasted (nuts|pecans|almonds|coconut))\b",
    re.I,
)
BAKING = {"yeast", "active dry yeast", "dry yeast", "instant yeast", "baking powder", "baking soda"}


def alias_table():
    names = [line.split("|")[0] for line in ITEMS.strip().splitlines()]
    table = {}
    for line in ALIASES.strip().splitlines():
        name, rest = line.split(":", 1)
        assert name in names, name
        for a in rest.split(";"):
            table[a.strip().lower()] = name
    return names, table


def matcher(table):
    """NER ingredient -> topping, by the longest alias that the ingredient ends with (whole words)."""
    by_len = sorted(table, key=len, reverse=True)
    cache = {}

    def match(ing):
        ing = re.sub(r"\s+", " ", ing.lower().strip())
        if ing not in cache:
            cache[ing] = next((table[a] for a in by_len if ing == a or ing.endswith(" " + a)), None)
        return cache[ing]

    return match


def read_recipes(folder):
    files = sorted(Path(folder).glob("*.parquet"))
    if files:
        for f in files:
            pf = pq.ParquetFile(f)
            for batch in pf.iter_batches(columns=["title", "NER"], batch_size=50_000):
                d = batch.to_pydict()
                yield from zip(d["title"], d["NER"])
    else:
        import csv
        csv.field_size_limit(10**8)
        with open(Path(folder) / "full_dataset.csv", newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                yield row["title"], row["NER"]


def main(folder):
    names, table = alias_table()
    match = matcher(table)
    single, pair = Counter(), Counter()
    total = sandwiches = used = 0
    for title, ner in read_recipes(folder):
        total += 1
        if not title or not SANDWICH.search(title) or NOT_SANDWICH.search(title):
            continue
        ings = json.loads(ner) if isinstance(ner, str) else ner
        if any(i.lower().strip() in BAKING for i in ings):
            continue  # it bakes the bread rather than fills it
        sandwiches += 1
        tops = sorted({t for t in map(match, ings) if t})
        if len(tops) < 2:
            continue
        used += 1
        single.update(tops)
        pair.update(combinations(tops, 2))
    dutch = [sorted({x.strip() for x in line.split(",")}) for line in DUTCH_RECIPES.strip().splitlines()]
    out = {
        "source": "RecipeNLG (sandwich-like titles) + flavours.DUTCH_RECIPES",
        "recipes_total": total, "sandwich_recipes": sandwiches, "recipes_used": used,
        "single": dict(single), "pair": {f"{a}|{b}": n for (a, b), n in pair.items()},
        "dutch": dutch,
    }
    Path("recipe_counts.json").write_text(json.dumps(out, ensure_ascii=False, indent=0, sort_keys=True))
    print(f"{total} recipes, {sandwiches} sandwich-like, {used} with 2+ of our toppings; "
          f"{len(single)} toppings and {len(pair)} pairs seen; + {len(dutch)} Dutch recipes")
    print("most common:", ", ".join(f"{k} {v}" for k, v in single.most_common(15)))


if __name__ == "__main__":
    main(sys.argv[1])
