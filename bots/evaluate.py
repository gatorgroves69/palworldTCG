"""Position evaluation shared by the bots. Higher = better for `me`.

Units are roughly "one card in hand = 3.5". The weights are hand-set, not
fitted to win rates; calibration must not be done by tuning them to match
the target (docs/assumptions.md, bots section).
"""
from __future__ import annotations

from engine.game import Game
from engine.state import CardInstance

WIN = 1000.0
LIFE = 4.0          # per life point
LOW_LIFE_BONUS = 3.0  # extra per life point for the last 3
HAND_CARD = 3.5
INTERRUPT_IN_HAND = 1.5  # extra: it's a defensive option on their turn
PAL_BODY = 3.0  # a Pal on the base is worth more than the same card in hand
GEAR_BASE = HAND_CARD  # a Gear on the base is at least the card it cost ...
GEAR_PER_COST = 0.4    # ... plus its lasting ACT value, which scales with cost
RESOURCE = 0.5         # per Material/Ingredient (spent 3 at a time on ~1-card effects)
SOUL_FOR_INTERRUPT = 0.5  # a standing soul lets you pay an Interrupt's ① on their turn


def pal_value(game: Game, c: CardInstance) -> float:
    """What a Pal on the base is worth: a body, its hitting power, its strike."""
    return PAL_BODY + max(game.power(c), 0) / 150 + 1.5 * game.strike(c)


def gear_value(c: CardInstance) -> float:
    """Gear stays on the base and keeps activating; a one-step lookahead can't
    see those future uses, so value it above the card in hand."""
    return GEAR_BASE + GEAR_PER_COST * c.defn.cost


def structure_value(c: CardInstance) -> float:
    """Like gear: the card, plus its repeatable ability, scaled by cost."""
    return HAND_CARD + GEAR_PER_COST * c.defn.cost


def hand_value(ps, known: bool = True) -> float:
    """`known=False` for the opponent's hand: only its size is public."""
    v = HAND_CARD * len(ps.hand)
    if known:
        v += INTERRUPT_IN_HAND * sum(1 for c in ps.hand if c.kw("interrupt"))
    return v


def life_value(life: int) -> float:
    life = max(life, 0)
    return LIFE * life + LOW_LIFE_BONUS * min(life, 3)


def _locked(game: Game, c: CardInstance, owner_next_turn: bool) -> bool:
    """Will `c` still be rested during its owner's next turn?"""
    if not c.rested:
        return False
    return bool(c.stand_locks and not game.can_stand(c)) or (
        owner_next_turn and c.owner in c.skip_stand)


def evaluate(game: Game, me: int) -> float:
    if game.winner is not None or game.reason:
        if game.winner is None:
            return 0.0
        return WIN if game.winner == me else -WIN
    opp = game.opponent(me)
    P, O = game.players[me], game.players[opp]
    score = life_value(P.life) - life_value(O.life)
    score += hand_value(P) - hand_value(O, known=False)

    opp_max_power = max((game.power(c) for c in O.pals if not _locked(game, c, True)), default=0)
    my_turn = game.active == me
    for c in P.pals:
        v = pal_value(game, c)
        if my_turn and c.rested:
            # Rested through their turn: can't block, and can be attacked.
            v *= 0.7 if opp_max_power >= game.power(c) else 0.9
        if _locked(game, c, True):
            v *= 0.5
        score += v
    for c in O.pals:
        v = pal_value(game, c)
        if _locked(game, c, True):
            v *= 0.5
        score -= v
    score += sum(gear_value(c) for c in P.base if c.type.value == "gear")
    score -= sum(gear_value(c) for c in O.base if c.type.value == "gear")
    score += sum(structure_value(c) for c in P.structures)
    score -= sum(structure_value(c) for c in O.structures)
    for kind in ("material", "ingredient"):
        score += RESOURCE * (min(P.resources[kind], 9) - min(O.resources[kind], 9))
    if any(c.kw("interrupt") for c in P.hand) and my_turn:
        score += SOUL_FOR_INTERRUPT * min(P.souls_standing, 1)
    for ps, sign in ((P, 1), (O, -1)):
        if len(ps.deck) <= 4:
            score -= sign * (5 - len(ps.deck)) * 6
    return score
