"""Parse decklist files (`data/decks/*.txt`).

Format, one card per line, with `# main` and `# soul` section headers:

    # main
    4 BP01-001 Cattiva
    ...
    # soul
    10 BP01-S01 Soul

Other lines starting with `#` are comments. Blank lines are ignored.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from engine.deck import Deck
from engine.model import CardDef

LINE = re.compile(r"^(\d+)\s+(\S+)(?:\s+(.*))?$")


@dataclass
class DeckEntry:
    count: int
    code: str
    name: str
    section: str


class DecklistError(ValueError):
    pass


def parse_decklist(text: str, source: str = "<decklist>") -> list[DeckEntry]:
    section: str | None = None
    entries: list[DeckEntry] = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            header = line[1:].strip().lower()
            if header in ("main", "soul"):
                section = header
            continue
        m = LINE.match(line)
        if not m:
            raise DecklistError(f"{source}:{n}: can't parse line {raw!r}")
        if section is None:
            raise DecklistError(f"{source}:{n}: card before any '# main' / '# soul' header")
        entries.append(DeckEntry(int(m.group(1)), m.group(2), (m.group(3) or "").strip(), section))
    return entries


def build_deck(entries: list[DeckEntry], card_db: dict[str, CardDef], name: str) -> Deck:
    """Expand entries into a Deck using the card database. Unknown codes are an error."""
    unknown = sorted({e.code for e in entries if e.code not in card_db})
    if unknown:
        raise DecklistError(f"{name}: codes not in card database: {', '.join(unknown)}")
    main: list[CardDef] = []
    soul: list[CardDef] = []
    for e in entries:
        (main if e.section == "main" else soul).extend([card_db[e.code]] * e.count)
    return Deck(name, main, soul)


def load_deck(path: str | Path, card_db: dict[str, CardDef]) -> Deck:
    path = Path(path)
    return build_deck(parse_decklist(path.read_text(encoding="utf-8"), str(path)),
                      card_db, path.stem)
