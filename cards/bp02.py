"""BP02 "Legends Awaken" red, blue and colorless cards, from the preview data.

The set is NOT released (docs/assumptions.md C31). Implemented early so lists can be
tested on release day. Texts may change before release: re-check them then.
"""
from __future__ import annotations

from engine.abilities import ActAbility, CardImpl, Trigger
from engine.state import Zone

from .common import (choose_pal, consume_cost, graveyard_cards, has_resources, is_dragon_pal,
                     look_top, my_gears, opp_pals, shuffle_deck)
from .registry import REGISTRY

reg = REGISTRY.register


class Legendary(CardImpl):
    """CONT Legendary: only 1 Pal with this card name can be put into your base."""
    legendary = True

    def can_play(self, game, card):
        return not any(x.name == card.name for x in game.players[card.owner].base)


def _is_legendary(c) -> bool:
    return c.is_pal and getattr(c.impl, "legendary", False)


# BP02-001 Orserk – Thunderclap Roar
# ACT [Consume 2 Material] Choose 1 of the following that was not chosen this turn: ...
def _orserk_pump(game, card, ctx):
    t = choose_pal(game, card.owner, "Orserk: +500/+1 Strike to 1 of your Pals",
                   lambda c: c.owner == card.owner, up_to=False, intent="help")
    if t:
        game.add_mod(t, "power", 500, "turn", "Orserk")
        game.add_mod(t, "strike", 1, "turn", "Orserk")


def _orserk_bolt(game, card, ctx):
    t = choose_pal(game, card.owner, "Orserk: 900 damage to 1 opposing Pal",
                   lambda c: c.owner != card.owner, up_to=False, intent="harm", amount=900)
    if t:
        game.deal_card_damage(t, 900, card)


def _orserk_stand(game, card, ctx):
    t = choose_pal(game, card.owner, "Orserk: stand 1 ◇3-or-less Pal",
                   lambda c: c.defn.cost <= 3, up_to=False, intent="stand")
    if t:
        game.stand(t)


@reg
class Orserk(CardImpl):
    code = "BP02-001"
    text = ("ACT [Consume 2 Material] Choose 1 of the following that was not chosen this turn.\n"
            "・Choose 1 of your Pals, and it gets Power +500/Strike +1 until end of turn.\n"
            "・Choose 1 of your opponent's Pals, and deal 900 Damage.\n"
            "・Choose 1 ◇3 or less Pal, and stand it.")
    acts = [ActAbility(n, f, once_per_turn=True, can_pay_extra=has_resources("material", 2),
                       pay_extra=consume_cost("material", 2))
            for n, f in (("+500/+1 Strike", _orserk_pump), ("900 damage", _orserk_bolt),
                         ("stand a ◇3- Pal", _orserk_stand))]


# BP02-003 Faleris – Marcus' Soaring Wings
# CONT Power +200 for each of your gears. AUTO OnDeploy deploy any number of ◇8+ gears with
# different card names from your hand.
@reg
class Faleris(CardImpl):
    code = "BP02-003"
    text = ("CONT This card gets Power +200 for each of your gears.\nAUTO OnDeploy Choose any "
            "number of ◇8 or greater gears with different card names from your hand, and "
            "deploy them.")

    def power_mod(self, game, card):
        return 200 * len(my_gears(game, card.owner))

    def on_deploy(self, game, card):
        p = card.owner
        gears = [c for c in game.players[p].hand if c.type.value == "gear" and c.defn.cost >= 8]
        names = set()
        for c in game.choose_cards(p, "Faleris: deploy ◇8+ gears from hand", gears,
                                   n=len(gears), up_to=True, intent="deploy"):
            if c.name not in names:
                names.add(c.name)
                game.deploy(c)


