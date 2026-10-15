"""HeuristicBot: one-step lookahead over main-phase actions.

For each legal action it copies the game, *determinizes* the copy (reshuffles
everything this player can't see: the opponent's hand and deck, and its own
deck), performs the action with RuleBot answering every nested decision on
both sides, and scores the result with `evaluate`. Actions whose outcome
depends on the deck (damage checks, draws, reveals) are sampled a few times.
It takes the best action if it beats doing nothing, otherwise ends the turn.

This is the seam for a stronger bot: an MCTS bot would replace the one-step
scoring with rollouts over the same clone/determinize machinery.
"""
from __future__ import annotations

import random

from engine.actions import Activate, Attack, EndMain, Pass, SoulDraw
from engine.game import GameOver

from .evaluate import EXPOSURE, HAND_CARD, evaluate, pal_value
from .rules import RuleBot

MARGIN = 0.25  # an action must beat ending the turn by this much


def determinize(game, me: int, rng: random.Random) -> None:
    """Reshuffle what `me` can't know, in place, in a cloned game."""
    from engine.state import Zone
    opp = game.players[game.opponent(me)]
    hidden = opp.hand + opp.deck
    rng.shuffle(hidden)
    n = len(opp.hand)
    opp.hand, opp.deck = hidden[:n], hidden[n:]
    for c in opp.hand:  # keep each card's zone label in step with its list
        c.zone = Zone.HAND
    for c in opp.deck:
        c.zone = Zone.DECK
    for c in hidden:  # their own knowledge isn't ours
        c.known_top = False
    # Our own deck stays hidden too, except the cards we put on top ourselves
    # (Aurora Guide, Elphidran Aqua): those stay where we know they are.
    deck = game.players[me].deck
    k = 0
    while k < len(deck) and deck[k].known_top:
        k += 1
    rest = deck[k:]
    rng.shuffle(rest)
    deck[k:] = rest


# Structures whose assign ability builds an engine (cards, resources, souls, revives, damage).
ENGINE_ASSIGN = {"TD01-008", "BP01-016", "BP01-066", "TD02-008", "BP01-043", "TD01-020",
                 "BP01-090", "BP01-064", "BP01-015", "TD01-009"}


