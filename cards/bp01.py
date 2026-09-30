"""BP01 "Dawn of Palpagos" cards used by the M1 decks."""
from __future__ import annotations

from engine.abilities import ActAbility, CardImpl, Trigger
from engine.model import Color
from engine.state import Zone

from .common import choose_pal, is_dragon_pal, opp_pals, put_on_top, rest_card
from .registry import REGISTRY

reg = REGISTRY.register


# BP01-002 Suzaku – Hellfire Wings
# CONT When your red card would deal Damage other than battle damage to a Pal, deal +200 Damage
# instead (Strengthens this card's ability too).
# AUTO OnDeploy Choose up to 1 Pal, and deal 700 Damage.
@reg
class Suzaku(CardImpl):
    code = "BP01-002"
    text = ("CONT When your red card would deal Damage other than battle damage to a Pal, deal "
            "+200 Damage instead (Strengthens this card's ability too).\nAUTO OnDeploy Choose up "
            "to 1 Pal, and deal 700 Damage.")

    def modify_effect_damage(self, game, card, source, target, amount):
        # Each Suzaku is its own replacement effect, so two Suzakus give +400 (Q3).
        if target.is_pal and source.owner == card.owner and source.defn.color is Color.RED:
            return amount + 200
        return amount

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Suzaku: deal 700 damage to up to 1 Pal")
        if t:
            game.deal_card_damage(t, 700, card)


# BP01-007 Kitsun – Wyrmbane Fangs
# AUTO OnDeploy Choose up to 1 ◇7 or greater Pal, and deal 1200 Damage.
@reg
class Kitsun(CardImpl):
    code = "BP01-007"
    text = "AUTO OnDeploy Choose up to 1 ◇7 or greater Pal, and deal 1200 Damage."

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Kitsun: deal 1200 to up to 1 ◇7+ Pal",
                       lambda c: c.defn.cost >= 7)
        if t:
            game.deal_card_damage(t, 1200, card)


# BP01-008 Sparkit – Hazardous Contact
# AUTO OnDeploy Choose up to 1 Pal in the stand state, and deal 500 Damage.
@reg
class Sparkit(CardImpl):
    code = "BP01-008"
    text = "AUTO OnDeploy Choose up to 1 Pal in the stand state, and deal 500 Damage."

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Sparkit: deal 500 to up to 1 standing Pal",
                       lambda c: not c.rested)
        if t:
            game.deal_card_damage(t, 500, card)


def _plus200(game, card, ctx):
    t = choose_pal(game, card.owner, f"{card.name}: +200 power to 1 Pal", up_to=False)
    if t:
        game.add_mod(t, "power", 200, "turn", card.name)


# BP01-020 Pump-Action Shotgun (Gear)
# AUTO OnDeploy Choose all of your opponent's Pals, and deal 1200 Damage.
# ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn.
@reg
class PumpActionShotgun(CardImpl):
    code = "BP01-020"
    text = ("AUTO OnDeploy Choose all of your opponent's Pals, and deal 1200 Damage.\nACT [Rest "
            "this card] Choose 1 Pal, and it gets Power +200 until end of turn.")
    acts = [ActAbility("+200 power", _plus200, rest_self=True)]

    def on_deploy(self, game, card):
        for t in opp_pals(game, card.owner):
            game.deal_card_damage(t, 1200, card)


# BP01-028 Pengullet – Yearning for the Sky
# AUTO When this card is put into the graveyard, draw 1 card.
@reg
class Pengullet(CardImpl):
    code = "BP01-028"
    text = "AUTO When this card is put into the graveyard, draw 1 card."

    def triggers(self, game, card, event):
        # Active only on the base (CR 10.3.5): base -> graveyard, not discards or flips.
        if (event.kind == "left_base" and event.card_uid == card.uid
                and event.data["to"] is Zone.GRAVEYARD):
            return [Trigger(card.owner, f"{card.name}: draw 1",
                            lambda g, p=card.owner: g.draw(p), card.uid)]
        return []


# BP01-029 Azurobe – Water Dragon Waltz
# AUTO OnDeploy Draw 1 card, choose up to 1 Pal, and rest it.
@reg
class Azurobe(CardImpl):
    code = "BP01-029"
    text = "AUTO OnDeploy Draw 1 card, choose up to 1 Pal, and rest it."

    def on_deploy(self, game, card):
        game.draw(card.owner)
        t = choose_pal(game, card.owner, "Azurobe: rest up to 1 Pal")
        if t:
            rest_card(game, t)


# BP01-032 Fuack – Manic Wave Ripper
# AUTO When this card is attacked, this card gets Power +300 until end of turn.
@reg
class Fuack(CardImpl):
    code = "BP01-032"
    text = "AUTO When this card is attacked, this card gets Power +300 until end of turn."

    def triggers(self, game, card, event):
        # "Attacked" = chosen as the attack target at declaration (CR 9.3.2), not blocking (Q1).
        if event.kind == "attack" and event.data.get("target") == card.uid:
            inc = card.incarnation

            def boost(g, c=card, inc=inc):
                if g.on_base(c, inc):
                    g.add_mod(c, "power", 300, "turn", "Fuack")
            return [Trigger(card.owner, f"{card.name}: +300 when attacked", boost, card.uid)]
        return []


