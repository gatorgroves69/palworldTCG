"""BP01 blue and green cards added for M2."""
from __future__ import annotations

from engine.abilities import ActAbility, CardImpl, Trigger
from engine.state import Zone

from .common import (choose_pal, consume_cost, discard_cost, has_resources, look_top,
                     my_structures, opp_pals, rest_card, shuffle_deck)
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


REGISTRY.vanilla("BP01-037")  # Surfent – Swift Swimmer (no abilities)


def _draw_then_discard(game, p, draw: int, discard: int, who: str) -> None:
    game.draw(p, draw)
    for c in game.choose_cards(p, f"{who}: discard {discard}", list(game.players[p].hand),
                               discard, intent="discard"):
        game.log(f"  {game.pname(p)} discards {c.name}")
        game.discard(c)


# BP01-030 Reptyro Cryst – Glacial Devourer
# AUTO OnDeploy Draw 1 card.
# ACT 1/Turn [Discard 1 card from hand] Look at the top 5 cards of your deck, choose up to 2 ◇6
# or less structures from among them and deploy them, and shuffle the rest of the cards with the
# deck.
_DISCARD1 = discard_cost(1)


def _cryst_dig(game, card, ctx):
    p = card.owner
    top = look_top(game, p, 5)
    ok = [c for c in top if c.is_structure and c.defn.cost <= 6]
    for c in game.choose_cards(p, "Reptyro Cryst: deploy up to 2 ◇6- structures", ok, 2,
                               up_to=True, intent="recover"):
        game.log(f"  {game.pname(p)} deploys {c.name} with Reptyro Cryst")
        game.deploy(c)
    shuffle_deck(game, p)


@reg
class ReptyroCryst(CardImpl):
    code = "BP01-030"
    text = ("AUTO OnDeploy Draw 1 card.\nACT 1/Turn [Discard 1 card from hand] Look at the top 5 "
            "cards of your deck, choose up to 2 ◇6 or less structures from among them and deploy "
            "them, and shuffle the rest of the cards with the deck.")
    acts = [ActAbility("dig for structures", _cryst_dig, once_per_turn=True,
                       can_pay_extra=_DISCARD1[0], pay_extra=_DISCARD1[1])]

    def on_deploy(self, game, card):
        game.draw(card.owner)


# BP01-031 Penking – Mighty Warrior of the Deep
# CONT All of your main name 《Pengullet》 Pals get Power +700.
@reg
class Penking(CardImpl):
    code = "BP01-031"
    text = "CONT All of your main name 《Pengullet》 Pals get Power +700."

    def aura_power(self, game, card, target):
        return 700 if (target.owner == card.owner and target.is_pal
                       and "Pengullet" in game.main_names(target)) else 0


# BP01-033 Wumpo – Frostpeak Sentinel
# CONT If this card is in the rest state, all of your opponent's Pals get Strike -1.
@reg
class Wumpo(CardImpl):
    code = "BP01-033"
    text = "CONT If this card is in the rest state, all of your opponent's Pals get Strike -1."

    def aura_strike(self, game, card, target):
        return -1 if card.rested and target.is_pal and target.owner != card.owner else 0


# BP01-035 Mau Cryst – Harbinger of Riches
# AUTO When this card is assigned to a 「Farming」 structure, draw 1 card.
@reg
class MauCryst(CardImpl):
    code = "BP01-035"
    text = "AUTO When this card is assigned to a 「Farming」 structure, draw 1 card."

    def triggers(self, game, card, event):
        if event.kind == "assigned" and event.card_uid == card.uid:
            s = game.card(event.data["structure"])
            if "farming" in s.defn.work:  # work suitability from cards.json (C26)
                return [Trigger(card.owner, f"{card.name}: draw 1",
                                lambda g, p=card.owner: g.draw(p), card.uid)]
        return []


# BP01-036 Celaray – Loop De Loop
# AUTO OnAttack Draw 1 card, choose 1 card from your hand, and discard it.
@reg
class Celaray(CardImpl):
    code = "BP01-036"
    text = "AUTO OnAttack Draw 1 card, choose 1 card from your hand, and discard it."

    def on_attack(self, game, card):
        _draw_then_discard(game, card.owner, 1, 1, "Celaray")


def _antique_names(game, p) -> set[str]:
    return {n for s in game.players[p].structures for n in game.names(s) if "Antique" in n}


