"""TD01 trial deck (Red・Blue) cards used by the M1 decks."""
from __future__ import annotations

from engine.abilities import CardImpl

from .common import choose_pal, put_on_top, rest_card
from .registry import REGISTRY

reg = REGISTRY.register

INTERRUPT_TEXT = ("ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 "
                  "other card from hand] Nullify the opponent's attack. Battle damage does not "
                  "occur)")


# TD01-004 Foxparks – A Toasty Hug
# ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other card from
# hand] Nullify the opponent's attack. Battle damage does not occur)
@reg
class Foxparks(CardImpl):
    code = "TD01-004"
    text = INTERRUPT_TEXT
    keywords = {"interrupt": True}


# TD01-012 Elphidran Aqua – Gentle Ripples
# AUTO OnDeploy Draw 2 cards, choose 1 card from your hand, and put it on the top of the deck.
@reg
class ElphidranAqua(CardImpl):
    code = "TD01-012"
    text = ("AUTO OnDeploy Draw 2 cards, choose 1 card from your hand, and put it on the top of "
            "the deck.")

    def on_deploy(self, game, card):
        p = card.owner
        game.draw(p, 2)
        for c in game.choose_cards(p, "Elphidran Aqua: put 1 card from hand on top of the deck",
                                   list(game.players[p].hand), 1):
            put_on_top(game, c)


# TD01-015 Hangyu Cryst – Frigid Wanderer
# AUTO OnDeploy Choose up to 1 ◇3 or less Pal, and rest it.
@reg
class HangyuCryst(CardImpl):
    code = "TD01-015"
    text = "AUTO OnDeploy Choose up to 1 ◇3 or less Pal, and rest it."

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Hangyu Cryst: rest up to 1 ◇3- Pal",
                       lambda c: c.defn.cost <= 3)
        if t:
            rest_card(game, t)


# TD01-016 Reindrix – Icy Gaze
# ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other card from
# hand] Nullify the opponent's attack. Battle damage does not occur)
@reg
class Reindrix(CardImpl):
    code = "TD01-016"
    text = INTERRUPT_TEXT
    keywords = {"interrupt": True}


# TD01-023 Lamball – My First Pal
# CONT This card cannot be attacked by ◇4 or greater Pals.
@reg
class Lamball(CardImpl):
    code = "TD01-023"
    text = "CONT This card cannot be attacked by ◇4 or greater Pals."

    def can_be_attacked_by(self, game, card, attacker):
        return attacker.defn.cost < 4
