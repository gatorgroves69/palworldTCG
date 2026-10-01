"""Load data/cards.json (Palify API response) into CardDefs. Read-only."""
from __future__ import annotations

import json
from pathlib import Path

from engine.model import CardDef, CardType, Color

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "cards.json"

# Fields that must agree when the raw file lists the same code more than once
# (SOUL-001 appears in both trial decks).
GAMEPLAY_FIELDS = ("name", "type", "subtype", "color", "cost", "power", "strike",
                   "durability", "lucky", "effect")


class CardDataError(ValueError):
    pass


def _to_def(raw: dict) -> CardDef:
    ctype = CardType(raw["type"].strip().lower())
    color = Color(raw["color"].strip().lower()) if raw.get("color") else Color.COLORLESS
    # Palify stores structure durability in "power" and leaves "durability" null.
    power = raw.get("power")
    if ctype is CardType.STRUCTURE and raw.get("durability") is not None:
        power = raw["durability"]
    return CardDef(
        code=raw["code"],
        name=raw["name"],
        type=ctype,
        color=color,
        cost=raw.get("cost") or 0,
        power=power or 0,
        strike=raw.get("strike") or 0,
        lucky=bool(raw.get("lucky")),
        subtype=raw.get("subtype") or "",
        text=raw.get("effect") or "",
        elements=_elements(raw),
        work=tuple(w.lower() for w in (raw.get("workSuitability") or "").split()),
    )


def _elements(raw: dict) -> tuple[str, ...]:
    # Palify keeps the element icons under "game.element", e.g. "Water / Dragon".
    el = (raw.get("game") or {}).get("element") or ""
    return tuple(e.strip().lower() for e in el.split("/") if e.strip())


def load_card_db(path: str | Path = DEFAULT_PATH) -> dict[str, CardDef]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    raws = data["cards"] if isinstance(data, dict) else data
    db: dict[str, CardDef] = {}
    first_raw: dict[str, dict] = {}
    for raw in raws:
        code = raw["code"]
        if code in first_raw:
            a, b = first_raw[code], raw
            diff = [f for f in GAMEPLAY_FIELDS if a.get(f) != b.get(f)]
            if diff:
                raise CardDataError(f"{code} listed twice with different {diff}")
            continue
        first_raw[code] = raw
        db[code] = _to_def(raw)
    return db