class HeuristicBot(RuleBot):
    soul_draw_eager = False  # "@human": see choose_action
    engine_first = False  # "@seq": assign engine structures before attacking (see _engine_first)
    name = "heuristic"

    depth = 1  # actions looked ahead within our own turn

    def __init__(self, seed: int = 0, samples: int = 3, exposure=None,
                 hidden_info: bool = True, evaluator=None) -> None:
        """`exposure`: how much a Pal left rested is worth (see evaluate); lower is
        more cautious about attacking. `hidden_info=False` skips determinizing,
        for use inside simulations that are already determinized."""
        super().__init__(seed)
        self.samples = samples
        self.exposure = exposure or getattr(self, "exposure_default", EXPOSURE)
        self.hidden_info = hidden_info
        self.evaluate = evaluator or evaluate
        opts = {}
        if getattr(self, "resource_scale", 1.0) != 1.0:
            opts["resource_scale"] = self.resource_scale
        if getattr(self, "open_soul_by_life", False):
            opts["open_soul_by_life"] = True
        if getattr(self, "death_value", False):
            opts["death_value"] = True
        if getattr(self, "struct_scale", 1.0) != 1.0:
            opts["struct_scale"] = self.struct_scale
        if getattr(self, "kill_scale", 1.0) != 1.0:
            opts["kill_scale"] = self.kill_scale
        if evaluator is None and opts:
            import functools
            self.evaluate = functools.partial(evaluate, **opts)

    def choose_action(self, game, player, actions):
        if any(isinstance(a, Pass) for a in actions):
            return self.quick_step(game, player, actions)
        if self.engine_first:
            actions = self._prune_activations(game, actions)
        end = next((a for a in actions if isinstance(a, EndMain)), None)
        base = self.evaluate(game, player, exposure=self.exposure)
        if end is None:  # forced to keep attacking (CR 7.5.2.1): best non-ending action
            base = float("-inf")
        # Common random numbers: every action is scored on the same determinized samples,
        # so differences between actions aren't sampling noise.
        seeds = [self.rng.random() for _ in range(self.samples)]
        best, best_val = end, base + MARGIN
        if end is None:
            best = next(a for a in actions if not isinstance(a, SoulDraw))
        for a in actions:
            if a is end or isinstance(a, SoulDraw):
                continue
            v = self.score(game, player, a, seeds)
            if v > best_val:
                best, best_val = a, v
        if self.engine_first:
            alt = self._engine_first(game, player, actions, best, seeds)
            if alt is not None:
                return alt
        # Rest 3 souls to draw only with souls nothing else wants (a 3-for-1 rate).
        if best is end and any(isinstance(a, SoulDraw) for a in actions):
            return SoulDraw()
        # "@human": real players soul-draw ~3x a game (Stone Pit pilots 2.9, the bot 0.7):
        # draw first when the best play gains less than most of a card.
        if (self.soul_draw_eager and best is not end
                and any(isinstance(a, SoulDraw) for a in actions)
                and best_val - base < 0.6 * HAND_CARD):
            return SoulDraw()
        return best

    @staticmethod
    def _prune_activations(game, actions):
        """Engine decks see one Activate per (structure, ability, X, assigned Pal): 70+
        near-duplicates and 30 s games. Keep, per ability, X in {1, max} and two assign
        choices: the least valuable standing Pal and the most expensive one (for
        cost-scaled abilities like Medicine Workbench)."""
        groups, out = {}, []
        for a in actions:
            if isinstance(a, Activate) and (a.assign_uid is not None or a.x is not None):
                groups.setdefault((a.uid, a.index), []).append(a)
            else:
                out.append(a)
        for acts in groups.values():
            xs = sorted({a.x for a in acts if a.x is not None})
            keep_x = {xs[0], xs[-1]} if xs else {None}
            acts = [a for a in acts if a.x in keep_x]
            pals = {a.assign_uid for a in acts if a.assign_uid is not None}
            if pals:
                cheap = min(pals, key=lambda u: pal_value(game, game.card(u)))
                dear = max(pals, key=lambda u: game.card(u).defn.cost)
                acts = [a for a in acts if a.assign_uid in (cheap, dear)]
            out.extend(acts)
        return out

    def _engine_first(self, game, player, actions, best, seeds):
        """Palify calibration (2026-10-13): real Stone Pit pilots activate Stone Pit ~3.7
        times a game, this bot ~0.8, because it attacks with every Pal (or ends the turn)
        before assigning one. Before an attack or the end of the main phase, run the best
        engine structure that assigns a Pal, unless the attacks this turn are lethal."""
        if not (best is None or isinstance(best, (EndMain, Attack))):
            return None
        engine = [a for a in actions if isinstance(a, Activate) and a.assign_uid is not None
                  and game.card(a.uid).code in ENGINE_ASSIGN]
        if not engine:
            return None
        if isinstance(best, Attack):
            opp = game.players[game.opponent(player)]
            ready = sum(game.strike(c) for c in game.players[player].pals
                        if game.can_attack(c))
            if ready >= opp.life:
                return None
        return max(engine, key=lambda a: self.score(game, player, a, seeds))

    def score(self, game, player, action, seeds=None) -> float:
        seeds = seeds or [self.rng.random() for _ in range(self.samples)]
        n = len(seeds) if self._random_outcome(action) else 1
        total = 0.0
        for seed in seeds[:n]:
            rng = random.Random(seed)
            g = game.clone([RuleBot(), RuleBot()], rng=rng)
            if self.hidden_info:
                determinize(g, player, rng)
            try:
                g.perform(action)
            except GameOver:
                pass
            v = self.evaluate(g, player, exposure=self.exposure)
            if self.depth >= 2 and not g.reason and not isinstance(action, EndMain):
                v = max(v, self._best_followup(g, player))
            total += v
        return total / n

    beam = 4  # follow-ups explored further when depth >= 3

    def _best_followup(self, g, player, depth_left: int | None = None) -> float:
        """Best position reachable with more actions this turn (on this sample).
        Lets setup actions (discounts, night, grants, no-block) show their payoff.
        With depth >= 3 the `beam` most promising follow-ups are searched one step
        further, so three-step plans (Furnace -> Shotgun -> attack) are visible."""
        if depth_left is None:
            depth_left = self.depth - 1
        scored = []
        for b in g.legal_actions(player):
            if isinstance(b, (EndMain, SoulDraw)):
                continue
            h = g.clone([RuleBot(), RuleBot()], rng=random.Random(0))
            try:
                h.perform(b)
            except GameOver:
                pass
            scored.append((self.evaluate(h, player, exposure=self.exposure), h))
        if not scored:
            return float("-inf")
        best = max(v for v, _ in scored)
        if depth_left >= 2:
            scored.sort(key=lambda x: -x[0])
            for v, h in scored[: self.beam]:
                if not h.reason:
                    best = max(best, self._best_followup(h, player, depth_left - 1))
        return best

    @staticmethod
    def _random_outcome(action) -> bool:
        # Attacks on the player flip cards; everything else is close enough with one sample.
        return isinstance(action, Attack) and action.target_uid is None


