"""cards.json loader and deck validator, against the real data file (read-only)."""
from collections import Counter

import pytest

from cards.db import DEFAULT_PATH, load_card_db
from cards.validate import check
from engine import CardType, Color

pytestmark = pytest.mark.skipif(not DEFAULT_PATH.exists(), reason="data/cards.json missing")


@pytest.fixture(scope="module")
def db():
    return load_card_db()


def test_loads_every_code(db):
    assert len(db) == 183  # 184 raw entries, SOUL-001 listed twice
    assert Counter(d.type for d in db.values())[CardType.PAL] == 108


def test_structure_durability_from_power_field(db):
    assert db["BP01-016"].type is CardType.STRUCTURE and db["BP01-016"].power == 800
    assert all(d.power > 0 for d in db.values() if d.type is CardType.STRUCTURE)


def test_fields(db):
    j = db["BP01-001"]
    assert (j.cost, j.power, j.strike, j.lucky, j.color) == (8, 1700, 4, True, Color.RED)
    assert db["SOUL-001"].type is CardType.SOUL and db["SOUL-001"].color is Color.COLORLESS


def _write(tmp_path, main, soul):
    text = "# main\n" + "".join(f"{n} {c} x\n" for c, n in main) + "# soul\n" \
        + "".join(f"{n} {c} x\n" for c, n in soul)
    p = tmp_path / "d.txt"
    p.write_text(text)
    return p


def _legal_main(db):
    reds = [d.code for d in db.values() if d.color is Color.RED and not d.lucky]
    names, main = set(), []
    for c in reds:
        if db[c].name not in names and len(main) < 12:
            names.add(db[c].name)
            main.append((c, 4))
    main.append((next(d.code for d in db.values()
                      if d.color is Color.RED and not d.lucky and d.name not in names), 2))
    return main


def test_validator_accepts_legal(db, tmp_path):
    assert check(_write(tmp_path, _legal_main(db), [("SOUL-001", 10)]), db) == []


def test_validator_flags_unknown_code(db, tmp_path):
    probs = check(_write(tmp_path, _legal_main(db), [("BP01-000", 10)]), db)
    assert probs and "BP01-000" in probs[0]
