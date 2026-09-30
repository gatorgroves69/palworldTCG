"""Print and check decklists: `python -m cards.validate data/decks/*.txt`

Checks: 50 main / 10 soul, every code in cards.json, the name in the list
matches cards.json, <=4 per card name (CR 6.1.1.2), <=8 lucky (CR 6.1.1.3),
<=2 colours (Quick Manual). Exit status 1 if any deck has a problem.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from engine.deck import deck_problems

from .db import DEFAULT_PATH, load_card_db
from .decklist import build_deck, parse_decklist


def check(path: Path, db) -> list[str]:
    entries = parse_decklist(path.read_text(encoding="utf-8"), str(path))
    print(f"\n=== {path.name}")
    problems: list[str] = []
    warnings: list[str] = []
    for sec in ("main", "soul"):
        rows = [e for e in entries if e.section == sec]
        print(f"# {sec} ({sum(e.count for e in rows)})")
        for e in rows:
            d = db.get(e.code)
            if d is None:
                print(f"  {e.count} {e.code:<10} {e.name}   <-- NOT IN cards.json")
                continue
            info = f"{d.type.value}, {d.color.value}, cost {d.cost}"
            if d.type.value == "pal":
                info += f", {d.power}/S{d.strike}"
            elif d.type.value == "structure":
                info += f", dur {d.power}"
            if d.lucky:
                info += ", LUCKY"
            print(f"  {e.count} {e.code:<10} {d.name}  ({info})")
            if e.name and e.name.strip().lower() != d.name.strip().lower():
                warnings.append(f"{e.code}: list says '{e.name}', cards.json says '{d.name}'")
    dupes = [c for c, n in Counter((e.section, e.code) for e in entries).items() if n > 1]
    if dupes:
        warnings.append(f"code listed on more than one line: {dupes}")
    unknown = sorted({e.code for e in entries if e.code not in db})
    if unknown:
        problems.append(f"codes not in cards.json: {', '.join(unknown)}")
    else:
        deck = build_deck(entries, db, path.stem)
        problems += deck_problems(deck)
        colors = Counter(c.color.value for c in deck.main)
        print(f"colours: {dict(colors)}   lucky: {sum(c.lucky for c in deck.main)}   "
              f"names at max copies: "
              f"{sum(1 for n in Counter(c.name for c in deck.main).values() if n == 4)}")
    for w in warnings:
        print(f"WARNING: {w}")
    print("RESULT: " + ("OK" if not problems else "FAIL\n  - " + "\n  - ".join(problems)))
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("decks", nargs="+", type=Path)
    ap.add_argument("--cards", type=Path, default=DEFAULT_PATH)
    args = ap.parse_args(argv)
    db = load_card_db(args.cards)
    bad = [p for p in args.decks if check(p, db)]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
