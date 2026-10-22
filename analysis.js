// Graph analysis on the score matrix S (integers -10..10). Pure functions, usable in browser and node.
const Analysis = (() => {
  const sum = (xs) => { let s = 0; for (const x of xs) s += x; return s; };
  const msum = (m) => sum(m.values());
  // small seeded PRNG so results are reproducible
  const rng = (seed) => () => ((seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0) / 4294967296);

  // neighbours i~j when S[i][j] >= thr
  function goodAdj(S, thr) {
    return S.map((row, i) => row.flatMap((v, j) => (i !== j && v >= thr ? [j] : [])));
  }

  // connected components; `skip` = node treated as removed
  function components(adj, skip = -1) {
    const comp = new Array(adj.length).fill(-1);
    let c = 0;
    for (let s = 0; s < adj.length; s++) {
      if (s === skip || comp[s] >= 0) continue;
      const stack = [s];
      comp[s] = c;
      while (stack.length) for (const j of adj[stack.pop()]) if (j !== skip && comp[j] < 0) { comp[j] = c; stack.push(j); }
      c++;
    }
    return { comp, count: c };
  }

  // Communities by signed modularity (Gómez et al. 2009): good pairs (>= thr) attract with their score,
  // clashes (<= bad) repel with weight `clash` × |score|. `gamma` is the resolution (higher = smaller clusters).
  // Louvain with random restarts, then a Leiden-style refinement so every cluster is connected by good pairs.
  // Nodes in `skip`, or without any good partner, get their own singleton community.
  function communities(S, { thr = 7, bad = -5, gamma = 1.5, clash = 0.1, skip = new Set(), restarts = 6 } = {}) {
    const n0 = S.length;
    const edges = (keep, w) => S.map((row, i) => new Map(skip.has(i) ? [] : row.flatMap((v, j) => (i !== j && !skip.has(j) && keep(v) ? [[j, w(v)]] : []))));
    const P0 = edges((v) => v >= thr, (v) => v), M0 = edges((v) => v <= bad, (v) => -v * clash);
    const kp0 = P0.map(msum), km0 = M0.map(msum);
    const Wp = sum(kp0) || 1, Wm = sum(km0) || 1;

    // gain of putting a node (weights w to communities, degrees kp/km) into community c
    const gainFn = (w, tp, tm, kp, km) => (c) => (w.get(c) || 0) - gamma * ((tp[c] * kp) / Wp - (tm[c] * km) / Wm);

    function quality(c) {
      let q = 0;
      const tp = new Map(), tm = new Map();
      for (let i = 0; i < n0; i++) {
        for (const [j, x] of P0[i]) if (c[i] === c[j]) q += x;
        for (const [j, x] of M0[i]) if (c[i] === c[j]) q -= x;
        tp.set(c[i], (tp.get(c[i]) || 0) + kp0[i]); tm.set(c[i], (tm.get(c[i]) || 0) + km0[i]);
      }
      for (const v of tp.values()) q -= (gamma * v * v) / Wp;
      for (const v of tm.values()) q += (gamma * v * v) / Wm;
      return q / (Wp + Wm);
    }

    // one round of local moves over graph (P, M); returns true if anything moved
    function localMoves(P, M, comm, order, allowed = () => true) {
      // labels n..2n-1 are spare empty communities, so a node can always break away on its own
      const n = P.length, kp = P.map(msum), km = M.map(msum);
      const tp = new Array(2 * n).fill(0), tm = new Array(2 * n).fill(0);
      for (let i = 0; i < n; i++) { tp[comm[i]] += kp[i]; tm[comm[i]] += km[i]; }
      let moved = true, any = false, passes = 0;
      while (moved && passes++ < 40) {
        moved = false;
        for (const i of order) {
          if (!allowed(i) || !kp[i]) continue;
          const ci = comm[i], w = new Map([[ci, 0]]), good = new Set();
          for (const [j, x] of P[i]) if (j !== i) { w.set(comm[j], (w.get(comm[j]) || 0) + x); good.add(comm[j]); }
          for (const [j, x] of M[i]) if (j !== i) w.set(comm[j], (w.get(comm[j]) || 0) - x);
          tp[ci] -= kp[i]; tm[ci] -= km[i];
          const gain = gainFn(w, tp, tm, kp[i], km[i]);
          // only join a community it shares a good pair with; otherwise stand alone
          const alone = tp[n + i] || tm[n + i] ? ci : n + i;
          let best = good.has(ci) ? ci : alone, g = gain(best);
          for (const c of good) { const x = gain(c); if (x > g + 1e-9) { g = x; best = c; } }
          tp[best] += kp[i]; tm[best] += km[i];
          if (best !== ci) { comm[i] = best; moved = any = true; }
        }
      }
      return any;
    }

    function run(seed) {
      const r = rng(seed), shuffle = (n) => { const o = [...Array(n).keys()]; for (let i = n - 1; i > 0; i--) { const j = (r() * (i + 1)) | 0; [o[i], o[j]] = [o[j], o[i]]; } return o; };
      let P = P0, M = M0, member = [...Array(n0).keys()];
      for (;;) {
        const n = P.length, comm = [...Array(n).keys()];
        if (!localMoves(P, M, comm, shuffle(n))) break;
        const ids = new Map();
        comm.forEach((c) => ids.has(c) || ids.set(c, ids.size));
        if (ids.size === n) { member = member.map((c) => ids.get(comm[c])); break; }
        const agg = (G) => {
          const out = Array.from({ length: ids.size }, () => new Map());
          for (let i = 0; i < n; i++) for (const [j, x] of G[i]) { const a = ids.get(comm[i]), b = ids.get(comm[j]); out[a].set(b, (out[a].get(b) || 0) + x); }
          return out;
        };
        P = agg(P); M = agg(M);
        member = member.map((c) => ids.get(comm[c]));
      }
      // refinement: split each community into its good-pair-connected pieces; the stray pieces
      // (not the largest piece) get to move again node by node, so nothing sits in a cluster it has no link to
      const piece = new Array(n0).fill(-1), pieceSize = [];
      for (let s = 0; s < n0; s++) {
        if (piece[s] >= 0) continue;
        const id = pieceSize.length, st = [s];
        piece[s] = id; pieceSize.push(1);
        while (st.length) for (const j of P0[st.pop()].keys()) if (piece[j] < 0 && member[j] === member[s]) { piece[j] = id; pieceSize[id]++; st.push(j); }
      }
      const main = new Map();
      piece.forEach((p, i) => { const m = main.get(member[i]); if (m === undefined || pieceSize[p] > pieceSize[m]) main.set(member[i], p); });
      const stray = piece.map((p, i) => main.get(member[i]) !== p);
      const comm = piece.map((p, i) => (stray[i] ? p : main.get(member[i])));
      localMoves(P0, M0, comm, shuffle(n0), (i) => stray[i]);
      localMoves(P0, M0, comm, shuffle(n0));
      return comm;
    }

    let best, bq = -Infinity;
    for (let s = 1; s <= restarts; s++) { const c = run(s * 7919), q = quality(c); if (q > bq) { bq = q; best = c; } }
    // relabel by size, largest community = 0
    const size = new Map();
    best.forEach((c) => size.set(c, (size.get(c) || 0) + 1));
    const order = [...size.keys()].sort((a, b) => size.get(b) - size.get(a) || a - b);
    const rank = new Map(order.map((c, k) => [c, k]));
    return best.map((c) => rank.get(c));
  }

  // Per-node stats. Open triangle at B: A~B, B~C good but S[A][C] <= bad.
  function nodeStats(S, adj, bad) {
    return S.map((row, b) => {
      const nb = adj[b];
      let closed = 0, open = 0;
      const examples = [];
      for (let x = 0; x < nb.length; x++)
        for (let y = x + 1; y < nb.length; y++) {
          const v = S[nb[x]][nb[y]];
          if (adj[nb[x]].includes(nb[y])) closed++;
          if (v <= bad) { open++; examples.push([nb[x], nb[y], v]); }
        }
      const pairs = (nb.length * (nb.length - 1)) / 2;
      examples.sort((p, q) => p[2] - q[2]);
      return {
        degree: nb.length,
        strength: sum(nb.map((j) => row[j])) / 10,
        mean: (sum(row) - row[b]) / 10 / (row.length - 1),
        clustering: pairs ? closed / pairs : 0,
        open,
        examples: examples.slice(0, 5),
      };
    });
  }

  // Nodes whose removal splits their island into more pieces (articulation points).
  function bridges(adj) {
    const base = components(adj).count;
    return adj.flatMap((nb, i) => {
      if (!nb.length) return [];
      const extra = components(adj, i).count - base;
      return extra > 0 ? [[i, extra]] : [];
    });
  }

  // Cohesion of a set: mostly the mean pair score, pulled down by its worst pair.
  function fit(S, set) {
    let s = 0, n = 0, min = 10;
    for (let x = 0; x < set.length; x++)
      for (let y = x + 1; y < set.length; y++) { const v = S[set[x]][set[y]]; s += v; n++; if (v < min) min = v; }
    return n ? (0.6 * (s / n) + 0.4 * min) / 10 : 0;
  }

  // ---------- matching engine ----------
  // Categories that carry a sandwich. Two of the same kind on one slice is usually one too many.
  const MAIN = new Set(["cheese", "meat", "fish", "nut", "sweet", "jam", "hot", "salad", "egg"]);

  // Correlation of two toppings' score profiles against everything else: ~1 = they behave the same.
  function profileSim(S) {
    const n = S.length;
    const z = S.map((row) => {
      const m = sum(row) / n, sd = Math.sqrt(sum(row.map((v) => (v - m) ** 2)) / n) || 1;
      return row.map((v) => (v - m) / sd);
    });
    const sim = Array.from({ length: n }, () => new Float32Array(n));
    for (let a = 0; a < n; a++)
      for (let b = a; b < n; b++) {
        let c = 0;
        for (let k = 0; k < n; k++) if (k !== a && k !== b) c += z[a][k] * z[b][k];
        sim[a][b] = sim[b][a] = c / (n - 2);
      }
    return sim;
  }

  // Engine context: everything that only depends on the data, computed once.
  function engine(S, items) {
    const sim = profileSim(S);
    // interchangeable: same category and the rest of the world treats them alike (e.g. two hams)
    const subst = (a, b) => items[a].cat === items[b].cat && sim[a][b] > 0.85;
    return { S, items, sim, subst };
  }

  // Full breakdown of a sandwich: taste harmony, then deductions for redundancy and missing structure.
  function explain(E, set) {
    const { S, items, sim, subst } = E;
    const pairs = [];
    for (let x = 0; x < set.length; x++) for (let y = x + 1; y < set.length; y++) pairs.push([set[x], set[y], S[set[x]][set[y]]]);
    const harmony = fit(S, set);
    const penalties = [];
    for (const [a, b, v] of pairs) {
      // a known great pair is fine; otherwise two interchangeable toppings, or two mains of a kind, cost
      if (v >= 7 || items[a].cat !== items[b].cat) continue;
      const twin = v <= 3 && sim[a][b] > 0.95 && subst(a, b);
      if (!twin && !MAIN.has(items[a].cat)) continue;
      penalties.push({ kind: twin ? "twin" : "double", a, b, value: twin ? 0.12 : 0.05 });
    }
    if (set.length >= 2 && !set.some((i) => MAIN.has(items[i].cat))) penalties.push({ kind: "nomain", value: 0.08 });
    const weakest = pairs.length ? pairs.reduce((p, q) => (q[2] < p[2] ? q : p)) : null;
    const score = harmony - sum(penalties.map((p) => p.value));
    return { harmony, score, penalties, weakest, pairs };
  }
  const score = (E, set) => explain(E, set).score;

  // Two results are variants when everything that differs is a like-for-like substitute.
  function isVariant(E, a, b) {
    const da = a.filter((i) => !b.includes(i)), db = b.filter((i) => !a.includes(i));
    if (da.length !== db.length) return false;
    const left = db.slice();
    for (const x of da) {
      const k = left.findIndex((y) => E.subst(x, y));
      if (k < 0) return false;
      left.splice(k, 1);
    }
    return true;
  }

  // Beam search for the best sandwiches of `size` items containing all `seeds`.
  // `noise` > 0 jitters the ranking (seeded by `seed`) to surprise rather than optimise.
  function suggest(E, seeds, size, { count = 8, exclude = new Set(), noise = 0, seed = 1, width = 250 } = {}) {
    const { items } = E;
    const r = rng(seed);
    const cands = items.map((_, i) => i).filter((i) => !exclude.has(i) && !seeds.includes(i));
    let beam = seeds.length ? [seeds.slice()] : cands.map((i) => [i]);
    while (beam.length && beam[0].length < size) {
      const seen = new Map();
      for (const set of beam)
        for (const c of cands) {
          if (set.includes(c)) continue;
          const next = [...set, c];
          const key = next.slice().sort((a, b) => a - b).join(",");
          if (!seen.has(key)) seen.set(key, next);
        }
      const ranked = [...seen.values()].map((s) => [score(E, s) + (noise ? noise * -Math.log(-Math.log(r() || 1e-9)) : 0), s]).sort((a, b) => b[0] - a[0]);
      // keep the beam varied: one star topping (say mozzarella) may fill at most a sixth of it
      const cap = Math.ceil(width / 6), inBeam = new Map();
      beam = [];
      for (const [, set] of ranked) {
        if (set.some((i) => !seeds.includes(i) && (inBeam.get(i) || 0) >= cap)) continue;
        set.forEach((i) => inBeam.set(i, (inBeam.get(i) || 0) + 1));
        beam.push(set);
        if (beam.length >= width) break;
      }
    }
    // keep results distinct: no like-for-like variants of an earlier one, no topping in more than 3 results
    const out = [], uses = new Map();
    for (const set of beam) {
      if (out.some((o) => isVariant(E, set, o))) continue;
      if (set.some((i) => !seeds.includes(i) && (uses.get(i) || 0) >= 3)) continue;
      out.push(set);
      set.forEach((i) => uses.set(i, (uses.get(i) || 0) + 1));
      if (out.length >= count) break;
    }
    return out.map((set) => ({ set, ...explain(E, set) }));
  }

  // Best replacements for set[k], ranked by the new score.
  function swaps(E, set, k, { count = 6, exclude = new Set() } = {}) {
    const base = score(E, set);
    return E.items
      .map((_, c) => c)
      .filter((c) => !exclude.has(c) && !set.includes(c))
      .map((c) => { const next = set.slice(); next[k] = c; return { item: c, set: next, score: score(E, next) }; })
      .sort((a, b) => b.score - a.score)
      .slice(0, count)
      .map((s) => ({ ...s, delta: s.score - base }));
  }

  return { goodAdj, components, communities, nodeStats, bridges, fit, profileSim, engine, explain, score, isVariant, suggest, swaps, MAIN };
})();

if (typeof module !== "undefined") module.exports = Analysis;
