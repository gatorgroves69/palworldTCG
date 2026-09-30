"""Static card data: what is printed on a card. Pure data, no game logic."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CardType(str, Enum):
    PAL = "pal"
    STRUCTURE = "structure"
    GEAR = "gear"
    EVENT = "event"
    SOUL = "soul"


class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    COLORLESS = "colorless"


@dataclass(frozen=True)
class CardDef:
    """Printed information of a card (CR 2). `power` doubles as durability for structures."""

    code: str
    name: str
    type: CardType
    color: Color = Color.COLORLESS
    cost: int = 0
    power: int = 0
    strike: int = 0
    lucky: bool = False
    subtype: str = ""
    text: str = ""
    elements: tuple[str, ...] = ()  # lower-case, e.g. ("water", "dragon") (CR 2.4)

    @property
    def main_name(self) -> str:
        # CR 2.1.3.1: "Main – Sub" (em/en dash surrounded by spaces).
        for sep in (" – ", " — "):
            if sep in self.name:
                return self.name.split(sep, 1)[0]
        return self.name

    def has_element(self, element: str) -> bool:
        return element.lower() in self.elements

    def __deepcopy__(self, memo):  # immutable; share across game clones
        return self
