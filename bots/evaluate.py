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
RESOURCE_SPENDABLE = 1.0  # ... when a card that consumes that resource is on the base or in hand
# "@human": value of a Pal's own on-death payoff, so the bot deploys and trades these
# like real players (Palify: Stone Pit pilots deploy 2.6 Leezpunk a game, the bot 1.0).
# Counted while the Pal is on the base; when it dies the payoff shows up in hands instead.
DEATH_VALUE = {"TD02-014": HAND_CARD,        # Leezpunk: the opponent discards 1
               "BP01-084": HAND_CARD,        # Menasting: return a normal Pal to hand
               "BP01-028": 0.8 * HAND_CARD}  # Pengullet: draw 1
SOUL_FOR_INTERRUPT = 0.5  # a standing soul lets you pay an Interrupt's ① on their turn


def pal_value(game: Game, c: CardInstance) -> float:
    """What a Pal on the base is worth: a body, its hitting power, its strike."""
    return PAL_BODY + max(game.power(c), 0) / 150 + 1.5 * game.strike(c)


# Repeatable-ability pieces, valued by what one activation produces, in card units
# (a card = 3.5, 3 Material/Ingredient ~ 1.5-3, 500 damage to a Pal ~ 2), times the
# ~1.5 further activations a piece typically gets. Cost is a poor proxy for this: Stone
# Pit costs 1 and makes a card plus 3 Material every turn. Hand-set by card economics,
# not fitted (docs/assumptions.md S5).
ENGINE_BONUS = {
    "TD01-008": 6.0,  # Stone Pit: assign -> 3 Material + draw 1
    "BP01-016": 6.0,  # Primitive Furnace: assign -> 3 Material + draw 1; gear discount
    "TD02-008": 5.0,  # Berry Plantation: assign -> 3 Ingredient + draw 1
    "BP01-063": 5.0,  # Breeding Farm: reveal/deploy a Pal for Ingredient
    "TD01-009": 5.0,  # Weapon Workbench: 800 damage + Strike +1 for 1 Material
    "BP01-090": 4.0,  # Medieval Medicine Workbench: recur a Pal for 3 souls
    "TD01-020": 3.0,  # Primitive Workbench: reveal/deploy structures or gear
    "BP01-088": 3.0,  # Lamp: night on demand + Nocturnal for all
    "BP01-089": 2.5,  # Shoddy Bed: night on demand + a draw
    "BP01-015": 4.0,  # Mounted Machine Gun (gear): 500 damage per Material
    "BP01-044": 2.0,  # Pengullet Rocket Launcher (gear): pump / barrage
    "BP01-045": 2.0,  # Grappling Gun (gear)
}


def gear_value(c: CardInstance) -> float:
    """Gear stays on the base and keeps activating; a one-step lookahead can't
    see those future uses, so value it above the card in hand."""
    return GEAR_BASE + GEAR_PER_COST * c.defn.cost + ENGINE_BONUS.get(c.code, 0.0)


def structure_value(c: CardInstance) -> float:
    """Like gear: the card, plus its repeatable ability. Engine pieces get the bonus
    their per-turn output earns (ENGINE_BONUS); otherwise scaled by cost."""
    return HAND_CARD + GEAR_PER_COST * c.defn.cost + ENGINE_BONUS.get(c.code, 0.0)


def hand_value(ps, known: bool = True) -> float:
    """`known=False` for the opponent's hand: only its size is public."""
    v = HAND_CARD * len(ps.hand)
    if known:
        v += INTERRUPT_IN_HAND * sum(1 for c in ps.hand if c.kw("interrupt"))
    return v


_CONSUMES: dict[tuple[str, str], bool] = {}


def consumes(c: CardInstance, kind: str) -> bool:
    """Does this card have a cost or effect that spends `kind` (Material/Ingredient)?"""
    key = (c.code, kind)
    if key not in _CONSUMES:
        t = c.impl.text.lower()
        _CONSUMES[key] = "consume" in t and kind in t
    return _CONSUMES[key]


def resource_rate(game: Game, ps, kind: str) -> float:
    """Material is only worth what it can buy: full value with a spender in play or in
    hand (Machine Gun, Furnace, Breeding Farm, Lyleen), half otherwise."""
    if any(consumes(c, kind) for c in ps.base) or any(consumes(c, kind) for c in ps.hand):
        return RESOURCE_SPENDABLE
    return RESOURCE


def life_value(life: int) -> float:
    life = max(life, 0)
    return LIFE * life + LOW_LIFE_BONUS * min(life, 3)


def _locked(game: Game, c: CardInstance, owner_next_turn: bool) -> bool:
    """Will `c` still be rested during its owner's next turn?"""
    if not c.rested:
        return False
    return bool(c.stand_locks and not game.can_stand(c)) or (
        owner_next_turn and c.owner in c.skip_stand)


