"""BP01 green cards used by the Green/Purple Nocturnal list (gf deck candidate)."""
from __future__ import annotations

from engine.abilities import CardImpl

from .registry import REGISTRY
from .td01 import INTERRUPT_TEXT

reg = REGISTRY.register


# BP01-054 Warsect – Iron Fortress
# CONT Taunt
@reg
class Warsect(CardImpl):
    code = "BP01-054"
    text = ("CONT Taunt (Your opponent cannot attack other targets if a card with taunt can be "
            "targeted for an attack)")
    keywords = {"taunt": True}


# BP01-062 Wumpo Botan – Tropical Sentinel
# ACT Interrupt
@reg
class WumpoBotan(CardImpl):
    code = "BP01-062"
    text = INTERRUPT_TEXT
    keywords = {"interrupt": True}
