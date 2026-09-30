"""Card effect implementations, one per card code, registered in REGISTRY.

The card database loader (data/cards.json -> CardDef) is written once the
file exists, so its field mapping is based on the real data rather than a guess.
"""
from .registry import REGISTRY, Registry

__all__ = ["REGISTRY", "Registry"]
