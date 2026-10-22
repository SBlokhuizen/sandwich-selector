"""A small neural pairing model (PyTorch), trained on hand-set scores, recipe evidence and the rules.

Each topping is described by its category, tags, flavour profile and cuisines, plus a small learned
embedding of its own. A symmetric pair network turns two toppings into a score in [-1, 1].

Training targets, all pairs at once:
  - hand-set pairs (overrides, clashes, classics): weight 1
  - pairs with recipe evidence (evidence.py), calibrated to the score scale: weight 0.5 × confidence
  - every other pair: a weak pull towards the rule score, firmer for outright rule clashes

Run: .venv/bin/python pairnet.py      (5-fold cross-validation against the ridge model)
"""
import contextlib
import io

import numpy as np
import torch
from torch import nn

import build as b
import evidence as ev

TAGS = sorted({t for line in b.ITEMS.strip().splitlines() for t in line.split("|")[3].split()})
CUIS = ["uni", "nl", "snack", "sw", "it", "med", "fr", "us", "as"]


def item_features(items):
    rows = []
    for it in items:
        cat = [float(it["cat"] == c) for c in b.CATS]
        tag = [float(t in it["tags"]) for t in TAGS]
        fl = [v / 3 for v in it["flavour"]]
        cu = [float(c in it["cuisine"]) for c in CUIS]
        rows.append(cat + tag + fl + cu)
    return torch.tensor(rows, dtype=torch.float32)


def calibrate(E, labels):
    """Map recipe PMI to the score scale with score = a·tanh(pmi/c) + b, fitted on pairs that have both."""
    ov = [k for k in E if k in labels]
    pm = np.array([E[k][0] for k in ov]); lab = np.array([labels[k] for k in ov])
    best = None
    for c in [0.5, 1, 1.5, 2, 3]:
        A = np.vstack([np.tanh(pm / c), np.ones_like(pm)]).T
        coef, *_ = np.linalg.lstsq(A, lab, rcond=None)
        err = ((A @ coef - lab) ** 2).mean()
        if best is None or err < best[0]:
            best = (err, c, coef)
    _, c, (a, k) = best
    return lambda p: a * np.tanh(p / c) + k


class PairNet(nn.Module):
    def __init__(self, n_items, n_feat, use_rule, emb=8, hidden=64):
        super().__init__()
        self.use_rule = use_rule
        self.item = nn.Sequential(nn.Linear(n_feat, hidden), nn.GELU(), nn.Linear(hidden, 24))
        self.own = nn.Embedding(n_items, emb)
        nn.init.normal_(self.own.weight, std=0.01)
        d = 24 + emb
        self.pair = nn.Sequential(nn.Linear(3 * d + (1 if use_rule else 0), hidden), nn.GELU(), nn.Linear(hidden, hidden), nn.GELU(), nn.Linear(hidden, 1))

    def forward(self, F, i, j, rule):
        e = torch.cat([self.item(F), self.own.weight], 1)
        a, c = e[i], e[j]
        x = [a + c, a * c, (a - c).abs()]  # symmetric in the two toppings
        if self.use_rule:
            x.append(rule[:, None])
        return torch.tanh(self.pair(torch.cat(x, 1)).squeeze(1))


def targets(items, R, labels, E, held_out=()):
    """Training pairs (i, j), target, weight."""
    n = len(items)
    to_score = calibrate(E, {k: v for k, v in labels.items() if k not in held_out})
    iu, ju = np.triu_indices(n, 1)
    y = R[iu, ju].copy()
    w = np.where(R[iu, ju] <= -0.8, 0.3, 0.005)  # rule prior: firm for clear clashes, loose elsewhere
    pos = {(int(a), int(c)): k for k, (a, c) in enumerate(zip(iu, ju))}
    for k, (p, conf) in E.items():
        y[pos[k]] = to_score(p); w[pos[k]] = 0.5 * conf
    for k, v in labels.items():
        if k in held_out:
            continue
        y[pos[k]] = v; w[pos[k]] = 1.0
    return iu, ju, y, w, pos


