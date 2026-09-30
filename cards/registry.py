"""Card implementations keyed by card code.

Every card that can appear in a simulated deck must be registered here,
including cards with no abilities (register those with `vanilla`). Looking up
an unregistered code raises `UnimplementedCardError`, and `Game` refuses to
start with such a deck. An unimplemented card is never played as a vanilla body.
"""
from __future__ import annotations

from engine.abilities import CardImpl, VanillaImpl
from engine.game import UnimplementedCardError


class Registry:
    def __init__(self) -> None:
        self._impls: dict[str, CardImpl] = {}

    def register(self, cls: type[CardImpl]) -> type[CardImpl]:
        """Class decorator: `@REGISTRY.register` on a CardImpl subclass."""
        if not cls.code:
            raise ValueError(f"{cls.__name__} has no card code")
        if cls.code in self._impls:
            raise ValueError(f"duplicate implementation for {cls.code}")
        self._impls[cls.code] = cls()
        return cls

    def vanilla(self, code: str, text: str = "") -> None:
        """Register a card that genuinely has no abilities (text must be empty
        or reminder-only; say so in `text`)."""
        cls = type(f"Vanilla_{code}", (VanillaImpl,), {"code": code, "text": text})
        self.register(cls)

    def __call__(self, code: str) -> CardImpl:
        try:
            return self._impls[code]
        except KeyError:
            raise UnimplementedCardError(f"card {code} has no implementation") from None

    def __contains__(self, code: str) -> bool:
        return code in self._impls

    def codes(self) -> list[str]:
        return sorted(self._impls)

    def missing(self, codes) -> list[str]:
        return sorted({c for c in codes if c not in self._impls})


REGISTRY = Registry()
