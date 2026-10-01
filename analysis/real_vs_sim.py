"""Your logged games vs what the sim and online data expect.

    python -m analysis.real_vs_sim [--deck cattiva-azurobe-br] [--summary results/runs/<job>/summary.json]

Reads data/games/real_games.csv (logged through Mew), resolves deck aliases from
config/operator.json, and for each opponent prints your record, your win rate
with a 95% interval, the online win rate for the archetype (latest
data/calibration/matchups_*.json), and the sim's estimate (from a gauntlet
summary.json). A matchup is flagged only when your record is clearly different
from the online rate (two-sided binomial test, p < 0.05), since a handful of games
proves little either way.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / "data" / "games" / "real_games.csv"
OPERATOR = ROOT / "config" / "operator.json"
CAL_DIR = ROOT / "data" / "calibration"


def wilson(k: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def binom_p(k: int, n: int, p: float) -> float:
    """Two-sided exact binomial test: P(an outcome at least as unlikely as k)."""
    if n == 0:
        return 1.0
    probs = [math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    return min(1.0, sum(q for q in probs if q <= probs[k] * (1 + 1e-9)))


def load_games(path: Path = GAMES, aliases: dict | None = None) -> list[dict]:
    aliases = aliases or {}
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("my_deck", "opp_deck"):
            r[k] = aliases.get(r[k], r[k])
    return rows


def online_rates(deck: str) -> dict[str, tuple[float, int]]:
    files = sorted(CAL_DIR.glob("matchups_*.json"))
    if not files:
        return {}
    rows = json.loads(files[-1].read_text(encoding="utf-8"))
    return {r["deck_b"]: (r["win_rate_a"], r.get("games") or 0)
            for r in rows if r["deck_a"] == deck}


def report(deck: str, games: list[dict], sim: dict | None = None) -> str:
    mine = [g for g in games if g["my_deck"] == deck]
    if not mine:
        return (f"No games logged yet for {deck}. Log one by telling Mew, for example: "
                "`log W chillet-bp 1st weekly — notes`.\n")
    online = online_rates(deck)
    sim_field = (sim or {}).get("field", {})
    by_opp: dict[str, list[dict]] = defaultdict(list)
    for g in mine:
        by_opp[g["opp_deck"]].append(g)

    def score(rows):
        return sum(1.0 if r["result"] == "W" else 0.5 if r["result"] == "D" else 0.0
                   for r in rows)

    total = score(mine)
    lo, hi = wilson(total, len(mine))
    first = [g for g in mine if g["first_or_second"] == "first"]
    second = [g for g in mine if g["first_or_second"] == "second"]
    L = [f"# {deck}: your games vs expectations", "",
         f"{len(mine)} games, {100 * total / len(mine):.0f}% "
         f"(95% range {100 * lo:.0f}–{100 * hi:.0f}%). "
         f"Going first {score(first):g}/{len(first)}, going second {score(second):g}/"
         f"{len(second)}.", "",
         "| Opponent | Games | Record | You | Online | Sim | |",
         "|---|---|---|---|---|---|---|"]
    for opp, rows in sorted(by_opp.items(), key=lambda kv: -len(kv[1])):
        k = score(rows)
        n = len(rows)
        w = sum(r["result"] == "W" for r in rows)
        l_ = sum(r["result"] == "L" for r in rows)
        d = n - w - l_
        rec = f"{w}-{l_}" + (f"-{d}" if d else "")
        on = online.get(opp)
        sm = sim_field.get(opp, {}).get("win_rate")
        flag = ""
        if on and n >= 5:
            p = binom_p(round(k), n, on[0])
            if p < 0.05:
                flag = "above online" if k / n > on[0] else "below online"
        L.append(f"| {opp} | {n} | {rec} | {100 * k / n:.0f}% | "
                 + (f"{100 * on[0]:.0f}% (n={on[1]})" if on else "—") + " | "
                 + (f"{100 * sm:.0f}%" if sm is not None else "—") + f" | {flag} |")
    L += ["", "Flags appear only when your record differs from the online rate beyond "
          "chance (p < 0.05). With fewer than about 10 games per matchup, expect none."]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m analysis.real_vs_sim")
    ap.add_argument("--deck", default=None, help="default: config/operator.json default_deck")
    ap.add_argument("--summary", type=Path, default=None,
                    help="a gauntlet summary.json for the sim column")
    a = ap.parse_args(argv)
    cfg = json.loads(OPERATOR.read_text(encoding="utf-8")) if OPERATOR.exists() else {}
    deck = a.deck or cfg.get("default_deck", "cattiva-azurobe-br")
    sim = json.loads(a.summary.read_text(encoding="utf-8")) if a.summary else None
    print(report(deck, load_games(aliases=cfg.get("aliases", {})), sim))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
