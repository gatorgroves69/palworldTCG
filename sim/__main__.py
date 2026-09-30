"""Command-line entry point.

    python -m sim run --deck data/decks/A.txt --opp data/decks/B.txt --games 2000 --seed 1 \\
        --out results/<run_id>/
    python -m sim replay --deck ... --opp ... --game-seed 1000017
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from bots import BOTS

from .runner import MatchSpec, make_game, run


def _spec(a) -> MatchSpec:
    return MatchSpec(a.deck, a.opp, a.bot, a.structures, a.cards)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m sim")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--deck", required=True, help="decklist for the deck under test")
        p.add_argument("--opp", required=True, help="opponent decklist")
        p.add_argument("--bot", default="heuristic", choices=sorted(BOTS))
        p.add_argument("--structures", default="any", choices=["any", "rested_only"],
                       help="A2: may standing structures be attacked (docs/assumptions.md)")
        p.add_argument("--cards", default=None, help="cards.json path (default data/cards.json)")

    r = sub.add_parser("run", help="play a batch and write summary.json + games.jsonl")
    common(r)
    r.add_argument("--games", type=int, default=2000)
    r.add_argument("--seed", type=int, default=1)
    r.add_argument("--out", type=Path, default=None, help="default results/<timestamp>_<decks>/")
    r.add_argument("--workers", type=int, default=None)
    r.add_argument("--logs", type=int, default=2, help="write full logs for the first N games")
    r.add_argument("--no-report", action="store_true")

    m = sub.add_parser("matrix", help="every pair of decks, calibrated against real data")
    m.add_argument("--decks", nargs="+", required=True)
    m.add_argument("--games", type=int, default=2000)
    m.add_argument("--seed", type=int, default=1)
    m.add_argument("--out", type=Path, default=None)
    m.add_argument("--workers", type=int, default=None)
    m.add_argument("--bot", default="heuristic", choices=sorted(BOTS))
    m.add_argument("--structures", default="any", choices=["any", "rested_only"])

    o = sub.add_parser("optimize", help="M3: propose and test card swaps vs the weighted field")
    o.add_argument("--deck", required=True)
    o.add_argument("--rounds", type=int, default=1)
    o.add_argument("--seed", type=int, default=1)
    o.add_argument("--bot", default="heuristic2", choices=sorted(BOTS))
    o.add_argument("--confirm-bot", default="heuristic", choices=sorted(BOTS))
    o.add_argument("--max-tries", type=int, default=6, help="swaps tested per round")
    o.add_argument("--batch", type=int, default=800, help="games per batch per version")
    o.add_argument("--max-batches", type=int, default=5)
    o.add_argument("--confirm-games", type=int, default=3000)
    o.add_argument("--baseline-games", type=int, default=3000)

    gt = sub.add_parser("gauntlet", help="M4: one deck vs the weighted field; Telegram summary")
    gt.add_argument("--deck", required=True)
    gt.add_argument("--games", type=int, default=20000)
    gt.add_argument("--seed", type=int, default=1)
    gt.add_argument("--bot", default="heuristic2", choices=sorted(BOTS))
    gt.add_argument("--out", type=Path, default=None)
    gt.add_argument("--workers", type=int, default=None)

    p = sub.add_parser("replay", help="replay one game and print its full log")
    common(p)
    p.add_argument("--game-seed", type=int, required=True)

    a = ap.parse_args(argv)
    if a.cmd == "gauntlet":
        from .overnight import run_gauntlet
        r = run_gauntlet(a.deck, a.games, a.seed, a.bot, a.out, a.workers)
        print((Path(r["out"]) / "telegram.txt").read_text(encoding="utf-8"))
        print(f"\nwrote {r['out']}/summary.json, telegram.txt, games.jsonl")
        return 0
    if a.cmd == "optimize":
        from .optimize import TestConfig, optimize
        cfg = TestConfig(batch=a.batch, max_batches=a.max_batches, confirm_games=a.confirm_games)
        optimize(a.deck, a.rounds, a.seed, a.bot, a.confirm_bot, a.max_tries, cfg,
                 a.baseline_games)
        return 0
    if a.cmd == "matrix":
        from .matrix import run_matrix
        out = a.out or Path("results") / (
            datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "_matrix")
        r = run_matrix(a.decks, a.games, a.seed, out, a.bot, a.structures, a.workers)
        print((out / "matrix.md").read_text(encoding="utf-8"))
        print(f"wrote {out}/matrix.json, matrix.md ({r['passing_pairs']}/"
              f"{r['calibrated_pairs']} calibrated pairs within ±5)")
        return 0
    spec = _spec(a)
    if a.cmd == "replay":
        g = make_game(spec, a.game_seed, log=True)
        g.play()
        print("\n".join(g.lines))
        return 0

    out = a.out or Path("results") / (
        datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        + f"_{Path(a.deck).stem}_vs_{Path(a.opp).stem}")
    print(f"{a.games} games: {Path(a.deck).stem} vs {Path(a.opp).stem} -> {out}")
    summary = run(spec, a.games, a.seed, out, a.workers, a.logs)
    if not a.no_report:
        from analysis.report import write_report
        write_report(out)
    print(json.dumps({k: summary[k] for k in ("win_rate", "ci95", "going_first", "going_second",
                                              "avg_turns")}, indent=2))
    print(f"wrote {out}/summary.json, games.jsonl" + ("" if a.no_report else ", report.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
