"""Soul cards. All carry only reminder text for the CR 8.5 "rest 3 souls, draw 1" action,
which the engine implements, so they are registered as vanilla (docs/assumptions.md A4)."""
from .registry import REGISTRY

# (During your turn, you may rest 3 souls once during the main phase to draw 1 card.)
SOUL_TEXT = "(During your turn, you may rest 3 souls once during the main phase to draw 1 card.)"
SOUL_CODES = ["SOUL-000", "SOUL-001", "SOUL-002", "SOUL-003", "SOUL-004", "SOUL-005", "SOUL-006",
              "SOUL-007", "SOUL-008", "SOUL-009", "SOUL-010", "SOUL-013", "SOUL-020", "SOUL-021",
              "SOUL-022", "SOUL-023", "SOUL-024"]

for _code in SOUL_CODES:
    REGISTRY.vanilla(_code, SOUL_TEXT)
