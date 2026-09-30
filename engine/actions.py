"""Player decisions. Main-phase actions are enumerated by `Game.legal_actions`;
the other decisions (block, quick step, targets) go through `Decision`."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PlayCard:
    uid: int

@dataclass(frozen=True)
class Activate:
    uid: int
    index: int
    assign_uid: int | None = None  # Pal assigned to pay the cost, if the ability needs one

@dataclass(frozen=True)
class Attack:
    attacker_uid: int
    target_uid: int | None  # None = attack the player

@dataclass(frozen=True)
class SoulDraw:
    """Rest 3 souls to draw 1 card, once per turn (CR 8.5)."""

@dataclass(frozen=True)
class EndMain:
    pass

@dataclass(frozen=True)
class UseInterrupt:
    """Interrupt from hand (CR 12.8): pay ① or discard `discard_uid`."""
    uid: int
    discard_uid: int | None = None  # None = pay 1 soul instead

@dataclass(frozen=True)
class Pass:
    pass


Action = PlayCard | Activate | Attack | SoulDraw | EndMain | UseInterrupt | Pass


@dataclass
class Decision:
    """A choice put to a player mid-resolution.

    `options` are opaque values (usually card uids); the agent returns a list
    of between `min` and `max` of them.
    kinds: "block", "quick", "target", "overload", "may", "order".
    """

    kind: str
    player: int
    prompt: str
    options: list[Any]
    min: int = 1
    max: int = 1
    context: dict = field(default_factory=dict)
