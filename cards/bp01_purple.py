"""BP01 purple cards added for M2: the night / Nocturnal package."""
from __future__ import annotations

from engine.abilities import ActAbility, CardImpl, Trigger
from engine.state import Zone

from .common import (choose_pal, discard_cost, graveyard_cards, mill_cost, opp_pals,
                     plus_power)
from .registry import REGISTRY

reg = REGISTRY.register


def _nocturnal_pal(game, c) -> bool:
    return c.is_pal and game.has_kw(c, "nocturnal")


# BP01-073 Helzephyr – Wings of the Moonless Night
# CONT Nocturnal (If it is night, this card gets Power +300)
# AUTO When your 〈Nocturnal〉 Pal is deployed, if it is night, choose up to 1 Pal with cost less
# than or equal to that, and put it into the graveyard. If you put 1 or more Pals this way, at
# the end of that turn, rest this card.
@reg
class Helzephyr(CardImpl):
    code = "BP01-073"
    text = ("CONT Nocturnal (If it is night, this card gets Power +300)\nAUTO When your "
            "〈Nocturnal〉 Pal is deployed, if it is night, choose up to 1 Pal with cost less than "
            "or equal to that, and put it into the graveyard. If you put 1 or more Pals this way, "
            "at the end of that turn, rest this card.")
    keywords = {"nocturnal": True}

    def triggers(self, game, card, event):
        if event.kind != "deployed" or event.player != card.owner:
            return []
        new = game.card(event.card_uid)
        # Includes Helzephyr's own deployment: it is a Nocturnal Pal too (C13).
        if not _nocturnal_pal(game, new) or not game.is_night():
            return []
        me, me_inc, limit = card.uid, card.incarnation, new.defn.cost

        def fire(g, me=me, me_inc=me_inc, limit=limit):
            if not g.is_night():  # "if it is night" is checked again on resolution
                return
            src = g.card(me)
            t = choose_pal(g, src.owner, f"Helzephyr: destroy up to 1 Pal with cost ≤ {limit}",
                           lambda c: c.defn.cost <= limit, intent="harm")
            if t:
                g.send_to_graveyard(t, "Helzephyr")

                def rest_me(g2, me=me, me_inc=me_inc):
                    c = g2.card(me)
                    if g2.on_base(c, me_inc):
                        c.rested = True
                        g2.log(f"  {c.name} is rested (Helzephyr)")
                g.at_end_of_turn(Trigger(src.owner, "Helzephyr: rest at end of turn", rest_me,
                                         me), src)
        return [Trigger(card.owner, f"{card.name}: Nocturnal Pal deployed at night", fire,
                        card.uid)]


# BP01-074 Shadowbeak – Seed of Despair
# CONT While this card is in the rest state, it is night.
# CONT If it is night, your Pal's AUTO activates twice.
# AUTO At the end of your turn, choose up to 1 of your Pals, and butcher it. If you butchered 1
# or more cards this way, your opponent chooses 1 of their Pals, and puts it into the graveyard.
def _shadowbeak_edict(game, p):
    mine = game.choose_cards(p, "Shadowbeak: butcher up to 1 of your Pals",
                             list(game.players[p].pals), 1, up_to=True, intent="edict")
    for c in mine:
        game.send_to_graveyard(c, "butchered")
    if mine:
        opp = game.opponent(p)
        for c in game.choose_cards(opp, "Shadowbeak: put 1 of your Pals into the graveyard",
                                   opp_pals(game, p), 1, intent="sacrifice"):
            game.send_to_graveyard(c, "Shadowbeak")


@reg
class Shadowbeak(CardImpl):
    code = "BP01-074"
    text = ("CONT While this card is in the rest state, it is night.\nCONT If it is night, your "
            "Pal's AUTO activates twice.\nAUTO At the end of your turn, choose up to 1 of your "
            "Pals, and butcher it. If you butchered 1 or more cards this way, your opponent "
            "chooses 1 of their Pals, and puts it into the graveyard.")

    def makes_night(self, game, card):
        return card.rested

    def auto_multiplier(self, game, card, source):
        # Every AUTO of your Pals, keyword ones included, and itself (C10).
        return 2 if source.owner == card.owner and game.is_night() else 1

    def triggers(self, game, card, event):
        if event.kind == "turn_end" and event.player == card.owner:
            return [Trigger(card.owner, f"{card.name}: end-of-turn butcher",
                            lambda g, p=card.owner: _shadowbeak_edict(g, p), card.uid)]
        return []


# BP01-078 Lyleen Noct – Providence of the Goddess
# ACT [Rest this card, discard 1 card from hand] Choose 1 ◇6 or less Pal from your graveyard, and
# deploy it in the rest state.
_LYLEEN_DISCARD = discard_cost(1)


