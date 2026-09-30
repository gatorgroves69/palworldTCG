"""PlanBot: picks how to play each turn by simulating the opponent's reply.

At the first main-phase decision of each turn it considers a few versions of
HeuristicBot that differ only in how cautious they are about leaving attackers
rested (`STYLES`). For each style it plays the rest of the turn on `samples`
determinized copies, the same seeds for every style, then plays the
opponent's whole reply turn with a standard HeuristicBot, and scores the
position at the start of our next turn. The best style plays the real turn.

One-action lookahead can't see the opponent's reply, so it either overextends
or stalls. Choosing the turn's style from rollouts that include the reply
fixes that at about 10x the cost of HeuristicBot.
"""
from __future__ import annotations

import random

from engine.actions import Pass
from engine.game import GameOver

from .evaluate import EXPOSURE, evaluate
from .heuristic import HeuristicBot, determinize

STYLES = {
    "cautious": (0.5, 0.8),
    "standard": EXPOSURE,
    "aggressive": (0.95, 1.0),
}


class PlanBot(HeuristicBot):
    name = "plan"

    def __init__(self, seed: int = 0, samples: int = 4, styles: dict | None = None) -> None:
        super().__init__(seed)
        self.plan_samples = samples
        self.styles = styles or STYLES
        self._planned_turn = -1
        self.style = "standard"

    def choose_action(self, game, player, actions):
        if any(isinstance(a, Pass) for a in actions):
            return self.quick_step(game, player, actions)
        if game.turn != self._planned_turn:
            self._planned_turn = game.turn
            self.style = self.pick_style(game, player)
            self.exposure = self.styles[self.style]
        return super().choose_action(game, player, actions)

    def pick_style(self, game, me) -> str:
        seeds = [self.rng.random() for _ in range(self.plan_samples)]
        best, best_v = None, None
        for name, exp in self.styles.items():
            v = sum(self.rollout(game, me, exp, s) for s in seeds) / len(seeds)
            if best_v is None or v > best_v + 1e-9:
                best, best_v = name, v
        return best

    def rollout(self, game, me, exposure, seed) -> float:
        rng = random.Random(seed)
        mine = HeuristicBot(rng.randrange(1 << 30), samples=1, exposure=exposure,
                            hidden_info=False)
        theirs = HeuristicBot(rng.randrange(1 << 30), samples=1, hidden_info=False)
        agents = [None, None]
        agents[me], agents[1 - me] = mine, theirs
        g = game.clone(agents, rng=rng)
        determinize(g, me, rng)
        try:
            g.main_phase()
            g.end_phase()
            g.take_turn()  # the opponent's reply
        except GameOver:
            pass
        return evaluate(g, me, leaf=True)
