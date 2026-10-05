"""SS01 Sleeve & Card Set Vol.1 cards."""
from engine import Attack, Zone
from tests.test_cards_m2 import G, box, play, put  # noqa: F401


def test_grizzbolt_hits_all_opposing_pals_and_suzaku_boosts_it(box):
    g, bots = G(box)
    a, b = put(g, 1, "TD01-023"), put(g, 1, "BP01-028")  # Lamball 200, Pengullet 600
    mine = put(g, 0, "BP01-008")
    play(g, bots, 0, "SS01-001")
    assert a.zone is Zone.GRAVEYARD and b.damage == 300 and mine.damage == 0
    put(g, 0, "BP01-002")  # Suzaku: red effect damage +200
    c = put(g, 1, "TD01-016")  # Reindrix 600
    g.players[0].souls_rested = 0
    play(g, bots, 0, "SS01-001")
    assert c.damage == 500


def test_chillet_ice_blade_draws_when_its_opponent_dies(box):
    g, bots = G(box)
    ch = put(g, 0, "SS01-002")       # 1000
    v = put(g, 1, "BP01-028", rested=True)  # Pengullet 600
    hand = len(g.players[0].hand)
    g.perform(Attack(ch.uid, v.uid))
    assert v.zone is Zone.GRAVEYARD and ch.zone is Zone.BASE
    assert len(g.players[0].hand) == hand + 1


def test_chillet_ice_blade_no_draw_when_attacking_player(box):
    g, bots = G(box)
    ch = put(g, 0, "SS01-002")
    hand = len(g.players[0].hand)
    g.perform(Attack(ch.uid, None))
    assert len(g.players[0].hand) == hand


def test_cattiva_brimming_power_by_souls(box):
    g, _ = G(box)
    c = put(g, 0, "SS01-004")
    ps = g.players[0]
    for souls, power in [(4, 300), (5, 500), (9, 500), (10, 700)]:
        ps.souls = souls
        assert g.power(c) == power


def test_quivern_deals_700_when_attacking_a_pal(box):
    g, bots = G(box)
    q = put(g, 0, "SS01-005")  # 1300
    tgt = put(g, 1, "BP01-028", rested=True)
    other = put(g, 1, "TD01-016")  # Reindrix 600
    bots[1].answers.append([])           # no block
    bots[0].answers.append([other.uid])  # Quivern's 700
    g.perform(Attack(q.uid, tgt.uid))
    assert other.zone is Zone.GRAVEYARD and tgt.zone is Zone.GRAVEYARD


def test_quivern_no_trigger_attacking_player(box):
    g, bots = G(box)
    q = put(g, 0, "SS01-005")
    other = put(g, 1, "TD01-016", rested=True)
    g.perform(Attack(q.uid, None))
    assert other.damage == 0
