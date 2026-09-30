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

from .runner import MatchSpec, make_game, run


def _spec(a) -> MatchSpec:
    return MatchSpec(a.deck, a.opp, a.bot, a.structures, a.cards)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m sim")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--deck", required=True, help="decklist for the deck under test")
        p.add_argument("--opp", required=True, help="opponent decklist")
        p.add_argument("--bot", default="heuristic", choices=["heuristic", "rules", "random"])
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

    p = sub.add_parser("replay", help="replay one game and print its full log")
    common(p)
    p.add_argument("--game-seed", type=int, required=True)

    a = ap.parse_args(argv)
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
