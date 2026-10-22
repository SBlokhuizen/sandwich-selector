// Graph analysis on the score matrix S (integers -10..10). Pure functions, usable in browser and node.
const Analysis = (() => {
  const sum = (xs) => { let s = 0; for (const x of xs) s += x; return s; };

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

  // Louvain modularity communities on the weighted good-edge graph.
  function louvain(S, thr) {
    let adj = S.map((row, i) => new Map(row.flatMap((v, j) => (i !== j && v >= thr ? [[j, v]] : []))));
    let member = adj.map((_, i) => i);
    for (;;) {
      const n = adj.length, k = adj.map((m) => sum(m.values())), m2 = sum(k);
      if (!m2) break;
      const comm = adj.map((_, i) => i), tot = k.slice();
      let moved = true, any = false;
      while (moved) {
        moved = false;
        for (let i = 0; i < n; i++) {
          const ci = comm[i], w = new Map();
          for (const [j, x] of adj[i]) if (j !== i) w.set(comm[j], (w.get(comm[j]) || 0) + x);
          tot[ci] -= k[i];
          let best = ci, gain = (w.get(ci) || 0) - (tot[ci] * k[i]) / m2;
          for (const [c, x] of w) {
            const g = x - (tot[c] * k[i]) / m2;
            if (g > gain + 1e-9) { gain = g; best = c; }
          }
          tot[best] += k[i];
          comm[i] = best;
          if (best !== ci) moved = any = true;
        }
      }
      if (!any) break;
      const ids = new Map();
      comm.forEach((c) => ids.has(c) || ids.set(c, ids.size));
      const next = Array.from({ length: ids.size }, () => new Map());
      for (let i = 0; i < n; i++)
        for (const [j, x] of adj[i]) {
          const a = ids.get(comm[i]), b = ids.get(comm[j]);
          next[a].set(b, (next[a].get(b) || 0) + x);
        }
      member = member.map((c) => ids.get(comm[c]));
      adj = next;
    }
    // relabel by size, largest community = 0
    const size = new Map();
    member.forEach((c) => size.set(c, (size.get(c) || 0) + 1));
    const order = [...size.keys()].sort((a, b) => size.get(b) - size.get(a));
    return member.map((c) => order.indexOf(c));
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

  // Beam search for the most cohesive sandwiches of `size` items containing all `seeds`.
  function suggest(S, items, seeds, size, count = 8, exclude = new Set()) {
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
      beam = [...seen.values()].map((s) => [fit(S, s), s]).sort((a, b) => b[0] - a[0]).slice(0, 80).map((x) => x[1]);
    }
    // diversity: drop a result that only swaps one item for a same-category item of an earlier result
    const out = [];
    for (const set of beam) {
      const similar = out.some((r) => {
        const a = set.filter((i) => !r.includes(i)), b = r.filter((i) => !set.includes(i));
        return a.length <= 1 && (a.length === 0 || items[a[0]].cat === items[b[0]].cat);
      });
      if (!similar) out.push(set);
      if (out.length >= count) break;
    }
    return out.map((set) => ({ set, fit: fit(S, set) }));
  }

  return { goodAdj, components, louvain, nodeStats, bridges, fit, suggest };
})();

if (typeof module !== "undefined") module.exports = Analysis;
