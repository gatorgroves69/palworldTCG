"""BP01 colorless cards."""
from __future__ import annotations

from engine.abilities import CardImpl

from .registry import REGISTRY

reg = REGISTRY.register

REGISTRY.vanilla("BP01-099")  # Direhowl – Proud Fang (no abilities)


# BP01-100 The Adventure Begins (Event)
# If you have not played any other cards during this game, draw 2 cards.
# If you have 3 or more Pals with 《My First》 in their different card names, choose all of your
# Pals, and they get Power +1000/Strike +5 until end of turn.
@reg
class TheAdventureBegins(CardImpl):
    code = "BP01-100"
    text = ("If you have not played any other cards during this game, draw 2 cards.\nIf you have "
            "3 or more Pals with 《My First》 in their different card names, choose all of your "
            "Pals, and they get Power +1000/Strike +5 until end of turn.")

    def resolve_event(self, game, card, mode):
        p = card.owner
        # "Played" = played from hand (stats.played already holds this card itself) (C27).
        if len(game.stats[p].played) <= 1:
            game.draw(p, 2)
        pals = game.players[p].pals
        first = {n for c in pals for n in game.names(c) if "My First" in n}
        if len(first) >= 3:
            for c in pals:
                game.add_mod(c, "power", 1000, "turn", card.name)
                game.add_mod(c, "strike", 5, "turn", card.name)
