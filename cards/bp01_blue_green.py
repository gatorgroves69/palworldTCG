"""BP01 blue and green cards added for M2."""
from __future__ import annotations

from engine.abilities import ActAbility, CardImpl, Trigger
from engine.state import Zone

from .common import (choose_pal, consume_cost, has_resources, look_top, my_structures,
                     shuffle_deck)
from .registry import REGISTRY

reg = REGISTRY.register


# BP01-034 Teafant – Fountain of Cheer
# AUTO Serious 400 (OnAssign Choose 1 Pal, and it gets Power +400 until end of turn)
@reg
class Teafant(CardImpl):
    code = "BP01-034"
    text = "AUTO Serious 400 (OnAssign Choose 1 Pal, and it gets Power +400 until end of turn)"
    keywords = {"serious": 400}


# BP01-045 Grappling Gun (Gear)
# ACT [Rest this card] Choose 1 Pal, and it gets Power +200 and the skill in 〈〉 until end of
# turn. 〈AUTO Vigilance (At the end of your turn, stand this card)〉.
def _grapple(game, card, ctx):
    t = choose_pal(game, card.owner, "Grappling Gun: choose 1 Pal", up_to=False, intent="help",
                   amount=200)
    if t:
        game.add_mod(t, "power", 200, "turn", card.name)
        game.grant_keyword(t, "vigilance", "turn")


@reg
class GrapplingGun(CardImpl):
    code = "BP01-045"
    text = ("ACT [Rest this card] Choose 1 Pal, and it gets Power +200 and the skill in 〈〉 until "
            "end of turn. 〈AUTO Vigilance (At the end of your turn, stand this card)〉.")
    acts = [ActAbility("+200 and Vigilance", _grapple, rest_self=True)]


# BP01-046 Victor's Strategy (Event)
# Choose 1 of the following:
# ・Look at the top 5 cards of your deck, choose 1 card from among them and add it to hand, and
#   shuffle the rest of the cards with the deck.
# ・Choose 1 Pal, and return it to hand.
# ・Draw X cards. X is equal to the number of your structures.
@reg
class VictorsStrategy(CardImpl):
    code = "BP01-046"
    text = ("Choose 1 of the following:\n・Look at the top 5 cards of your deck, choose 1 card from "
            "among them and add it to hand, and shuffle the rest of the cards with the deck.\n"
            "・Choose 1 Pal, and return it to hand.\n・Draw X cards. X is equal to the number of "
            "your structures.")

    def modes(self, game, card):
        return ["take 1 of the top 5", "return 1 Pal to hand", "draw X (X = your structures)"]

    def resolve_event(self, game, card, mode):
        p = card.owner
        if mode == 0:
            top = look_top(game, p, 5)
            for c in game.choose_cards(p, "Victor: add 1 card to hand", top, 1,
                                       intent="recover"):
                game.move(c, Zone.HAND)
                game.stats[p].drawn.append(c.code)
                game.log(f"  {game.pname(p)} adds {c.name} to hand")
            shuffle_deck(game, p)
        elif mode == 1:
            t = choose_pal(game, p, "Victor: return 1 Pal to hand", up_to=False, intent="harm")
            if t:
                game.return_to_hand(t)
        elif mode == 2:
            game.draw(p, len(my_structures(game, p)))


# BP01-049 Lyleen – Blessing of the Goddess
# AUTO OnDeploy Get 3 Ingredient.
# ACT 1/Turn [Consume 3 Ingredient] Look at the top 5 cards of your deck, choose up to 1 ◇6 or
# less Pal from among them and deploy it, and shuffle the rest of the cards with the deck.
def _lyleen_dig(game, card, ctx):
    p = card.owner
    top = look_top(game, p, 5)
    pals = [c for c in top if c.is_pal and c.defn.cost <= 6]
    for c in game.choose_cards(p, "Lyleen: deploy up to 1 ◇6- Pal", pals, 1, up_to=True,
                               intent="recover"):
        game.log(f"  {game.pname(p)} deploys {c.name} with Lyleen")
        game.deploy(c)
    shuffle_deck(game, p)


