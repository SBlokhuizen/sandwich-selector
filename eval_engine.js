// node eval_engine.js — how delicious are the engine's suggestions?
// 1. Classics: seeded with a classic's first topping, does the engine find that classic (or all but one of it)?
// 2. Audit: for every topping as the seed, the top 3 sandwiches of 3, how many pairs are proven (hand-set),
//    how many are merely okay (< +0.5), and how many put cuisines together that do not meet.
const fs = require("fs");
const A = require("./analysis.js");
const DATA = new Function(fs.readFileSync(__dirname + "/data.js", "utf8") + "; return DATA;")();
const { S, items } = DATA;
const N = items.length;
const E = A.engine(S, items, { known: DATA.K, classics: DATA.classics });
const opts = { proven: process.argv.includes("--proven") };
const butter = new Set(items.flatMap((it, i) => (it.cat === "butter" ? [i] : [])));
const known = new Set((DATA.K || []).map(([i, j]) => i * N + j));
const isKnown = (a, b) => known.has(Math.min(a, b) * N + Math.max(a, b));

let found = 0, near = 0, tried = 0;
const missed = [];
for (const c of DATA.classics || []) {
  if (c.set.length < 3 || c.set.length > 5) continue;
  tried++;
  const res = A.suggest(E, [c.set[0]], c.set.length, { exclude: butter, ...opts });
  const overlap = Math.max(0, ...res.map((r) => r.set.filter((i) => c.set.includes(i)).length));
  if (overlap === c.set.length) found++;
  else if (overlap === c.set.length - 1) near++;
  else missed.push(c.name);
}
console.log(`classics found ${found}/${tried}, all but one topping ${near}/${tried}`);
if (missed.length) console.log("  missed:", missed.join(", "));

let pairs = 0, provenPairs = 0, okay = 0, sets = 0, mixed = 0, empty = 0, minSum = 0;
for (let s = 0; s < N; s++) {
  if (butter.has(s)) continue;
  const res = A.suggest(E, [s], 3, { count: 3, exclude: butter, ...opts });
  if (!res.length) empty++;
  for (const r of res) {
    sets++;
    let min = 10;
    for (const [a, b, v] of r.pairs) { pairs++; if (isKnown(a, b)) provenPairs++; if (v < 5) okay++; min = Math.min(min, v); }
    minSum += min;
    if (A.strangers(E, r.set).length) mixed++;
  }
}
console.log(`audit of ${sets} sandwiches: proven pairs ${(100 * provenPairs / pairs).toFixed(0)}% · pairs below +0.5 ${(100 * okay / pairs).toFixed(1)}% · clashing cuisines ${(100 * mixed / sets).toFixed(1)}% · average weakest pair ${(minSum / sets / 10).toFixed(2)} · seeds with no result ${empty}`);