# BP01-039 Antique Curtain (Structure)
# AUTO OnDeploy Choose up to X of your opponent's Pals, and return them to hand. X is equal to
# the number of different card names among your structures with 《Antique》 in their card names
# (For example, if the current state has 4 《Antique Mirror》, and 《Antique Curtain》 is deployed,
# return up to 2 cards).
@reg
class AntiqueCurtain(CardImpl):
    code = "BP01-039"
    text = ("AUTO OnDeploy Choose up to X of your opponent's Pals, and return them to hand. X is "
            "equal to the number of different card names among your structures with 《Antique》 in "
            "their card names (For example, if the current state has 4 《Antique Mirror》, and "
            "《Antique Curtain》 is deployed, return up to 2 cards).")

    def on_deploy(self, game, card):
        x = len(_antique_names(game, card.owner))
        for c in game.choose_cards(card.owner, f"Antique Curtain: return up to {x} Pals",
                                   opp_pals(game, card.owner), x, up_to=True, intent="harm"):
            game.return_to_hand(c)


# BP01-040 Antique Dresser (Structure)
# ACT 1/Turn [Discard 1 card from hand] Declare 1 card name. Choose all of your cards, and they
# get that declared card name in addition until end of turn.
# ACT 1/Turn [Discard X cards from hand] Choose X of your Pals, and they get Power +1000/Strike
# +1 until end of turn.
def _declare(game, card, ctx):
    from engine.actions import Decision
    p = card.owner
    options = sorted({c.defn.name for c in game.cards.values()})  # names that exist in the game
    name = game.ask(Decision("declare", p, "Antique Dresser: declare a card name", options,
                             context={"intent": "declare"}))[0]
    game.log(f"  {game.pname(p)} declares {name}")
    for c in game.players[p].base:  # "all of your cards" = your cards in the base (C25)
        c.added_names.append((name, "turn"))


def _dresser_x(game, card):
    n = min(len(game.players[card.owner].hand), len(game.players[card.owner].pals))
    return list(range(1, n + 1))


def _dresser_discard_x(game, card, ctx):
    hand = list(game.players[card.owner].hand)
    for c in game.choose_cards(card.owner, f"Antique Dresser: discard {ctx['x']}", hand,
                               ctx["x"], intent="discard"):
        game.discard(c)


def _dresser_pump(game, card, ctx):
    pals = list(game.players[card.owner].pals)
    for c in game.choose_cards(card.owner, f"Antique Dresser: +1000/+1 to {ctx['x']} Pals",
                               pals, ctx["x"], intent="help", amount=1000):
        game.add_mod(c, "power", 1000, "turn", "Antique Dresser")
        game.add_mod(c, "strike", 1, "turn", "Antique Dresser")


@reg
class AntiqueDresser(CardImpl):
    code = "BP01-040"
    text = ("ACT 1/Turn [Discard 1 card from hand] Declare 1 card name. Choose all of your cards, "
            "and they get that declared card name in addition until end of turn.\nACT 1/Turn "
            "[Discard X cards from hand] Choose X of your Pals, and they get Power +1000/Strike +1 "
            "until end of turn.")
    acts = [ActAbility("declare a card name", _declare, once_per_turn=True,
                       can_pay_extra=_DISCARD1[0], pay_extra=_DISCARD1[1]),
            ActAbility("+1000/+1 to X Pals", _dresser_pump, once_per_turn=True,
                       x_options=_dresser_x, pay_extra=_dresser_discard_x)]


# BP01-041 Hot Spring (Structure)
# ACT 1/Turn [Assign 1 Pal] Choose up to 2 ◇6 or less Pals, and rest them. Those cards do not
# stand during your opponent's next stand phase.
def _hot_spring(game, card, ctx):
    pals = [c for ps in game.players for c in ps.pals if c.defn.cost <= 6]
    for c in game.choose_cards(card.owner, "Hot Spring: rest and lock up to 2 ◇6- Pals", pals, 2,
                               up_to=True, intent="lock"):
        rest_card(game, c)
        game.skip_next_stand(c, game.opponent(card.owner))


@reg
class HotSpring(CardImpl):
    code = "BP01-041"
    text = ("ACT 1/Turn [Assign 1 Pal] Choose up to 2 ◇6 or less Pals, and rest them. Those cards "
            "do not stand during your opponent's next stand phase.")
    acts = [ActAbility("rest and lock 2 Pals", _hot_spring, assign=True, once_per_turn=True)]


# BP01-042 Antique Mirror (Structure)
# AUTO OnDeploy Draw 1 card.
@reg
class AntiqueMirror(CardImpl):
    code = "BP01-042"
    text = "AUTO OnDeploy Draw 1 card."

    def on_deploy(self, game, card):
        game.draw(card.owner)


# BP01-043 Sphere Workbench (Structure)
# ACT 1/Turn [Assign 1 Pal] Draw 2 cards, choose 1 card from your hand, and discard it.
@reg
class SphereWorkbench(CardImpl):
    code = "BP01-043"
    text = "ACT 1/Turn [Assign 1 Pal] Draw 2 cards, choose 1 card from your hand, and discard it."
    acts = [ActAbility("draw 2, discard 1",
                       lambda g, c, ctx: _draw_then_discard(g, c.owner, 2, 1, "Sphere Workbench"),
                       assign=True, once_per_turn=True)]
