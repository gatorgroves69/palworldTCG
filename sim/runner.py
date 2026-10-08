"""Run batches of games in parallel and write results.

Every game gets its own seed (`game_seed(run_seed, i)`), and both bots are
seeded from it, so any single game can be replayed exactly with
`python -m sim replay`, no matter how many workers the batch used.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import time
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path

from engine import Game, RulesConfig

DECK_SIDE, OPP_SIDE = 0, 1


def game_seed(run_seed: int, i: int) -> int:
    return run_seed * 1_000_000 + i


@dataclass(frozen=True)
class MatchSpec:
    deck: str
    opp: str
    bot: str = "heuristic"
    structures_attackable: str = "any"
    cards: str | None = None
    mulligan: str = "default"  # keep-or-redraw rule for the deck under test (sim/mulligan.py)
    deck_bot: str | None = None  # a different bot for the deck under test only (J17 sweeps)


_CACHE: dict = {}


def _setup(spec: MatchSpec):
    """Load decks and card implementations once per worker process."""
    key = spec
    if key not in _CACHE:
        import cards  # noqa: F401  (registers implementations)
        from bots import bot_class
        from cards import REGISTRY
        from cards.db import DEFAULT_PATH, load_card_db
        from cards.decklist import load_deck
        from engine.deck import validate_deck
        db = load_card_db(spec.cards or DEFAULT_PATH)
        decks = [load_deck(spec.deck, db), load_deck(spec.opp, db)]
        for d in decks:
            validate_deck(d)
        _CACHE[key] = (decks, REGISTRY, bot_class(spec.bot))
    return _CACHE[key]


def make_game(spec: MatchSpec, seed: int, log: bool = False) -> Game:
    decks, registry, bot_cls = _setup(spec)
    from bots import bot_class
    deck_cls = bot_class(spec.deck_bot) if spec.deck_bot else bot_cls
    bots = [deck_cls(seed * 2 + 1), bot_cls(seed * 2 + 2)]
    if spec.mulligan != "default":
        from .mulligan import redraw_fn
        bots[DECK_SIDE].choose_redraw = redraw_fn(spec.mulligan)
    return Game(decks, registry, bots, seed=seed, log=log,
                rules=RulesConfig(structures_attackable=spec.structures_attackable))


def play_one(args) -> dict:
    spec, seed, keep_log = args
    g = make_game(spec, seed, log=keep_log)
    r = g.play()
    rec = {
        "seed": seed,
        "winner": {DECK_SIDE: "deck", OPP_SIDE: "opp", None: "draw"}[r.winner],
        "reason": r.reason,
        "turns": r.turns,
        "first": "deck" if r.first_player == DECK_SIDE else "opp",
        "life": r.life,
        "drawn": [st.drawn for st in r.stats],
        "opening": [st.opening_hand for st in r.stats],
        "redrew": [st.redrew for st in r.stats],
        "played": [st.played for st in r.stats],
        "life_lost_to": [dict(st.life_lost_to) for st in r.stats],
        "lucky_saves": [st.lucky_saves for st in r.stats],
        "hand_end": [[c.code for c in g.players[p].hand] for p in (0, 1)],
        "history": [[h["turn"], h["active"], h["life"], h["hand"], h["deck"], h["pals"],
                     h["board_power"]] for h in r.history],
    }
    if keep_log:
        rec["_log"] = "\n".join(g.lines)
    return rec


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def rate(games: list[dict]) -> dict:
    """Win rate for the deck; draws count as half a win."""
    n = len(games)
    w = sum(g["winner"] == "deck" for g in games)
    d = sum(g["winner"] == "draw" for g in games)
    k = w + d / 2
    lo, hi = wilson(round(k), n)
    return {"games": n, "wins": w, "losses": n - w - d, "draws": d,
            "win_rate": round(k / n, 4) if n else None, "ci95": [round(lo, 4), round(hi, 4)]}


def git_commit() -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return None


def run(spec: MatchSpec, games: int, seed: int, out: Path, workers: int | None = None,
        logs: int = 2, progress: bool = True) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    workers = workers or os.cpu_count() or 1
    jobs = [(spec, game_seed(seed, i), i < logs) for i in range(games)]
    t0 = time.time()
    results: list[dict] = []
    with Pool(workers) as pool:
        for rec in pool.imap(play_one, jobs, chunksize=max(1, games // (workers * 8))):
            results.append(rec)
            if progress and len(results) % max(1, games // 10) == 0:
                print(f"  {len(results)}/{games} games", flush=True)
    elapsed = time.time() - t0

    logdir = out / "logs"
    with open(out / "games.jsonl", "w", encoding="utf-8") as f:
        for rec in results:
            log = rec.pop("_log", None)
            if log is not None:
                logdir.mkdir(exist_ok=True)
                (logdir / f"game_{rec['seed']}.log").write_text(log, encoding="utf-8")
            f.write(json.dumps(rec, separators=(",", ":")) + "\n")

    first = [g for g in results if g["first"] == "deck"]
    second = [g for g in results if g["first"] == "opp"]
    summary = {
        "deck": Path(spec.deck).stem,
        "opp": Path(spec.opp).stem,
        "bot": spec.bot,
        "rules": {"structures_attackable": spec.structures_attackable},
        "seed": seed,
        "commit": git_commit(),
        **rate(results),
        "going_first": rate(first),
        "going_second": rate(second),
        "avg_turns": round(sum(g["turns"] for g in results) / len(results), 2),
        "end_reasons": {r: sum(g["reason"] == r for g in results)
                        for r in sorted({g["reason"] for g in results})},
        "seconds": round(elapsed, 1),
        "replay": (f"python -m sim replay --deck {spec.deck} --opp {spec.opp} --bot {spec.bot} "
                   f"--structures {spec.structures_attackable} --game-seed <seed>"),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