@reg
class Lyleen(CardImpl):
    code = "BP01-049"
    text = ("AUTO OnDeploy Get 3 Ingredient.\nACT 1/Turn [Consume 3 Ingredient] Look at the top "
            "5 cards of your deck, choose up to 1 ◇6 or less Pal from among them and deploy it, "
            "and shuffle the rest of the cards with the deck.")
    acts = [ActAbility("dig for a Pal", _lyleen_dig, once_per_turn=True,
                       can_pay_extra=has_resources("ingredient", 3),
                       pay_extra=consume_cost("ingredient", 3))]

    def on_deploy(self, game, card):
        game.gain_resource(card.owner, "ingredient", 3)


# BP01-052 Rushoar – Reckless Destruction
# AUTO When this card attacks a structure, this card gets Power +800 until end of turn.
@reg
class Rushoar(CardImpl):
    code = "BP01-052"
    text = ("AUTO When this card attacks a structure, this card gets Power +800 until end of "
            "turn.")

    def triggers(self, game, card, event):
        t = event.data.get("target")
        if (event.kind == "attack" and event.card_uid == card.uid and t is not None
                and game.card(t).is_structure):
            return [Trigger(card.owner, f"{card.name}: +800 vs a structure",
                            lambda g, u=card.uid: g.add_mod(g.card(u), "power", 800, "turn",
                                                            "Rushoar"), card.uid)]
        return []


# BP01-070 Lily's Strategy (Event)
# Choose 1 of the following:
# ・Choose all of your Pals, and they get Power +1000 until end of turn.
# ・Choose 1 structure or gear, and put it into the graveyard.
# ・Increase your soul by 1 card in the rest state.
@reg
class LilysStrategy(CardImpl):
    code = "BP01-070"
    text = ("Choose 1 of the following:\n・Choose all of your Pals, and they get Power +1000 until "
            "end of turn.\n・Choose 1 structure or gear, and put it into the graveyard.\n・Increase "
            "your soul by 1 card in the rest state.")

    def modes(self, game, card):
        return ["all your Pals +1000", "destroy 1 structure or gear", "+1 soul (rested)"]

    def resolve_event(self, game, card, mode):
        p = card.owner
        if mode == 0:
            for c in game.players[p].pals:
                game.add_mod(c, "power", 1000, "turn", "Lily's Strategy")
        elif mode == 1:
            things = [c for ps in game.players for c in ps.base if not c.is_pal]
            for c in game.choose_cards(p, "Lily: destroy 1 structure or gear", things, 1,
                                       intent="harm"):
                game.send_to_graveyard(c, "Lily's Strategy")
        elif mode == 2:
            game.add_soul_rested(p)


# BP01-071 Found an Egg! (Event)
# Look at the top 5 cards of your deck, choose up to 1 Pal from among them and add it to hand,
# and shuffle the rest of the cards with the deck. If you choose 0 cards, get 3 Ingredient.
@reg
class FoundAnEgg(CardImpl):
    code = "BP01-071"
    text = ("Look at the top 5 cards of your deck, choose up to 1 Pal from among them and add it "
            "to hand, and shuffle the rest of the cards with the deck. If you choose 0 cards, get "
            "3 Ingredient.")

    def resolve_event(self, game, card, mode):
        p = card.owner
        top = look_top(game, p, 5)
        picked = game.choose_cards(p, "Found an Egg!: add up to 1 Pal to hand",
                                   [c for c in top if c.is_pal], 1, up_to=True, intent="recover")
        for c in picked:
            game.move(c, Zone.HAND)
            game.stats[p].drawn.append(c.code)
            game.log(f"  {game.pname(p)} adds {c.name} to hand")
        shuffle_deck(game, p)
        if not picked:
            game.gain_resource(p, "ingredient", 3)


# BP01-051 Petallia – Sweet Blessings
# AUTO OnDeploy Gain 1 life, choose 2 souls, and stand them.
@reg
class Petallia(CardImpl):
    code = "BP01-051"
    text = "AUTO OnDeploy Gain 1 life, choose 2 souls, and stand them."

    def on_deploy(self, game, card):
        ps = game.players[card.owner]
        game.gain_life(card.owner, 1)
        n = min(2, ps.souls_rested)  # standing an already-standing soul does nothing
        ps.souls_rested -= n
        game.log(f"  {game.pname(card.owner)} stands {n} soul(s) ({ps.souls_standing} standing)")
