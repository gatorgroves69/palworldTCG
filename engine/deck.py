"""Deck construction legality (CR 6.1 + Quick Manual colour limit)."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .model import CardDef, CardType, Color

MAIN_SIZE = 50
SOUL_SIZE = 10
MAX_COPIES = 4
MAX_LUCKY = 8
MAX_COLORS = 2


@dataclass
class Deck:
    name: str
    main: list[CardDef]
    soul: list[CardDef]


class DeckError(ValueError):
    pass


def deck_problems(deck: Deck) -> list[str]:
    """Every construction rule the deck breaks; empty if legal."""
    problems: list[str] = []
    if len(deck.main) != MAIN_SIZE:
        problems.append(f"main deck has {len(deck.main)} cards, needs exactly {MAIN_SIZE}")
    if len(deck.soul) != SOUL_SIZE:
        problems.append(f"soul deck has {len(deck.soul)} cards, needs exactly {SOUL_SIZE}")
    for name, n in Counter(c.name for c in deck.main).items():
        if n > MAX_COPIES:
            problems.append(f"{n} copies of '{name}' (max {MAX_COPIES})")
    lucky = sum(c.lucky for c in deck.main)
    if lucky > MAX_LUCKY:
        problems.append(f"{lucky} lucky cards (max {MAX_LUCKY})")
    colors = {c.color for c in deck.main} - {Color.COLORLESS}
    if len(colors) > MAX_COLORS:
        problems.append(f"{len(colors)} colours {sorted(x.value for x in colors)} (max {MAX_COLORS})")
    for c in deck.main:
        if c.type is CardType.SOUL:
            problems.append(f"soul card {c.code} in main deck")
            break
    for c in deck.soul:
        if c.type is not CardType.SOUL:
            problems.append(f"non-soul card {c.code} in soul deck")
            break
    return problems


def validate_deck(deck: Deck) -> None:
    problems = deck_problems(deck)
    if problems:
        raise DeckError(f"illegal deck '{deck.name}': " + "; ".join(problems))
