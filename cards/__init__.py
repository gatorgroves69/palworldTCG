"""Card effect implementations, one per card code, registered in REGISTRY.

Importing this package registers every implemented card.
"""
from . import (bp01, bp01_blue_green, bp01_colorless, bp01_purple, bp01_red,  # noqa: F401
               bp02, souls, ss01, td01, td02)
from .registry import REGISTRY, Registry

__all__ = ["REGISTRY", "Registry"]
