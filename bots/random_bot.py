"""Uniformly random legal play. Used to fuzz the engine, not to measure decks."""
from __future__ import annotations

from engine.actions import EndMain, Pass

from .base import Bot


class RandomBot(Bot):
    name = "random"

    def __init__(self, seed: int = 0, end_bias: float = 0.15) -> None:
        super().__init__(seed)
        self.end_bias = end_bias  # chance of ending the main phase early

    def choose_redraw(self, game, player):
        return self.rng.random() < 0.2

    def choose_action(self, game, player, actions):
        stop = next((a for a in actions if isinstance(a, (EndMain, Pass))), None)
        if stop is not None and self.rng.random() < self.end_bias:
            return stop
        return self.rng.choice(actions)

    def choose(self, game, decision):
        k = self.rng.randint(decision.min, min(decision.max, len(decision.options)))
        return self.rng.sample(decision.options, k)