def _revive_small(game, card, ctx):
    p = card.owner
    gy = graveyard_cards(game, p, lambda c: c.is_pal and c.defn.cost <= 6)
    for c in game.choose_cards(p, "Lyleen Noct: deploy a ◇6- Pal from graveyard, rested", gy, 1,
                               intent="recover"):
        game.log(f"  {game.pname(p)} deploys {c.name} from the graveyard (rested)")
        game.deploy(c, rested=True)


@reg
class LyleenNoct(CardImpl):
    code = "BP01-078"
    text = ("ACT [Rest this card, discard 1 card from hand] Choose 1 ◇6 or less Pal from your "
            "graveyard, and deploy it in the rest state.")
    # Offered only when there is something to revive (the cost could be paid anyway, for nothing).
    acts = [ActAbility("revive a ◇6- Pal", _revive_small, rest_self=True,
                       can_pay_extra=_LYLEEN_DISCARD[0], pay_extra=_LYLEEN_DISCARD[1],
                       condition=lambda g, c: bool(graveyard_cards(
                           g, c.owner, lambda x: x.is_pal and x.defn.cost <= 6)))]


# BP01-079 Depresso – Late Night Hustler
# CONT Nocturnal (If it is night, this card gets Power +300)
# CONT Nocturnal (If it is night, this card gets Power +300)
@reg
class Depresso(CardImpl):
    code = "BP01-079"
    text = ("CONT Nocturnal (If it is night, this card gets Power +300)\nCONT Nocturnal (If it is "
            "night, this card gets Power +300)")
    keywords = {"nocturnal": 2}  # two instances: +600 at night (C12)


# BP01-080 Daedream – First Slumber
# CONT Nocturnal (If it is night, this card gets Power +300)
@reg
class DaedreamFirstSlumber(CardImpl):
    code = "BP01-080"
    text = "CONT Nocturnal (If it is night, this card gets Power +300)"
    keywords = {"nocturnal": True}


# BP01-082 Daedream – Deep Slumber
# CONT Nocturnal (If it is night, this card gets Power +300)
@reg
class DaedreamDeepSlumber(CardImpl):
    code = "BP01-082"
    text = "CONT Nocturnal (If it is night, this card gets Power +300)"
    keywords = {"nocturnal": True}


# BP01-084 Menasting – Darkness-Dwelling Scorpion
# AUTO Retaliate (When this card is put into the graveyard during battle, put the opposing combat
# Pal into the graveyard)
# AUTO When this card is put into the graveyard, choose up to 1 normal Pal from your graveyard,
# and return it to hand.
@reg
class Menasting(CardImpl):
    code = "BP01-084"
    text = ("AUTO Retaliate (When this card is put into the graveyard during battle, put the "
            "opposing combat Pal into the graveyard)\nAUTO When this card is put into the "
            "graveyard, choose up to 1 normal Pal from your graveyard, and return it to hand.")
    keywords = {"retaliate": True}

    def triggers(self, game, card, event):
        if (event.kind == "left_base" and event.card_uid == card.uid
                and event.data["to"] is Zone.GRAVEYARD):
            def fire(g, p=card.owner):
                gy = graveyard_cards(g, p, lambda c: c.is_pal and c.defn.subtype == "Normal")
                for c in g.choose_cards(p, "Menasting: return up to 1 normal Pal to hand", gy, 1,
                                        up_to=True, intent="recover"):
                    g.return_to_hand(c)
            return [Trigger(card.owner, f"{card.name}: return a normal Pal", fire, card.uid)]
        return []


# BP01-085 Maraith – Twilight Messenger
# CONT While this card is in the rest state, it is night.
# CONT If it is night, all of your opponent's Pals get Power -200 (It is not put into the
# graveyard even if Power becomes 0 or less).
@reg
class Maraith(CardImpl):
    code = "BP01-085"
    text = ("CONT While this card is in the rest state, it is night.\nCONT If it is night, all of "
            "your opponent's Pals get Power -200 (It is not put into the graveyard even if Power "
            "becomes 0 or less).")

    def makes_night(self, game, card):
        return card.rested

    def aura_power(self, game, card, target):
        if target.is_pal and target.owner != card.owner and game.is_night():
            return -200
        return 0


_MILL3 = mill_cost(3)


def _night(game, card, ctx):
    game.make_night(card.owner)


# BP01-088 Lamp (Structure)
# ACT 1/Turn [Put the top 3 cards of the deck into the graveyard] It becomes night until the end
# of the opponent's next turn.
# CONT All of your Pals get the skill in 〈 〉. 〈CONT Nocturnal (If it is night, this card gets
# Power +300)〉.
@reg
class Lamp(CardImpl):
    code = "BP01-088"
    text = ("ACT 1/Turn [Put the top 3 cards of the deck into the graveyard] It becomes night "
            "until the end of the opponent's next turn.\nCONT All of your Pals get the skill in 〈 "
            "〉. 〈CONT Nocturnal (If it is night, this card gets Power +300)〉.")
    acts = [ActAbility("make it night", _night, once_per_turn=True,
                       can_pay_extra=_MILL3[0], pay_extra=_MILL3[1])]

    def grant_keywords(self, game, card, target):
        # One more Nocturnal instance on each of your Pals, even ones that have it (C12).
        return {"nocturnal": 1} if target.is_pal and target.owner == card.owner else {}