# BP02-004 Chillet Ignis – Ember-Clad Dragon (renamed and reworded in the 2026-10-12 data
# refresh; same effect)
# AUTO OnDeploy You may discard 1 Dragon Pal from hand. If you discarded a card this way,
# choose 1 Pal, and deal 700 Damage.
@reg
class ChilletIgnis(CardImpl):
    code = "BP02-004"
    text = ("AUTO OnDeploy You may discard 1 Dragon Pal from hand. If you discarded a card "
            "this way, choose 1 Pal, and deal 700 Damage.")

    def on_deploy(self, game, card):
        p = card.owner
        dragons = [c for c in game.players[p].hand if is_dragon_pal(c)]
        picked = game.choose_cards(p, "Chillet Ignis: discard a Dragon for 700 damage?",
                                   dragons, 1, up_to=True, intent="discard")
        if not picked:
            return
        game.discard(picked[0])
        t = choose_pal(game, p, "Chillet Ignis: 700 damage to 1 Pal", up_to=False,
                       intent="harm", amount=700)
        if t:
            game.deal_card_damage(t, 700, card)


# BP02-007 Flambelle – Feverish Tears
# ACT [Rest this card] Get 2 Material.
@reg
class FlambelleFeverish(CardImpl):
    code = "BP02-007"
    text = "ACT [Rest this card] Get 2 Material."
    acts = [ActAbility("get 2 Material",
                       lambda g, c, ctx: g.gain_resource(c.owner, "material", 2), rest_self=True)]


# BP02-010 Relaxaurus Lux – Party Time
# CONT Assault. AUTO When the opposing combat Pal is put into the graveyard during this
# card's attack, stand this card.
@reg
class RelaxaurusLux(CardImpl):
    code = "BP02-010"
    text = ("CONT Assault (This card can attack Pals in the stand state)\nAUTO When the opposing "
            "combat Pal is put into the graveyard during this card's attack, stand this card.")
    keywords = {"assault": True}

    def triggers(self, game, card, event):
        b = game.battle
        if (b is None or b.attacker is not card or event.kind != "left_base"
                or event.data["to"] is not Zone.GRAVEYARD or card.zone is not Zone.BASE):
            return []
        opp = b.opponent_of(card)
        if opp is None or opp.uid != event.card_uid:
            return []
        return [Trigger(card.owner, f"{card.name}: stand", lambda g: g.stand(card), card.uid)]


# BP02-013 Foxparks – Breathing Practice (vanilla)
@reg
class FoxparksBreathing(CardImpl):
    code = "BP02-013"
    text = ""


# BP02-025 Frostallion – Everlasting Rime
# Legendary. CONT Pals in your hand cost 2 less (min 1). AUTO At the end of your turn,
# draw until your hand has 4 cards.
@reg
class Frostallion(Legendary):
    code = "BP02-025"
    text = ("CONT Legendary (Only 1 〈Legendary〉 Pal with the same card name can be put into your base)\nCONT Reduce the cost of Pals in your hand by 2. It does not become "
            "◇0 or less from this ability.\nAUTO At the end of your turn, draw until your hand "
            "has 4 cards.")

    def aura_cost(self, game, card, target):
        return -2 if target.is_pal and target.owner == card.owner else 0

    def triggers(self, game, card, event):
        if event.kind == "turn_end" and event.player == card.owner:
            def fire(g, p=card.owner):
                g.draw(p, max(0, 4 - len(g.players[p].hand)))
            return [Trigger(card.owner, f"{card.name}: draw to 4", fire, card.uid)]
        return []


# BP02-026 Foxcicle – Aurora Hymn
# CONT Legendary Pals in your hand cost 1 less (min 1). AUTO OnDeploy Draw 1, then discard 1.
@reg
class Foxcicle(CardImpl):
    code = "BP02-026"
    text = ("CONT Reduce the cost of 〈Legendary〉 Pals in your hand by 1. It does not become ◇0 "
            "or less from this ability.\nAUTO OnDeploy Draw 1 card, choose 1 card from your "
            "hand, and discard it.")

    def aura_cost(self, game, card, target):
        return -1 if _is_legendary(target) and target.owner == card.owner else 0

    def on_deploy(self, game, card):
        p = card.owner
        game.draw(p)
        for c in game.choose_cards(p, "Foxcicle: discard 1 card", list(game.players[p].hand), 1,
                                   intent="discard"):
            game.discard(c)