# BP01-038 Cryolinx – Arctic Ordeal
# ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other card from
# hand] Nullify the opponent's attack. Battle damage does not occur)
@reg
class Cryolinx(CardImpl):
    code = "BP01-038"
    text = ("ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other "
            "card from hand] Nullify the opponent's attack. Battle damage does not occur)")
    keywords = {"interrupt": True}


# BP01-044 Pengullet Rocket Launcher (Gear)
# ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn. If its main name
# is 《Pengullet》, instead it gets Power +500 and the skill in 〈〉 until end of turn. 〈ACT [Rest
# this card] Choose all of your opponent's Pals, and they get X Damage. X is equal to this card's
# Power. Put this card into the graveyard〉.
def _barrage(game, card, ctx):
    # `card` is the Pengullet that was granted this ability. X is its current power (Q7).
    x = game.power(card)
    for t in opp_pals(game, card.owner):
        game.deal_card_damage(t, x, card)
    game.send_to_graveyard(card, "Rocket Launcher barrage")


BARRAGE = ActAbility("Rocket barrage (X = power to all opposing Pals)", _barrage, rest_self=True)


def _launcher(game, card, ctx):
    t = choose_pal(game, card.owner, "Rocket Launcher: choose 1 Pal", up_to=False)
    if t is None:
        return
    if t.defn.main_name == "Pengullet":
        game.add_mod(t, "power", 500, "turn", card.name)
        game.grant_act(t, BARRAGE, "turn")
    else:
        game.add_mod(t, "power", 200, "turn", card.name)


@reg
class PengulletRocketLauncher(CardImpl):
    code = "BP01-044"
    text = ("ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn. If its "
            "main name is 《Pengullet》, instead it gets Power +500 and the skill in 〈〉 until end "
            "of turn. 〈ACT [Rest this card] Choose all of your opponent's Pals, and they get X "
            "Damage. X is equal to this card's Power. Put this card into the graveyard〉.")
    acts = [ActAbility("power up a Pal", _launcher, rest_self=True)]


# BP01-047 Pal Sphere (Event)
# Draw 3 cards.
@reg
class PalSphere(CardImpl):
    code = "BP01-047"
    text = "Draw 3 cards."

    def resolve_event(self, game, card, mode):
        game.draw(card.owner, 3)


# BP01-048 Aurora Guide (Event)
# Quick Draw 1 card, choose up to 1 card from your hand, and put it on the top of the deck.
@reg
class AuroraGuide(CardImpl):
    code = "BP01-048"
    text = "Quick Draw 1 card, choose up to 1 card from your hand, and put it on the top of the deck."

    @property
    def quick(self):
        return True

    def resolve_event(self, game, card, mode):
        p = card.owner
        game.draw(p)
        for c in game.choose_cards(p, "Aurora Guide: put up to 1 card from hand on top of deck",
                                   list(game.players[p].hand), n=1, up_to=True):
            put_on_top(game, c)


# BP01-077 Pyrin Noct – Steed of Azure Flames
# CONT Nocturnal (If it is night, this card gets Power +300)
# ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other card from
# hand] Nullify the opponent's attack. Battle damage does not occur)
@reg
class PyrinNoct(CardImpl):
    code = "BP01-077"
    text = ("CONT Nocturnal (If it is night, this card gets Power +300)\nACT Interrupt (Hand Quick "
            "[①, discard this card] OR [Discard this card and 1 other card from hand] Nullify the "
            "opponent's attack. Battle damage does not occur)")
    keywords = {"nocturnal": True, "interrupt": True}


