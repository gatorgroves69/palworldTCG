"""Rules interpretations that are switchable because the rules are ambiguous.
Each field names its entry in docs/assumptions.md."""
from __future__ import annotations

from dataclasses import dataclass

STRUCTURE_TARGETING = ("any", "rested_only")


@dataclass(frozen=True)
class RulesConfig:
    # A2 / CR 9.2.3: may a standing structure be chosen as an attack target?
    structures_attackable: str = "any"

    def __post_init__(self) -> None:
        if self.structures_attackable not in STRUCTURE_TARGETING:
            raise ValueError(f"structures_attackable must be one of {STRUCTURE_TARGETING}")
