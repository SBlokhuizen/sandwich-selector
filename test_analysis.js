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
const comm = A.louvain(S, 7);
assert.strictEqual(comm[0], comm[1]); assert.strictEqual(comm[3], comm[4]); assert.notStrictEqual(comm[0], comm[4]);
const st = A.nodeStats(S, adj, -5);
assert.strictEqual(st[2].open, 1); // 1~2~3 with 1 x 3 bad
assert.strictEqual(st[0].clustering, 1);
const items = S.map(() => ({ cat: "x" }));
assert.deepStrictEqual(A.suggest(S, items, [0], 3, 1)[0].set.slice().sort(), [0, 1, 2]);

// real data loads and analyses
const DATA = new Function(fs.readFileSync(__dirname + "/data.js", "utf8") + "; return DATA;")();
const idx = (name) => DATA.items.findIndex((i) => i.name === name);
const r = A.suggest(DATA.S, DATA.items, [idx("Pindakaas")], 3, 5);
assert(r.length === 5 && r.every((x) => x.set.includes(idx("Pindakaas")) && x.fit > 0.5));
const c = A.louvain(DATA.S, 7);
console.log("communities:", Math.max(...c) + 1, "| PB suggestions:", r.map((x) => x.set.map((i) => DATA.items[i].name).join(" + ")).join(" ; "));
console.log("ok");
