"""Loss tags: why did the losing side lose this game?

A game can carry several tags. Tags describe the *loser's* game. Thresholds
are fixed here (not tuned per run) so tags are comparable across runs.
"""
from __future__ import annotations

from collections import Counter

EARLY_PAL_COST = 4        # a Pal you can deploy by your 2nd turn
BOARD_DEFICIT = 1000      # total Pal power behind by this much counts as "behind"
FAST_GAME_TURNS = 12      # games this short are "fast"
LOST_TO_SHARE = 0.4       # one card did >= 40% of the damage


def rnd(turn: int) -> int:
    """Round number: turns 1-2 are round 1, 3-4 round 2, ..."""
    return (turn + 1) // 2


def own_turns(went_first: bool, n: int) -> list[int]:
    start = 1 if went_first else 2
    return [start + 2 * k for k in range(n)]


def loss_tags(g: dict, db) -> list[str]:
    """Tags for the loser of game record `g` (see sim/runner.py for the format)."""
    if g["winner"] == "draw":
        return ["draw"]
    L = 0 if g["winner"] == "opp" else 1
    W = 1 - L
    loser_first = (g["first"] == "deck") == (L == 0)
    tags: list[str] = []

    opening = g["opening"][L]
    if not any(db[c].type.value == "pal" and db[c].cost <= EARLY_PAL_COST for c in opening):
        tags.append("weak_opening_hand")

    played_turns = {t for t, _ in g["played"][L]}
    if not played_turns & set(own_turns(loser_first, 2)):
        tags.append("no_early_play")

    hist = g["history"]
    behind_from = None
    for i, (turn, _active, _life, _hand, _deck, _pals, bp) in enumerate(hist):
        if all(h[6][W] > h[6][L] for h in hist[i:]) and bp[W] - bp[L] >= BOARD_DEFICIT:
            behind_from = turn
            break
    if behind_from is not None:
        r = rnd(behind_from)
        tags.append("behind_on_board_by_round_" + ("1-3" if r <= 3 else "4-6" if r <= 6 else "7+"))

    if g["reason"] == "deckout":
        tags.append("decked_out")
    elif any(h[3][L] == 0 for h in hist[-4:]):
        tags.append("ran_out_of_cards")

    lost = g["life_lost_to"][L]
    total = sum(lost.values())
    if total:
        code, amt = max(lost.items(), key=lambda kv: kv[1])
        if amt / total >= LOST_TO_SHARE:
            tags.append(f"lost_to:{code}")

    if not loser_first and g["turns"] <= FAST_GAME_TURNS:
        tags.append("too_slow_on_the_draw")

    if g["lucky_saves"][W] >= 3:
        tags.append("opponent_lucky_saves_3+")

    return tags or ["untagged"]


def tag_counts(games: list[dict], db, loser: str) -> tuple[Counter, int]:
    """Tag frequencies over games lost by `loser` ("deck" or "opp")."""
    winner = "opp" if loser == "deck" else "deck"
    lost = [g for g in games if g["winner"] == winner]
    c: Counter = Counter()
    for g in lost:
        c.update(set(loss_tags(g, db)))
    return c, len(lost)
