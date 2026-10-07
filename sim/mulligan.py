"""Keep-or-redraw rules for the deck under test, compared on the same seeds.

    python -m sim mulligan --deck <list> --games 12000 --seed 141 [--bot heuristic2]

Each rule decides from the 5-card opening hand only. The opponent always uses the
bot's own rule. The report gives, per rule: weighted win rate vs the field, going
first / going second, and how often the rule redraws.
"""
from __future__ import annotations

from typing import Callable


def _cheap_pals(hand, top=4):
    return [c for c in hand if c.is_pal and c.defn.cost <= top]


def _heavy(hand):
    return sum(1 for c in hand if c.defn.cost >= 7)


# name -> (plain-English rule, redraw?(hand))
RULES: dict[str, tuple[str, Callable]] = {
    "default": ("Redraw with no Pal costing ◇4 or less, or 3+ cards costing ◇7+",
                lambda h: not _cheap_pals(h) or _heavy(h) >= 3),
    "keep_all": ("Never redraw",
                 lambda h: False),
    "need_2drop": ("Redraw without a ◇2 Pal (Lamball, Cattiva, Fuack)",
                   lambda h: not _cheap_pals(h, 2)),
    "two_cheap": ("Redraw without 2+ Pals costing ◇4 or less",
                  lambda h: len(_cheap_pals(h)) < 2),
    "cheap_and_heavy2": ("Redraw with no Pal costing ◇4 or less, or 2+ cards costing ◇7+",
                         lambda h: not _cheap_pals(h) or _heavy(h) >= 2),
}


def redraw_fn(rule: str):
    """A choose_redraw(game, player) for the bot playing the deck under test."""
    _, f = RULES[rule]
    return lambda game, player: f(game.players[player].hand)


def mulligan_report(deck: str, games: int, seed: int, bot: str, rules: list[str],
                    workers: int | None = None) -> str:
    from .gauntlet import field_weights, play_gauntlet
    weights = field_weights()
    rows = {}
    for r in rules:
        res = play_gauntlet(deck, weights, games, seed, bot, workers=workers,
                            keep_records=True, mulligan=r)
        first = second = 0.0
        redraws = n = 0
        for d, w in weights.items():
            recs = res.per_opp[d].records
            f = [g for g in recs if g["first"] == "deck"]
            s = [g for g in recs if g["first"] == "opp"]
            first += w * sum(g["winner"] == "deck" for g in f) / max(len(f), 1)
            second += w * sum(g["winner"] == "deck" for g in s) / max(len(s), 1)
            redraws += sum(bool(g["redrew"][0]) for g in recs)
            n += len(recs)
        rows[r] = (res.win_rate, res.se, first, second, redraws / max(n, 1))
    base = rows.get("default", next(iter(rows.values())))
    lines = [f"**Mulligan rules**, `{deck}`, bot {bot}, {games} games per rule, seed {seed} "
             "(same seeds for every rule)", "",
             "| Rule | Win | vs default | Going first | Going second | Redraws |",
             "|---|---|---|---|---|---|"]
    for r, (wr, se, f, s, rd) in rows.items():
        d = wr - base[0]
        z = d / ((se ** 2 + base[1] ** 2) ** 0.5) if r != "default" else 0
        lines.append(f"| {RULES[r][0]} | {100 * wr:.1f}% | "
                     + ("—" if r == "default" else f"{100 * d:+.1f} (z {z:.1f})")
                     + f" | {100 * f:.1f}% | {100 * s:.1f}% | {100 * rd:.0f}% |")
    return "\n".join(lines) + "\n"