# BP01-089 Shoddy Bed (Structure)
# ACT 1/Turn [Put the top 3 cards of the deck into the graveyard] It becomes night until the end
# of the opponent's next turn.
# AUTO At the end of your turn, if you have a 〈Nocturnal〉 Pal in the rest state, draw 1 card.
@reg
class ShoddyBed(CardImpl):
    code = "BP01-089"
    text = ("ACT 1/Turn [Put the top 3 cards of the deck into the graveyard] It becomes night "
            "until the end of the opponent's next turn.\nAUTO At the end of your turn, if you have "
            "a 〈Nocturnal〉 Pal in the rest state, draw 1 card.")
    acts = [ActAbility("make it night", _night, once_per_turn=True,
                       can_pay_extra=_MILL3[0], pay_extra=_MILL3[1])]

    def triggers(self, game, card, event):
        if event.kind == "turn_end" and event.player == card.owner and any(
                c.rested and _nocturnal_pal(game, c) for c in game.players[card.owner].pals):
            return [Trigger(card.owner, f"{card.name}: draw 1",
                            lambda g, p=card.owner: g.draw(p), card.uid)]
        return []


# BP01-090 Medieval Medicine Workbench (Structure)
# ACT 1/Turn [③, assign 1 Pal] Choose 1 cost X or less Pal from your graveyard, and deploy it in
# the rest state. X is equal to the cost of the assigned Pal +2.
def _workbench(game, card, ctx):
    p = card.owner
    limit = ctx["assigned"].defn.cost + 2
    gy = graveyard_cards(game, p, lambda c: c.is_pal and c.defn.cost <= limit)
    for c in game.choose_cards(p, f"Workbench: deploy a ◇{limit}- Pal from graveyard, rested",
                               gy, 1, intent="recover"):
        game.log(f"  {game.pname(p)} deploys {c.name} from the graveyard (rested)")
        game.deploy(c, rested=True)


@reg
class MedievalMedicineWorkbench(CardImpl):
    code = "BP01-090"
    text = ("ACT 1/Turn [③, assign 1 Pal] Choose 1 cost X or less Pal from your graveyard, and "
            "deploy it in the rest state. X is equal to the cost of the assigned Pal +2.")
    acts = [ActAbility("revive a Pal", _workbench, souls=3, assign=True, once_per_turn=True,
                       condition=lambda g, c: bool(graveyard_cards(g, c.owner,
                                                                   lambda x: x.is_pal)))]


# BP01-094 Daedream's Necklace (Gear)
# AUTO OnDeploy Choose up to 1 main name 《Daedream》 Pal from your hand, and deploy it.
# ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn. It becomes night
# until the end of the opponent's next turn.
def _necklace_act(game, card, ctx):
    plus_power(200)(game, card, ctx)
    game.make_night(card.owner)


@reg
class DaedreamsNecklace(CardImpl):
    code = "BP01-094"
    text = ("AUTO OnDeploy Choose up to 1 main name 《Daedream》 Pal from your hand, and deploy "
            "it.\nACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn. It "
            "becomes night until the end of the opponent's next turn.")
    acts = [ActAbility("+200 and make it night", _necklace_act, rest_self=True)]

    def on_deploy(self, game, card):
        p = card.owner
        options = [c for c in game.players[p].hand
                   if c.is_pal and "Daedream" in game.main_names(c)]
        for c in game.choose_cards(p, "Necklace: deploy up to 1 Daedream from hand", options, 1,
                                   up_to=True, intent="recover"):
            game.log(f"  {game.pname(p)} deploys {c.name} with the Necklace")
            game.deploy(c)


# BP01-076 Tombat – Out of Nowhere!?
# AUTO OnDeploy Reveal the top 3 cards of your deck, choose up to 1 Pal from among them and add
# it to hand, and put the remaining cards into the graveyard.
@reg
class Tombat(CardImpl):
    code = "BP01-076"
    text = ("AUTO OnDeploy Reveal the top 3 cards of your deck, choose up to 1 Pal from among them "
            "and add it to hand, and put the remaining cards into the graveyard.")

    def on_deploy(self, game, card):
        p = card.owner
        top = list(game.players[p].deck[:3])
        game.log(f"  {game.pname(p)} reveals " + ", ".join(c.name for c in top))
        for c in game.choose_cards(p, "Tombat: add up to 1 Pal to hand",
                                   [c for c in top if c.is_pal], 1, up_to=True,
                                   intent="recover"):
            top.remove(c)
            game.move(c, Zone.HAND)
            game.stats[p].drawn.append(c.code)
            game.log(f"  {game.pname(p)} adds {c.name} to hand")
        for c in top:
            game.move(c, Zone.GRAVEYARD)
        if top:
            game.log(f"  {', '.join(c.name for c in top)} go to the graveyard")
