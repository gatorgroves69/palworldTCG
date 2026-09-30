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

from engine.actions import Attack, EndMain, Pass, SoulDraw
from engine.game import GameOver

from .evaluate import evaluate
from .rules import RuleBot

MARGIN = 0.25  # an action must beat ending the turn by this much


def determinize(game, me: int, rng: random.Random) -> None:
    """Reshuffle what `me` can't know, in place, in a cloned game."""
    opp = game.players[game.opponent(me)]
    hidden = opp.hand + opp.deck
    rng.shuffle(hidden)
    n = len(opp.hand)
    opp.hand, opp.deck = hidden[:n], hidden[n:]
    rng.shuffle(game.players[me].deck)


class HeuristicBot(RuleBot):
    name = "heuristic"

    def __init__(self, seed: int = 0, samples: int = 3) -> None:
        super().__init__(seed)
        self.samples = samples

    def choose_action(self, game, player, actions):
        if any(isinstance(a, Pass) for a in actions):
            return self.quick_step(game, player, actions)
        end = next(a for a in actions if isinstance(a, EndMain))
        base = evaluate(game, player)
        best, best_val = end, base + MARGIN
        for a in actions:
            if a is end or isinstance(a, SoulDraw):
                continue
            v = self.score(game, player, a)
            if v > best_val:
                best, best_val = a, v
        # Rest 3 souls to draw only with souls nothing else wants (a 3-for-1 rate).
        if best is end and any(isinstance(a, SoulDraw) for a in actions):
            return SoulDraw()
        return best

    def score(self, game, player, action) -> float:
        n = self.samples if self._random_outcome(action) else 1
        total = 0.0
        for _ in range(n):
            g = game.clone([RuleBot(), RuleBot()], rng=self.rng)
            determinize(g, player, self.rng)
            try:
                g.perform(action)
            except GameOver:
                pass
            total += evaluate(g, player)
        return total / n

    @staticmethod
    def _random_outcome(action) -> bool:
        # Attacks on the player flip cards; everything else is close enough with one sample.
        return isinstance(action, Attack) and action.target_uid is None
