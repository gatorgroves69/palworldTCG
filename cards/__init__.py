"""Card effect implementations, one per card code, registered in REGISTRY.

Importing this package registers every implemented card.
"""
from . import bp01, bp01_blue_green, bp01_purple, bp01_red, souls, td01, td02  # noqa: F401
from .registry import REGISTRY, Registry

__all__ = ["REGISTRY", "Registry"]