# BP02-029 Jolthog Cryst – Midwinter Awakening
# AUTO OnDeploy You may reveal 1 Legendary Pal from your hand; if you didn't, rest this card.
@reg
class JolthogCryst(CardImpl):
    code = "BP02-029"
    text = ("AUTO OnDeploy You may reveal 1 〈Legendary〉 Pal from your hand, and if you did not "
            "reveal a card, rest this card.")

    def on_deploy(self, game, card):
        p = card.owner
        legends = [c for c in game.players[p].hand if _is_legendary(c)]
        if legends:
            game.log(f"  {game.pname(p)} reveals {legends[0].name} for Jolthog Cryst")
        else:
            card.rested = True


# BP02-047 Overloaded with Love (Event)
# Look at the top 3 cards of your deck, add up to 1 Pal and up to 1 structure to hand, and
# put the rest on the bottom of your deck in any order.
@reg
class OverloadedWithLove(CardImpl):
    code = "BP02-047"
    text = ("Look at the top 3 cards of your deck, choose up to 1 Pal and up to 1 structure from "
            "among them and add them to hand, and put the rest of the cards on the bottom of "
            "your deck in any order.")

    def resolve_event(self, game, card, mode):
        p = card.owner
        top = look_top(game, p, 3)
        taken = []
        for kind, pred in (("Pal", lambda c: c.is_pal), ("structure", lambda c: c.is_structure)):
            cands = [c for c in top if pred(c) and c not in taken]
            taken += game.choose_cards(p, f"Overloaded with Love: add up to 1 {kind} to hand",
                                       cands, 1, up_to=True, intent="recover")
        for c in taken:
            game.move(c, Zone.HAND)
        for c in top:
            if c not in taken:
                game.move(c, Zone.DECK, top=False)


# BP02-097 Jetragon – Legendary Guardian Dragon
# Legendary. ACT 1/Turn [Exile 2 ◇7+ Pals from the graveyard] Gains Vigilance until end of
# turn. Then, if all exiled cards were Legendary, choose up to 3 Legendary Pals and stand them.
def _jetragon_pay(game, card, ctx):
    p = card.owner
    big = graveyard_cards(game, p, lambda c: c.is_pal and c.defn.cost >= 7)
    chosen = game.choose_cards(p, "Jetragon: exile 2 ◇7+ Pals from your graveyard", big, 2,
                               intent="discard")
    if len(chosen) != 2:
        raise ValueError("Jetragon: needs 2 ◇7+ Pals in the graveyard")
    for c in chosen:
        game.move(c, Zone.EXILE)
    ctx["exiled"] = chosen


def _jetragon_fire(game, card, ctx):
    game.grant_keyword(card, "vigilance", "turn")
    if all(_is_legendary(c) for c in ctx.get("exiled", [])):
        legends = [c for ps in game.players for c in ps.base if _is_legendary(c)]
        for c in game.choose_cards(card.owner, "Jetragon: stand up to 3 Legendary Pals", legends,
                                   3, up_to=True, intent="stand"):
            game.stand(c)


@reg
class Jetragon(Legendary):
    code = "BP02-097"
    text = ("CONT Legendary (Only 1 〈Legendary〉 Pal with the same card name can be put into your base)\nACT 1/Turn [Exile 2 ◇7 or greater Pals from the graveyard] This "
            "card gets the skill in 〈〉 until end of turn. 〈AUTO Vigilance (At the end of your turn, "
            "stand this card)〉. Then, if all of the cards exiled by this ability have 〈Legendary〉, "
            "choose up to 3 〈Legendary〉 Pals, and stand them.")
    acts = [ActAbility("exile 2 ◇7+ Pals: Vigilance", _jetragon_fire, once_per_turn=True,
                       can_pay_extra=lambda g, c: len(graveyard_cards(
                           g, c.owner, lambda x: x.is_pal and x.defn.cost >= 7)) >= 2,
                       pay_extra=_jetragon_pay)]


