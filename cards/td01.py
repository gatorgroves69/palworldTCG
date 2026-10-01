"""TD01 trial deck (Red・Blue) cards used by the M1 decks."""
from __future__ import annotations

from engine.abilities import ActAbility, CardImpl, Trigger

from .common import (choose_pal, consume_cost, has_resources, plus_power, put_on_top,
                     rest_card)
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
                                   list(game.players[p].hand), 1, intent="top"):
            put_on_top(game, c)


# TD01-015 Hangyu Cryst – Frigid Wanderer
# AUTO OnDeploy Choose up to 1 ◇3 or less Pal, and rest it.
@reg
class HangyuCryst(CardImpl):
    code = "TD01-015"
    text = "AUTO OnDeploy Choose up to 1 ◇3 or less Pal, and rest it."

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Hangyu Cryst: rest up to 1 ◇3- Pal",
                       lambda c: c.defn.cost <= 3, intent="harm")
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


# TD01-008 Stone Pit (Structure)
# ACT 1/Turn [Assign 1 Pal] Get 3 Material, and draw 1 card. (You can rest your standing Pal to
# assign it)
def _material_and_draw(game, card, ctx):
    game.gain_resource(card.owner, "material", 3)
    game.draw(card.owner)


@reg
class StonePit(CardImpl):
    code = "TD01-008"
    text = ("ACT 1/Turn [Assign 1 Pal] Get 3 Material, and draw 1 card. (You can rest your "
            "standing Pal to assign it)")
    acts = [ActAbility("get 3 Material and draw", _material_and_draw, assign=True,
                       once_per_turn=True)]


# TD01-010 Single-Shot Rifle (Gear)
# AUTO OnDeploy Choose up to 1 Pal, and deal 1500 Damage.
# ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn.
@reg
class SingleShotRifle(CardImpl):
    code = "TD01-010"
    text = ("AUTO OnDeploy Choose up to 1 Pal, and deal 1500 Damage.\nACT [Rest this card] "
            "Choose 1 Pal, and it gets Power +200 until end of turn.")
    acts = [ActAbility("+200 power", plus_power(200), rest_self=True)]

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Single-Shot Rifle: deal 1500 to up to 1 Pal",
                       intent="harm", amount=1500)
        if t:
            game.deal_card_damage(t, 1500, card)


for _code in ("TD01-002", "TD01-003", "TD01-013", "TD01-014"):
    # Jolthog, Kelpsea Ignis, Jolthog Cryst, Pengullet – Frequent Flyer: no abilities
    REGISTRY.vanilla(_code)


# PR-001 Lamball – My First Pal (promo printing; same text as TD01-023)
@reg
class LamballPromo(Lamball):
    code = "PR-001"


# TD01-001 Grizzbolt – Rumbling Tank
# CONT Assault (This card can attack Pals in the stand state)
@reg
class GrizzboltRumblingTank(CardImpl):
    code = "TD01-001"
    text = "CONT Assault (This card can attack Pals in the stand state)"
    keywords = {"assault": True}


# TD01-005 Arsox – Burning Spoils
# AUTO OnDeploy Get 2 Material.
@reg
class Arsox(CardImpl):
    code = "TD01-005"
    text = "AUTO OnDeploy Get 2 Material."

    def on_deploy(self, game, card):
        game.gain_resource(card.owner, "material", 2)


# TD01-006 Mossanda Lux – Vanguard Captain
# ACT [Consume 2 Material] This card gets Power +500 until end of turn.
@reg
class MossandaLux(CardImpl):
    code = "TD01-006"
    text = "ACT [Consume 2 Material] This card gets Power +500 until end of turn."
    acts = [ActAbility("+500 power", lambda g, c, ctx: g.add_mod(c, "power", 500, "turn",
                                                                 c.name),
                       can_pay_extra=has_resources("material", 2),
                       pay_extra=consume_cost("material", 2))]


# TD01-007 Blazamut – Molten Sovereign
# AUTO OnDeploy Choose up to 1 Pal, and deal 1000 Damage.
@reg
class Blazamut(CardImpl):
    code = "TD01-007"
    text = "AUTO OnDeploy Choose up to 1 Pal, and deal 1000 Damage."

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Blazamut: deal 1000 to up to 1 Pal", intent="harm",
                       amount=1000)
        if t:
            game.deal_card_damage(t, 1000, card)


# TD01-009 Weapon Workbench (Structure)
# ACT 1/Turn [Consume 1 Material, assign 1 Pal] Choose up to 1 Pal, and deal 800 Damage. Choose
# all of your Pals, and they get Strike +1 until end of turn. (You can rest your standing Pal to
# assign it)
def _weapon_bench(game, card, ctx):
    t = choose_pal(game, card.owner, "Weapon Workbench: deal 800 to up to 1 Pal", intent="harm",
                   amount=800)
    if t:
        game.deal_card_damage(t, 800, card)
    for c in game.players[card.owner].pals:
        game.add_mod(c, "strike", 1, "turn", card.name)


@reg
class WeaponWorkbench(CardImpl):
    code = "TD01-009"
    text = ("ACT 1/Turn [Consume 1 Material, assign 1 Pal] Choose up to 1 Pal, and deal 800 "
            "Damage. Choose all of your Pals, and they get Strike +1 until end of turn. (You can "
            "rest your standing Pal to assign it)")
    acts = [ActAbility("800 damage, Strike +1 to all", _weapon_bench, assign=True,
                       once_per_turn=True, can_pay_extra=has_resources("material", 1),
                       pay_extra=consume_cost("material", 1))]