class LearnedHeuristicBot(HeuristicBot):
    """HeuristicBot scoring positions with the learned evaluation."""
    name = "heuristic-learned"

    weights = "eval_weights.json"

    def __init__(self, seed: int = 0, samples: int = 3) -> None:
        from .evaluate import learned_evaluator
        super().__init__(seed, samples, evaluator=learned_evaluator(self.weights))



class TwoStepHeuristicBot(HeuristicBot):
    """HeuristicBot that scores each action together with its best follow-up action."""
    name = "heuristic2"
    depth = 2


class ThreeStepHeuristicBot(TwoStepHeuristicBot):
    """TwoStepHeuristicBot with a pruned third step: three-action plans within the
    turn become visible (setup -> payoff -> attack). About 2-3x slower."""
    name = "heuristic3"
    depth = 3


class LookaheadBot(TwoStepHeuristicBot):
    """EXPERIMENTAL, weaker than TwoStepHeuristicBot (39-45% in mirrors); not used for runs.

    Two-step bot that re-ranks its top candidates by looking a full turn cycle ahead.

    For the `top_k` actions the two-step score likes best, it plays `rollouts`
    determinized simulations each: the action, the rest of our turn, the
    opponent's whole turn and our *next* whole turn (fast one-step bots), then
    scores the position. Engine pieces (Structures, Gear, Material) pay off
    on the next turn, which the two-step score can't see.
    """
    name = "lookahead"
    top_k = 3
    rollouts = 2

    def choose_action(self, game, player, actions):
        if any(isinstance(a, Pass) for a in actions):
            return self.quick_step(game, player, actions)
        seeds = [self.rng.random() for _ in range(self.samples)]
        scored = []
        for a in actions:
            if isinstance(a, SoulDraw):
                continue
            scored.append((self.score(game, player, a, seeds) if not isinstance(a, EndMain)
                           else self.evaluate(game, player, exposure=self.exposure) + MARGIN, a))
        scored.sort(key=lambda x: -x[0])
        top = [a for _, a in scored[: self.top_k]]
        if len(top) == 1:
            return top[0]
        rseeds = [self.rng.random() for _ in range(self.rollouts)]
        best, best_v = top[0], None
        for a in top:
            v = sum(self._turn_cycle(game, player, a, s) for s in rseeds) / len(rseeds)
            if best_v is None or v > best_v:
                best, best_v = a, v
        if isinstance(best, EndMain) and any(isinstance(a, SoulDraw) for a in actions):
            return SoulDraw()
        return best

    def _turn_cycle(self, game, me, action, seed) -> float:
        rng = random.Random(seed)
        bots = [HeuristicBot(rng.randrange(1 << 30), samples=1, hidden_info=False)
                for _ in range(2)]
        g = game.clone(bots, rng=rng)
        determinize(g, me, rng)
        try:
            if not isinstance(action, EndMain):
                g.perform(action)
                g.main_phase()
            g.end_phase()
            g.take_turn()                       # opponent's reply
            g.begin_turn()                      # our next turn
            g.main_phase()
        except GameOver:
            pass
        return self.evaluate(g, me, exposure=self.exposure)