# ---------------------------------------------------------------------------------------------
# Added 2026-10-16 from the 2026-10-12 data refresh (texts may still change before release).

def _plus_strike1(game, card, ctx):
    t = choose_pal(game, card.owner, f"{card.name}: Strike +1 to 1 Pal",
                   lambda c: c.owner == card.owner, up_to=False, intent="help")
    if t:
        game.add_mod(t, "strike", 1, "turn", card.name)


def _plus_power200(game, card, ctx):
    t = choose_pal(game, card.owner, f"{card.name}: +200 Power to 1 Pal", up_to=False,
                   intent="help", amount=200)
    if t:
        game.add_mod(t, "power", 200, "turn", card.name)


# BP02-018 Rocket Launcher (Gear)
# AUTO OnDeploy Choose up to 3 Pals, and deal 1000 Damage.
# ACT [Rest this card] Choose 1 Pal, and it gets Strike +1 until end of turn.
@reg
class RocketLauncher(CardImpl):
    code = "BP02-018"
    text = ("AUTO OnDeploy Choose up to 3 Pals, and deal 1000 Damage.\nACT [Rest this card] "
            "Choose 1 Pal, and it gets Strike +1 until end of turn.")
    acts = [ActAbility("Strike +1", _plus_strike1, rest_self=True)]

    def on_deploy(self, game, card):
        p = card.owner
        pals = [c for ps in game.players for c in ps.pals]
        for t in game.choose_cards(p, "Rocket Launcher: deal 1000 to up to 3 Pals", pals, 3,
                                   up_to=True, intent="harm", amount=1000):
            game.deal_card_damage(t, 1000, card)


# BP02-022 Axel's Gambit (Event, lucky)
# Choose all of your Pals and gears, and stand them.
@reg
class AxelsGambit(CardImpl):
    code = "BP02-022"
    text = "Choose all of your Pals and gears, and stand them."

    def resolve_event(self, game, card, mode):
        p = card.owner
        for c in list(game.players[p].base):
            if (c.is_pal or c.type.value == "gear") and c.rested:
                game.stand(c)
                game.log(f"  {c.name} stands")


# BP02-023 Marcus' Turf (Event)
# Look at the top 5 cards of your deck, choose up to 1 ◇8 or greater red card from among them
# and add it to hand, and shuffle the rest of the cards with the deck.
@reg
class MarcusTurf(CardImpl):
    code = "BP02-023"
    text = ("Look at the top 5 cards of your deck, choose up to 1 ◇8 or greater red card from "
            "among them and add it to hand, and shuffle the rest of the cards with the deck.")

    def resolve_event(self, game, card, mode):
        p = card.owner
        top = look_top(game, p, 5)
        hits = [c for c in top if c.defn.cost >= 8 and c.defn.color.value == "red"]
        for c in game.choose_cards(p, "Marcus' Turf: add a ◇8+ red card", hits, 1, up_to=True,
                                   intent="recover"):
            game.move(c, Zone.HAND)
            game.log(f"  {c.name} goes to the hand")
        shuffle_deck(game, p)


# BP02-046 Victor's Gambit (Event, lucky)
# Choose 1 of your Pals, choose 1 Pal from your hand with the same cost as that card, and
# deploy it.
def _victor_pairs(game, p):
    costs = {c.defn.cost for c in game.players[p].pals}
    return [c for c in game.players[p].hand if c.is_pal and c.defn.cost in costs
            and c.impl.can_play(game, c)]


@reg
class VictorsGambit(CardImpl):
    code = "BP02-046"
    text = ("Choose 1 of your Pals, choose 1 Pal from your hand with the same cost as that "
            "card, and deploy it.")

    def can_play(self, game, card):
        return bool(_victor_pairs(game, card.owner))

    def resolve_event(self, game, card, mode):
        p = card.owner
        for c in game.choose_cards(p, "Victor's Gambit: deploy a Pal of the same cost",
                                   _victor_pairs(game, p), 1, up_to=False, intent="deploy"):
            game.deploy(c)


