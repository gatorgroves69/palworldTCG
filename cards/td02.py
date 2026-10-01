"""TD02 trial deck (Green・Purple) cards used by the M1 decks."""
from __future__ import annotations

from engine.abilities import CardImpl, Trigger
from engine.state import Zone

from .common import all_pals, choose_pal
from .registry import REGISTRY
from .td01 import INTERRUPT_TEXT

reg = REGISTRY.register


# TD02-012 Astegon – Aegis Wyvern of Death
# AUTO OnDeploy Choose up to 1 Pal, and it gets Power -1000 until end of turn (It is not put into
# the graveyard even if Power becomes 0 or less).
# AUTO OnAttack Choose all Pals with Power 300 or less, and put them into the graveyard (Choose
# your Pals too).
@reg
class Astegon(CardImpl):
    code = "TD02-012"
    text = ("AUTO OnDeploy Choose up to 1 Pal, and it gets Power -1000 until end of turn (It is "
            "not put into the graveyard even if Power becomes 0 or less).\nAUTO OnAttack Choose "
            "all Pals with Power 300 or less, and put them into the graveyard (Choose your Pals "
            "too).")

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Astegon: -1000 power to up to 1 Pal", intent="harm",
                       amount=-1000)
        if t:
            game.add_mod(t, "power", -1000, "turn", "Astegon")

    def on_attack(self, game, card):
        doomed = [c for c in all_pals(game) if game.power(c) <= 300]
        for c in doomed:
            game.send_to_graveyard(c, "Astegon")


# TD02-017 Blazehowl Noct – Darkflame Defender
# ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other card from
# hand] Nullify the opponent's attack. Battle damage does not occur)
@reg
class BlazehowlNoct(CardImpl):
    code = "TD02-017"
    text = INTERRUPT_TEXT
    keywords = {"interrupt": True}


# TD02-021 Strike from the Darkness (Event)
# Choose 1 Pal, and put it into the graveyard.
@reg
class StrikeFromTheDarkness(CardImpl):
    code = "TD02-021"
    text = "Choose 1 Pal, and put it into the graveyard."

    def resolve_event(self, game, card, mode):
        t = choose_pal(game, card.owner, "Strike from the Darkness: destroy 1 Pal", up_to=False,
                       intent="harm")
        if t:
            game.send_to_graveyard(t, "Strike from the Darkness")


# TD02-023 Cattiva – My First Pal
# CONT This card cannot be attacked by ◇3 or less Pals.
@reg
class Cattiva(CardImpl):
    code = "TD02-023"
    text = "CONT This card cannot be attacked by ◇3 or less Pals."

    def can_be_attacked_by(self, game, card, attacker):
        return attacker.defn.cost > 3


# TD02-004 Dinossom – Radiant Fragrance
# ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other card from
# hand] Nullify the opponent's attack. Battle damage does not occur)
@reg
class Dinossom(CardImpl):
    code = "TD02-004"
    text = INTERRUPT_TEXT
    keywords = {"interrupt": True}


# TD02-014 Leezpunk – Treasure Bandit
# AUTO When this card is put into the graveyard, your opponent chooses 1 card from their hand,
# and discards it.
@reg
class Leezpunk(CardImpl):
    code = "TD02-014"
    text = ("AUTO When this card is put into the graveyard, your opponent chooses 1 card from "
            "their hand, and discards it.")

    def triggers(self, game, card, event):
        if (event.kind == "left_base" and event.card_uid == card.uid
                and event.data["to"] is Zone.GRAVEYARD):
            def fire(g, opp=game.opponent(card.owner)):
                for c in g.choose_cards(opp, "Leezpunk: choose 1 card from your hand to discard",
                                        list(g.players[opp].hand), 1, intent="discard"):
                    g.log(f"  {g.pname(opp)} discards {c.name}")
                    g.discard(c)
            return [Trigger(card.owner, f"{card.name}: opponent discards", fire, card.uid)]
        return []


# TD02-024 Chikipi – My First Pal
# AUTO When this card is put into the graveyard, get 1 Ingredient.
@reg
class Chikipi(CardImpl):
    code = "TD02-024"
    text = "AUTO When this card is put into the graveyard, get 1 Ingredient."

    def triggers(self, game, card, event):
        if (event.kind == "left_base" and event.card_uid == card.uid
                and event.data["to"] is Zone.GRAVEYARD):
            return [Trigger(card.owner, f"{card.name}: get 1 Ingredient",
                            lambda g, p=card.owner: g.gain_resource(p, "ingredient", 1),
                            card.uid)]
        return []
