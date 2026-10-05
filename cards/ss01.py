"""SS01 "Sleeve & Card Set Vol.1" cards (released October 2026; docs/assumptions.md C29)."""
from __future__ import annotations

from engine.abilities import CardImpl, Trigger
from engine.state import Zone

from .common import opp_pals
from .registry import REGISTRY

reg = REGISTRY.register


# SS01-001 Grizzbolt – Raining Lightning
# AUTO OnDeploy Choose all of your opponent's Pals, and deal 300 Damage.
@reg
class Grizzbolt(CardImpl):
    code = "SS01-001"
    text = "AUTO OnDeploy Choose all of your opponent's Pals, and deal 300 Damage."

    def on_deploy(self, game, card):
        for t in opp_pals(game, card.owner):
            game.deal_card_damage(t, 300, card)


# SS01-002 Chillet – Finishing Ice Blade
# AUTO When this card's opposing combat Pal is put into the graveyard, draw 1 card.
@reg
class ChilletIceBlade(CardImpl):
    code = "SS01-002"
    text = "AUTO When this card's opposing combat Pal is put into the graveyard, draw 1 card."

    def triggers(self, game, card, event):
        # C30: only while this card is still in the base when its opponent leaves (if both
        # are put into the graveyard by the same rule action, this card is checked first or
        # second depending on order, so a mutual kill may not draw).
        b = game.battle
        if (b is None or event.kind != "left_base" or event.data["to"] is not Zone.GRAVEYARD
                or card.zone is not Zone.BASE):
            return []
        opp = b.opponent_of(card)
        if opp is None or opp.uid != event.card_uid:
            return []
        return [Trigger(card.owner, f"{card.name}: draw 1",
                        lambda g, p=card.owner: g.draw(p), card.uid)]


# SS01-003 Depresso – Midnight Effort (purple: not used by red/blue decks)
# CONT Nocturnal. AUTO OnDeploy If it is night, choose up to 1 structure, and it gets
# Durability -500 until end of turn.


# SS01-004 Cattiva – Brimming with Confidence
# CONT If you have 5 or more souls, this card gets Power +200.
# CONT If you have 10 or more souls, this card gets Power +200.
@reg
class CattivaBrimming(CardImpl):
    code = "SS01-004"
    text = ("CONT If you have 5 or more souls, this card gets Power +200.\nCONT If you have 10 "
            "or more souls, this card gets Power +200.")

    def power_mod(self, game, card):
        souls = game.players[card.owner].souls
        return (200 if souls >= 5 else 0) + (200 if souls >= 10 else 0)


# SS01-005 Quivern – Wyvern's Breath
# AUTO When this card attacks a Pal or structure, choose up to 1 Pal or structure, and deal
# 700 Damage.
@reg
class Quivern(CardImpl):
    code = "SS01-005"
    text = ("AUTO When this card attacks a Pal or structure, choose up to 1 Pal or structure, "
            "and deal 700 Damage.")

    def on_attack(self, game, card):
        b = game.battle
        if b is None or b.target is None:  # attacking the player
            return
        cands = [c for ps in game.players for c in ps.base if c.is_pal or c.is_structure]
        picked = game.choose_cards(card.owner, "Quivern: deal 700 damage to up to 1 Pal or "
                                   "structure", cands, n=1, up_to=True, intent="harm",
                                   amount=700)
        for t in picked:
            game.deal_card_damage(t, 700, card)
