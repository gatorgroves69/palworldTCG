"""The interface every card implementation fills in.

Card implementations live in `cards/` and subclass `CardImpl`. The engine only
ever talks to cards through this interface, so `engine/` never imports `cards/`.

Keywords from CR 12 (Brave, Serious, Interrupt, Vigilance, Taunt, Stealth,
Retaliate, Nocturnal, Breakthrough, Assault) are handled by the engine; a card
just declares them in `keywords`. Everything else goes in the hook methods.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .game import Game
    from .state import CardInstance

# Keywords that take a number (Brave 200, Serious 100) map to that number;
# flag keywords map to True.
KEYWORDS = frozenset({
    "brave", "serious", "interrupt", "vigilance", "taunt", "stealth",
    "retaliate", "nocturnal", "breakthrough", "assault",
})


@dataclass
class ActAbility:
    """An 【ACT】 ability of a card in the base (CR 10.1.1.1).

    Cost: `souls` souls rested, plus a standing Pal assigned if `assign` (for
    structures), plus whatever `can_pay_extra`/`pay_extra` define.
    """

    name: str
    effect: Callable[["Game", "CardInstance", dict], None]
    souls: int = 0
    assign: bool = False
    rest_self: bool = False  # cost includes [Rest this card]
    once_per_turn: bool = False
    quick: bool = False
    can_pay_extra: Callable[["Game", "CardInstance"], bool] | None = None
    pay_extra: Callable[["Game", "CardInstance"], None] | None = None
    condition: Callable[["Game", "CardInstance"], bool] | None = None


@dataclass
class Trigger:
    """An automatic ability waiting to resolve at the next check timing (CR 10.8)."""

    master: int
    name: str
    fn: Callable[["Game"], None]
    source_uid: int | None = None


class CardImpl:
    """Base class for a card's rules. Subclasses set `code` and `text`.

    Hook methods are no-ops by default. The engine checks whether a subclass
    overrode `on_deploy`, `on_attack` and `on_assign` so that a card with no
    such ability doesn't queue empty triggers.
    """

    code: str = ""
    text: str = ""
    keywords: dict[str, int | bool] = {}
    acts: list[ActAbility] = []

    def __init__(self) -> None:
        bad = set(self.keywords) - KEYWORDS
        if bad:
            raise ValueError(f"{self.code}: unknown keyword(s) {sorted(bad)}")

    # ---- playing the card -------------------------------------------------
    def can_play(self, game: "Game", card: "CardInstance") -> bool:
        """Extra conditions on playing this card from hand (beyond cost)."""
        return True

    def cost_mod(self, game: "Game", card: "CardInstance") -> int:
        """Change to this card's cost while it is in hand."""
        return 0

    def modes(self, game: "Game", card: "CardInstance") -> list[str]:
        """For "Choose 1 of the following" cards: the mode names. The mode is
        chosen when the card is played (CR 10.6.2.2.1) and is part of the action."""
        return []

    def resolve_event(self, game: "Game", card: "CardInstance", mode: int | None) -> None:
        """Effect of an event card when played."""

    @property
    def quick(self) -> bool:
        """True for 【Quick】 event cards (playable in the Quick step)."""
        return False

    # ---- AUTO hooks -------------------------------------------------------
    def on_deploy(self, game: "Game", card: "CardInstance") -> None: ...
    def on_attack(self, game: "Game", card: "CardInstance") -> None: ...
    def on_assign(self, game: "Game", card: "CardInstance") -> None: ...

    def triggers(self, game: "Game", card: "CardInstance", event: "Event") -> list[Trigger]:
        """Other AUTO abilities: return the triggers this event fires for `card`.

        Called for every card in a base, and for a card that has just left
        the base (zone-change triggers, CR 10.8.4)."""
        return []

    # ---- CONT hooks -------------------------------------------------------
    def power_mod(self, game: "Game", card: "CardInstance") -> int:
        return 0

    def strike_mod(self, game: "Game", card: "CardInstance") -> int:
        return 0

    def can_be_blocked(self, game: "Game", card: "CardInstance") -> bool:
        return True

    def can_attack(self, game: "Game", card: "CardInstance") -> bool:
        return True

    def can_be_attacked_by(self, game: "Game", card: "CardInstance",
                           attacker: "CardInstance") -> bool:
        return True

    def modify_effect_damage(self, game: "Game", card: "CardInstance", source: "CardInstance",
                             target: "CardInstance", amount: int) -> int:
        """Replacement effect on non-battle damage dealt to a Pal or structure
        (e.g. Suzaku). `card` is the card with this ability, on the base."""
        return amount

    def __deepcopy__(self, memo):  # stateless; share across game clones
        return self

    # ---- helpers ----------------------------------------------------------
    def overrides(self, hook: str) -> bool:
        return getattr(type(self), hook) is not getattr(CardImpl, hook)


class VanillaImpl(CardImpl):
    """A card with no abilities. It must still be registered explicitly, so
    that an unimplemented card is never mistaken for a vanilla one."""


@dataclass
class Event:
    """Something that happened, broadcast to card `triggers` hooks."""

    kind: str
    player: int | None = None
    card_uid: int | None = None
    data: dict = field(default_factory=dict)
