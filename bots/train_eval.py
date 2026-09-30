"""Fit the learned evaluation from self-play: `python -m bots.train_eval`.

1. Play `--games` games per deck pairing (every pair of decks in data/decks
   plus mirrors) with `--bot` on both sides.
2. After every turn, record the position's features from both players' sides,
   labelled with who eventually won.
3. Fit an L2-regularised logistic regression P(win | features) and write
   bots/eval_weights.json.

Only simulated outcomes are used, never the real-world calibration data.
Needs numpy (training only): `uv run --with numpy python -m bots.train_eval`.
"""
from __future__ import annotations

import argparse
import glob
import itertools
import json
from multiprocessing import Pool
from pathlib import Path

from engine.game import GameOver

from .features import FEATURES, features

OUT = Path(__file__).resolve().parent / "eval_weights.json"


def _positions(args) -> list[tuple[list[float], float]]:
    deck, opp, bot, seed = args
    from sim.runner import MatchSpec, make_game
    g = make_game(MatchSpec(deck, opp, bot), seed)
    rows: list[tuple[int, list[float]]] = []
    try:
        g.setup()
        while g.turn < g.turn_cap:
            g.take_turn()
            for p in (0, 1):
                rows.append((p, features(g, p, g.active == p)))
    except GameOver:
        pass
    if g.winner is None:
        return []
    return [(x, 1.0 if p == g.winner else 0.0) for p, x in rows]


def generate(games: int, bot: str, seed: int) -> tuple[list, list]:
    decks = sorted(glob.glob("data/decks/*.txt"))
    pairs = list(itertools.combinations(decks, 2)) + [(d, d) for d in decks]
    jobs = [(a, b, bot, seed * 1_000_000 + k * 1000 + i)
            for k, (a, b) in enumerate(pairs) for i in range(games)]
    X, y = [], []
    with Pool() as pool:
        for rows in pool.imap_unordered(_positions, jobs, chunksize=4):
            for x, label in rows:
                X.append(x)
                y.append(label)
    return X, y


def fit(X, y, l2: float = 1e-3, steps: int = 3000, lr: float = 0.5):
    import numpy as np
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    mu[0], sd[0] = 0.0, 1.0  # bias column
    sd[sd == 0] = 1.0
    Z = (X - mu) / sd
    w = np.zeros(Z.shape[1])
    for _ in range(steps):  # full-batch gradient descent; the problem is small
        p = 1 / (1 + np.exp(-Z @ w))
        grad = Z.T @ (p - y) / len(y) + l2 * np.r_[0.0, w[1:]]
        w -= lr * grad
    p = 1 / (1 + np.exp(-Z @ w))
    loss = float(-np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)))
    acc = float(np.mean((p > 0.5) == (y > 0.5)))
    raw = w / sd  # back to raw feature units
    raw[0] = w[0] - float(np.sum(w[1:] * mu[1:] / sd[1:]))
    return raw.tolist(), loss, acc


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=150, help="games per deck pairing")
    ap.add_argument("--bot", default="heuristic")
    ap.add_argument("--seed", type=int, default=77)
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    X, y = generate(a.games, a.bot, a.seed)
    w, loss, acc = fit(X, y)
    a.out.write_text(json.dumps({
        "features": FEATURES, "weights": w, "positions": len(y), "games_per_pair": a.games,
        "bot": a.bot, "seed": a.seed, "log_loss": round(loss, 4), "accuracy": round(acc, 4),
    }, indent=2), encoding="utf-8")
    print(f"{len(y)} positions, log loss {loss:.4f}, accuracy {acc:.3f} -> {a.out}")
    for f, v in zip(FEATURES, w):
        print(f"  {f:22} {v:+.4f}")


if __name__ == "__main__":
    main()
