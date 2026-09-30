"""Position features for the learned evaluation (public information + own hand).

`features(game, me, me_next)` describes the position from player `me`'s side.
`me_next` says whether `me` acts next (True at the start of our turn, False
when scoring a position in the middle or at the end of our own turn).
"""
from __future__ import annotations

from engine.game import Game

FEATURES = [
    "bias",
    "life_me", "life_opp", "low_life_me", "low_life_opp",
    "hand_me", "hand_opp", "interrupts_me",
    "pals_me", "pals_opp",
    "power_me", "power_opp", "strike_me", "strike_opp",
    "standing_power_me", "standing_power_opp",
    "max_power_me", "max_power_opp",
    "locked_me", "locked_opp",
    "gear_me", "gear_opp", "structures_me", "structures_opp",
    "low_deck_me", "low_deck_opp",
    "souls_me", "souls_opp",
    "resources_me", "resources_opp",
    "me_next",
]


def _side(game: Game, p: int, me_next_side: bool) -> dict:
    ps = game.players[p]
    pals = ps.pals
    powers = [max(game.power(c), 0) / 1000 for c in pals]
    locked = sum(1 for c in pals if c.rested and (
        (c.stand_locks and not game.can_stand(c)) or (me_next_side and p in c.skip_stand)))
    return {
        "life": max(ps.life, 0), "low_life": min(max(ps.life, 0), 3), "hand": len(ps.hand),
        "pals": len(pals), "power": sum(powers),
        "strike": sum(max(game.strike(c), 0) for c in pals),
        "standing_power": sum(pw for pw, c in zip(powers, pals) if not c.rested),
        "max_power": max(powers, default=0.0), "locked": locked,
        "gear": sum(1 for c in ps.base if c.type.value == "gear"),
        "structures": len(ps.structures),
        "low_deck": max(0, 6 - len(ps.deck)), "souls": ps.souls,
        "resources": min(ps.resources["material"] + ps.resources["ingredient"], 9),
    }


def features(game: Game, me: int, me_next: bool) -> list[float]:
    opp = game.opponent(me)
    a = _side(game, me, me_next)
    b = _side(game, opp, not me_next)
    x = {"bias": 1.0, "me_next": 1.0 if me_next else 0.0,
         "interrupts_me": sum(1 for c in game.players[me].hand if c.kw("interrupt"))}
    for k, v in a.items():
        x[f"{k}_me"] = v
    for k, v in b.items():
        x[f"{k}_opp"] = v
    return [float(x[f]) for f in FEATURES]
