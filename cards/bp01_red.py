"""BP01 red cards added for M2."""
from __future__ import annotations

from engine.abilities import ActAbility, CardImpl
from engine.model import CardType

from .common import (choose_pal, consume_cost, discard_cost, has_resources, look_top,
                     my_gears, opp_pals, shuffle_deck)
from .registry import REGISTRY
from .td01 import INTERRUPT_TEXT

reg = REGISTRY.register


# BP01-001 Jormuntide Ignis – Savage Lava Dragon
# ACT 1/Turn [③] OR [Discard 2 cards from hand] Stand this card.
def _stand_self(game, card, ctx):
    game.stand(card)
    game.log(f"  {card.name} stands" if not card.rested else f"  {card.name} can't stand")


_IGNIS_DISCARD = discard_cost(2)


@reg
class JormuntideIgnis(CardImpl):
    code = "BP01-001"
    text = "ACT 1/Turn [③] OR [Discard 2 cards from hand] Stand this card."
    # Two ways to pay one ability: they share a single 1/Turn (C16). Only offered while
    # rested, since standing a standing card does nothing.
    acts = [
        ActAbility("stand this card (pay ③)", _stand_self, souls=3, once_per_turn=True,
                   limit_key="ignis", condition=lambda g, c: c.rested),
        ActAbility("stand this card (discard 2)", _stand_self, once_per_turn=True,
                   limit_key="ignis", condition=lambda g, c: c.rested,
                   can_pay_extra=_IGNIS_DISCARD[0], pay_extra=_IGNIS_DISCARD[1]),
    ]


# BP01-005 Reptyro – Ore Gorger
# AUTO OnDeploy Get 3 Material.
# ACT 1/Turn [Consume 3 Material] Look at the top 5 cards of your deck, choose up to 1 ◇8 or
# less gear from among them and deploy it, and shuffle the rest of the cards with the deck.
def _reptyro_dig(game, card, ctx):
    p = card.owner
    top = look_top(game, p, 5)
    gears = [c for c in top if c.type is CardType.GEAR and c.defn.cost <= 8]
    for c in game.choose_cards(p, "Reptyro: deploy up to 1 ◇8- gear", gears, 1, up_to=True,
                               intent="recover"):
        game.log(f"  {game.pname(p)} deploys {c.name} with Reptyro")
        game.deploy(c)
    shuffle_deck(game, p)


@reg
class Reptyro(CardImpl):
    code = "BP01-005"
    text = ("AUTO OnDeploy Get 3 Material.\nACT 1/Turn [Consume 3 Material] Look at the top 5 "
            "cards of your deck, choose up to 1 ◇8 or less gear from among them and deploy it, "
            "and shuffle the rest of the cards with the deck.")
    acts = [ActAbility("dig for a gear", _reptyro_dig, once_per_turn=True,
                       can_pay_extra=has_resources("material", 3),
                       pay_extra=consume_cost("material", 3))]

    def on_deploy(self, game, card):
        game.gain_resource(card.owner, "material", 3)


# BP01-006 Foxparks – Light of Courage
# AUTO Brave 300 (OnAttack This card gets Power +300 until end of turn)
@reg
class FoxparksLightOfCourage(CardImpl):
    code = "BP01-006"
    text = "AUTO Brave 300 (OnAttack This card gets Power +300 until end of turn)"
    keywords = {"brave": 300}


# BP01-014 Blazehowl – Hellflame Defender
# ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other card from
# hand] Nullify the opponent's attack. Battle damage does not occur)
@reg
class BlazehowlHellflame(CardImpl):
    code = "BP01-014"
    text = INTERRUPT_TEXT
    keywords = {"interrupt": True}


# BP01-015 Mounted Machine Gun (Structure)
# ACT 1/Turn [Consume X Material, assign 1 Pal] Perform 〈Choose 1 Pal, and deal 500 Damage. 〉
# X times.
MMG_MAX_X = 8  # caps branching; 8 x 500 already kills anything in BP01


def _mmg_fire(game, card, ctx):
    for _ in range(ctx["x"]):
        t = choose_pal(game, card.owner, "Mounted Machine Gun: deal 500 to 1 Pal", up_to=False,
                       intent="harm", amount=500)
        if t:
            # Lethal damage is only checked after the whole effect (CR 11.4.2), so a Pal
            # can be chosen again after it has already taken lethal damage.
            game.deal_card_damage(t, 500, card)


@reg
class MountedMachineGun(CardImpl):
    code = "BP01-015"
    text = ("ACT 1/Turn [Consume X Material, assign 1 Pal] Perform 〈Choose 1 Pal, and deal 500 "
            "Damage. 〉 X times.")
    acts = [ActAbility("fire X times", _mmg_fire, assign=True, once_per_turn=True,
                       x_options=lambda g, c: list(range(
                           1, min(g.players[c.owner].resources["material"], MMG_MAX_X) + 1)),
                       pay_extra=consume_cost("material"))]