# TD01-011 Ignis Breath (Event)
# Quick Choose 1 Pal, and deal 500 Damage.
@reg
class IgnisBreath(CardImpl):
    code = "TD01-011"
    text = "Quick Choose 1 Pal, and deal 500 Damage."

    @property
    def quick(self):
        return True

    def resolve_event(self, game, card, mode):
        t = choose_pal(game, card.owner, "Ignis Breath: deal 500 to 1 Pal", up_to=False,
                       intent="harm", amount=500)
        if t:
            game.deal_card_damage(t, 500, card)


# TD01-017 Suzaku Aqua – Way of the Current
# AUTO Vigilance (At the end of your turn, stand this card)
@reg
class SuzakuAqua(CardImpl):
    code = "TD01-017"
    text = "AUTO Vigilance (At the end of your turn, stand this card)"
    keywords = {"vigilance": True}


# TD01-018 Mammorest Cryst – Roar of the Tundra
# CONT This card gets Power +200 for each of your structures.
# ACT [Discard 1 structure from hand] This card gets Strike +1 until end of turn.
def _has_structure_in_hand(game, card):
    return any(c.is_structure for c in game.players[card.owner].hand)


def _discard_structure(game, card, ctx):
    hand = [c for c in game.players[card.owner].hand if c.is_structure]
    for c in game.choose_cards(card.owner, "Mammorest Cryst: discard 1 structure", hand, 1,
                               intent="discard"):
        game.discard(c)


@reg
class MammorestCryst(CardImpl):
    code = "TD01-018"
    text = ("CONT This card gets Power +200 for each of your structures.\nACT [Discard 1 structure "
            "from hand] This card gets Strike +1 until end of turn.")
    acts = [ActAbility("Strike +1", lambda g, c, ctx: g.add_mod(c, "strike", 1, "turn", c.name),
                       can_pay_extra=_has_structure_in_hand, pay_extra=_discard_structure)]

    def power_mod(self, game, card):
        return 200 * len(game.players[card.owner].structures) if card.zone.value == "base" else 0


# TD01-019 Antique Wooden Chair (Structure)
# AUTO OnDeploy Choose up to 1 Pal, and it gets Power +1000 until end of turn.
@reg
class AntiqueWoodenChair(CardImpl):
    code = "TD01-019"
    text = "AUTO OnDeploy Choose up to 1 Pal, and it gets Power +1000 until end of turn."

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Antique Wooden Chair: +1000 to up to 1 Pal",
                       intent="help", amount=1000)
        if t:
            game.add_mod(t, "power", 1000, "turn", card.name)


# TD01-020 Primitive Workbench (Structure)
# ACT 1/Turn [Assign 1 Pal] Reveal the top card of your deck, if it is a ◇6 or less structure or
# gear, you may deploy it. If you did not deploy it, add it to hand. (You can rest your standing
# Pal to assign it)
def _primitive_bench(game, card, ctx):
    from engine.model import CardType
    from engine.state import Zone
    p = card.owner
    top = game.reveal_top(p)
    if top is None:
        return
    game.stats[p].drawn.append(top.code)
    if (top.type in (CardType.STRUCTURE, CardType.GEAR) and top.defn.cost <= 6
            and game.may(p, f"Primitive Workbench: deploy {top.name}?", intent="deploy")):
        game.log(f"  {game.pname(p)} deploys {top.name} with Primitive Workbench")
        game.deploy(top)
    else:
        game.move(top, Zone.HAND)
        game.log(f"  {top.name} is added to {game.pname(p)}'s hand")


@reg
class PrimitiveWorkbench(CardImpl):
    code = "TD01-020"
    text = ("ACT 1/Turn [Assign 1 Pal] Reveal the top card of your deck, if it is a ◇6 or less "
            "structure or gear, you may deploy it. If you did not deploy it, add it to hand. (You "
            "can rest your standing Pal to assign it)")
    acts = [ActAbility("reveal and deploy", _primitive_bench, assign=True, once_per_turn=True)]


# TD01-021 Single-Shot Sphere Launcher (Gear)
# AUTO OnDeploy Draw 1 card.
# ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn.
@reg
class SingleShotSphereLauncher(CardImpl):
    code = "TD01-021"
    text = ("AUTO OnDeploy Draw 1 card.\nACT [Rest this card] Choose 1 Pal, and it gets Power +200 "
            "until end of turn.")
    acts = [ActAbility("+200 power", plus_power(200), rest_self=True)]

    def on_deploy(self, game, card):
        game.draw(card.owner)


# TD01-022 Crystal Breath (Event)
# Quick Choose 1 Pal, and it gets Strike -3 until end of turn. That card does not stand during
# your opponent's next stand phase.
@reg
class CrystalBreath(CardImpl):
    code = "TD01-022"
    text = ("Quick Choose 1 Pal, and it gets Strike -3 until end of turn. That card does not "
            "stand during your opponent's next stand phase.")

    @property
    def quick(self):
        return True

    def resolve_event(self, game, card, mode):
        t = choose_pal(game, card.owner, "Crystal Breath: Strike -3 and lock 1 Pal", up_to=False,
                       intent="lock")
        if t:
            game.add_mod(t, "strike", -3, "turn", card.name)
            game.skip_next_stand(t, game.opponent(card.owner))


# TD01-024 Ribbuny – Little Princess
# AUTO When this card is put into the graveyard, get 1 Material.
@reg
class Ribbuny(CardImpl):
    code = "TD01-024"
    text = "AUTO When this card is put into the graveyard, get 1 Material."

    def triggers(self, game, card, event):
        if (event.kind == "left_base" and event.card_uid == card.uid
                and event.data["to"].value == "graveyard"):
            return [Trigger(card.owner, f"{card.name}: get 1 Material",
                            lambda g, p=card.owner: g.gain_resource(p, "material", 1), card.uid)]
        return []
