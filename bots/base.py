"""The interface every bot implements.

The engine calls three methods:
- `choose_redraw`: keep or redraw the opening hand (CR 6.2.1.7).
- `choose_action`: pick one of the legal actions. Used for the turn
  player's main phase and for the defender's Quick step (the options then
  include `Pass`).
- `choose`: answer a mid-resolution `Decision` (block, targets, "may", ...).

Search seam: a lookahead or MCTS bot implements the same interface. Inside
`choose_action` it calls `game.clone(rollout_agents)`, performs a candidate
action on the clone with `clone.perform(action)`, then continues the game
with `clone.take_turn()` or evaluates the position. Each bot gets its own
`random.Random`, so its randomness never disturbs the game's shuffles.

Fair play: bots are handed the full Game for cloning, but they must only
read public information and their own hand/deck order that they are allowed
to know (docs/assumptions.md S3).
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.actions import Action, Decision
    from engine.game import Game


class Bot:
    name = "bot"

    def __init__(self, seed: int = 0) -> None:
        self.rng = random.Random(seed)

    def choose_redraw(self, game: "Game", player: int) -> bool:
        raise NotImplementedError

    def choose_action(self, game: "Game", player: int, actions: list["Action"]) -> "Action":
        raise NotImplementedError

    def choose(self, game: "Game", decision: "Decision") -> list:
        raise NotImplementedError