# BP01-016 Primitive Furnace (Structure)
# ACT 1/Turn [Assign 1 Pal] Get 3 Material, and draw 1 card.
# ACT 1/Turn [Consume X Material] Reduce the cost of playing your next gear from hand by X until
# end of turn. It does not become ◇0 or less from this ability.
def _material_and_draw(game, card, ctx):
    game.gain_resource(card.owner, "material", 3)
    game.draw(card.owner)


def _furnace_x(game, card):
    # Only X values that can matter: up to (priciest gear in hand - 1), and what we own.
    gears = [c.defn.cost for c in game.players[card.owner].hand if c.type is CardType.GEAR]
    top = min(game.players[card.owner].resources["material"], max(gears, default=1) - 1)
    return list(range(1, top + 1))


def _furnace_discount(game, card, ctx):
    game.players[card.owner].gear_discount = ctx["x"]
    game.log(f"  {game.pname(card.owner)}'s next gear this turn costs {ctx['x']} less")


@reg
class PrimitiveFurnace(CardImpl):
    code = "BP01-016"
    text = ("ACT 1/Turn [Assign 1 Pal] Get 3 Material, and draw 1 card.\nACT 1/Turn [Consume X "
            "Material] Reduce the cost of playing your next gear from hand by X until end of turn. "
            "It does not become ◇0 or less from this ability.")
    acts = [ActAbility("get 3 Material and draw", _material_and_draw, assign=True,
                       once_per_turn=True),
            ActAbility("discount next gear by X", _furnace_discount, once_per_turn=True,
                       x_options=_furnace_x, pay_extra=consume_cost("material"))]


# BP01-019 Foxparks' Harness (Gear)
# ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn. If its main name
# is 《Foxparks》, it gets the skill in 〈〉 until end of turn. 〈AUTO OnAttack Choose up to 1 Pal,
# and deal 700 Damage 〉.
def _harness_on_attack(game, card):
    t = choose_pal(game, card.owner, "Harness: deal 700 to up to 1 Pal", intent="harm",
                   amount=700)
    if t:
        game.deal_card_damage(t, 700, card)  # the Foxparks (red) is the source (C22)


def _harness(game, card, ctx):
    t = choose_pal(game, card.owner, "Foxparks' Harness: choose 1 Pal", up_to=False,
                   intent="help", amount=200)
    if t is None:
        return
    game.add_mod(t, "power", 200, "turn", card.name)
    if t.defn.main_name == "Foxparks":
        game.grant_auto(t, "on_attack", "OnAttack: deal 700", _harness_on_attack, "turn")


@reg
class FoxparksHarness(CardImpl):
    code = "BP01-019"
    text = ("ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn. If its "
            "main name is 《Foxparks》, it gets the skill in 〈〉 until end of turn. 〈AUTO OnAttack "
            "Choose up to 1 Pal, and deal 700 Damage 〉.")
    acts = [ActAbility("power up a Pal", _harness, rest_self=True)]


# BP01-023 Axel's Strategy (Event)
# Choose 1 of the following:
# ・Choose 1 Pal, and deal 1500 Damage.
# ・Choose up to X Pals, and stand them. X is equal to your number of gears.
# ・Choose all of your opponent's ◇5 or greater Pals, and they cannot block until end of turn.
@reg
class AxelsStrategy(CardImpl):
    code = "BP01-023"
    text = ("Choose 1 of the following:\n・Choose 1 Pal, and deal 1500 Damage.\n・Choose up to X "
            "Pals, and stand them. X is equal to your number of gears.\n・Choose all of your "
            "opponent's ◇5 or greater Pals, and they cannot block until end of turn.")

    def modes(self, game, card):
        return ["deal 1500 to 1 Pal", "stand up to X Pals (X = your gears)",
                "opponent's ◇5+ Pals cannot block"]

    def resolve_event(self, game, card, mode):
        p = card.owner
        if mode == 0:
            t = choose_pal(game, p, "Axel: deal 1500 to 1 Pal", up_to=False, intent="harm",
                           amount=1500)
            if t:
                game.deal_card_damage(t, 1500, card)
        elif mode == 1:
            x = len(my_gears(game, p))
            rested = [c for ps in game.players for c in ps.pals if c.rested]
            for c in game.choose_cards(p, f"Axel: stand up to {x} Pals", rested, x, up_to=True,
                                       intent="stand"):
                game.stand(c)
                game.log(f"  {c.name} stands")
        elif mode == 2:
            for c in opp_pals(game, p):
                if c.defn.cost >= 5:
                    game.add_mod(c, "no_block", 1, "turn", "Axel's Strategy")



# BP01-012 Flambelle – Scorching Tears
# AUTO OnDeploy Get 2 Material.
@reg
class Flambelle(CardImpl):
    code = "BP01-012"
    text = "AUTO OnDeploy Get 2 Material."

    def on_deploy(self, game, card):
        game.gain_resource(card.owner, "material", 2)