# BP01-095 Zoe's Strategy (Event)
# Choose 1 of the following:
# ・Choose up to 5 of your opponent's Material and/or Ingredient in total, and your opponent loses
#   them.
# ・Choose up to 1 Pal from your graveyard, and return it to hand. Your opponent chooses 1 card
#   from their hand, and discards it.
# ・Choose 1 of your Pals, and butcher it. If you butchered 1 or more cards this way, choose 1 of
#   your opponent's Pals, and put it into the graveyard.
@reg
class ZoesStrategy(CardImpl):
    code = "BP01-095"
    text = ("Choose 1 of the following:\n・Choose up to 5 of your opponent's Material and/or "
            "Ingredient in total, and your opponent loses them.\n・Choose up to 1 Pal from your "
            "graveyard, and return it to hand. Your opponent chooses 1 card from their hand, and "
            "discards it.\n・Choose 1 of your Pals, and butcher it. If you butchered 1 or more "
            "cards this way, choose 1 of your opponent's Pals, and put it into the graveyard.")

    def modes(self, game, card):
        return ["opponent loses up to 5 resources",
                "return a Pal from graveyard, opponent discards 1",
                "butcher your Pal, destroy an opposing Pal"]

    def resolve_event(self, game, card, mode):
        p, opp = card.owner, game.opponent(card.owner)
        if mode == 0:
            # Choosing fewer than the maximum is never better, so take as many as possible.
            res = game.players[opp].resources
            left = 5
            for k in ("material", "ingredient"):
                take = min(left, res[k])
                res[k] -= take
                left -= take
            game.log(f"  {game.pname(opp)} resources now {res}")
        elif mode == 1:
            gy = [c for c in game.players[p].graveyard if c.is_pal]
            for c in game.choose_cards(p, "Zoe: return up to 1 Pal from graveyard", gy, 1, True):
                game.return_to_hand(c)
            for c in game.choose_cards(opp, "Zoe: choose 1 card from your hand to discard",
                                       list(game.players[opp].hand), 1):
                game.log(f"  {game.pname(opp)} discards {c.name}")
                game.discard(c)
        elif mode == 2:
            mine = game.choose_cards(p, "Zoe: butcher 1 of your Pals",
                                     list(game.players[p].pals), 1)
            for c in mine:
                game.send_to_graveyard(c, "butchered")
            if mine:
                for c in game.choose_cards(p, "Zoe: put 1 opposing Pal into the graveyard",
                                           opp_pals(game, p), 1):
                    game.send_to_graveyard(c, "Zoe's Strategy")


# BP01-098 Elphidran – Gentle Radiance
# AUTO OnAttack You may reveal 1 card from your hand. If you revealed a Dragon Pal this way, this
# card gets Power +500 until end of turn.
@reg
class Elphidran(CardImpl):
    code = "BP01-098"
    text = ("AUTO OnAttack You may reveal 1 card from your hand. If you revealed a Dragon Pal this "
            "way, this card gets Power +500 until end of turn.")

    def on_attack(self, game, card):
        dragons = [c for c in game.players[card.owner].hand if is_dragon_pal(c)]
        # Revealing a non-Dragon does nothing, so only Dragon Pals are offered.
        shown = game.choose_cards(card.owner, "Elphidran: reveal a Dragon Pal from hand?",
                                  dragons, 1, up_to=True)
        if shown:
            game.log(f"  {game.pname(card.owner)} reveals {shown[0].name}")
            game.add_mod(card, "power", 500, "turn", "Elphidran")


# BP01-025 Chillet – Dragon Whisperer
# AUTO OnDeploy Reveal the top card of your deck, and if it is a ◇8 or less Dragon Pal, you may
# deploy it. If you did not deploy it, add it to hand.
@reg
class Chillet(CardImpl):
    code = "BP01-025"
    text = ("AUTO OnDeploy Reveal the top card of your deck, and if it is a ◇8 or less Dragon Pal, "
            "you may deploy it. If you did not deploy it, add it to hand.")

    def on_deploy(self, game, card):
        p = card.owner
        top = game.reveal_top(p)
        if top is None:
            return
        game.stats[p].drawn.append(top.code)  # the card reaches hand or base: count it as seen
        if (is_dragon_pal(top) and top.defn.cost <= 8
                and game.may(p, f"Chillet: deploy {top.name} for free?")):
            game.log(f"  {game.pname(p)} deploys {top.name} with Chillet")
            game.deploy(top)
        else:
            game.move(top, Zone.HAND)
            game.log(f"  {top.name} is added to {game.pname(p)}'s hand")


# BP01-026 Relaxaurus – Hungry Gunner
# AUTO OnDeploy Choose up to 1 ◇6 or less Pal, and rest it. While this card is in the base, that
# card does not stand.
@reg
class Relaxaurus(CardImpl):
    code = "BP01-026"
    text = ("AUTO OnDeploy Choose up to 1 ◇6 or less Pal, and rest it. While this card is in the "
            "base, that card does not stand.")

    def on_deploy(self, game, card):
        t = choose_pal(game, card.owner, "Relaxaurus: rest and lock up to 1 ◇6- Pal",
                       lambda c: c.defn.cost <= 6)
        if t:
            rest_card(game, t)
            game.lock_standing(t, card)


# BP01-027 Jormuntide – Surging Sea Serpent
# AUTO OnDeploy Draw 1 card, choose up to 1 ◇7 or less Pal, and rest it. That card does not
# stand during your opponent's next stand phase.
@reg
class Jormuntide(CardImpl):
    code = "BP01-027"
    text = ("AUTO OnDeploy Draw 1 card, choose up to 1 ◇7 or less Pal, and rest it. That card "
            "does not stand during your opponent's next stand phase.")

    def on_deploy(self, game, card):
        game.draw(card.owner)
        t = choose_pal(game, card.owner, "Jormuntide: rest up to 1 ◇7- Pal",
                       lambda c: c.defn.cost <= 7)
        if t:
            rest_card(game, t)
            game.skip_next_stand(t, game.opponent(card.owner))