def train(items, R, labels, E, use_rule=True, held_out=(), seeds=3, steps=1500, verbose=False):
    torch.set_num_threads(8)
    F = item_features(items)
    iu, ju, y, w, pos = targets(items, R, labels, E, held_out)
    I, J = torch.tensor(iu), torch.tensor(ju)
    Y, W = torch.tensor(y, dtype=torch.float32), torch.tensor(w, dtype=torch.float32)
    rule = torch.tensor(R[iu, ju], dtype=torch.float32)
    preds = []
    for s in range(seeds):
        torch.manual_seed(s)
        net = PairNet(len(items), F.shape[1], use_rule)
        opt = torch.optim.AdamW(net.parameters(), lr=3e-3, weight_decay=1e-3)
        for step in range(steps):
            opt.zero_grad()
            out = net(F, I, J, rule)
            loss = (W * (out - Y) ** 2).sum() / W.sum() + 1e-3 * net.own.weight.pow(2).sum()
            loss.backward()
            opt.step()
        with torch.no_grad():
            preds.append(net(F, I, J, rule).numpy())
    P = np.zeros_like(R)
    P[iu, ju] = np.mean(preds, 0)
    return P + P.T, pos


def report(name, pred, y):
    good, bad = pred[y >= 0.6], pred[y <= 0.0]
    auc = (good[:, None] > bad[None, :]).mean() + 0.5 * (good[:, None] == bad[None, :]).mean()
    fake = ((pred >= 0.6) & (y <= 0.2)).sum() / max(1, (y <= 0.2).sum())
    print(f"  {name:28s} RMSE {np.sqrt(((pred - y) ** 2).mean()):.3f} · ranks good above bad {auc:.1%} · bad passed off as good {fake:.1%}")


def cross_validate(folds=5, seed=7, strict=True, seeds=1, steps=1000, ridge_only=False):
    """strict: hold out whole hand-set lines (a line like "pindakaas × hagelslag" makes many near-identical
    pairs), and also report a run where held-out pairs lose their recipe evidence too."""
    items = b.parse_items()
    R = b.rule_matrix(items)
    groups = {}
    labels = b.hand_set(items, groups)
    E = ev.recipe_evidence(items)
    keys = list(labels)
    y = np.array([labels[k] for k in keys])
    rng = np.random.default_rng(seed)
    if strict:
        names = sorted(set(groups.values()))
        gfold = dict(zip(names, rng.permutation(len(names)) % folds))
        fold = np.array([gfold[groups[k]] for k in keys])
    else:
        fold = rng.permutation(len(keys)) % folds
    preds = {"rules only": np.array([R[k] for k in keys])}
    runs = [("ridge (current)", None, False), ("ridge + recipes", "ridge", False), ("ridge + recipes, hidden for held-out", "ridge", True)]
    runs += [] if ridge_only else [("neural net", False, False), ("neural net, no recipes for held-out", False, True)]
    for name, use_rule, hide in runs:
        p = np.zeros(len(keys))
        for f in range(folds):
            held = {keys[q] for q in np.where(fold == f)[0]}
            if use_rule is None:
                with contextlib.redirect_stdout(io.StringIO()):
                    M = b.learn(items, R, {k: v for k, v in labels.items() if k not in held}, verbose=False)
            elif use_rule == "ridge":
                train_labels = {k: v for k, v in labels.items() if k not in held}
                to_score = calibrate(E, train_labels)
                Ev = {k: (to_score(p_), 0.5 * c_) for k, (p_, c_) in E.items() if k not in train_labels and not (hide and k in held)}
                M = b.learn(items, R, train_labels, verbose=False, evidence=Ev)
            else:
                Ef = {k: v for k, v in E.items() if not (hide and k in held)}
                M, _ = train(items, R, labels, Ef, use_rule=use_rule, held_out=held, seeds=seeds, steps=steps)
            for q in np.where(fold == f)[0]:
                p[q] = M[keys[q]]
        preds[name] = p
        print(f"  ...{name} done", flush=True)
    print(f"{len(keys)} hand-set pairs in {len(set(groups.values()))} source lines, {folds}-fold cross-validation, {'whole lines held out' if strict else 'random pairs'}")
    for name, p in preds.items():
        report(name, p, y)


if __name__ == "__main__":
    import sys
    cross_validate(ridge_only="--ridge" in sys.argv)