# BP02-099 Eikthyrdeer – Warden of the Woods (colorless Pal, 900/S2, Interrupt)
@reg
class Eikthyrdeer(CardImpl):
    code = "BP02-099"
    text = ("ACT Interrupt (Hand Quick [①, discard this card] OR [Discard this card and 1 other "
            "card from hand] Nullify the opponent's attack. Battle damage does not occur)")
    keywords = {"interrupt": True}


# BP02-044 Frostallion Saddle (Gear)
# CONT Your main name 《Frostallion》 Pals cannot be chosen by the effects of your opponent's
# Pals. ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn.
# The CONT half isn't modelled (it only protects Frostallion from Pal effects).
@reg
class FrostallionSaddle(CardImpl):
    code = "BP02-044"
    text = ("CONT Your main name 《Frostallion》 Pals cannot be chosen by the effects of your "
            "opponent's Pals.\nACT [Rest this card] Choose 1 Pal, and it gets Power +200 until "
            "end of turn.")
    acts = [ActAbility("+200 power", _plus_power200, rest_self=True)]


# ---------------------------------------------------------------------------------------------
# The Swee package (added 2026-10-16). "Main name" is the part before " – ".

def _is_swee(c) -> bool:
    return c.is_pal and c.defn.main_name == "Swee"


def _swee_family(c) -> bool:
    return c.is_pal and c.defn.main_name in ("Swee", "Sweepa")


# BP02-034 Swee – Hibernating Together (◇3 400/S1)
# CONT You may put up to 8 cards with the same card name as this card into your deck.
# AUTO OnDeploy If you have a total of 3 or more main name 《Sweepa》 and/or 《Swee》 Pals,
# draw 1 card.
# The deck-building CONT is enforced in engine/deck.copy_limit.
@reg
class Swee(CardImpl):
    code = "BP02-034"
    text = ("CONT You may put up to 8 cards with the same card name as this card into your deck.\n"
            "AUTO OnDeploy If you have a total of 3 or more main name 《Sweepa》 and/or 《Swee》 "
            "Pals, draw 1 card.")

    def on_deploy(self, game, card):
        if sum(_swee_family(c) for c in game.players[card.owner].pals) >= 3:
            game.draw(card.owner)


# BP02-027 Sweepa – Record Breaker (◇6 1200/S2, lucky)
# AUTO OnDeploy Choose up to 101 main name 《Swee》 Pals from your hand, and deploy them.
@reg
class Sweepa(CardImpl):
    code = "BP02-027"
    text = "AUTO OnDeploy Choose up to 101 main name 《Swee》 Pals from your hand, and deploy them."

    def on_deploy(self, game, card):
        p = card.owner
        swees = [c for c in game.players[p].hand if _is_swee(c)]
        for c in game.choose_cards(p, "Sweepa: deploy Swee from hand", swees, 101, up_to=True,
                                   intent="deploy"):
            game.deploy(c)


# BP02-045 Sweepa Saddle (Gear ◇3)
# AUTO OnDeploy Reveal the top 5 cards of your deck, choose any number of main name 《Swee》
# Pals from among them, add them to hand, and shuffle the rest of the cards with the deck.
# ACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end of turn.
@reg
class SweepaSaddle(CardImpl):
    code = "BP02-045"
    text = ("AUTO OnDeploy Reveal the top 5 cards of your deck, choose any number of main name "
            "《Swee》 Pals from among them, add them to hand, and shuffle the rest of the cards "
            "with the deck.\nACT [Rest this card] Choose 1 Pal, and it gets Power +200 until end "
            "of turn.")
    acts = [ActAbility("+200 power", _plus_power200, rest_self=True)]

    def on_deploy(self, game, card):
        p = card.owner
        top = look_top(game, p, 5)
        for c in game.choose_cards(p, "Sweepa Saddle: take Swee", [c for c in top if _is_swee(c)],
                                   5, up_to=True, intent="recover"):
            game.move(c, Zone.HAND)
            game.log(f"  {c.name} goes to the hand")
        shuffle_deck(game, p)
