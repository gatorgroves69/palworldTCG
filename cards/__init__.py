"""Card effect implementations, one per card code, registered in REGISTRY.

Importing this package registers every implemented card.
"""
from . import bp01, souls, td01, td02  # noqa: F401  (registration side effects)
from .registry import REGISTRY, Registry

__all__ = ["REGISTRY", "Registry"]
