// node test_analysis.js — self-check for analysis.js on a toy graph and on the real data
const assert = require("assert");
const fs = require("fs");
const A = require("./analysis.js");

// toy: two triangles {0,1,2} {3,4,5} joined via node 2-3; 0 and 4 hate each other
const n = 6, S = Array.from({ length: n }, () => new Array(n).fill(0));
const set = (a, b, v) => (S[a][b] = S[b][a] = v);
[[0, 1], [1, 2], [0, 2], [3, 4], [4, 5], [3, 5], [2, 3]].forEach(([a, b]) => set(a, b, 10));
set(1, 3, -10);
const adj = A.goodAdj(S, 7);
assert.strictEqual(A.components(adj).count, 1);
assert.deepStrictEqual(A.bridges(adj).map((b) => b[0]).sort(), [2, 3]);
const comm = A.communities(S, { thr: 7, bad: -5, gamma: 1 });
assert.strictEqual(comm[0], comm[1]); assert.strictEqual(comm[3], comm[4]); assert.notStrictEqual(comm[0], comm[4]);
// an item without good partners stays alone, even when it clashes with someone
const S2 = S.map((r) => [...r, -8]); S2.push(new Array(n + 1).fill(-8)); S2[n][n] = 0;
const comm2 = A.communities(S2, { thr: 7, bad: -5, gamma: 1, clash: 0.5 });
assert(comm2.filter((c) => c === comm2[n]).length === 1);
const st = A.nodeStats(S, adj, -5);
assert.strictEqual(st[2].open, 1); // 1~2~3 with 1 x 3 bad
assert.strictEqual(st[0].clustering, 1);
const items = S.map(() => ({ cat: "x" }));
const E0 = A.engine(S, items);
assert.deepStrictEqual(A.suggest(E0, [0], 3, { count: 1 })[0].set.slice().sort(), [0, 1, 2]);
assert.strictEqual(A.explain(E0, [0, 1, 3]).weakest[2], -10);
assert.strictEqual(A.swaps(E0, [0, 1, 3], 2)[0].item, 2);

// real data loads and analyses
const DATA = new Function(fs.readFileSync(__dirname + "/data.js", "utf8") + "; return DATA;")();
const idx = (name) => DATA.items.findIndex((i) => i.name === name);
const E = A.engine(DATA.S, DATA.items, { known: DATA.K, classics: DATA.classics });
const butter0 = () => new Set(DATA.items.flatMap((it, i) => (it.cat === "butter" ? [i] : [])));
const r = A.suggest(E, [idx("Pindakaas")], 3, { count: 5 });
assert(r.length === 5 && r.every((x) => x.set.includes(idx("Pindakaas")) && x.score > 0.5));
// results are not like-for-like variants of each other, and exclusions hold
for (let a = 0; a < r.length; a++) for (let b = a + 1; b < r.length; b++) assert(!A.isVariant(E, r[a].set, r[b].set));
const banana = idx("Banaan");
assert(A.suggest(E, [idx("Pindakaas")], 3, { exclude: new Set([banana]) }).every((x) => !x.set.includes(banana)));
// two interchangeable toppings on one sandwich get marked down
assert(A.explain(E, [idx("Sambal oelek"), idx("Sambal badjak"), idx("Kroket")]).penalties.some((p) => p.kind === "twin"));
// classics are recognised, estimated pairs are marked down, strict mode only keeps proven pairs
const gezond = DATA.classics.find((c) => c.name === "Broodje gezond").set;
assert.strictEqual(A.classicOf(E, gezond).kind, "is");
assert(A.explain(E, gezond.slice(0, 3)).classic.kind === "part");
for (const r of A.suggest(E, [idx("Brie")], 4, { proven: true, exclude: butter0() })) assert(A.proven(E, r.set, [idx("Brie")]));
assert(A.explain(E, [idx("Mozzarella"), idx("Sambal oelek")]).penalties.some((p) => p.kind === "stranger"));
// surprise mode is reproducible per seed
assert.deepStrictEqual(A.suggest(E, [], 3, { noise: 0.05, seed: 9, count: 1 })[0].set, A.suggest(E, [], 3, { noise: 0.05, seed: 9, count: 1 })[0].set);
const butter = new Set(DATA.items.flatMap((it, i) => (it.cat === "butter" ? [i] : [])));
const c = A.communities(DATA.S, { thr: 7, bad: -5, skip: butter });
// every cluster member has a good partner inside its own cluster
c.forEach((k, i) => { if (c.filter((x) => x === k).length > 1) assert(c.some((x, j) => j !== i && x === k && DATA.S[i][j] >= 7), DATA.items[i].name); });
console.log("communities:", Math.max(...c) + 1, "| PB suggestions:", r.map((x) => x.set.map((i) => DATA.items[i].name).join(" + ")).join(" ; "));
// every topping is drawn as itself on the animated sandwich, not as a generic fallback
const Sandwich = require("./sandwich.js");
const unlooked = DATA.items.filter((it) => !Sandwich.look(it).matched).map((it) => it.name);
assert.deepStrictEqual(unlooked, [], "toppings without a look: " + unlooked.join(", "));
assert.strictEqual(Sandwich.look({ name: "Haringsalade" }).kind, "blob");
assert(!Sandwich.svg(DATA.items, DATA.items.map((_, i) => i)).svg.includes("NaN"));
console.log("ok");
