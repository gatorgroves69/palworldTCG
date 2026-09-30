"""Mutable game state: card instances, players, battle context."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .abilities import CardImpl
from .model import CardDef, CardType


class Zone(str, Enum):
    DECK = "deck"
    HAND = "hand"
    BASE = "base"
    GRAVEYARD = "graveyard"
    EXILE = "exile"
    RESOLUTION = "resolution"  # an event card while it resolves (CR 4.11)


@dataclass
class Mod:
    """A temporary or permanent change to a stat (power, strike)."""

    stat: str
    amount: int
    until: str | None = "turn"  # "turn", "battle", or None (while on base)
    source: str = ""


@dataclass
class CardInstance:
    uid: int
    defn: CardDef
    impl: CardImpl
    owner: int
    zone: Zone = Zone.DECK
    rested: bool = False
    damage: int = 0
    mods: list[Mod] = field(default_factory=list)
    # Bumped whenever the card leaves the base: it is a "new card" (CR 4.1.4).
    incarnation: int = 0
    deployed_turn: int = -1
    assigned_to: int | None = None  # uid of the structure this Pal was assigned to this turn
    act_uses: dict[int, int] = field(default_factory=dict)  # ACT index -> uses this turn
    granted: list = field(default_factory=list)  # [(ActAbility, until)] granted by effects (〈〉)
    granted_kw: list = field(default_factory=list)  # [(keyword, until)]
    granted_auto: list = field(default_factory=list)  # [(hook, name, fn(game, card), until)]
    stand_locks: list = field(default_factory=list)  # [(source uid, source incarnation)]
    skip_stand: list = field(default_factory=list)  # players whose next stand phase it skips

    @property
    def code(self) -> str:
        return self.defn.code

    @property
    def name(self) -> str:
        return self.defn.name

    @property
    def type(self) -> CardType:
        return self.defn.type

    @property
    def is_pal(self) -> bool:
        return self.defn.type is CardType.PAL

    @property
    def is_structure(self) -> bool:
        return self.defn.type is CardType.STRUCTURE

    def kw(self, name: str) -> int | bool:
        return self.impl.keywords.get(name, False)

    def reset_for_new_zone(self) -> None:
        self.rested = False
        self.damage = 0
        self.mods.clear()
        self.incarnation += 1
        self.assigned_to = None
        self.act_uses.clear()
        self.granted.clear()
        self.granted_kw.clear()
        self.granted_auto.clear()
        self.stand_locks.clear()
        self.skip_stand.clear()

    def label(self) -> str:
        return f"{self.name} [{self.code}]#{self.uid}"


@dataclass
class PlayerState:
    idx: int
    deck: list[CardInstance] = field(default_factory=list)  # index 0 = top
    hand: list[CardInstance] = field(default_factory=list)
    base: list[CardInstance] = field(default_factory=list)  # Pals, structures, gear
    graveyard: list[CardInstance] = field(default_factory=list)
    exile: list[CardInstance] = field(default_factory=list)
    soul_deck: int = 10
    souls: int = 0  # soul cards in the soul area
    souls_rested: int = 0
    life: int = 10
    damage_taken: int = 0
    resources: dict[str, int] = field(default_factory=lambda: {"material": 0, "ingredient": 0})
    redrew: bool = False
    soul_draw_used: bool = False
    gear_discount: int = 0  # Primitive Furnace: next gear from hand costs X less this turn

    @property
    def souls_standing(self) -> int:
        return self.souls - self.souls_rested

    @property
    def pals(self) -> list[CardInstance]:
        return [c for c in self.base if c.is_pal]

    @property
    def structures(self) -> list[CardInstance]:
        return [c for c in self.base if c.is_structure]


@dataclass
class Battle:
    attacker: CardInstance
    attacker_player: int
    target: CardInstance | None  # None = the defending player
    defender: int
    blocked_by: CardInstance | None = None
    nullified: bool = False

    def opponent_of(self, card: CardInstance) -> CardInstance | None:
        """The 'battle opponent' (CR 9.4.3) of `card`, if the target is a Pal."""
        if self.target is None or not self.target.is_pal:
            return None
        if card is self.attacker:
            return self.target
        if card is self.target:
            return self.attacker
        return None