EXPOSURE = (0.7, 0.9)  # value kept by a rested Pal facing a bigger / no bigger enemy
LUCKY_FLIP = 0.18      # rough per-flip lucky chance for the race estimate


def incoming(game: Game, attackers, life: int) -> float:
    """Expected life lost next turn to `attackers` hitting the player, before blocks."""
    total = 0.0
    for c in attackers:
        s = game.strike(c)
        if s > 0:
            total += s * (1 - LUCKY_FLIP) ** s
    return min(total, float(life))


def race_term(game: Game, me: int, leaf: bool) -> float:
    """The race: who is closer to lethal, and are my standing Pals needed as blockers?

    A standing Pal of mine absorbs their biggest attacker next turn. That is worth a
    lot when their expected damage would put me within two turns of dead, and little
    when I am safely ahead, which is when attacking with it is right. Scored at the
    end of my turn (not at a leaf, where my rested Pals are about to stand)."""
    opp = game.opponent(me)
    P, O = game.players[me], game.players[opp]
    their_attackers = [c for c in O.pals if not _locked(game, c, True)]
    threat = incoming(game, their_attackers, P.life)
    if threat <= 0:
        return 0.0
    urgency = min(1.0, (2 * threat) / max(P.life, 1))  # 1.0 when two such turns kill me
    blockers = [c for c in P.pals if not c.rested] if (game.active == me and not leaf) \
        else list(P.pals)
    if not blockers:
        return 0.0
    # Each blocker can stop one attacker; the first stops the biggest hit.
    hits = sorted((game.strike(c) * (1 - LUCKY_FLIP) ** game.strike(c)
                   for c in their_attackers if game.strike(c) > 0), reverse=True)
    saved = sum(hits[: len(blockers)])
    return urgency * LIFE * saved


def evaluate(game: Game, me: int, leaf: bool = False,
             exposure: tuple[float, float] = EXPOSURE, resource_scale: float = 1.0,
             open_soul_by_life: bool = False, death_value: bool = False) -> float:
    """`leaf=True`: scoring at the start of our turn after simulating the opponent's
    reply, so our rested Pals are about to stand and aren't penalized as exposed."""
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
        v = pal_value(game, c) + (DEATH_VALUE.get(c.code, 0.0) if death_value else 0.0)
        if my_turn and c.rested and not leaf:
            # Rested through their turn: can't block, and can be attacked.
            v *= exposure[0] if opp_max_power >= game.power(c) else exposure[1]
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
        score += resource_scale * resource_rate(game, P, kind) * min(P.resources[kind], 9)
        score -= resource_scale * resource_rate(game, O, kind) * min(O.resources[kind], 9)
    if any(c.kw("interrupt") for c in P.hand) and my_turn:
        open_soul = SOUL_FOR_INTERRUPT
        if open_soul_by_life:  # "@human": a soul kept for ① saves a discard, likelier when low
            open_soul = HAND_CARD * (0.15 if P.life >= 7 else 0.4 if P.life >= 4 else 0.7)
        score += open_soul * min(P.souls_standing, 1)
    score += race_term(game, me, leaf) - race_term(game, opp, leaf)
    for ps, sign in ((P, 1), (O, -1)):
        if len(ps.deck) <= 4:
            score -= sign * (5 - len(ps.deck)) * 6
    return score


# ---------------------------------------------------------------- learned evaluation
_LEARNED: dict[str, dict] = {}
LEARNED_SCALE = 16.0  # logit -> roughly the hand-set units (one card ~ 3.5)
DEFAULT_WEIGHTS = "eval_weights.json"


def load_weights(name: str = DEFAULT_WEIGHTS) -> dict:
    if name not in _LEARNED:
        import json
        from pathlib import Path
        _LEARNED[name] = json.loads((Path(__file__).resolve().parent / name)
                                    .read_text(encoding="utf-8"))
    return _LEARNED[name]


def learned_evaluator(name: str = DEFAULT_WEIGHTS):
    """Logistic model fitted on self-play (bots/train_eval.py). `leaf` = we act next.
    `exposure` is accepted for interface compatibility and ignored."""
    from .features import features
    w = load_weights(name)["weights"]

    def evaluate_learned(game: Game, me: int, leaf: bool = False, exposure=None) -> float:
        if game.winner is not None or game.reason:
            if game.winner is None:
                return 0.0
            return WIN if game.winner == me else -WIN
        x = features(game, me, me_next=leaf)
        return LEARNED_SCALE * sum(a * b for a, b in zip(w, x))
    return evaluate_learned


def evaluate_learned(game: Game, me: int, leaf: bool = False, exposure=None) -> float:
    return learned_evaluator()(game, me, leaf, exposure)
